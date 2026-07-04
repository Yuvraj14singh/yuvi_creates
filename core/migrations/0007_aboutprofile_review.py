from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0006_add_razorpay_payment_method_choice"),
    ]

    operations = [
        migrations.CreateModel(
            name="AboutProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(default="Yuvraj Singh", max_length=120)),
                ("role", models.CharField(default="Freelance Web Developer", max_length=160)),
                ("photo", models.FileField(blank=True, upload_to="about/")),
                ("headline", models.CharField(max_length=220)),
                ("bio", models.TextField()),
                ("highlight_one", models.CharField(blank=True, max_length=120)),
                ("highlight_two", models.CharField(blank=True, max_length=120)),
                ("highlight_three", models.CharField(blank=True, max_length=120)),
                ("is_active", models.BooleanField(default=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("client_name", models.CharField(max_length=120)),
                ("business_name", models.CharField(blank=True, max_length=160)),
                ("rating", models.PositiveSmallIntegerField(default=5)),
                ("quote", models.TextField()),
                ("is_featured", models.BooleanField(default=True)),
                ("order", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["order", "-created_at"],
            },
        ),
    ]
