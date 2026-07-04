from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_add_premium_business_packages"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentbooking",
            name="payment_amount_paise",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="paymentbooking",
            name="razorpay_order_id",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="paymentbooking",
            name="razorpay_payment_id",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="paymentbooking",
            name="razorpay_signature",
            field=models.CharField(blank=True, max_length=220),
        ),
    ]
