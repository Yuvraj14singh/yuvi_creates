from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


def validate_attachment_size(value):
    if value.size > 10 * 1024 * 1024:
        raise ValidationError("Files must be 10 MB or smaller.")


def lead_attachment_path(instance, filename):
    safe_name = Path(filename).name
    return f"lead_attachments/{instance.lead_id}/{safe_name}"


class Lead(models.Model):
    class Category(models.TextChoices):
        CRICKET_LEAGUE = "cricket_league", "Cricket League"
        CRICKET_TEAM = "cricket_team", "Cricket Team"
        CRICKET_CLUB = "cricket_club", "Cricket Club"
        CRICKET_ACADEMY = "cricket_academy", "Cricket Academy"
        EVENT_COMPANY = "event_company", "Event Company"
        SPORTS_MEDIA = "sports_media", "Sports Media"
        STREAMING_PARTNER = "streaming_partner", "Live Streaming Partner"
        CAFE = "cafe", "Cafe"
        TRAVEL = "travel_business", "Travel Business"
        REAL_ESTATE = "real_estate", "Real Estate"
        OTHER = "other", "Other"

    class Source(models.TextChoices):
        INSTAGRAM = "instagram", "Instagram"
        EMAIL = "email", "Email"
        WHATSAPP = "whatsapp", "WhatsApp"
        LINKEDIN = "linkedin", "LinkedIn"
        REFERRAL = "referral", "Referral"
        OFFLINE = "offline", "Offline"
        OTHER = "other", "Other"

    class Priority(models.TextChoices):
        HIGH = "high", "High"
        MEDIUM = "medium", "Medium"
        LOW = "low", "Low"

    class Status(models.TextChoices):
        NEW = "new", "New Lead"
        DM_SENT = "dm_sent", "DM Sent"
        EMAIL_SENT = "email_sent", "Email Sent"
        REPLIED = "replied", "Replied"
        DEMO_REQUESTED = "demo_requested", "Demo Requested"
        DEMO_SENT = "demo_sent", "Demo Sent"
        WAITING = "waiting", "Waiting"
        FOLLOW_UP_DUE = "follow_up_due", "Follow-up Due"
        FOLLOW_UP_1 = "follow_up_1", "Follow-up 1"
        FOLLOW_UP_2 = "follow_up_2", "Follow-up 2"
        MEETING = "meeting_scheduled", "Meeting Scheduled"
        PROPOSAL_SENT = "proposal_sent", "Proposal Sent"
        NEGOTIATION = "negotiation", "Negotiation"
        WON = "won", "Won"
        LOST = "lost", "Lost"
        NOT_INTERESTED = "not_interested", "Not Interested"

    CLOSED_STATUSES = (Status.WON, Status.LOST, Status.NOT_INTERESTED)

    business_name = models.CharField("Business / league name", max_length=180, db_index=True)
    contact_person = models.CharField(max_length=140, blank=True, db_index=True)
    category = models.CharField(max_length=30, choices=Category.choices, default=Category.OTHER, db_index=True)
    city = models.CharField(max_length=120, blank=True, db_index=True)
    state = models.CharField(max_length=120, blank=True)
    country = models.CharField(max_length=120, default="India", blank=True)
    instagram_handle = models.CharField(max_length=120, blank=True, db_index=True)
    instagram_url = models.URLField(blank=True)
    email = models.EmailField(blank=True, db_index=True)
    phone_number = models.CharField(max_length=40, blank=True, db_index=True)
    website_url = models.URLField(blank=True)
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.INSTAGRAM, db_index=True)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM, db_index=True)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.NEW, db_index=True)
    first_contact_date = models.DateField(null=True, blank=True)
    last_contact_date = models.DateField(null=True, blank=True, db_index=True)
    next_follow_up_date = models.DateField(null=True, blank=True, db_index=True)
    expected_budget = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    proposal_sent = models.BooleanField(default=False, db_index=True)
    demo_sent = models.BooleanField(default=False, db_index=True)
    reply_received = models.BooleanField(default=False, db_index=True)
    meeting_scheduled = models.BooleanField(default=False, db_index=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="created_leads")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    is_archived = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "lead"
        verbose_name_plural = "leads"
        indexes = [models.Index(fields=["is_archived", "status", "next_follow_up_date"])]

    def __str__(self):
        return self.business_name

    def get_absolute_url(self):
        return reverse("leads:detail", args=[self.pk])

    @property
    def is_follow_up_due_today(self):
        return not self.is_closed and self.next_follow_up_date == timezone.localdate()

    @property
    def is_follow_up_overdue(self):
        return bool(not self.is_closed and self.next_follow_up_date and self.next_follow_up_date < timezone.localdate())

    @property
    def is_closed(self):
        return self.status in self.CLOSED_STATUSES

    @property
    def follow_up_status(self):
        if not self.next_follow_up_date:
            return "Not set"
        if self.is_follow_up_due_today:
            return "Due Today"
        if self.is_follow_up_overdue:
            return "Overdue"
        if self.is_closed:
            return "Closed"
        return "Upcoming"

    @property
    def display_contact_information(self):
        return self.email or self.phone_number or self.instagram_handle or "No contact information"


class LeadActivity(models.Model):
    class ActivityType(models.TextChoices):
        CREATED = "created", "Lead Created"
        NOTE = "note", "Note Added"
        DM_SENT = "dm_sent", "Instagram DM Sent"
        EMAIL_SENT = "email_sent", "Email Sent"
        WHATSAPP_SENT = "whatsapp_sent", "WhatsApp Message Sent"
        REPLIED = "replied", "Reply Received"
        DEMO_REQUESTED = "demo_requested", "Demo Requested"
        DEMO_SENT = "demo_sent", "Demo Sent"
        FOLLOW_UP_SENT = "follow_up_sent", "Follow-up Sent"
        CALL = "call", "Call Completed"
        MEETING = "meeting", "Meeting Scheduled"
        PROPOSAL = "proposal", "Proposal Sent"
        STATUS_CHANGED = "status_changed", "Status Changed"
        WON = "won", "Lead Won"
        LOST = "lost", "Lead Lost"
        OTHER = "other", "Other"

    CONTACT_TYPES = {
        "dm_sent", "email_sent", "whatsapp_sent", "replied", "demo_sent",
        "follow_up_sent", "call", "meeting", "proposal", "won", "lost",
    }

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="activities")
    activity_type = models.CharField(max_length=30, choices=ActivityType.choices, default=ActivityType.NOTE, db_index=True)
    message = models.TextField(blank=True)
    activity_date = models.DateField(default=timezone.localdate, db_index=True)
    next_follow_up_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="lead_activities")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-activity_date", "-created_at"]
        verbose_name_plural = "lead activities"

    def __str__(self):
        return f"{self.lead} — {self.get_activity_type_display()}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        updates = {}
        if self.next_follow_up_date:
            updates["next_follow_up_date"] = self.next_follow_up_date
        if self.activity_type in self.CONTACT_TYPES:
            updates["last_contact_date"] = self.activity_date
        if updates:
            Lead.objects.filter(pk=self.lead_id).update(**updates, updated_at=timezone.now())


class LeadAttachment(models.Model):
    ALLOWED_EXTENSIONS = ["pdf", "png", "jpg", "jpeg", "webp", "mp4", "mov", "doc", "docx", "xls", "xlsx"]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="attachments")
    title = models.CharField(max_length=180)
    file = models.FileField(
        upload_to=lead_attachment_path,
        validators=[FileExtensionValidator(ALLOWED_EXTENSIONS), validate_attachment_size],
    )
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="lead_attachments")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.lead} — {self.title}"
