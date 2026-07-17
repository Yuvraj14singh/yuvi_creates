from django.test import TestCase
from django.urls import reverse

from .models import Enquiry, Package, PackageMarketPrice, Review


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


class PackagesPageTests(TestCase):
    def test_premium_solution_categories_render(self):
        response = self.client.get(reverse("packages"))
        self.assertEqual(response.status_code, 200)
        for category in (
            "Business Websites",
            "Restaurant &amp; Cafe Websites",
            "Travel &amp; Tourism Websites",
            "Beauty &amp; Personal Brand Websites",
            "Sports &amp; Community Websites",
            "Custom Business Systems",
        ):
            self.assertContains(response, category)
        self.assertContains(response, "Get a Project Quote")
        self.assertContains(response, "Discuss Your Project")
        self.assertContains(response, "View Full Scope")
        self.assertContains(response, "Custom Quotes, Clear Scope")
        self.assertNotContains(response, "Request Pricing")
        self.assertNotContains(response, "Starting price available on request")
        self.assertNotContains(response, "Tailored Pricing")
        self.assertNotContains(response, "Scope-Based Pricing")
        self.assertNotContains(response, 'class="investment"')
        self.assertContains(response, "₹18,000 – ₹30,000")
        self.assertContains(response, "$450 – $700 USD")
        self.assertContains(response, 'role="dialog"')
        self.assertContains(response, 'data-scope-template=')
        self.assertNotContains(response, 'class="full-scope"')

    def test_focused_package_query_highlights_relevant_solution(self):
        response = self.client.get(reverse("packages"), {"focus": "restaurant"})
        self.assertContains(response, 'data-solution-link="restaurant-cafe-websites"')
        self.assertContains(response, "Restaurant and cafe packages")

    def test_proposal_link_prefills_existing_contact_form(self):
        self.client.get(reverse("packages"))
        package = Package.objects.first()
        response = self.client.get(reverse("contact"), {"package": package.pk, "market": "US_INTL"})
        self.assertContains(response, package.title)
        self.assertContains(response, "$450 – $700 USD")

    def test_international_quote_fields_are_saved(self):
        self.client.get(reverse("packages"))
        package = Package.objects.first()
        response = self.client.post(
            reverse("contact"),
            {
                "name": "International Client",
                "business_name": "Example Studio",
                "email": "client@example.com",
                "phone": "+1 555 0100",
                "country": "Canada",
                "preferred_currency": "CAD",
                "business_type": "Professional services",
                "package_interested_in": package.title,
                "current_website_or_social_link": "",
                "estimated_pages": "5–7 pages",
                "required_features": "Enquiry form and appointment requests",
                "preferred_timeline": "Flexible",
                "budget_level": "Not sure yet",
                "message": "We need a clear international business website.",
            },
        )
        self.assertRedirects(response, reverse("contact"))
        enquiry = Enquiry.objects.get(email="client@example.com")
        self.assertEqual(enquiry.country, "Canada")
        self.assertEqual(enquiry.preferred_currency, "CAD")
        self.assertEqual(enquiry.package_interested_in, package.title)

    def test_internal_price_remains_available_to_staff_data(self):
        self.client.get(reverse("packages"))
        package = Package.objects.first()
        self.assertTrue(package.price)
        self.assertTrue(package.public_pricing_type)
        self.assertEqual(package.market_prices.filter(is_active=True).count(), 5)

    def test_all_supported_currency_choices_are_available(self):
        from .forms import EnquiryForm
        values = {value for value, label in EnquiryForm().fields["preferred_currency"].choices}
        self.assertTrue({"INR", "USD", "GBP", "AUD", "CAD", "Other"}.issubset(values))

    def test_market_prices_are_manually_seeded_for_each_market(self):
        self.client.get(reverse("packages"))
        package = Package.objects.get(title="Professional Business Website")
        prices = {price.market_code: (price.min_price, price.max_price) for price in package.market_prices.all()}
        self.assertEqual(prices["IN"], (35000, 65000))
        self.assertEqual(prices["US_INTL"], (850, 1400))
        self.assertEqual(prices["UK"], (650, 1100))
        self.assertEqual(prices["AU"], (1300, 2200))
        self.assertEqual(prices["CA"], (1150, 1900))
        premium_inr = Package.objects.get(title="Premium Business Website").market_prices.get(market_code="IN")
        self.assertEqual(premium_inr.public_label, "₹70,000 – ₹1,40,000")
        custom_usd = Package.objects.get(title="Custom Business System").market_prices.get(market_code="US_INTL")
        self.assertEqual(custom_usd.public_label, "Starting from $2,500 USD")

    def test_server_ignores_tampered_market_and_price_context(self):
        self.client.get(reverse("packages"))
        package = Package.objects.get(title="Starter Business Website")
        response = self.client.post(
            reverse("contact") + f"?package={package.pk}&market=INVALID&displayed_price_context=$1",
            {
                "name": "Safe Client", "business_name": "Safe Co", "email": "safe@example.com", "phone": "123456",
                "country": "India", "preferred_currency": "USD", "business_type": "Services",
                "package_interested_in": "Tampered package", "estimated_pages": "5", "required_features": "Contact form",
                "preferred_timeline": "Flexible", "budget_level": "Not sure yet", "message": "Project details",
            },
        )
        self.assertRedirects(response, reverse("contact"))
        enquiry = Enquiry.objects.get(email="safe@example.com")
        self.assertEqual(enquiry.package_interested_in, package.title)
        self.assertEqual(enquiry.selected_market, "IN")
        self.assertEqual(enquiry.preferred_currency, "INR")
        self.assertEqual(enquiry.displayed_price_context, "₹18,000 – ₹30,000")

    def test_final_quote_fields_are_not_public_form_fields(self):
        from .forms import EnquiryForm
        fields = EnquiryForm().fields
        self.assertNotIn("final_quote_amount", fields)
        self.assertNotIn("final_quote_currency", fields)
        self.assertNotIn("displayed_price_context", fields)
