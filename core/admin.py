from django.contrib import admin

from .models import (
    AboutProfile,
    Enquiry,
    Industry,
    Package,
    PaymentBooking,
    PackageMarketPrice,
    PortfolioProject,
    Review,
    Service,
)
from .admin_utils import PremiumAdminFormMixin


@admin.register(Industry)
class IndustryAdmin(PremiumAdminFormMixin, admin.ModelAdmin):
    list_display = ("title", "slug", "badge", "is_active", "order")
    list_filter = ("is_active",)
    search_fields = ("title", "short_description", "hero_heading")
    list_editable = ("is_active", "order")
    filter_horizontal = ("packages", "demos")


class PackageMarketPriceInline(admin.TabularInline):
    model = PackageMarketPrice
    extra = 0
    fields = ("market_code", "currency_code", "currency_symbol", "min_price", "max_price", "pricing_mode", "is_active", "display_order")


@admin.register(Service)
class ServiceAdmin(PremiumAdminFormMixin, admin.ModelAdmin):
    list_display = ("title", "order")
    search_fields = ("title", "description")
    list_editable = ("order",)


@admin.register(Package)
class PackageAdmin(PremiumAdminFormMixin, admin.ModelAdmin):
    list_display = ("title", "category", "price", "public_pricing_type", "is_featured", "order")
    list_filter = ("category", "public_pricing_type", "is_featured")
    search_fields = ("title", "short_description", "included_features")
    list_editable = ("public_pricing_type", "is_featured", "order")
    inlines = (PackageMarketPriceInline,)


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(PremiumAdminFormMixin, admin.ModelAdmin):
    list_display = ("title", "experience_level", "is_featured", "is_new", "is_popular", "is_luxury", "is_fast_launch", "is_mobile_first", "is_active", "order")
    list_filter = ("industries", "experience_level", "is_featured", "is_new", "is_popular", "is_luxury", "is_fast_launch", "is_mobile_first", "is_active")
    search_fields = ("title", "description", "tech_stack")
    list_editable = ("experience_level", "is_featured", "is_new", "is_popular", "is_luxury", "is_fast_launch", "is_mobile_first", "is_active", "order")


@admin.register(AboutProfile)
class AboutProfileAdmin(PremiumAdminFormMixin, admin.ModelAdmin):
    list_display = ("name", "role", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "role", "headline", "bio")
    readonly_fields = ("updated_at",)


@admin.register(Review)
class ReviewAdmin(PremiumAdminFormMixin, admin.ModelAdmin):
    list_display = ("client_name", "business_name", "location", "service_received", "rating", "source", "status", "is_featured", "created_at")
    list_filter = ("status", "rating", "source", "is_featured", "created_at")
    search_fields = ("client_name", "business_name", "email", "location", "service_received", "quote")
    list_editable = ("status", "is_featured")
    readonly_fields = ("created_at", "submitted_ip")
    date_hierarchy = "created_at"
    actions = ("approve_reviews", "reject_reviews")

    @admin.action(description="Approve selected reviews")
    def approve_reviews(self, request, queryset):
        queryset.update(status=Review.Status.APPROVED)

    @admin.action(description="Reject selected reviews")
    def reject_reviews(self, request, queryset):
        queryset.update(status=Review.Status.REJECTED)


@admin.register(Enquiry)
class EnquiryAdmin(PremiumAdminFormMixin, admin.ModelAdmin):
    list_display = ("name", "business_name", "country", "selected_market", "preferred_currency", "budget_level", "package_interested_in", "final_quote_amount", "final_quote_currency", "created_at")
    list_filter = ("selected_market", "preferred_currency", "budget_level", "business_type", "created_at")
    search_fields = ("name", "business_name", "email", "phone", "country", "package_interested_in", "required_features", "message")
    readonly_fields = ("created_at",)

    def get_readonly_fields(self, request, obj=None):
        return ("created_at", "displayed_price_context")


@admin.register(PaymentBooking)
class PaymentBookingAdmin(PremiumAdminFormMixin, admin.ModelAdmin):
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
