from django.db import migrations


def add_premium_business_packages(apps, schema_editor):
    Package = apps.get_model("core", "Package")

    packages = [
        {
            "category": "Premium Business Website",
            "title": "Premium Business Website",
            "price": "₹50,000-₹75,000",
            "short_description": "A premium business website for brands that want stronger design, more trust sections, and a polished enquiry journey.",
            "included_features": "Custom premium homepage\nUp to 8-10 pages/sections\nService/product pages\nPortfolio or gallery section\nTestimonials/reviews section\nFAQ section\nLead enquiry form\nWhatsApp/call CTA\nGoogle Map/location section\nBasic animations\nBasic SEO-friendly structure\nSpeed/basic performance optimization\nDomain/hosting setup support\nLaunch/setup support\n3 rounds revisions",
            "scope_limits": "Up to 8-10 pages/sections\nAdvanced backend features quoted separately\nContent and photos finalized before development\n3 rounds revisions",
            "order": 3,
        },
        {
            "category": "Premium Business Website",
            "title": "Premium Plus Business Website",
            "price": "₹75,000-₹1,20,000+",
            "short_description": "A high-end business website with deeper custom design, richer sections, stronger conversion flow, and advanced polish.",
            "included_features": "Everything in Premium Business Website\nMore custom page layouts\nMore premium animations\nAdvanced CTA flow\nLarger portfolio/gallery/product showcase\nMultiple landing pages or service pages\nBlog/news/offers setup placeholder\nBetter performance optimization\nContent arrangement help\nMore design polish\nMore revision support\nFuture admin/payment integration planning",
            "scope_limits": "Final quote depends on pages, content, integrations, and design level\nCustom backend/payment gateway quoted separately\nTimeline confirmed after full scope discussion",
            "order": 4,
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

    Package.objects.filter(title="Custom Business System").update(order=5, is_featured=True)


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_broaden_business_content"),
    ]

    operations = [
        migrations.RunPython(add_premium_business_packages, noop),
    ]
