from django.db import migrations, models
import django.db.models.deletion


INDUSTRIES = [
    ("General Business & Services", "business-services", "▦", "Most Requested", "Professional websites that build trust and turn visits into enquiries.", "BUSINESS WEBSITE SOLUTIONS", "Make Your Business Easier to Trust and Contact.", "Present services, proof and contact options through a polished website built around real business goals.", "#6842d8"),
    ("Restaurant & Cafe", "restaurant-cafe", "◉", "High Conversion", "Websites for restaurants, cafes, bakeries and dessert businesses.", "FOOD BUSINESS WEBSITE SOLUTIONS", "Turn Your Menu and Ambience Into More Visits and Enquiries.", "Showcase menus, signature products, offers, location, gallery and ordering options for restaurants, cafes, bakeries and dessert brands.", "#a65b35"),
    ("Travel & Tourism", "travel-tourism", "✈", "Booking Focused", "Present destinations, itineraries and booking enquiries clearly.", "TRAVEL WEBSITE SOLUTIONS", "Present Destinations and Packages With Clarity.", "Help travellers compare experiences, understand itineraries and enquire through an airy, confidence-building website.", "#3182a0"),
    ("Beauty, Salon & Makeup", "beauty-salon", "✦", "Premium Industry", "Turn beauty portfolios and services into booking enquiries.", "BEAUTY WEBSITE SOLUTIONS", "Turn Your Work Into a Premium Booking Experience.", "Present services, transformations, galleries and booking options in an elegant experience tailored to your beauty brand.", "#a45f82"),
    ("Sports, Cricket & Community", "cricket-sports", "●", "Registration Ready", "Bring teams, fixtures, registrations and updates together.", "SPORTS WEBSITE SOLUTIONS", "Give Your League One Official Digital Home.", "Bring teams, fixtures, standings, registrations, sponsors and updates together in one professional platform.", "#4167c7"),
    ("Real Estate", "real-estate", "⌂", "Lead Generation", "Showcase properties and turn buyer interest into qualified leads.", "REAL ESTATE WEBSITE SOLUTIONS", "Turn Property Interest Into Qualified Enquiries.", "Showcase listings, locations, amenities and property details through a professional experience designed to build buyer confidence.", "#596677"),
    ("Gym & Fitness", "gym-fitness", "◆", "High Conversion", "Convert fitness interest into trials and memberships.", "FITNESS WEBSITE SOLUTIONS", "Convert Fitness Interest Into Membership Enquiries.", "Present programmes, trainers, plans and transformations through an energetic website built to generate enquiries.", "#526a36"),
    ("Hotels & Hospitality", "hotels-hospitality", "▤", "Booking Focused", "Help guests explore rooms, amenities and booking options.", "HOTEL WEBSITE SOLUTIONS", "Help Guests Explore, Trust and Book With Confidence.", "Show rooms, amenities, experiences, location and enquiry options through a premium hospitality website.", "#8c6847"),
    ("Wedding & Event Planning", "wedding-events", "◇", "Premium Industry", "Showcase celebrations, services and planning expertise.", "EVENT WEBSITE SOLUTIONS", "Showcase Every Celebration With Style and Detail.", "Present past events, planning services, decor options and enquiry flows in a refined visual experience.", "#a06f91"),
    ("Shops & Product Businesses", "shops-products", "▣", "", "A polished storefront for products, offers and local enquiries.", "SHOP WEBSITE SOLUTIONS", "Present Products, Offers and Your Brand in One Polished Storefront.", "Make products easier to discover while keeping location, offers, WhatsApp and enquiry actions clear.", "#5370a8"),
    ("Personal Brands & Portfolios", "personal-portfolios", "◎", "Trust Focused", "Show expertise, selected work and services professionally.", "PORTFOLIO WEBSITE SOLUTIONS", "Turn Your Experience Into a Strong Personal Brand.", "Bring your work, services, proof and contact journey together in one focused professional portfolio.", "#7552ba"),
    ("Web Design & Creative Agencies", "creative-agencies", "✣", "", "Present services, process and selected work with authority.", "AGENCY WEBSITE SOLUTIONS", "Make Your Creative Work Feel as Strong as the Results.", "Show services, process, projects and proof through a confident agency experience designed for serious enquiries.", "#6842d8"),
    ("Pet Shops & Pet Services", "pet-services", "♢", "", "Friendly product, grooming and local-service enquiry flows.", "PET BUSINESS WEBSITE SOLUTIONS", "Bring Products, Care and Enquiries Into One Friendly Experience.", "Present products, grooming, offers, reviews and store information through a warm, practical website.", "#438b83"),
    ("Local Service Businesses", "local-services", "◫", "Trust Focused", "Make services, proof, location and contact easy to understand.", "LOCAL SERVICE WEBSITE SOLUTIONS", "Turn Local Searches Into Real Customer Enquiries.", "Present services, pricing, proof, service areas and contact options through a credible local-business website.", "#526c9a"),
    ("Clinics & Healthcare Practices", "clinic-healthcare", "+", "Trust Focused", "Credible clinic websites with profiles and appointment enquiries.", "CLINIC WEBSITE SOLUTIONS", "Build Patient Trust Before the First Appointment.", "Present doctors, treatments, timings, locations and appointment options through a clean, credible and patient-friendly website.", "#397f94"),
    ("Custom Business Systems", "custom-systems", "⚙", "", "Tailored admin, booking, payment and management workflows.", "CUSTOM SYSTEM SOLUTIONS", "Build the Workflow Your Business Actually Needs.", "Combine a professional public website with tailored admin controls, bookings, payments or operational tools.", "#6842d8"),
]

