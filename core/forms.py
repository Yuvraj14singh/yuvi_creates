import re

from django import forms

from .models import (
    Enquiry,
    PaymentBooking,
    Review,
)


INPUT_CLASS = "form-control"

BUDGET_CHOICES_BY_CURRENCY = {
    "INR": ["Under ₹25,000", "₹25,000 – ₹50,000", "₹50,000 – ₹1,00,000", "₹1,00,000 – ₹2,00,000", "₹2,00,000+", "Not sure yet"],
    "USD": ["Under $750", "$750 – $1,500", "$1,500 – $3,000", "$3,000 – $5,000", "$5,000+", "Not sure yet"],
    "GBP": ["Under £600", "£600 – £1,200", "£1,200 – £2,500", "£2,500 – £4,000", "£4,000+", "Not sure yet"],
    "AUD": ["Under A$1,000", "A$1,000 – A$2,000", "A$2,000 – A$4,000", "A$4,000 – A$7,000", "A$7,000+", "Not sure yet"],
    "CAD": ["Under C$900", "C$900 – C$1,800", "C$1,800 – C$3,500", "C$3,500 – C$6,000", "C$6,000+", "Not sure yet"],
    "Other": ["Entry-level project", "Standard business project", "Premium business project", "Advanced/custom system", "Not sure yet"],
}


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
            "business_name": "Business / brand",
            "email": "Private email",
            "location": "City / country",
            "service_received": "Website or service",
            "quote": "Share your experience",
        }
        for name, placeholder in placeholders.items():
            self.fields[name].widget.attrs["placeholder"] = placeholder

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        if rating not in range(1, 6):
            raise forms.ValidationError("Choose a rating from 1 to 5.")
        return rating


class EnquiryForm(forms.ModelForm):
    budget_level = forms.ChoiceField(label="Approximate budget range", required=False)

    class Meta:
        model = Enquiry
        fields = [
            "name",
            "business_name",
            "email",
            "phone",
            "country",
            "preferred_currency",
            "business_type",
            "package_interested_in",
            "current_website_or_social_link",
            "estimated_pages",
            "required_features",
            "preferred_timeline",
            "budget_level",
            "message",
        ]
        widgets = {
            "required_features": forms.Textarea(attrs={"rows": 4}),
            "message": forms.Textarea(attrs={"rows": 5}),
        }
        labels = {
            "name": "Full name",
            "business_name": "Business or organisation name",
            "phone": "Phone or WhatsApp number",
            "business_type": "Business industry",
            "package_interested_in": "Required service / package",
            "current_website_or_social_link": "Current website URL",
            "estimated_pages": "Estimated number of pages",
            "required_features": "Required features",
            "preferred_timeline": "Preferred timeline",
            "budget_level": "Approximate budget range",
            "message": "Project description",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", INPUT_CLASS)
        self.fields["country"].required = True
        self.fields["preferred_currency"].required = True
        self.fields["current_website_or_social_link"].required = False
        all_budget_choices = []
        for choices in BUDGET_CHOICES_BY_CURRENCY.values():
            for choice in choices:
                if choice not in all_budget_choices:
                    all_budget_choices.append(choice)
        self.fields["budget_level"].choices = [("", "Select an optional budget range")] + [(choice, choice) for choice in all_budget_choices]
        self.fields["budget_level"].widget.attrs["data-budget-select"] = ""
        self.fields["preferred_currency"].widget.attrs["data-currency-select"] = ""
        self.fields["name"].widget.attrs.setdefault("placeholder", "Your full name")
        self.fields["business_name"].widget.attrs.setdefault("placeholder", "Business or brand name")
        self.fields["email"].widget.attrs.setdefault("placeholder", "you@example.com")
        self.fields["phone"].widget.attrs.setdefault("placeholder", "Phone / WhatsApp")
        self.fields["country"].widget.attrs.setdefault("placeholder", "Country")
        self.fields["business_type"].widget.attrs.setdefault("placeholder", "Your industry")
        self.fields["package_interested_in"].widget.attrs.setdefault("placeholder", "Service / package")
        self.fields["current_website_or_social_link"].widget.attrs.setdefault("placeholder", "Website or social URL")
        self.fields["estimated_pages"].widget.attrs.setdefault("placeholder", "Page count / not sure")
        self.fields["required_features"].widget.attrs.setdefault("placeholder", "Features you need")
        self.fields["preferred_timeline"].widget.attrs.setdefault("placeholder", "Preferred timeline")
        self.fields["message"].widget.attrs.setdefault("placeholder", "Tell me about your project")

    def clean(self):
        cleaned_data = super().clean()
        currency = cleaned_data.get("preferred_currency")
        budget = cleaned_data.get("budget_level")
        if budget and budget not in BUDGET_CHOICES_BY_CURRENCY.get(currency, []):
            self.add_error("budget_level", "Choose a budget option that matches your preferred currency.")
        return cleaned_data


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
        self.fields["phone"].widget.attrs.setdefault("placeholder", "Phone / WhatsApp")
        self.fields["business_type"].widget.attrs.setdefault("placeholder", "Your industry")
        self.fields["current_website_or_social_link"].widget.attrs.setdefault("placeholder", "Website or social URL")

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
