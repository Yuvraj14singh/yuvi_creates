from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import LeadAttachmentForm, LeadForm
from .models import Lead, LeadActivity


User = get_user_model()


class LeadModelTests(TestCase):
    def test_follow_up_states_and_closed_rules(self):
        today = timezone.localdate()
        lead = Lead.objects.create(business_name="Test League", next_follow_up_date=today)
        self.assertTrue(lead.is_follow_up_due_today)
        lead.next_follow_up_date = today - timedelta(days=1)
        self.assertTrue(lead.is_follow_up_overdue)
        lead.status = Lead.Status.WON
        self.assertFalse(lead.is_follow_up_overdue)
        self.assertTrue(lead.is_closed)

    def test_activity_updates_follow_up_and_last_contact(self):
        lead = Lead.objects.create(business_name="Academy")
        activity_date = timezone.localdate()
        follow_up = activity_date + timedelta(days=3)
        LeadActivity.objects.create(lead=lead, activity_type=LeadActivity.ActivityType.CALL, activity_date=activity_date, next_follow_up_date=follow_up)
        lead.refresh_from_db()
        self.assertEqual(lead.last_contact_date, activity_date)
        self.assertEqual(lead.next_follow_up_date, follow_up)


class LeadFormTests(TestCase):
    def test_email_and_negative_budget_validation(self):
        form = LeadForm(data={"business_name": "League", "email": "wrong", "expected_budget": "-1", "category": Lead.Category.OTHER, "source": Lead.Source.OTHER, "priority": Lead.Priority.MEDIUM, "status": Lead.Status.NEW})
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)
        self.assertIn("expected_budget", form.errors)

    def test_dangerous_attachment_extension_rejected(self):
        form = LeadAttachmentForm(data={"title": "Bad"}, files={"file": SimpleUploadedFile("bad.exe", b"x")})
        self.assertFalse(form.is_valid())


class StaffPermissionAndFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.staff = User.objects.create_user("staff", password="pass12345", is_staff=True)
        cls.superuser = User.objects.create_superuser("root", "root@example.com", "pass12345")
        cls.normal = User.objects.create_user("normal", password="pass12345")

    def setUp(self):
        self.lead = Lead.objects.create(business_name="Delhi Cricket League", contact_person="Dev", city="Delhi", created_by=self.staff)

    def test_logged_out_redirected_and_normal_user_forbidden(self):
        response = self.client.get(reverse("leads:dashboard"))
        self.assertRedirects(response, f"{reverse('leads:login')}?next={reverse('leads:dashboard')}")
        self.client.force_login(self.normal)
        self.assertEqual(self.client.get(reverse("leads:dashboard")).status_code, 403)
        self.assertEqual(self.client.post(reverse("leads:action", args=[self.lead.pk, "won"])).status_code, 403)

    def test_staff_and_superuser_access(self):
        for user in (self.staff, self.superuser):
            self.client.force_login(user)
            self.assertEqual(self.client.get(reverse("leads:dashboard")).status_code, 200)
            self.assertEqual(self.client.get(reverse("leads:detail", args=[self.lead.pk])).status_code, 200)
            self.assertEqual(self.client.get(reverse("leads:follow_ups")).status_code, 200)
            self.assertEqual(self.client.get(reverse("leads:archived")).status_code, 200)
            self.client.logout()

    def test_staff_can_create_lead_and_created_activity(self):
        self.client.force_login(self.staff)
        response = self.client.post(reverse("leads:add"), {
            "business_name": "Mumbai Team", "category": Lead.Category.CRICKET_TEAM,
            "source": Lead.Source.INSTAGRAM, "priority": Lead.Priority.HIGH, "status": Lead.Status.NEW,
            "country": "India",
        })
        lead = Lead.objects.get(business_name="Mumbai Team")
        self.assertRedirects(response, lead.get_absolute_url())
        self.assertEqual(lead.created_by, self.staff)
        self.assertTrue(lead.activities.filter(activity_type=LeadActivity.ActivityType.CREATED).exists())

    def test_edit_status_creates_activity(self):
        self.client.force_login(self.staff)
        response = self.client.post(reverse("leads:edit", args=[self.lead.pk]), {
            "business_name": self.lead.business_name, "category": Lead.Category.OTHER,
            "source": Lead.Source.OTHER, "priority": Lead.Priority.MEDIUM, "status": Lead.Status.REPLIED,
            "country": "India",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.lead.activities.filter(activity_type=LeadActivity.ActivityType.STATUS_CHANGED).exists())

    def test_add_activity_updates_lead(self):
        self.client.force_login(self.staff)
        next_date = timezone.localdate() + timedelta(days=2)
        self.client.post(reverse("leads:activity_add", args=[self.lead.pk]), {
            "activity_type": LeadActivity.ActivityType.REPLIED, "message": "Interested",
            "activity_date": timezone.localdate(), "next_follow_up_date": next_date,
        })
        self.lead.refresh_from_db()
        self.assertEqual(self.lead.next_follow_up_date, next_date)
        self.assertEqual(self.lead.last_contact_date, timezone.localdate())

    def test_post_quick_actions(self):
        self.client.force_login(self.staff)
        actions = [
            ("replied", Lead.Status.REPLIED, "reply_received"),
            ("demo-requested", Lead.Status.DEMO_REQUESTED, None),
            ("demo-sent", Lead.Status.DEMO_SENT, "demo_sent"),
            ("proposal-sent", Lead.Status.PROPOSAL_SENT, "proposal_sent"),
            ("won", Lead.Status.WON, None), ("lost", Lead.Status.LOST, None),
        ]
        for action, status, flag in actions:
            response = self.client.post(reverse("leads:action", args=[self.lead.pk, action]))
            self.assertEqual(response.status_code, 302)
            self.lead.refresh_from_db()
            self.assertEqual(self.lead.status, status)
            if flag:
                self.assertTrue(getattr(self.lead, flag))
        self.assertEqual(self.client.get(reverse("leads:action", args=[self.lead.pk, "won"])).status_code, 405)

    def test_archive_excludes_and_restore_returns_lead(self):
        self.client.force_login(self.staff)
        self.client.post(reverse("leads:action", args=[self.lead.pk, "archive"]))
        self.lead.refresh_from_db()
        self.assertTrue(self.lead.is_archived)
        self.assertNotContains(self.client.get(reverse("leads:list")), self.lead.business_name)
        self.assertContains(self.client.get(reverse("leads:archived")), self.lead.business_name)
        self.client.post(reverse("leads:action", args=[self.lead.pk, "restore"]))
        self.lead.refresh_from_db()
        self.assertFalse(self.lead.is_archived)

    def test_search_filter_sort_and_pagination_preservation(self):
        Lead.objects.bulk_create([Lead(business_name=f"Lead {number:02d}", city="Jaipur", priority=Lead.Priority.HIGH) for number in range(20)])
        self.client.force_login(self.staff)
        response = self.client.get(reverse("leads:list"), {"q": "Lead", "priority": Lead.Priority.HIGH, "sort": "business", "direction": "asc", "page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertIn("q=Lead", response.context["querystring"])
        self.assertIn("priority=high", response.context["querystring"])

    def test_admin_login_css_and_public_pages(self):
        self.assertEqual(self.client.get(reverse("admin:login")).status_code, 200)
        self.assertContains(self.client.get(reverse("admin:login")), "yuvi_admin.css")
        for name in ("home", "services", "packages", "portfolio", "contact"):
            self.assertEqual(self.client.get(reverse(name)).status_code, 200)
