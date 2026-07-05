from django.db import migrations


PACKAGE_CATEGORY = "Pet Shop Websites"


PACKAGES = [
    {
        "title": "Basic Pet Shop Website",
        "price": "₹16,000+",
        "short_description": "A clean starter website for pet shops that need essential business details, limited product highlights, contact CTAs, and local trust.",
        "included_features": "Home page\nAbout pet shop\nProduct categories overview\nBasic product highlights up to 6-8 items\nSimple grooming/service section if content is provided\nSimple offers/banner section\nGallery up to 8-10 images\nTimings\nGoogle Map\nCall button\nWhatsApp enquiry button\nInstagram link\nMobile responsive design\nBasic SEO-friendly setup",
        "scope_limits": "Best for simple pet shops and local pet supply stores\nProduct photos and content provided by client\nLimited product highlights only, not full inventory\nNo ecommerce, payment gateway, cart, or inventory system included",
    },
    {
        "title": "Professional Pet Shop Website",
        "price": "₹28,000+",
        "short_description": "A stronger pet shop website for growing stores that need product/service sections, grooming enquiries, offers, testimonials, and a better lead flow.",
        "included_features": "Home page\nAbout section\nUp to 4-5 product/service categories\nPet food, toys, accessories, and grooming sections\nFeatured products section up to 10-15 items\nOffers section\nGallery up to 15 images\nTestimonials\nWhatsApp enquiry flow\nContact form\nGoogle Map\nInstagram link\nMobile responsive design\nBasic SEO\nBasic speed optimization\nLaunch/setup support",
        "scope_limits": "Best for growing stores with multiple product/service categories\nProduct photos and content provided by client\nDetailed inventory/ecommerce system quoted separately\nOnline payment, cart, and stock management not included\nIncludes 1-2 rounds of minor revisions",
    },
    {
        "title": "Premium Pet Shop Website",
        "price": "₹45,000+",
        "short_description": "A premium pet shop website with custom design, detailed product/service pages, stronger trust sections, and basic admin control for limited updates.",
        "included_features": "Premium custom design\nProduct category pages\nDetailed product/service pages\nGrooming appointment enquiry\nPet care information sections\nPackages/offers section\nAdvanced gallery\nTestimonials/reviews\nFAQ section\nWhatsApp and call CTA flow\nGoogle Map\nBasic admin panel for limited products, offers, and gallery updates\nMobile responsive design\nBasic SEO\nSpeed optimization\nLaunch/setup support",
        "scope_limits": "Final scope depends on products, services, gallery size, and admin panel needs\nBasic admin panel is for limited product/offer/gallery updates only\nFull ecommerce, online payment, cart, stock management, and advanced inventory system are not included\nEcommerce/payment/inventory system will be quoted separately\nIncludes 1-2 rounds of minor revisions",
    },
]


OLD_PRICES = {
    "Basic Pet Shop Website": "₹14,000+",
    "Professional Pet Shop Website": "₹24,000+",
    "Premium Pet Shop Website": "₹38,000+",
}


def update_pet_shop_packages(apps, schema_editor):
    Package = apps.get_model("core", "Package")
    for item in PACKAGES:
        Package.objects.filter(title=item["title"], category=PACKAGE_CATEGORY).update(
            price=item["price"],
            short_description=item["short_description"],
            summary=item["short_description"],
            included_features=item["included_features"],
            scope_limits=item["scope_limits"],
        )


def restore_pet_shop_prices(apps, schema_editor):
    Package = apps.get_model("core", "Package")
    for title, price in OLD_PRICES.items():
        Package.objects.filter(title=title, category=PACKAGE_CATEGORY).update(price=price)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0011_add_pet_shop_websites"),
    ]

    operations = [
        migrations.RunPython(update_pet_shop_packages, restore_pet_shop_prices),
    ]
