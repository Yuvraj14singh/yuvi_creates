from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0005_add_razorpay_payment_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymentbooking",
            name="payment_method",
            field=models.CharField(
                choices=[
                    ("Razorpay", "Razorpay"),
                    ("UPI", "UPI"),
                    ("Google Pay", "Google Pay"),
                    ("PhonePe", "PhonePe"),
                    ("Paytm", "Paytm"),
                    ("Card / Net Banking", "Card / Net Banking"),
                    ("Manual Bank Transfer", "Manual Bank Transfer"),
                ],
                max_length=40,
            ),
        ),
    ]