CLINIC_PACKAGES = [
    ("Starter Clinic Website", "A credible clinic website covering the information patients look for first.", ["Professional homepage", "Doctor or clinic introduction", "Services and treatments", "Timings and location map", "Contact and WhatsApp", "Mobile responsive layout", "Basic SEO structure"], ["Best for: Single-doctor and small clinics", "Up to 5 core pages or sections", "2 revision rounds"]),
    ("Professional Clinic Website", "A detailed clinic experience with doctor profiles, treatment pages and appointment enquiries.", ["Everything in Starter", "Doctor profile pages", "Treatment detail pages", "Appointment enquiry form", "Patient FAQs and testimonials", "Multiple location support", "Admin-saved enquiries"], ["Best for: Growing clinics and specialist practices", "Up to 10 pages or sections", "3 revision rounds"]),
    ("Premium Multi-Doctor Clinic Website", "A premium multi-doctor website with departments, richer content and advanced enquiry flows.", ["Multiple doctors and departments", "Advanced appointment enquiry flow", "Rich treatment content", "Ethical before/after gallery option", "Resources or health education section", "Admin content management", "Integration planning"], ["Best for: Multi-doctor clinics and diagnostic centres", "Final structure confirmed after content review", "3 revision rounds"]),
    ("Custom Appointment & Clinic System", "A tailored clinic system for advanced appointment, content or operational workflows.", ["Custom appointment workflow", "Doctor and schedule management", "Admin dashboard", "Enquiry and patient-request records", "Custom modules", "Integration planning", "Launch support"], ["Best for: Clinics needing tailored operational tools", "Custom scope required", "Third-party integrations quoted separately"]),
]

CLINIC_PRICES = {
    "Starter Clinic Website": {"IN": (25000, 40000, "INR", "₹"), "US_INTL": (650, 1000, "USD", "$"), "UK": (500, 800, "GBP", "£"), "AU": (1000, 1550, "AUD", "A$"), "CA": (900, 1350, "CAD", "C$")},
    "Professional Clinic Website": {"IN": (45000, 80000, "INR", "₹"), "US_INTL": (1100, 1900, "USD", "$"), "UK": (850, 1500, "GBP", "£"), "AU": (1700, 3000, "AUD", "A$"), "CA": (1500, 2600, "CAD", "C$")},
    "Premium Multi-Doctor Clinic Website": {"IN": (85000, 160000, "INR", "₹"), "US_INTL": (2000, 3700, "USD", "$"), "UK": (1600, 2900, "GBP", "£"), "AU": (3100, 5800, "AUD", "A$"), "CA": (2700, 5000, "CAD", "C$")},
    "Custom Appointment & Clinic System": {"IN": (125000, None, "INR", "₹"), "US_INTL": (3000, None, "USD", "$"), "UK": (2400, None, "GBP", "£"), "AU": (4700, None, "AUD", "A$"), "CA": (4100, None, "CAD", "C$")},
}


