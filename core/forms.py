import re

from django import forms

from .models import (
    Enquiry,
    PaymentBooking,
    Review,
)


INPUT_CLASS = "form-control"


class ReviewForm(forms.ModelForm):
    rating = forms.TypedChoiceField(
        label="Your rating",
        choices=[(5, "5 — Excellent"), (4, "4 — Very good"), (3, "3 — Good"), (2, "2 — Fair"), (1, "1 — Poor")],
        coerce=int,
    )

    class Meta:
        model = Review
        fields = ["client_name", "business_name", "email", "location", "service_received", "rating", "quote"]
        labels = {"client_name": "Your name", "business_name": "Business / brand name", "service_received": "Service or project", "quote": "Your feedback"}
        widgets = {"quote": forms.Textarea(attrs={"rows": 5})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", INPUT_CLASS)
        self.fields["business_name"].required = False
        self.fields["location"].required = False
        placeholders = {
            "client_name": "Your full name",
            "business_name": "Business or brand (optional)",
            "email": "you@example.com (kept private)",
            "location": "City, state (optional)",
            "service_received": "Restaurant website, landing page...",
            "quote": "Tell others about the work, communication and final result",
        }
        for name, placeholder in placeholders.items():
            self.fields[name].widget.attrs["placeholder"] = placeholder

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        if rating not in range(1, 6):
            raise forms.ValidationError("Choose a rating from 1 to 5.")
        return rating


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
