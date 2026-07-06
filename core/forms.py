import re

from django import forms

from .models import (
    Client,
    ClientContentStatus,
    ClientDomainHosting,
    ClientNote,
    ClientPayment,
    ClientProject,
    Enquiry,
    PaymentBooking,
    ProjectProgressTask,
)


INPUT_CLASS = "form-control"


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = [
            "name",
            "business_name",
            "email",
            "phone",
            "business_type",
            "package_interested_in",
            "current_website_or_social_link",
            "message",
        ]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", INPUT_CLASS)
        self.fields["current_website_or_social_link"].required = True
        self.fields["name"].widget.attrs.setdefault("placeholder", "Your full name")
        self.fields["business_name"].widget.attrs.setdefault("placeholder", "Business or brand name")
        self.fields["email"].widget.attrs.setdefault("placeholder", "you@example.com")
        self.fields["phone"].widget.attrs.setdefault("placeholder", "WhatsApp / mobile number")
        self.fields["business_type"].widget.attrs.setdefault("placeholder", "Restaurant, cafe, tour agency, shop...")
        self.fields["package_interested_in"].widget.attrs.setdefault("placeholder", "Starter, premium, restaurant, travel...")
        self.fields["current_website_or_social_link"].widget.attrs.setdefault("placeholder", "https://instagram.com/yourbrand")
        self.fields["message"].widget.attrs.setdefault("placeholder", "Share your requirement, timeline, city, and any reference website")


class PaymentBookingForm(forms.ModelForm):
    payable_amount = forms.IntegerField(
        label="Payment amount (INR)",
        min_value=1,
        widget=forms.NumberInput(attrs={"inputmode": "numeric"}),
    )

    class Meta:
        model = PaymentBooking
        fields = [
            "client_name",
            "business_name",
            "email",
            "phone",
            "business_type",
            "payable_amount",
            "current_website_or_social_link",
        ]

    def __init__(self, *args, **kwargs):
        self.selected_package = kwargs.pop("selected_package", None)
        super().__init__(*args, **kwargs)
        required_fields = {
            "client_name",
            "business_name",
            "email",
            "phone",
            "business_type",
            "payable_amount",
            "current_website_or_social_link",
        }
        for name, field in self.fields.items():
            field.widget.attrs.setdefault("class", INPUT_CLASS)
            field.required = name in required_fields
            if not field.required:
                field.widget.attrs.pop("required", None)
        self.fields["client_name"].widget.attrs.setdefault("placeholder", "Your full name")
        self.fields["business_name"].widget.attrs.setdefault("placeholder", "Business or brand name")
        self.fields["email"].widget.attrs.setdefault("placeholder", "you@example.com")
        self.fields["phone"].widget.attrs.setdefault("placeholder", "WhatsApp / mobile number")
        self.fields["business_type"].widget.attrs.setdefault("placeholder", "Restaurant, cafe, tour agency, shop...")
        self.fields["current_website_or_social_link"].widget.attrs.setdefault("placeholder", "https://instagram.com/yourbrand")

        amount_field = self.fields["payable_amount"]
        amount_field.widget.attrs.setdefault("placeholder", "Enter amount to pay")
        if self.selected_package:
            minimum, maximum = self._package_amount_bounds(self.selected_package.price)
            amount_field.initial = minimum
            amount_field.min_value = minimum
            amount_field.widget.attrs["min"] = minimum
            if maximum and maximum != minimum:
                amount_field.max_value = maximum
                amount_field.widget.attrs["max"] = maximum
                amount_field.help_text = f"Enter any amount between ₹{minimum:,} and ₹{maximum:,}."
            elif maximum == minimum:
                amount_field.widget.attrs["readonly"] = "readonly"
                amount_field.help_text = f"This package amount is fixed at ₹{minimum:,}."
            else:
                amount_field.help_text = f"Enter ₹{minimum:,} or more for this package."

    def clean_payable_amount(self):
        amount = self.cleaned_data["payable_amount"]
        if not self.selected_package:
            return amount
        minimum, maximum = self._package_amount_bounds(self.selected_package.price)
        if amount < minimum:
            raise forms.ValidationError(f"Amount must be at least ₹{minimum:,}.")
        if maximum and amount > maximum:
            raise forms.ValidationError(f"Amount cannot be more than ₹{maximum:,} for this package.")
        return amount

    @staticmethod
    def _package_amount_bounds(price):
        amounts = [int(value.replace(",", "")) for value in re.findall(r"[\d,]+", price)]
        if not amounts:
            return 1, None
        if len(amounts) == 1:
            return amounts[0], amounts[0] if "+" not in price else None
        return amounts[0], amounts[1]


