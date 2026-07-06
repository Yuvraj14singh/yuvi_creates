from django.db import migrations


SERVICE_TITLE = "Wedding & Event Planner Websites"
SERVICE_DESCRIPTION = "Premium websites for wedding planners, event planners, decorators, party organizers, and event management brands."
PACKAGE_CATEGORY = "Wedding & Event Planner Websites"


PACKAGES = [
    {
        "title": "Basic Wedding/Event Planner Website",
        "price": "₹18,000+",
        "short_description": "A clean starter website for small event planners, decorators, party planners, and wedding service providers.",
        "included_features": "Home page\nAbout business\nServices overview\nBasic event categories section\nPortfolio/gallery up to 10 images\nTestimonials section\nLocation/service area\nCall button\nWhatsApp enquiry button\nContact section\nInstagram/social link\nMobile responsive design\nBasic SEO-friendly setup",
        "scope_limits": "Timeline: 5-7 days\nBest for: Small event planners, decorators, birthday/party planners, and wedding service providers who need a simple online presence.\nBest for simple online presence and enquiry generation.\nPortfolio photos and content should be provided by client.\nNo admin panel, payment system, or advanced booking system included.",
        "order": 35,
    },
    {
        "title": "Professional Wedding/Event Planner Website",
        "price": "₹32,000+",
        "short_description": "A stronger event planner website with portfolio, service sections, enquiry flow, and professional brand presentation.",
        "included_features": "Home page\nAbout section\nDetailed services section\nWedding planning section\nBirthday/party planning section\nCorporate/event planning section if available\nDecoration/theme section\nPortfolio/gallery up to 20 images\nTestimonials/reviews section\nPackages/plans section\nEnquiry/contact form\nWhatsApp enquiry flow\nGoogle Map/service area section\nCall button\nInstagram/social link\nMobile responsive design\nBasic SEO\nBasic speed optimization\nLaunch/setup support",
        "scope_limits": "Timeline: 8-12 days\nBest for: Wedding planners and event planners who want a stronger portfolio, service sections, enquiry flow, and professional brand presentation.\nBest for businesses that want clients to check services, past work, packages, and enquiry options clearly.\nPhotos, videos, package details, and content should be provided by client.\nAdmin panel, payment gateway, and advanced booking calendar are not included.",
        "order": 36,
        "is_featured": True,
    },
    {
        "title": "Premium Wedding/Event Planner Website",
        "price": "₹55,000+",
        "short_description": "A high-end event planner website with premium custom design, detailed pages, portfolio storytelling, and limited admin control.",
        "included_features": "Premium custom design\nHome page\nAbout business/brand story\nDetailed service pages\nWedding planning page\nEvent management page\nDecoration/theme page\nPortfolio/event gallery section\nCase study style event sections\nPackages/plans section\nTestimonials/reviews\nFAQ section\nEnquiry form\nWhatsApp and call CTA flow\nGoogle Map/service area section\nBasic admin panel for limited portfolio, packages, and testimonial updates\nMobile responsive design\nBasic SEO\nSpeed optimization\nLaunch/setup support",
        "scope_limits": "Timeline: 12-20 days\nBest for: Premium wedding planners, event management companies, decorators, luxury event brands, and agencies that need a high-end portfolio website.\nBasic admin panel is for limited portfolio, package, and testimonial updates only.\nAdvanced booking calendar, CRM, online payment, vendor management, guest management, and automation systems are not included.\nThese advanced systems will be quoted separately if required.",
        "order": 37,
    },
]


def add_wedding_event_content(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    Package = apps.get_model("core", "Package")
    PortfolioProject = apps.get_model("core", "PortfolioProject")

    Service.objects.update_or_create(
        title=SERVICE_TITLE,
        defaults={"description": SERVICE_DESCRIPTION, "icon": "09", "order": 9},
    )

    for item in PACKAGES:
        Package.objects.update_or_create(
            title=item["title"],
            defaults={
                "category": PACKAGE_CATEGORY,
                "price": item["price"],
                "short_description": item["short_description"],
                "summary": item["short_description"],
                "included_features": item["included_features"],
                "scope_limits": item["scope_limits"],
                "is_featured": item.get("is_featured", False),
                "order": item["order"],
            },
        )

    PortfolioProject.objects.update_or_create(
        title="Wedding & Event Planner Website Demo",
        defaults={
            "description": "A premium event planning website demo for weddings, parties, corporate events, decoration services, portfolio showcase, and booking enquiries.",
            "tech_stack": "Event Planner Demo",
            "order": 14,
        },
    )


def remove_wedding_event_content(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    Package = apps.get_model("core", "Package")
    PortfolioProject = apps.get_model("core", "PortfolioProject")

    Service.objects.filter(title=SERVICE_TITLE).delete()
    Package.objects.filter(category=PACKAGE_CATEGORY).delete()
    PortfolioProject.objects.filter(title="Wedding & Event Planner Website Demo").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0015_remove_hotel_timelines"),
    ]

    operations = [
        migrations.RunPython(add_wedding_event_content, remove_wedding_event_content),
    ]