def seed(apps, schema_editor):
    Industry = apps.get_model("core", "Industry")
    Package = apps.get_model("core", "Package")
    Price = apps.get_model("core", "PackageMarketPrice")
    Demo = apps.get_model("core", "PortfolioProject")
    industries = {}
    for order, values in enumerate(INDUSTRIES, 1):
        title, slug, icon, badge, short, eyebrow, heading, text, accent = values
        industries[slug], _ = Industry.objects.get_or_create(slug=slug, defaults={"title": title, "icon": icon, "badge": badge, "short_description": short, "eyebrow": eyebrow, "hero_heading": heading, "hero_text": text, "accent": accent, "order": order})
    demo_map = {
        "restaurant-cafe": ["Restaurant Website Demo", "Cafe Landing Page Demo"], "travel-tourism": ["Trips & Tours Website Demo"],
        "beauty-salon": ["Salon Makeup Artist Demo"], "cricket-sports": ["Cricket Intelligence Dashboard Demo"], "real-estate": ["Real Estate Property Demo"],
        "gym-fitness": ["Gym Website Demo"], "hotels-hospitality": ["Hotel Website Demo"], "wedding-events": ["Wedding & Event Planner Website Demo"],
        "shops-products": ["Shop Website Demo"], "personal-portfolios": ["Personal Portfolio Website"], "creative-agencies": ["Web Design Agency Demo"],
        "pet-services": ["Pet Shop Website Demo"], "local-services": ["Local Service Business Demo"], "business-services": ["Local Service Business Demo"],
    }
    category_map = {
        "restaurant-cafe": ["Digital Menu / Single Page Website", "Basic Restaurant Website", "Professional Restaurant Website", "Premium Restaurant Website", "Advanced Restaurant System"],
        "travel-tourism": ["Trips & Tours Website"], "beauty-salon": ["Salon & Makeup Artist Websites"], "cricket-sports": ["Sports & Community Websites"],
        "hotels-hospitality": ["Hotel Websites"], "wedding-events": ["Wedding & Event Planner Websites"], "pet-services": ["Pet Shop Websites"],
        "custom-systems": ["Advanced Business System", "Advanced Restaurant System"],
    }
    business_categories = ["Starter Business Website", "Professional Business Website", "Premium Business Website"]
    for slug in ["business-services", "real-estate", "gym-fitness", "shops-products", "personal-portfolios", "creative-agencies", "local-services"]:
        category_map[slug] = business_categories
    for slug, categories in category_map.items():
        industries[slug].packages.add(*Package.objects.filter(category__in=categories))
    for slug, titles in demo_map.items():
        industries[slug].demos.add(*Demo.objects.filter(title__in=titles))
    order = (Package.objects.order_by("-order").values_list("order", flat=True).first() or 0)
    for offset, (title, description, features, limits) in enumerate(CLINIC_PACKAGES, 1):
        package, _ = Package.objects.get_or_create(title=title, defaults={"category": "Clinic & Healthcare Websites", "price": "Market-specific pricing", "short_description": description, "included_features": "\n".join(features), "scope_limits": "\n".join(limits), "summary": description, "public_pricing_type": "SCOPE_BASED" if title.startswith("Custom") else "CUSTOM_QUOTE", "order": order + offset})
        industries["clinic-healthcare"].packages.add(package)
        for display_order, (market, values) in enumerate(CLINIC_PRICES[title].items(), 1):
            minimum, maximum, currency, symbol = values
            Price.objects.get_or_create(package=package, market_code=market, defaults={"currency_code": currency, "currency_symbol": symbol, "min_price": minimum, "max_price": maximum, "pricing_mode": "STARTING_FROM" if maximum is None else "RANGE", "is_active": True, "display_order": display_order})
    clinic_demo, _ = Demo.objects.get_or_create(title="Clinic Website Demo", defaults={"description": "A calm, professional clinic website concept featuring doctor profiles, treatments, timings, appointment enquiries, FAQs, reviews and location details.", "tech_stack": "Healthcare Website", "order": 11})
    industries["clinic-healthcare"].demos.add(clinic_demo)
    faqs = {
        "real-estate": "Can property listings be managed from an admin panel?|Yes. An editable listing workflow can be included when confirmed in scope.\nCan leads be sent to email or WhatsApp?|Enquiry forms, email notifications and WhatsApp actions can be configured.",
        "clinic-healthcare": "Can patients request appointments online?|Yes. The website can collect appointment enquiries; confirmed booking automation is scoped separately.\nCan multiple doctors have separate profiles?|Yes. Doctor profiles, treatments and timings can be structured separately.\nAre third-party appointment integrations available?|Available integrations can be reviewed and quoted after compatibility checks.",
        "cricket-sports": "Can fixtures and points tables be updated?|Yes. Admin-managed fixtures and standings can be included in the agreed scope.\nCan registrations be collected?|Registration enquiry forms and admin-saved submissions can be included.",
    }
    for industry in Industry.objects.all():
        industry.faq = faqs.get(industry.slug, "Can the website be customized for my business?|Yes. Content, sections, colours and functionality are finalized around the confirmed scope.\nCan more features be added later?|Additional functionality can be reviewed and quoted as the business grows.")
        industry.save(update_fields=["faq"])


def unseed(apps, schema_editor):
    apps.get_model("core", "Industry").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("core", "0021_enquiry_displayed_price_context_and_more")]
    operations = [
        migrations.CreateModel(
            name="Industry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)), ("slug", models.SlugField(max_length=120, unique=True)),
                ("icon", models.CharField(blank=True, max_length=12)), ("badge", models.CharField(blank=True, max_length=40)),
                ("short_description", models.CharField(max_length=220)), ("eyebrow", models.CharField(max_length=120)),
                ("hero_heading", models.CharField(max_length=220)), ("hero_text", models.TextField()),
                ("accent", models.CharField(default="#6842d8", max_length=20)), ("hero_image", models.ImageField(blank=True, upload_to="industries/")),
                ("faq", models.TextField(blank=True, help_text="One question and answer per line, separated with |")),
                ("is_active", models.BooleanField(default=True)), ("order", models.PositiveSmallIntegerField(default=0)),
                ("demos", models.ManyToManyField(blank=True, related_name="industries", to="core.portfolioproject")),
                ("packages", models.ManyToManyField(blank=True, related_name="industries", to="core.package")),
            ],
            options={"verbose_name_plural": "Industries", "ordering": ["order", "title"]},
        ),
        migrations.RunPython(seed, unseed),
    ]
