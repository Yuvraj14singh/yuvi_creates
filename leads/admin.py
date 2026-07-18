from django.contrib import admin

from .models import Lead, LeadActivity, LeadAttachment
from core.admin_utils import PremiumAdminFormMixin


class LeadActivityInline(admin.TabularInline):
    model = LeadActivity
    extra = 0
    fields = ("activity_type", "message", "activity_date", "next_follow_up_date", "created_by", "created_at")
    readonly_fields = ("created_at",)
    autocomplete_fields = ("created_by",)


class LeadAttachmentInline(admin.TabularInline):
    model = LeadAttachment
    extra = 0
    fields = ("title", "file", "uploaded_by", "uploaded_at")
    readonly_fields = ("uploaded_at",)
    autocomplete_fields = ("uploaded_by",)


@admin.register(Lead)
class LeadAdmin(PremiumAdminFormMixin, admin.ModelAdmin):
    list_display = ("business_name", "contact_person", "category", "source", "priority", "status", "next_follow_up_date", "reply_received", "demo_sent", "proposal_sent", "is_archived")
    search_fields = ("business_name", "contact_person", "email", "phone_number", "instagram_handle", "city")
    list_filter = ("category", "source", "priority", "status", "reply_received", "demo_sent", "proposal_sent", "is_archived", "created_at", "next_follow_up_date")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("created_by",)
    date_hierarchy = "created_at"
    list_per_page = 30
    inlines = (LeadActivityInline, LeadAttachmentInline)
    fieldsets = (
        ("Business", {"fields": ("business_name", "contact_person", "category", "city", "state", "country")}),
        ("Contact", {"fields": ("instagram_handle", "instagram_url", "email", "phone_number", "website_url")}),
        ("Pipeline", {"fields": ("source", "priority", "status", "first_contact_date", "last_contact_date", "next_follow_up_date", "expected_budget")}),
        ("Signals", {"fields": ("proposal_sent", "demo_sent", "reply_received", "meeting_scheduled", "is_archived")}),
        ("Internal", {"fields": ("notes", "created_by", "created_at", "updated_at")}),
    )


@admin.register(LeadActivity)
class LeadActivityAdmin(PremiumAdminFormMixin, admin.ModelAdmin):
    list_display = ("lead", "activity_type", "activity_date", "next_follow_up_date", "created_by", "created_at")
    search_fields = ("lead__business_name", "lead__contact_person", "message")
    list_filter = ("activity_type", "activity_date", "created_at")
    autocomplete_fields = ("lead", "created_by")
    readonly_fields = ("created_at",)
    date_hierarchy = "activity_date"
    list_per_page = 40


@admin.register(LeadAttachment)
class LeadAttachmentAdmin(PremiumAdminFormMixin, admin.ModelAdmin):
    list_display = ("title", "lead", "uploaded_by", "uploaded_at")
    search_fields = ("title", "lead__business_name")
    autocomplete_fields = ("lead", "uploaded_by")
    readonly_fields = ("uploaded_at",)


admin.site.site_header = "Yuvi Creates Administration"
admin.site.site_title = "Yuvi Creates Admin"
admin.site.index_title = "Yuvi Creates Dashboard"
