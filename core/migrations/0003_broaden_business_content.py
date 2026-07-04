from django.db import migrations


def add_business_content(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    Package = apps.get_model("core", "Package")
    PortfolioProject = apps.get_model("core", "PortfolioProject")

    services = [
        ("Business Websites", "Professional websites for cafes, restaurants, travel agencies, gyms, shops, institutes, salons, and local service businesses.", "01"),
        ("Trips & Tours Websites", "Tour package websites with itinerary sections, destination pages, enquiry forms, WhatsApp CTA, and booking lead flow.", "02"),
        ("Shop / Local Store Websites", "Product showcase websites with offers, location, gallery, contact flow, and WhatsApp enquiry.", "10"),
        ("Gym / Fitness Websites", "Membership, trainer, timetable, transformation, and lead-generation websites for gyms and fitness brands.", "11"),
    ]
    for index, (title, description, icon) in enumerate(services, start=1):
        Service.objects.update_or_create(
            title=title,
            defaults={"description": description, "icon": icon, "order": index},
        )
    existing_service_order = {
        "Restaurant/Cafe Websites": ("03", 3),
        "Digital Menu / QR Menu Websites": ("04", 4),
        "Landing Pages": ("05", 5),
        "Portfolio Websites": ("06", 6),
        "Small Business Websites": ("07", 7),
        "Website Redesign / Improvement": ("08", 8),
        "Responsive Website Development": ("09", 9),
        "Basic SEO-Friendly Website Setup": ("10", 10),
        "Domain/Hosting Setup Support": ("11", 11),
    }
    for title, (icon, order) in existing_service_order.items():
        Service.objects.filter(title=title).update(icon=icon, order=order)

    packages = [
        {
            "category": "Starter Business Website",
            "title": "Starter Business Website",
            "price": "₹12,000-₹18,000",
            "short_description": "A clean 3-5 section website for any small business that needs a professional online presence.",
            "included_features": "Professional homepage\nAbout/business intro section\nServices or products section\nGallery or highlights section\nContact section\nWhatsApp button\nCall button\nGoogle Map embed\nMobile responsive design\nBasic SEO title/description\n1-2 rounds minor revisions",
            "scope_limits": "Up to 5 sections\nBest for simple businesses\nContent and photos provided by client\n1-2 rounds minor revisions",
            "order": 0,
        },
        {
            "category": "Professional Business Website",
            "title": "Professional Business Website",
            "price": "₹25,000-₹45,000",
            "short_description": "A stronger multi-page website for service providers, shops, gyms, institutes, clinics, salons, and personal brands.",
            "included_features": "Premium homepage\nAbout page\nServices/products pages\nPortfolio/work or gallery page\nTestimonials section\nFAQ section\nContact/enquiry form\nWhatsApp/call CTA\nGoogle Map\nBasic SEO-friendly structure\nAdmin-saved enquiries\n2-3 rounds revisions",
            "scope_limits": "Up to 6-8 pages/sections\nAdvanced features quoted separately\n2-3 rounds revisions",
            "order": 1,
        },
        {
            "category": "Trips & Tours Website",
            "title": "Tour & Travel Website",
            "price": "₹30,000-₹60,000",
            "short_description": "A tour business website for destinations, trip packages, itinerary details, and booking enquiries.",
            "included_features": "Premium travel homepage\nTour package listing\nIndividual package/detail sections\nItinerary highlights\nDestination gallery\nPricing or starting-from prices\nBooking/enquiry form\nWhatsApp CTA\nGoogle Map/location support\nFAQ section\nBasic SEO-friendly structure\nAdmin-saved enquiries",
            "scope_limits": "Up to 8-10 tour packages\nOnline payment/booking automation quoted separately\nPhotos and package details provided by client",
            "order": 2,
        },
        {
            "category": "Advanced Business System",
            "title": "Custom Business System",
            "price": "₹80,000+",
            "short_description": "A custom website system with admin panel, bookings, payments, dashboards, or content management.",
            "included_features": "Custom backend\nAdmin panel\nEnquiry/customer management\nBooking or request flow\nPayment gateway integration placeholder\nContent management\nCustom pages/modules\nPerformance and launch setup support",
            "scope_limits": "Custom quote required\nGateway keys and provider accounts are added only during real integration\nDomain and hosting charges are separate",
            "order": 3,
        },
    ]
    for item in packages:
        Package.objects.update_or_create(
            title=item["title"],
            defaults={
                "category": item["category"],
                "price": item["price"],
                "short_description": item["short_description"],
                "summary": item["short_description"],
                "included_features": item["included_features"],
                "scope_limits": item["scope_limits"],
                "is_featured": True,
                "order": item["order"],
            },
        )

    projects = [
        ("Trips & Tours Website Demo", "A travel website concept with package cards, itinerary sections, destination gallery, and booking enquiry flow.", "Django, HTML, CSS, JavaScript"),
        ("Local Service Business Demo", "A polished service-provider website with pricing, FAQs, testimonials, and contact flow.", "Django, HTML, CSS"),
        ("Shop Website Demo", "A local shop website concept with product highlights, offers, location, and WhatsApp lead flow.", "HTML, CSS, JavaScript"),
    ]
    for index, (title, description, stack) in enumerate(projects, start=20):
        PortfolioProject.objects.update_or_create(
            title=title,
            defaults={"description": description, "tech_stack": stack, "order": index},
        )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_seed_initial_content"),
    ]

    operations = [
        migrations.RunPython(add_business_content, noop),
    ]
