from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Lead, LeadActivity, LeadAttachment


class StyledFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "staff-checkbox")
            else:
                field.widget.attrs.setdefault("class", "staff-control")
            if field.required:
                field.widget.attrs.setdefault("required", "required")


class StaffLoginForm(StyledFormMixin, AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "autofocus": True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))


class LeadForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Lead
        exclude = ("created_by", "created_at", "updated_at", "is_archived")
        widgets = {
            "first_contact_date": forms.DateInput(attrs={"type": "date"}),
            "last_contact_date": forms.DateInput(attrs={"type": "date"}),
            "next_follow_up_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 5, "placeholder": "Internal context, requirements, or next steps"}),
            "expected_budget": forms.NumberInput(attrs={"step": "0.01", "min": "0", "placeholder": "₹"}),
            "business_name": forms.TextInput(attrs={"placeholder": "Business, league, team, or brand"}),
            "phone_number": forms.TextInput(attrs={"inputmode": "tel", "placeholder": "+91…"}),
            "instagram_handle": forms.TextInput(attrs={"placeholder": "@handle"}),
        }

    def clean_expected_budget(self):
        value = self.cleaned_data.get("expected_budget")
        if value is not None and value < 0:
            raise forms.ValidationError("Expected budget cannot be negative.")
        return value


class LeadActivityForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = LeadActivity
        fields = ("activity_type", "message", "activity_date", "next_follow_up_date")
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "What happened? Add useful context."}),
            "activity_date": forms.DateInput(attrs={"type": "date"}),
            "next_follow_up_date": forms.DateInput(attrs={"type": "date"}),
        }


class FollowUpForm(StyledFormMixin, forms.Form):
    next_follow_up_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    message = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Follow-up note"}))


class LeadAttachmentForm(StyledFormMixin, forms.ModelForm):
    ALLOWED_CONTENT_TYPES = {
        "application/pdf", "image/png", "image/jpeg", "image/webp", "video/mp4",
        "video/quicktime", "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }

    class Meta:
        model = LeadAttachment
        fields = ("title", "file")
        widgets = {"file": forms.ClearableFileInput(attrs={"accept": ".pdf,.png,.jpg,.jpeg,.webp,.mp4,.mov,.doc,.docx,.xls,.xlsx"})}

    def clean_file(self):
        uploaded = self.cleaned_data["file"]
        content_type = getattr(uploaded, "content_type", "")
        if content_type and content_type not in self.ALLOWED_CONTENT_TYPES:
            raise forms.ValidationError("This file content type is not allowed.")
        return uploaded
