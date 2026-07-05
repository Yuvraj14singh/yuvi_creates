from django.db import migrations


SALON_CATEGORY = "Salon & Makeup Artist Websites"
SALON_DESCRIPTION = "Professional websites for salons, beauty studios, bridal makeup artists, and personal beauty brands."


PACKAGES = [
    {
        "title": "Basic Salon Website",
        "price": "₹15,000+",
        "short_description": "A clean starter website for salons that need services, location, timings, gallery, and direct booking CTAs.",
        "included_features": "Home page\nAbout salon\nServices list\nBasic price/menu section\nGallery\nTimings\nGoogle Map\nCall button\nWhatsApp booking button\nInstagram link\nMobile responsive design\nBasic SEO-friendly setup",
        "scope_limits": "",
        "order": 20,
    },
    {
        "title": "Professional Salon Website",
        "price": "₹25,000+",
        "short_description": "A polished salon website with categorized services, offers, proof sections, and a stronger booking enquiry flow.",
        "included_features": "Home page\nAbout section\nServices with categories\nHair, Skin, Makeup, and Nails sections\nPrice list\nGallery\nBefore/after section\nTestimonials\nOffers section\nWhatsApp booking flow\nContact form\nGoogle Map\nInstagram link\nMobile responsive design\nBasic SEO\nBasic speed optimization\nLaunch/setup support",
        "scope_limits": "",
        "order": 21,
        "is_featured": True,
    },
    {
        "title": "Premium Salon Website",
        "price": "₹40,000+",
        "short_description": "A premium salon website with custom design, detailed service pages, portfolio sections, and basic admin control.",
        "included_features": "Premium custom design\nService category pages\nDetailed service pages\nStaff/artist section\nPackages/offers section\nAdvanced gallery\nBefore/after portfolio\nTestimonials/reviews\nBooking enquiry form\nWhatsApp and call CTA flow\nGoogle Map\nBasic admin panel for services, offers, and gallery\nMobile responsive design\nBasic SEO\nSpeed optimization\nLaunch/setup support",
        "scope_limits": "",
        "order": 22,
    },
    {
        "title": "Basic Makeup Artist Portfolio",
        "price": "₹12,000+",
        "short_description": "A simple beauty portfolio for makeup artists who need a professional gallery and fast WhatsApp booking path.",
        "included_features": "Home page\nAbout artist\nServices\nBasic packages section\nPortfolio/gallery\nInstagram link\nWhatsApp booking button\nCall button\nLocation/service area\nMobile responsive design\nBasic SEO-friendly setup",
        "scope_limits": "",
        "order": 23,
    },
    {
        "title": "Professional Makeup Artist Website",
        "price": "₹22,000+",
        "short_description": "A complete makeup artist website for bridal, party, engagement, reception, and HD makeup enquiries.",
        "included_features": "Home page\nAbout artist\nBridal makeup section\nParty makeup section\nEngagement, reception, and HD makeup sections\nPackages/pricing section\nPortfolio gallery\nClient testimonials\nBooking enquiry form\nWhatsApp booking flow\nInstagram link\nGoogle Map/service area\nMobile responsive design\nBasic SEO\nLaunch/setup support",
        "scope_limits": "",
        "order": 24,
        "is_featured": True,
    },
    {
        "title": "Premium Makeup Artist Website",
        "price": "₹35,000+",
        "short_description": "A premium makeup artist website with detailed services, bridal/event packages, portfolio proof, FAQ, and basic admin control.",
        "included_features": "Premium custom design\nDetailed service pages\nBridal packages\nParty/event makeup packages\nPortfolio gallery\nBefore/after section\nTestimonials\nFAQ section\nBooking enquiry form\nWhatsApp CTA flow\nInstagram/profile links\nBasic admin panel for gallery, packages, and testimonials\nMobile responsive design\nBasic SEO\nSpeed optimization\nLaunch/setup support",
        "scope_limits": "",
        "order": 25,
    },
]


def add_salon_makeup_artist_packages(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    Package = apps.get_model("core", "Package")

    Service.objects.filter(title="Salon / Makeup Artist Websites").update(
        title=SALON_CATEGORY,
        description=SALON_DESCRIPTION,
    )
    Service.objects.update_or_create(
        title=SALON_CATEGORY,
        defaults={"description": SALON_DESCRIPTION, "icon": "06", "order": 6},
    )

    for item in PACKAGES:
        Package.objects.update_or_create(
            title=item["title"],
            defaults={
                "category": SALON_CATEGORY,
                "price": item["price"],
                "short_description": item["short_description"],
                "summary": item["short_description"],
                "included_features": item["included_features"],
                "scope_limits": item["scope_limits"],
                "is_featured": item.get("is_featured", False),
                "order": item["order"],
            },
        )


def remove_salon_makeup_artist_packages(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    Package = apps.get_model("core", "Package")

    Package.objects.filter(category=SALON_CATEGORY).delete()
    Service.objects.filter(title=SALON_CATEGORY).update(
        title="Salon / Makeup Artist Websites",
        description="Elegant beauty websites for salons, makeup artists, bridal services, service packages, gallery, reviews, and booking flow.",
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0008_remove_pitchqi_portfolio_word"),
    ]

    operations = [
        migrations.RunPython(add_salon_makeup_artist_packages, remove_salon_makeup_artist_packages),
    ]
