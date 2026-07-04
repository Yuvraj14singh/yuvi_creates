from django.db import models
from django.urls import reverse


class Service(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    icon = models.CharField(max_length=40, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class Package(models.Model):
    title = models.CharField(max_length=160)
    category = models.CharField(max_length=120, blank=True)
    price = models.CharField(max_length=80)
    short_description = models.TextField()
    included_features = models.TextField(help_text="One feature per line.")
    scope_limits = models.TextField(blank=True, help_text="One scope limit per line.")
    summary = models.TextField(blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return f"{self.title} - {self.price}"

    def get_absolute_url(self):
        return reverse("checkout") + f"?package={self.pk}"


class PortfolioProject(models.Model):
    title = models.CharField(max_length=140)
    description = models.TextField()
    tech_stack = models.CharField(max_length=220)
    project_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]

    def __str__(self):
        return self.title


class AboutProfile(models.Model):
    name = models.CharField(max_length=120, default="Yuvraj Singh")
    role = models.CharField(max_length=160, default="Freelance Web Developer")
    photo = models.FileField(upload_to="about/", blank=True)
    headline = models.CharField(max_length=220)
    bio = models.TextField()
    highlight_one = models.CharField(max_length=120, blank=True)
    highlight_two = models.CharField(max_length=120, blank=True)
    highlight_three = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.name


class Review(models.Model):
    client_name = models.CharField(max_length=120)
    business_name = models.CharField(max_length=160, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    quote = models.TextField()
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.client_name} - {self.rating}/5"

    @property
    def stars(self):
        return "★" * max(1, min(self.rating, 5))


class Enquiry(models.Model):
    name = models.CharField(max_length=120)
    business_name = models.CharField(max_length=160, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    business_type = models.CharField(max_length=120)
    package_interested_in = models.CharField(max_length=160, blank=True)
    current_website_or_social_link = models.URLField(blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"{self.name} - {self.business_name or self.business_type}"


class PaymentBooking(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "Pending", "Pending"
        PENDING_VERIFICATION = "Pending Verification", "Pending Verification"
        PAID = "Paid", "Paid"
        FAILED = "Failed", "Failed"
        CANCELLED = "Cancelled", "Cancelled"

    class PaymentMethod(models.TextChoices):
        RAZORPAY = "Razorpay", "Razorpay"
        UPI = "UPI", "UPI"
        GOOGLE_PAY = "Google Pay", "Google Pay"
        PHONEPE = "PhonePe", "PhonePe"
        PAYTM = "Paytm", "Paytm"
        CARD_NET_BANKING = "Card / Net Banking", "Card / Net Banking"
        MANUAL_BANK_TRANSFER = "Manual Bank Transfer", "Manual Bank Transfer"

    client_name = models.CharField(max_length=120)
    business_name = models.CharField(max_length=160, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=40)
    business_type = models.CharField(max_length=120)
    current_website_or_social_link = models.URLField(blank=True)
    selected_package = models.CharField(max_length=180)
    package_price = models.CharField(max_length=80)
    payment_method = models.CharField(max_length=40, choices=PaymentMethod.choices)
    payment_status = models.CharField(
        max_length=30,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    payment_amount_paise = models.PositiveIntegerField(default=0)
    razorpay_order_id = models.CharField(max_length=120, blank=True)
    razorpay_payment_id = models.CharField(max_length=120, blank=True)
    razorpay_signature = models.CharField(max_length=220, blank=True)
    transaction_id = models.CharField(max_length=120, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client_name} - {self.selected_package}"
