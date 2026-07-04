from django.db import migrations


def remove_pitchqi_portfolio_word(apps, schema_editor):
    PortfolioProject = apps.get_model("core", "PortfolioProject")
    PortfolioProject.objects.filter(title="Cricket Project: PitchQI").update(
        title="Cricket Intelligence Dashboard Demo"
    )


def restore_pitchqi_portfolio_word(apps, schema_editor):
    PortfolioProject = apps.get_model("core", "PortfolioProject")
    PortfolioProject.objects.filter(title="Cricket Intelligence Dashboard Demo").update(
        title="Cricket Project: PitchQI"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_aboutprofile_review"),
    ]

    operations = [
        migrations.RunPython(remove_pitchqi_portfolio_word, restore_pitchqi_portfolio_word),
    ]
