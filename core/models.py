from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


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
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending approval"
        APPROVED = "Approved", "Approved"
        REJECTED = "Rejected", "Rejected"

    class Source(models.TextChoices):
        WEBSITE = "Website", "Website feedback form"
        GOOGLE = "Google", "Google"
        WHATSAPP = "WhatsApp", "WhatsApp"
        INSTAGRAM = "Instagram", "Instagram"
        LINKEDIN = "LinkedIn", "LinkedIn"
        OTHER = "Other", "Other"

    client_name = models.CharField(max_length=120)
    business_name = models.CharField(max_length=160, blank=True)
    email = models.EmailField(blank=True)
    location = models.CharField(max_length=140, blank=True)
    service_received = models.CharField(max_length=180, blank=True)
    rating = models.PositiveSmallIntegerField(default=5)
    quote = models.TextField()
    source = models.CharField(max_length=30, choices=Source.choices, default=Source.WEBSITE)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    submitted_ip = models.GenericIPAddressField(blank=True, null=True)
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

    @property
    def empty_stars(self):
        return "☆" * (5 - max(1, min(self.rating, 5)))


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


class ServiceCategory(models.Model):
    name = models.CharField(max_length=140, unique=True)
    slug = models.SlugField(max_length=160, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Service categories"

    def __str__(self):
        return self.name


class Client(models.Model):
    class LeadSource(models.TextChoices):
        GOOGLE_MAPS = "Google Maps", "Google Maps"
        INSTAGRAM = "Instagram", "Instagram"
        WHATSAPP = "WhatsApp", "WhatsApp"
        LINKEDIN = "LinkedIn", "LinkedIn"
        REFERRAL = "Referral", "Referral"
        OFFLINE = "Offline", "Offline"
        WEBSITE_FORM = "Website Form", "Website Form"
        OTHER = "Other", "Other"

    class CommunicationChannel(models.TextChoices):
        WHATSAPP = "WhatsApp", "WhatsApp"
        INSTAGRAM = "Instagram", "Instagram"
        CALL = "Call", "Call"
        EMAIL = "Email", "Email"
        LINKEDIN = "LinkedIn", "LinkedIn"
        OFFLINE = "Offline", "Offline"
        OTHER = "Other", "Other"

    service_category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name="clients")
    business_name = models.CharField(max_length=180)
    contact_person = models.CharField(max_length=140)
    phone = models.CharField(max_length=40, blank=True)
    whatsapp = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    business_type = models.CharField(max_length=140, blank=True)
    city = models.CharField(max_length=120, blank=True)
    address = models.TextField(blank=True)
    instagram_link = models.URLField(blank=True)
    google_maps_link = models.URLField(blank=True)
    current_website = models.URLField(blank=True)
    business_logo = models.FileField(upload_to="client_logos/", blank=True)
    lead_source = models.CharField(max_length=40, choices=LeadSource.choices, default=LeadSource.OTHER)
    communication_channel = models.CharField(
        max_length=40,
        choices=CommunicationChannel.choices,
        default=CommunicationChannel.WHATSAPP,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["business_name"]

    def __str__(self):
        return self.business_name


class ClientProject(models.Model):
    class ProjectStatus(models.TextChoices):
        LEAD = "Lead", "Lead"
        CONTACTED = "Contacted", "Contacted"
        INTERESTED = "Interested", "Interested"
        PROPOSAL_SENT = "Proposal Sent", "Proposal Sent"
        CLIENT_FINALISED = "Client Finalised", "Client Finalised"
        ADVANCE_PAID = "Advance Paid", "Advance Paid"
        CONTENT_PENDING = "Content Pending", "Content Pending"
        IN_DEVELOPMENT = "In Development", "In Development"
        REVIEW = "Review", "Review"
        REVISION = "Revision", "Revision"
        COMPLETED = "Completed", "Completed"
        DELIVERED = "Delivered", "Delivered"
        MAINTENANCE = "Maintenance", "Maintenance"
        CANCELLED = "Cancelled", "Cancelled"

    class PaymentStatus(models.TextChoices):
        NOT_PAID = "Not Paid", "Not Paid"
        ADVANCE_PAID = "Advance Paid", "Advance Paid"
        PARTIALLY_PAID = "Partially Paid", "Partially Paid"
        FULLY_PAID = "Fully Paid", "Fully Paid"
        REFUNDED = "Refunded", "Refunded"

    class Priority(models.TextChoices):
        LOW = "Low", "Low"
        MEDIUM = "Medium", "Medium"
        HIGH = "High", "High"
        URGENT = "Urgent", "Urgent"

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="projects")
    project_type = models.CharField(max_length=140, blank=True)
    package_selected = models.CharField(max_length=180, blank=True)
    final_scope_summary = models.TextField(blank=True)
    pages_required = models.TextField(blank=True)
    features_required = models.TextField(blank=True)
    admin_panel_required = models.BooleanField(default=False)
    payment_gateway_required = models.BooleanField(default=False)
    maintenance_required = models.BooleanField(default=False)
    quoted_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text="Auto-updated from quoted amount, advance, and saved payments.",
    )
    payment_status = models.CharField(
        max_length=30,
        choices=PaymentStatus.choices,
        default=PaymentStatus.NOT_PAID,
    )
    project_status = models.CharField(
        max_length=40,
        choices=ProjectStatus.choices,
        default=ProjectStatus.LEAD,
    )
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    start_date = models.DateField(null=True, blank=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    actual_delivery_date = models.DateField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    revision_rounds_included = models.PositiveIntegerField(default=1)
    client_approval_notes = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client.business_name} - {self.package_selected or self.project_type or 'Project'}"

    @property
    def received_amount(self):
        payments_total = self.payments.aggregate(total=models.Sum("amount"))["total"] or 0
        return self.advance_amount + payments_total

    def update_remaining_amount(self):
        self.remaining_amount = max(self.quoted_amount - self.received_amount, 0)
        self.save(update_fields=["remaining_amount", "updated_at"])


