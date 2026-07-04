# Generated for the Yuvi Creates starter project.
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Enquiry",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("business_name", models.CharField(blank=True, max_length=160)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=40)),
                ("business_type", models.CharField(max_length=120)),
                ("package_interested_in", models.CharField(blank=True, max_length=160)),
                ("current_website_or_social_link", models.URLField(blank=True)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"verbose_name_plural": "Enquiries", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Package",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=160)),
                ("category", models.CharField(blank=True, max_length=120)),
                ("price", models.CharField(max_length=80)),
                ("short_description", models.TextField()),
                ("included_features", models.TextField(help_text="One feature per line.")),
                ("scope_limits", models.TextField(blank=True, help_text="One scope limit per line.")),
                ("summary", models.TextField(blank=True)),
                ("is_featured", models.BooleanField(default=False)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["order", "title"]},
        ),
        migrations.CreateModel(
            name="PaymentBooking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("client_name", models.CharField(max_length=120)),
                ("business_name", models.CharField(blank=True, max_length=160)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=40)),
                ("business_type", models.CharField(max_length=120)),
                ("current_website_or_social_link", models.URLField(blank=True)),
                ("selected_package", models.CharField(max_length=180)),
                ("package_price", models.CharField(max_length=80)),
                ("payment_method", models.CharField(choices=[("UPI", "UPI"), ("Google Pay", "Google Pay"), ("PhonePe", "PhonePe"), ("Paytm", "Paytm"), ("Card / Net Banking", "Card / Net Banking"), ("Manual Bank Transfer", "Manual Bank Transfer")], max_length=40)),
                ("payment_status", models.CharField(choices=[("Pending", "Pending"), ("Pending Verification", "Pending Verification"), ("Paid", "Paid"), ("Failed", "Failed"), ("Cancelled", "Cancelled")], default="Pending", max_length=30)),
                ("transaction_id", models.CharField(blank=True, max_length=120)),
                ("message", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="PortfolioProject",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=140)),
                ("description", models.TextField()),
                ("tech_stack", models.CharField(max_length=220)),
                ("project_url", models.URLField(blank=True)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["order", "title"]},
        ),
        migrations.CreateModel(
            name="Service",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)),
                ("description", models.TextField()),
                ("icon", models.CharField(blank=True, max_length=40)),
                ("order", models.PositiveIntegerField(default=0)),
            ],
            options={"ordering": ["order", "title"]},
        ),
    ]
