from django.test import TestCase
from django.urls import reverse
import json

from .models import AboutProfile, Enquiry, Industry, Package, PackageMarketPrice, PortfolioProject, Review, Service
from .assistant import INTENT_NAMES, answer_message, match_intent


class AssistantEndpointTests(TestCase):
    def setUp(self):
        self.package = Package.objects.create(title="Assistant Starter", price="internal", short_description="Starter", included_features="Homepage")
        self.industry = Industry.objects.create(title="Assistant Clinic", slug="assistant-clinic", short_description="Clinic sites", eyebrow="Clinic", hero_heading="Clinic website", hero_text="Trust and appointments")
        self.industry.packages.add(self.package)
        PackageMarketPrice.objects.create(package=self.package, market_code="IN", currency_code="INR", currency_symbol="₹", min_price=20000, max_price=30000)

    def post_lead(self, **updates):
        payload = {"name":"Test Client","email":"assistant@example.com","phone":"12345","industry":self.industry.slug,"package_id":self.package.pk,"market":"IN","consent":True,"source_page":"/packages/"}
        payload.update(updates)
        return self.client.post(reverse("assistant_lead"), data=json.dumps(payload), content_type="application/json")

    def test_context_returns_server_price(self):
        response = self.client.get(reverse("assistant_context"), {"market":"IN"})
        self.assertEqual(response.status_code, 200)
        industry = next(item for item in response.json()["industries"] if item["slug"] == self.industry.slug)
        self.assertEqual(industry["packages"][0]["price"], "₹20,000 – ₹30,000")

    def test_consent_is_required(self):
        response = self.post_lead(consent=False)
        self.assertEqual(response.status_code, 400)
        self.assertFalse(Enquiry.objects.exists())

    def test_invalid_package_is_rejected(self):
        response = self.post_lead(package_id=999999)
        self.assertEqual(response.status_code, 400)

    def test_saved_price_is_loaded_server_side(self):
        response = self.post_lead(displayed_price_context="₹1")
        self.assertEqual(response.status_code, 200)
        enquiry = Enquiry.objects.get(email="assistant@example.com")
        self.assertEqual(enquiry.displayed_price_context, "₹20,000 – ₹30,000")


