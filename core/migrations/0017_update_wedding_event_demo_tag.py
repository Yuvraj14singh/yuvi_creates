from django.db import migrations


def update_wedding_event_demo_tag(apps, schema_editor):
    PortfolioProject = apps.get_model("core", "PortfolioProject")
    PortfolioProject.objects.filter(title="Wedding & Event Planner Website Demo").update(
        tech_stack="Event Planner Demo"
    )


def restore_wedding_event_demo_tag(apps, schema_editor):
    PortfolioProject = apps.get_model("core", "PortfolioProject")
    PortfolioProject.objects.filter(title="Wedding & Event Planner Website Demo").update(
        tech_stack="Django, HTML, CSS, JavaScript"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0016_add_wedding_event_planner_websites"),
    ]

    operations = [
        migrations.RunPython(update_wedding_event_demo_tag, restore_wedding_event_demo_tag),
    ]
