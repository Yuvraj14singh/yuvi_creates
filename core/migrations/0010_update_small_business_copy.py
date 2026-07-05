from django.db import migrations


NEW_DESCRIPTION = "Clean websites for service providers, clinics, consultants, repair services, tutors, and local professionals."
OLD_DESCRIPTION = "Clean websites for shops, gyms, service providers, and local businesses."


def update_small_business_copy(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    Service.objects.filter(title="Small Business Websites").update(description=NEW_DESCRIPTION)


def restore_small_business_copy(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    Service.objects.filter(title="Small Business Websites").update(description=OLD_DESCRIPTION)


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_add_salon_makeup_artist_packages"),
    ]

    operations = [
        migrations.RunPython(update_small_business_copy, restore_small_business_copy),
    ]
