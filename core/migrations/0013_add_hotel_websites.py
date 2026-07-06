from django.db import migrations


SERVICE_TITLE = "Hotel Websites"
SERVICE_DESCRIPTION = "Professional websites for hotels, guest houses, lodges, boutique stays, banquet hotels, and resorts."
PACKAGE_CATEGORY = "Hotel Websites"


PACKAGES = [
    {
        "title": "Basic Hotel Website",
        "price": "₹18,000+",
        "short_description": "A clean starter website for small hotels, guest houses, lodges, and budget stays that need essential details and booking enquiries.",
        "included_features": "Home page\nAbout hotel\nRooms overview\nBasic amenities section\nGallery up to 8-10 images\nTimings / check-in / check-out info\nGoogle Map\nCall button\nWhatsApp booking enquiry button\nContact section\nInstagram/social link\nMobile responsive design\nBasic SEO-friendly setup",
        "scope_limits": "Best for: Small hotels, guest houses, lodges, and budget stays.\nBest for hotels that need a simple online presence.\nNo online booking system, payment gateway, real-time room availability, or admin panel included.",
        "order": 32,
    },
    {
        "title": "Professional Hotel Website",
        "price": "₹32,000+",
        "short_description": "A stronger hotel website for better room presentation, guest trust, location clarity, and booking enquiries.",
        "included_features": "Home page\nAbout section\nRoom categories section\nRoom detail sections\nAmenities section\nDining / restaurant section if available\nBanquet / conference section if available\nGallery up to 15 images\nTestimonials/reviews section\nNearby places section\nWhatsApp booking enquiry flow\nContact form\nGoogle Map\nCall button\nInstagram/social link\nMobile responsive design\nBasic SEO\nBasic speed optimization\nLaunch/setup support",
        "scope_limits": "Best for: Hotels that want better room presentation, stronger trust, and clear booking enquiries.\nBest for hotels that want guests to check rooms, amenities, location, and enquiry options clearly.\nOnline payment, real-time booking engine, advanced booking management, and admin panel are not included.",
        "order": 33,
        "is_featured": True,
    },
    {
        "title": "Premium Hotel Website",
        "price": "₹55,000+",
        "short_description": "A premium hotel website with custom design, room pages, strong trust sections, enquiry flow, and limited admin control.",
        "included_features": "Premium custom design\nHome page\nAbout hotel\nRoom category pages\nDetailed room pages\nAmenities section\nDining / restaurant page\nBanquet / conference page\nGallery section\nNearby attractions section\nTestimonials/reviews\nFAQ section\nBooking enquiry form\nWhatsApp and call CTA flow\nGoogle Map\nBasic admin panel for limited room, gallery, and offer updates\nMobile responsive design\nBasic SEO\nSpeed optimization\nLaunch/setup support",
        "scope_limits": "Best for: Premium hotels, boutique hotels, banquet hotels, resorts, and hotel brands.\nBasic admin panel is for limited room, offer, and gallery updates only.\nOnline booking engine, payment gateway, real-time room availability, advanced booking calendar, and hotel management system are not included.\nThese advanced systems will be quoted separately if required.",
        "order": 34,
    },
]


def add_hotel_websites(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    Package = apps.get_model("core", "Package")

    Service.objects.update_or_create(
        title=SERVICE_TITLE,
        defaults={"description": SERVICE_DESCRIPTION, "icon": "08", "order": 8},
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


def remove_hotel_websites(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    Package = apps.get_model("core", "Package")

    Service.objects.filter(title=SERVICE_TITLE).delete()
    Package.objects.filter(category=PACKAGE_CATEGORY).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0012_update_pet_shop_package_scope"),
    ]

    operations = [
        migrations.RunPython(add_hotel_websites, remove_hotel_websites),
    ]
