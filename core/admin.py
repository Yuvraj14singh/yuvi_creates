from django.contrib import admin

from .models import (
    AboutProfile,
    Enquiry,
    Package,
    PaymentBooking,
    PortfolioProject,
    Review,
    Service,
)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    search_fields = ("title", "description")
    list_editable = ("order",)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "price", "is_featured", "order")
    list_filter = ("category", "is_featured")
    search_fields = ("title", "short_description", "included_features")
    list_editable = ("is_featured", "order")


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "tech_stack", "order")
    search_fields = ("title", "description", "tech_stack")
    list_editable = ("order",)


@admin.register(AboutProfile)
class AboutProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "role", "headline", "bio")
    readonly_fields = ("updated_at",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("client_name", "business_name", "rating", "is_featured", "order", "created_at")
    list_filter = ("rating", "is_featured", "created_at")
    search_fields = ("client_name", "business_name", "quote")
    list_editable = ("rating", "is_featured", "order")
    readonly_fields = ("created_at",)


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "business_name", "email", "phone", "business_type", "created_at")
    list_filter = ("business_type", "created_at")
    search_fields = ("name", "business_name", "email", "phone", "message")
    readonly_fields = ("created_at",)


@admin.register(PaymentBooking)
class PaymentBookingAdmin(admin.ModelAdmin):
    list_display = (
        "client_name",
        "business_name",
        "selected_package",
        "package_price",
        "payment_method",
        "payment_status",
        "transaction_id",
        "created_at",
    )
    list_filter = ("payment_status", "payment_method", "created_at")
    search_fields = (
        "client_name",
        "business_name",
        "email",
        "phone",
        "selected_package",
        "transaction_id",
        "message",
    )
    readonly_fields = ("created_at",)
