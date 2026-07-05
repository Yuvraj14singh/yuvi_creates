from django.db import migrations


def add_hotel_portfolio_demo(apps, schema_editor):
    PortfolioProject = apps.get_model("core", "PortfolioProject")
    PortfolioProject.objects.update_or_create(
        title="Hotel Website Demo",
        defaults={
            "description": "A premium hotel website concept with room categories, amenities, gallery, nearby attractions, and booking enquiry flow.",
            "tech_stack": "Django, HTML, CSS, JavaScript",
            "order": 13,
        },
    )


def remove_hotel_portfolio_demo(apps, schema_editor):
    PortfolioProject = apps.get_model("core", "PortfolioProject")
    PortfolioProject.objects.filter(title="Hotel Website Demo").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0013_add_hotel_websites"),
    ]

    operations = [
        migrations.RunPython(add_hotel_portfolio_demo, remove_hotel_portfolio_demo),
    ]