class StaffFormMixin:
    textarea_rows = 4
    required_fields = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in self.required_fields:
            if name in self.fields:
                self.fields[name].required = True
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", INPUT_CLASS)
            if field.required:
                field.widget.attrs["required"] = "required"
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault("rows", self.textarea_rows)
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
                field.widget.attrs.pop("required", None)
            if isinstance(field.widget, (forms.DateInput,)):
                field.widget.input_type = "date"


class ClientForm(StaffFormMixin, forms.ModelForm):
    required_fields = (
        "service_category",
        "business_name",
        "contact_person",
        "phone",
        "business_type",
        "city",
        "lead_source",
        "communication_channel",
    )

    class Meta:
        model = Client
        fields = [
            "service_category",
            "business_name",
            "contact_person",
            "phone",
            "whatsapp",
            "email",
            "business_type",
            "city",
            "address",
            "instagram_link",
            "google_maps_link",
            "current_website",
            "business_logo",
            "lead_source",
            "communication_channel",
        ]


class ClientProjectForm(StaffFormMixin, forms.ModelForm):
    required_fields = (
        "project_type",
        "package_selected",
        "quoted_amount",
        "payment_status",
        "project_status",
        "priority",
        "start_date",
        "expected_delivery_date",
    )

    class Meta:
        model = ClientProject
        fields = [
            "project_type",
            "package_selected",
            "final_scope_summary",
            "pages_required",
            "features_required",
            "admin_panel_required",
            "payment_gateway_required",
            "maintenance_required",
            "quoted_amount",
            "advance_amount",
            "remaining_amount",
            "payment_status",
            "project_status",
            "priority",
            "start_date",
            "expected_delivery_date",
            "actual_delivery_date",
            "assigned_to",
            "revision_rounds_included",
            "client_approval_notes",
            "internal_notes",
        ]


class ClientPaymentForm(StaffFormMixin, forms.ModelForm):
    required_fields = ("amount", "payment_type", "payment_mode", "payment_date")

    class Meta:
        model = ClientPayment
        fields = ["amount", "payment_type", "payment_mode", "payment_date", "invoice_number", "notes"]


class ClientNoteForm(StaffFormMixin, forms.ModelForm):
    required_fields = ("note",)

    class Meta:
        model = ClientNote
        fields = ["note", "next_follow_up_date"]


class ClientContentStatusForm(StaffFormMixin, forms.ModelForm):
    class Meta:
        model = ClientContentStatus
        fields = [
            "logo_received",
            "photos_received",
            "service_details_received",
            "price_list_received",
            "about_content_received",
            "contact_details_received",
            "social_links_received",
            "testimonials_received",
            "gallery_images_received",
            "domain_access_received",
            "hosting_access_received",
            "content_notes",
        ]


class ClientDomainHostingForm(StaffFormMixin, forms.ModelForm):
    class Meta:
        model = ClientDomainHosting
        fields = [
            "domain_required",
            "domain_name",
            "domain_provider",
            "domain_expiry_date",
            "hosting_required",
            "hosting_provider",
            "hosting_plan",
            "hosting_renewal_date",
            "deployment_url",
            "live_website_url",
            "access_given_by_client",
            "stored_in_password_manager",
            "notes",
        ]


class ProjectProgressTaskForm(StaffFormMixin, forms.ModelForm):
    required_fields = ("task_name", "status", "order")

    class Meta:
        model = ProjectProgressTask
        fields = ["task_name", "status", "order"]
