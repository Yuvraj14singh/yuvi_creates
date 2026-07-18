from django import forms


class PremiumAdminFormMixin:
    """Add concise form guidance without changing stored model data."""

    placeholder_overrides = {
        "name": "Full name", "role": "Founder & developer",
        "headline": "Short founder headline", "bio": "Brief founder story",
        "highlight_one": "e.g. Django development", "highlight_two": "e.g. Responsive design",
        "highlight_three": "e.g. Direct communication", "title": "Short title",
        "description": "Brief description", "short_description": "One-line summary",
        "email": "name@example.com", "phone": "Phone or WhatsApp",
        "business_name": "Business name", "client_name": "Client name",
        "location": "City, country", "service_received": "Service provided",
        "quote": "Short client review", "message": "Add brief details",
        "notes": "Internal notes", "tech_stack": "e.g. Django, HTML, CSS",
        "project_url": "https://example.com",
    }

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)
        excluded = (forms.Select, forms.CheckboxInput, forms.FileInput)
        if not formfield or isinstance(formfield.widget, excluded):
            return formfield
        placeholder = self.placeholder_overrides.get(db_field.name)
        if not placeholder:
            placeholder = "Add brief details" if isinstance(formfield.widget, forms.Textarea) else f"Enter {db_field.verbose_name}"
        formfield.widget.attrs.setdefault("placeholder", placeholder)
        return formfield
