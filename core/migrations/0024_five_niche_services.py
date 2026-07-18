from django.db import migrations


SERVICES = [
    ("Coaching & Institute Websites", "Professional admission-focused websites for coaching centres, academies, tutors, and education institutes.", "18", 18),
    ("Car Dealer & Auto Showroom Websites", "Premium inventory and enquiry websites for vehicle dealers, showrooms, and automotive businesses.", "19", 19),
    ("Construction & Interior Design Websites", "Project-led websites for builders, contractors, architects, and interior design studios.", "20", 20),
    ("Jewellery Store Websites", "Elegant collection and appointment websites for jewellers, boutiques, and custom jewellery brands.", "21", 21),
    ("Corporate Business Websites", "Authority-led websites for companies, B2B teams, consultancies, and professional organisations.", "22", 22),
]


def seed(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    for title, description, icon, order in SERVICES:
        Service.objects.update_or_create(
            title=title,
            defaults={"description": description, "icon": icon, "order": order},
        )


def unseed(apps, schema_editor):
    apps.get_model("core", "Service").objects.filter(
        title__in=[row[0] for row in SERVICES]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [("core", "0023_five_new_industries")]
    operations = [migrations.RunPython(seed, unseed)]
