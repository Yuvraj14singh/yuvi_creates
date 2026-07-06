from django.db import migrations


HOTEL_CATEGORY = "Hotel Websites"


def remove_hotel_timelines(apps, schema_editor):
    Package = apps.get_model("core", "Package")
    for package in Package.objects.filter(category=HOTEL_CATEGORY):
        lines = [
            line
            for line in package.scope_limits.splitlines()
            if not line.strip().lower().startswith("timeline:")
        ]
        package.scope_limits = "\n".join(lines)
        package.save(update_fields=["scope_limits"])


def restore_noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0014_add_hotel_portfolio_demo"),
    ]

    operations = [
        migrations.RunPython(remove_hotel_timelines, restore_noop),
    ]
