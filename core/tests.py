from django.test import TestCase
from django.urls import reverse

from .models import Review


class FeedbackFlowTests(TestCase):
    def test_public_feedback_is_saved_pending(self):
        response = self.client.post(
            reverse("feedback"),
            {
                "client_name": "Test Client",
                "business_name": "Test Brand",
                "email": "client@example.com",
                "location": "Delhi",
                "service_received": "Business website",
                "rating": "5",
                "quote": "Clear communication and a polished final website.",
            },
        )
        self.assertRedirects(response, reverse("feedback"))
        review = Review.objects.get(client_name="Test Client")
        self.assertEqual(review.status, Review.Status.PENDING)
        self.assertEqual(review.source, Review.Source.WEBSITE)

    def test_only_approved_featured_feedback_appears_on_homepage(self):
        pending = Review.objects.create(client_name="Pending Client", rating=4, quote="Pending review")
        approved = Review.objects.create(
            client_name="Approved Client",
            rating=5,
            quote="Approved review",
            status=Review.Status.APPROVED,
            is_featured=True,
        )
        response = self.client.get(reverse("home"))
        self.assertNotContains(response, pending.quote)
        self.assertContains(response, approved.quote)

    def test_feedback_page_renders(self):
        response = self.client.get(reverse("feedback"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Submit Feedback")