class ClientContentStatus(models.Model):
    project = models.OneToOneField(ClientProject, on_delete=models.CASCADE, related_name="content_status")
    logo_received = models.BooleanField(default=False)
    photos_received = models.BooleanField(default=False)
    service_details_received = models.BooleanField(default=False)
    price_list_received = models.BooleanField(default=False)
    about_content_received = models.BooleanField(default=False)
    contact_details_received = models.BooleanField(default=False)
    social_links_received = models.BooleanField(default=False)
    testimonials_received = models.BooleanField(default=False)
    gallery_images_received = models.BooleanField(default=False)
    domain_access_received = models.BooleanField(default=False)
    hosting_access_received = models.BooleanField(default=False)
    content_notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Content status - {self.project}"


class ClientDomainHosting(models.Model):
    project = models.OneToOneField(ClientProject, on_delete=models.CASCADE, related_name="domain_hosting")
    domain_required = models.BooleanField(default=False)
    domain_name = models.CharField(max_length=180, blank=True)
    domain_provider = models.CharField(max_length=140, blank=True)
    domain_expiry_date = models.DateField(null=True, blank=True)
    hosting_required = models.BooleanField(default=False)
    hosting_provider = models.CharField(max_length=140, blank=True)
    hosting_plan = models.CharField(max_length=140, blank=True)
    hosting_renewal_date = models.DateField(null=True, blank=True)
    deployment_url = models.URLField(blank=True)
    live_website_url = models.URLField(blank=True)
    access_given_by_client = models.BooleanField(default=False)
    stored_in_password_manager = models.BooleanField(default=False)
    notes = models.TextField(
        blank=True,
        help_text="Do not store passwords here. Note only where access is safely stored.",
    )

    def __str__(self):
        return f"Domain/hosting - {self.project}"


class ClientPayment(models.Model):
    class PaymentType(models.TextChoices):
        ADVANCE = "Advance", "Advance"
        PARTIAL = "Partial", "Partial"
        FINAL = "Final", "Final"
        MAINTENANCE = "Maintenance", "Maintenance"
        REFUND = "Refund", "Refund"
        OTHER = "Other", "Other"

    class PaymentMode(models.TextChoices):
        UPI = "UPI", "UPI"
        BANK_TRANSFER = "Bank Transfer", "Bank Transfer"
        CASH = "Cash", "Cash"
        RAZORPAY = "Razorpay", "Razorpay"
        OTHER = "Other", "Other"

    project = models.ForeignKey(ClientProject, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=30, choices=PaymentType.choices, default=PaymentType.PARTIAL)
    payment_mode = models.CharField(max_length=30, choices=PaymentMode.choices, default=PaymentMode.UPI)
    payment_date = models.DateField()
    invoice_number = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-payment_date", "-created_at"]

    def __str__(self):
        return f"{self.project} - {self.amount}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.project.update_remaining_amount()


class ClientNote(models.Model):
    project = models.ForeignKey(ClientProject, on_delete=models.CASCADE, related_name="notes")
    note = models.TextField()
    next_follow_up_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Note - {self.project}"


class ProjectProgressTask(models.Model):
    class TaskStatus(models.TextChoices):
        PENDING = "Pending", "Pending"
        IN_PROGRESS = "In Progress", "In Progress"
        DONE = "Done", "Done"

    project = models.ForeignKey(ClientProject, on_delete=models.CASCADE, related_name="progress_tasks")
    task_name = models.CharField(max_length=140)
    status = models.CharField(max_length=20, choices=TaskStatus.choices, default=TaskStatus.PENDING)
    order = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "task_name"]

    def __str__(self):
        return f"{self.task_name} - {self.project}"
