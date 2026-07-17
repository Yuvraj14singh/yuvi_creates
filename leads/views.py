from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import FollowUpForm, LeadActivityForm, LeadAttachmentForm, LeadForm, StaffLoginForm
from .models import Lead, LeadActivity, LeadAttachment


def staff_only(view_func):
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('leads:login')}?next={request.get_full_path()}")
        if not (request.user.is_staff or request.user.is_superuser):
            raise PermissionDenied("Staff access is required.")
        return view_func(request, *args, **kwargs)

    wrapped.__name__ = view_func.__name__
    wrapped.__doc__ = view_func.__doc__
    return wrapped


def staff_login(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        return redirect("leads:dashboard")
    form = StaffLoginForm(request=request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        if not (user.is_staff or user.is_superuser):
            form.add_error(None, "This account does not have staff access.")
        else:
            login(request, user)
            next_url = request.POST.get("next", "")
            if next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
                return redirect(next_url)
            return redirect("leads:dashboard")
    return render(request, "staff_dashboard/login.html", {"form": form, "next": request.GET.get("next", "")})


@require_POST
def staff_logout(request):
    logout(request)
    return redirect("leads:login")


def active_leads():
    return Lead.objects.filter(is_archived=False)


def dashboard_data():
    today = timezone.localdate()
    active = active_leads()
    open_leads = active.exclude(status__in=Lead.CLOSED_STATUSES)
    return {
        "total_leads": active.count(),
        "new_leads": active.filter(status=Lead.Status.NEW).count(),
        "replies_received": active.filter(reply_received=True).count(),
        "demo_requests": active.filter(status=Lead.Status.DEMO_REQUESTED).count(),
        "due_today_count": open_leads.filter(next_follow_up_date=today).count(),
        "overdue_count": open_leads.filter(next_follow_up_date__lt=today).count(),
        "meetings_scheduled": active.filter(meeting_scheduled=True).count(),
        "proposals_sent": active.filter(proposal_sent=True).count(),
        "won_clients": active.filter(status=Lead.Status.WON).count(),
        "lost_leads": Lead.objects.filter(Q(status=Lead.Status.LOST) | Q(is_archived=True)).distinct().count(),
        "today_followups": open_leads.filter(next_follow_up_date=today)[:6],
        "overdue_followups": open_leads.filter(next_follow_up_date__lt=today).order_by("next_follow_up_date")[:6],
        "upcoming_followups": open_leads.filter(next_follow_up_date__gt=today).order_by("next_follow_up_date")[:6],
        "recent_leads": active[:6],
        "recent_replies": active.filter(reply_received=True).order_by("-updated_at")[:6],
        "high_priority": open_leads.filter(priority=Lead.Priority.HIGH)[:6],
        "recent_activity": LeadActivity.objects.select_related("lead", "created_by")[:8],
        "status_groups": active.values("status").annotate(total=Count("id")).order_by("-total"),
    }


@staff_only
def dashboard(request):
    return render(request, "staff_dashboard/dashboard.html", dashboard_data())


@staff_only
def lead_dashboard(request):
    return render(request, "staff_dashboard/lead_dashboard.html", dashboard_data())


SORT_FIELDS = {
    "created": "created_at",
    "updated": "updated_at",
    "business": "business_name",
    "priority": "priority",
    "status": "status",
    "followup": "next_follow_up_date",
    "contact": "last_contact_date",
}


@staff_only
def lead_list(request):
    leads = active_leads()
    query = request.GET.get("q", "").strip()[:120]
    if query:
        leads = leads.filter(
            Q(business_name__icontains=query) | Q(contact_person__icontains=query)
            | Q(email__icontains=query) | Q(phone_number__icontains=query)
            | Q(instagram_handle__icontains=query) | Q(city__icontains=query)
        )
    choice_filters = {
        "category": dict(Lead.Category.choices), "status": dict(Lead.Status.choices),
        "priority": dict(Lead.Priority.choices), "source": dict(Lead.Source.choices),
    }
    selected = {}
    for key, choices in choice_filters.items():
        value = request.GET.get(key, "")
        if value in choices:
            leads = leads.filter(**{key: value})
            selected[key] = value
    for key in ("reply_received", "demo_sent"):
        value = request.GET.get(key, "")
        if value in {"yes", "no"}:
            leads = leads.filter(**{key: value == "yes"})
            selected[key] = value
    follow_up = request.GET.get("follow_up", "")
    try:
        if follow_up:
            leads = leads.filter(next_follow_up_date=timezone.datetime.strptime(follow_up, "%Y-%m-%d").date())
            selected["follow_up"] = follow_up
    except ValueError:
        follow_up = ""
    sort = request.GET.get("sort", "created")
    if sort not in SORT_FIELDS:
        sort = "created"
    direction = request.GET.get("direction", "desc")
    if direction not in {"asc", "desc"}:
        direction = "desc"
    order = SORT_FIELDS[sort]
    leads = leads.order_by(("-" if direction == "desc" else "") + order, "business_name")
    paginator = Paginator(leads, 15)
    page_obj = paginator.get_page(request.GET.get("page"))
    query_params = request.GET.copy()
    query_params.pop("page", None)
    return render(request, "staff_dashboard/lead_list.html", {
        "page_obj": page_obj, "query": query, "selected": selected, "sort": sort,
        "direction": direction, "querystring": query_params.urlencode(), "categories": Lead.Category.choices,
        "statuses": Lead.Status.choices, "priorities": Lead.Priority.choices, "sources": Lead.Source.choices,
    })


@staff_only
def lead_create(request):
    form = LeadForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        lead = form.save(commit=False)
        lead.created_by = request.user
        lead.save()
        LeadActivity.objects.create(lead=lead, activity_type=LeadActivity.ActivityType.CREATED, message="Lead created.", created_by=request.user)
        messages.success(request, "Lead created successfully.")
        return redirect(lead)
    return render(request, "staff_dashboard/lead_form.html", {"form": form, "page_title": "Add Lead"})


@staff_only
def lead_edit(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    old_status = lead.status
    form = LeadForm(request.POST or None, instance=lead)
    if request.method == "POST" and form.is_valid():
        lead = form.save()
        if old_status != lead.status:
            LeadActivity.objects.create(
                lead=lead, activity_type=LeadActivity.ActivityType.STATUS_CHANGED,
                message=f"Status changed from {dict(Lead.Status.choices).get(old_status)} to {lead.get_status_display()}.", created_by=request.user,
            )
        messages.success(request, "Lead updated successfully.")
        return redirect(lead)
    return render(request, "staff_dashboard/lead_form.html", {"form": form, "lead": lead, "page_title": "Edit Lead"})


@staff_only
def lead_detail(request, pk):
    lead = get_object_or_404(Lead.objects.select_related("created_by"), pk=pk)
    return render(request, "staff_dashboard/lead_detail.html", {
        "lead": lead, "activity_form": LeadActivityForm(), "attachment_form": LeadAttachmentForm(),
        "follow_up_form": FollowUpForm(),
    })


@staff_only
@require_POST
def activity_add(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    form = LeadActivityForm(request.POST)
    if form.is_valid():
        activity = form.save(commit=False)
        activity.lead = lead
        activity.created_by = request.user
        activity.save()
        messages.success(request, "Activity added.")
    else:
        messages.error(request, "Activity could not be added. Check the entered values.")
    return redirect(lead)


ACTION_MAP = {
    "replied": (Lead.Status.REPLIED, LeadActivity.ActivityType.REPLIED, {"reply_received": True}),
    "demo-requested": (Lead.Status.DEMO_REQUESTED, LeadActivity.ActivityType.DEMO_REQUESTED, {}),
    "demo-sent": (Lead.Status.DEMO_SENT, LeadActivity.ActivityType.DEMO_SENT, {"demo_sent": True}),
    "proposal-sent": (Lead.Status.PROPOSAL_SENT, LeadActivity.ActivityType.PROPOSAL, {"proposal_sent": True}),
    "meeting": (Lead.Status.MEETING, LeadActivity.ActivityType.MEETING, {"meeting_scheduled": True}),
    "won": (Lead.Status.WON, LeadActivity.ActivityType.WON, {}),
    "lost": (Lead.Status.LOST, LeadActivity.ActivityType.LOST, {}),
}


@staff_only
@require_POST
def lead_action(request, pk, action):
    lead = get_object_or_404(Lead, pk=pk)
    if action in ACTION_MAP:
        status, activity_type, flags = ACTION_MAP[action]
        lead.status = status
        for field, value in flags.items():
            setattr(lead, field, value)
        lead.save(update_fields=["status", *flags.keys(), "updated_at"])
        LeadActivity.objects.create(lead=lead, activity_type=activity_type, message=f"Marked as {lead.get_status_display()}.", created_by=request.user)
        messages.success(request, f"{lead.business_name} marked as {lead.get_status_display()}.")
    elif action == "archive":
        lead.is_archived = True
        lead.save(update_fields=["is_archived", "updated_at"])
        LeadActivity.objects.create(lead=lead, activity_type=LeadActivity.ActivityType.STATUS_CHANGED, message="Lead archived.", created_by=request.user)
        messages.success(request, "Lead archived.")
    elif action == "restore":
        lead.is_archived = False
        lead.save(update_fields=["is_archived", "updated_at"])
        LeadActivity.objects.create(lead=lead, activity_type=LeadActivity.ActivityType.STATUS_CHANGED, message="Lead restored.", created_by=request.user)
        messages.success(request, "Lead restored.")
    elif action == "schedule":
        form = FollowUpForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Choose a valid follow-up date.")
            return redirect(lead)
        LeadActivity.objects.create(
            lead=lead, activity_type=LeadActivity.ActivityType.NOTE,
            message=form.cleaned_data["message"] or "Follow-up scheduled.",
            next_follow_up_date=form.cleaned_data["next_follow_up_date"], created_by=request.user,
        )
        messages.success(request, "Follow-up scheduled.")
    else:
        raise Http404("Unknown action")
    next_url = request.POST.get("next", "")
    if next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
        return redirect(next_url)
    return redirect(lead)


@staff_only
def follow_ups(request):
    today = timezone.localdate()
    leads = active_leads().exclude(status__in=Lead.CLOSED_STATUSES)
    return render(request, "staff_dashboard/follow_ups.html", {
        "due_today": leads.filter(next_follow_up_date=today),
        "overdue": leads.filter(next_follow_up_date__lt=today).order_by("next_follow_up_date"),
        "upcoming": leads.filter(next_follow_up_date__gt=today).order_by("next_follow_up_date"),
        "no_date": leads.filter(next_follow_up_date__isnull=True),
    })


@staff_only
def archived_leads(request):
    leads = Lead.objects.filter(Q(is_archived=True) | Q(status__in=[Lead.Status.LOST, Lead.Status.NOT_INTERESTED])).distinct()
    return render(request, "staff_dashboard/archived.html", {"leads": leads})


@staff_only
@require_POST
def attachment_add(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    form = LeadAttachmentForm(request.POST, request.FILES)
    if form.is_valid():
        attachment = form.save(commit=False)
        attachment.lead = lead
        attachment.uploaded_by = request.user
        attachment.save()
        messages.success(request, "Attachment uploaded.")
    else:
        messages.error(request, "Attachment rejected. Use an allowed file type up to 10 MB.")
    return redirect(lead)


@staff_only
def attachment_download(request, pk):
    attachment = get_object_or_404(LeadAttachment, pk=pk)
    try:
        return FileResponse(attachment.file.open("rb"), as_attachment=True, filename=attachment.file.name.rsplit("/", 1)[-1])
    except FileNotFoundError:
        raise Http404("Attachment file not found")