class AssistantHumanLikeUpgradeTests(TestCase):
    def setUp(self):
        self.package = Package.objects.create(
            title="Premium Assistant Clinic Website", price="internal", short_description="Premium clinic scope",
            included_features="Doctor profiles\nAppointment requests\nServices\nTestimonials\nEnquiry management",
            scope_limits="Up to 8 pages\nOne clinic location",
        )
        self.industry, _ = Industry.objects.get_or_create(
            slug="clinic-healthcare",
            defaults={"title":"Clinics & Healthcare Practices", "short_description":"Clinic sites", "eyebrow":"Healthcare", "hero_heading":"Clinic website", "hero_text":"Build patient trust"},
        )
        self.industry.packages.clear()
        self.industry.packages.add(self.package)
        PackageMarketPrice.objects.create(
            package=self.package, market_code="AU", currency_code="AUD", currency_symbol="A$",
            min_price=1700, max_price=3000,
        )
        AboutProfile.objects.create(
            name="Test Founder", role="Web Developer", headline="Builds practical websites.",
            bio="Creates responsive business websites.", highlight_one="Django",
        )

    def post_message(self, message, **extra):
        payload = {"message": message, "source_page": "/"}
        payload.update(extra)
        return self.client.post(reverse("assistant_message"), json.dumps(payload), content_type="application/json")

    def test_registry_contains_exactly_150_intents(self):
        self.assertEqual(len(INTENT_NAMES), 150)
        self.assertEqual(len(set(INTENT_NAMES)), 150)

    def test_bootstrap_contains_public_knowledge_without_private_fields(self):
        data = self.client.get(reverse("assistant_bootstrap")).json()
        self.assertEqual(data["intent_count"], 150)
        self.assertEqual(data["founder"]["name"], "Test Founder")
        self.assertNotIn("email", data["founder"])
        self.assertNotIn("phone", data["founder"])

    def test_hinglish_context_is_remembered_for_follow_up_price(self):
        first = self.post_message("Mujhe clinic ki premium website chahiye")
        self.assertEqual(first.status_code, 200)
        second = self.post_message("Australia ka price kitna hai?")
        self.assertIn("A$1,700 – A$3,000 AUD", second.json()["reply"])
        self.assertEqual(second.json()["context"]["industry"], "clinic-healthcare")

    def test_current_page_adds_industry_context(self):
        response = self.post_message("premium price Australia", source_page="/packages/clinic-healthcare/")
        self.assertIn("A$1,700 – A$3,000 AUD", response.json()["reply"])

    def test_founder_answer_uses_database_profile(self):
        response = self.post_message("Who is Yuvraj?")
        self.assertContains(response, "Test Founder")
        self.assertContains(response, "Builds practical websites")

    def test_greeting_uses_multiple_variations(self):
        replies = [self.post_message("hello").json()["reply"] for _ in range(3)]
        self.assertEqual(len(set(replies)), 3)

    def test_restart_clears_old_context(self):
        self.post_message("clinic premium Australia")
        response = self.post_message("hello", restart=True)
        self.assertEqual(response.json()["context"].get("industry"), "")

    def test_package_and_pricing_endpoints_are_grounded(self):
        packages = self.client.get(reverse("assistant_packages"), {"industry": self.industry.slug})
        self.assertContains(packages, "Doctor profiles")
        pricing = self.client.get(reverse("assistant_pricing"), {"industry": self.industry.slug, "market": "AU"})
        self.assertEqual(pricing.json()["prices"][0]["price"], "A$1,700 – A$3,000 AUD")

    def test_all_registered_intents_can_generate_a_safe_response(self):
        for intent in INTENT_NAMES:
            payload = answer_message(intent.replace("_", " "), {})
            self.assertTrue(payload["reply"], intent)
            self.assertIn(payload["intent"], INTENT_NAMES)

    def test_chat_template_has_accessibility_and_trust_controls(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "data-chat-minimize")
        self.assertContains(response, "data-chat-unread")
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertContains(response, "Replies are based on current Yuvi Creates website information")

    def test_about_page_uses_public_founder_and_active_industries(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Meet <em>Yuvraj.</em>", html=True)
        self.assertContains(response, "WHY I STARTED YUVI CREATES")
        self.assertContains(response, "Premium Assistant Clinic Website", count=0)
        self.assertContains(response, "Clinics &amp; Healthcare Practices")
        self.assertContains(response, self.industry.get_absolute_url())
        self.assertContains(response, "ABOUT FAQ")
        self.assertNotContains(response, "years of experience")
        self.assertNotContains(response, "guaranteed leads")

    def test_assistant_uses_shared_approved_about_story(self):
        reason = self.post_message("Why was Yuvi Creates started?").json()["reply"]
        self.assertIn("every business deserves a website", reason)
        stack = self.post_message("Which technologies are used?").json()["reply"]
        self.assertIn("Python, Django, HTML, CSS, JavaScript", stack)


class DemoBadgeAndHomeTrustTests(TestCase):
    def setUp(self):
        self.featured = PortfolioProject.objects.create(
            title="Badge Premium Demo", description="A premium example", tech_stack="Django",
            experience_level=PortfolioProject.ExperienceLevel.PREMIUM,
            is_featured=True, is_new=True, is_popular=True,
        )
        self.inactive = PortfolioProject.objects.create(
            title="Private Draft Demo", description="Not public", tech_stack="Django", is_active=False,
        )

    def test_status_badges_follow_priority_and_stop_at_two(self):
        self.assertEqual(
            [item["label"] for item in self.featured.visible_status_badges],
            ["Featured", "New"],
        )

    def test_demo_collection_renders_level_status_and_combined_filter(self):
        response = self.client.get(reverse("portfolio"))
        self.assertContains(response, "Badge Premium Demo")
        self.assertContains(response, "Premium")
        self.assertContains(response, "Featured")
        self.assertContains(response, 'data-level="premium"')
        self.assertContains(response, "Project Level")
        self.assertNotContains(response, "Private Draft Demo")
        self.assertNotContains(response, "Request Similar</a>")

    def test_inactive_demo_cannot_be_opened_directly(self):
        response = self.client.get(reverse("portfolio_demo", args=[self.inactive.pk, "private-draft-demo"]))
        self.assertEqual(response.status_code, 404)

    def test_home_uses_new_conversion_trust_copy(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Built to Look Professional—and Help Visitors Take Action.")
        self.assertContains(response, "Professional Business Presence")
        self.assertContains(response, "A Website Partner Who Understands the Business Behind the Design.")
        self.assertContains(response, "You work directly with Yuvraj")
        self.assertNotContains(response, "The important things clients expect are already planned")
        self.assertContains(response, "Real experiences.")
        self.assertContains(response, "Share an honest review")

    def test_process_page_uses_clear_premium_project_journey(self):
        response = self.client.get(reverse("process"))
        self.assertContains(response, "From first idea to a website")
        self.assertContains(response, "Six practical phases")
        self.assertContains(response, "One clear point of communication")
        self.assertContains(response, "Discuss Your Website")

    def test_assistant_lists_only_active_badged_demos(self):
        premium = answer_message("Show premium demos", {})
        self.assertIn("Badge Premium Demo", premium["reply"])
        self.assertNotIn("Private Draft Demo", premium["reply"])
        featured = answer_message("Which demos are featured?", {})
        self.assertIn("Badge Premium Demo", featured["reply"])
        comparison = answer_message("What is the difference between starter and premium demos?", {})
        self.assertIn("Starter is a focused first presence", comparison["reply"])
        self.assertNotIn("₹", comparison["reply"])
        budget = answer_message("Which demo is suitable for a small budget?", {})
        self.assertIn("Starter demos", budget["reply"])
        self.assertIn("final price still depends", budget["reply"])


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


class ServicesPageUpgradeTests(TestCase):
    def test_every_service_has_enriched_business_content(self):
        response = self.client.get(reverse("services"))
        self.assertEqual(response.status_code, 200)
        service_count = Service.objects.count()
        self.assertContains(response, "BEST FOR", count=service_count)
        self.assertContains(response, ">Explore Service <span>", count=service_count)
        self.assertContains(response, ">Get a Quote →</a>", count=service_count)
        self.assertContains(response, "Industry-relevant direction")
        self.assertContains(response, "Final scope is confirmed before work begins")

    def test_service_cards_keep_database_content_and_valid_demo_links(self):
        from django.utils.html import conditional_escape
        from django.utils.text import slugify
        response = self.client.get(reverse("services"))
        for service in Service.objects.all():
            self.assertContains(response, conditional_escape(service.title))
            self.assertContains(response, reverse("service_demo", args=[service.pk, slugify(service.title)]), status_code=200)

    def test_every_service_demo_route_still_renders(self):
        from django.utils.html import conditional_escape
        self.client.get(reverse("services"))
        from django.utils.text import slugify
        for service in Service.objects.all():
            response = self.client.get(reverse("service_demo", args=[service.pk, slugify(service.title)]))
            self.assertEqual(response.status_code, 200, service.title)
            self.assertContains(response, conditional_escape(service.title))
            self.assertContains(response, "Recommended Page Flow")
            self.assertContains(response, "Service Essentials")
            self.assertContains(response, "Service FAQ")
            self.assertContains(response, "View Matching Packages")

    def test_each_service_quote_link_prefills_the_selected_service(self):
        self.client.get(reverse("services"))
        service = Service.objects.get(title="Hotel Websites")
        response = self.client.get(reverse("contact"), {"service": service.title, "source": "Service Detail Page"})
        self.assertContains(response, service.title)
        self.assertContains(response, "Enquiry source: Service Detail Page")


class PackagesPageTests(TestCase):
    def test_premium_solution_categories_render(self):
        response = self.client.get(reverse("packages"))
        self.assertEqual(response.status_code, 200)
        for category in (
            "General Business &amp; Services",
            "Restaurant &amp; Cafe",
            "Travel &amp; Tourism",
            "Clinics &amp; Healthcare Practices",
            "Sports, Cricket &amp; Community",
            "Custom Business Systems",
        ):
            self.assertContains(response, category)
        self.assertContains(response, "Choose Your Industry")
        self.assertContains(response, "View Packages", count=21)
        self.assertNotContains(response, 'data-scope-template=')

    def test_focused_package_query_highlights_relevant_solution(self):
        response = self.client.get(reverse("industry_packages", args=["restaurant-cafe"]))
        self.assertContains(response, "FOOD BUSINESS WEBSITE SOLUTIONS")
        self.assertContains(response, "View Full Scope")
        self.assertNotContains(response, "Starter Clinic Website")

    def test_every_active_industry_route_renders(self):
        self.client.get(reverse("packages"))
        for industry in Industry.objects.filter(is_active=True):
            response = self.client.get(reverse("industry_packages", args=[industry.slug]))
            self.assertEqual(response.status_code, 200, industry.slug)

    def test_clinic_packages_prices_and_demo_are_connected(self):
        self.client.get(reverse("packages"))
        industry = Industry.objects.get(slug="clinic-healthcare")
        self.assertEqual(industry.packages.count(), 4)
        self.assertTrue(industry.demos.filter(title="Clinic Website Demo").exists())
        starter = industry.packages.get(title="Starter Clinic Website")
        self.assertEqual(starter.market_prices.count(), 5)
        self.assertEqual(starter.market_prices.get(market_code="IN").public_label, "₹25,000 – ₹40,000")

    def test_industry_quote_prefill_is_server_validated(self):
        self.client.get(reverse("packages"))
        industry = Industry.objects.get(slug="clinic-healthcare")
        package = industry.packages.get(title="Professional Clinic Website")
        response = self.client.get(reverse("contact"), {"industry": industry.slug, "package": package.pk, "market": "AU"})
        self.assertContains(response, "Clinics &amp; Healthcare Practices")
        self.assertContains(response, package.title)
        self.assertContains(response, "A$1,700 – A$3,000 AUD")

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
