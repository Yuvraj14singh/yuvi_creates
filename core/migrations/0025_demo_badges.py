from django.db import migrations, models


BADGES = {
    "Restaurant Website Demo": ("premium", {"is_featured": True, "is_popular": True}),
    "Cafe Landing Page Demo": ("professional", {"is_popular": True, "is_fast_launch": True}),
    "Gym Website Demo": ("professional", {"is_mobile_first": True}),
    "Personal Portfolio Website": ("starter", {"is_fast_launch": True, "is_mobile_first": True}),
    "Cricket Intelligence Dashboard Demo": ("custom_system", {"is_featured": True, "is_popular": True}),
    "Real Estate Property Demo": ("premium", {"is_luxury": True}),
    "Salon Makeup Artist Demo": ("premium", {"is_luxury": True}),
    "Clinic Website Demo": ("professional", {"is_new": True, "is_mobile_first": True}),
    "Web Design Agency Demo": ("premium", {"is_featured": True}),
    "Pet Shop Website Demo": ("professional", {"is_mobile_first": True}),
    "Hotel Website Demo": ("premium", {"is_luxury": True}),
    "Wedding & Event Planner Website Demo": ("premium", {"is_luxury": True}),
    "Trips & Tours Website Demo": ("professional", {"is_popular": True}),
    "Local Service Business Demo": ("starter", {"is_fast_launch": True}),
    "Shop Website Demo": ("professional", {"is_mobile_first": True}),
    "Coaching Website Demo": ("professional", {"is_new": True}),
    "Car Dealer Website Demo": ("premium", {"is_new": True, "is_luxury": True}),
    "Construction & Interior Design Demo": ("premium", {"is_new": True}),
    "Luxury Jewellery Website Demo": ("premium", {"is_new": True, "is_luxury": True}),
    "Corporate Business Website Demo": ("professional", {"is_new": True}),
}


def seed_badges(apps, schema_editor):
    Project = apps.get_model("core", "PortfolioProject")
    for title, (level, flags) in BADGES.items():
        Project.objects.filter(title=title).update(experience_level=level, **flags)


class Migration(migrations.Migration):
    dependencies = [("core", "0024_five_niche_services")]
    operations = [
        migrations.AddField(model_name="portfolioproject", name="experience_level", field=models.CharField(choices=[("starter", "Starter"), ("professional", "Professional"), ("premium", "Premium"), ("custom_system", "Custom System")], default="professional", max_length=20)),
        migrations.AddField(model_name="portfolioproject", name="is_active", field=models.BooleanField(default=True)),
        migrations.AddField(model_name="portfolioproject", name="is_fast_launch", field=models.BooleanField(default=False)),
        migrations.AddField(model_name="portfolioproject", name="is_featured", field=models.BooleanField(default=False)),
        migrations.AddField(model_name="portfolioproject", name="is_luxury", field=models.BooleanField(default=False)),
        migrations.AddField(model_name="portfolioproject", name="is_mobile_first", field=models.BooleanField(default=False)),
        migrations.AddField(model_name="portfolioproject", name="is_new", field=models.BooleanField(default=False)),
        migrations.AddField(model_name="portfolioproject", name="is_popular", field=models.BooleanField(default=False)),
        migrations.RunPython(seed_badges, migrations.RunPython.noop),
    ]
