from django.contrib import admin

from .models import (
    AboutProfile,
    Client,
    ClientContentStatus,
    ClientDomainHosting,
    ClientNote,
    ClientPayment,
    ClientProject,
    Enquiry,
    Package,
    PaymentBooking,
    PortfolioProject,
    ProjectProgressTask,
    Review,
    Service,
    ServiceCategory,
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


class ClientProjectInline(admin.TabularInline):
    model = ClientProject
    extra = 0
    fields = ("package_selected", "quoted_amount", "payment_status", "project_status", "priority", "start_date", "expected_delivery_date", "assigned_to")
    show_change_link = True


class ClientContentStatusInline(admin.StackedInline):
    model = ClientContentStatus
    extra = 0
    max_num = 1
    can_delete = False


class ClientDomainHostingInline(admin.StackedInline):
    model = ClientDomainHosting
    extra = 0
    max_num = 1
    can_delete = False


class ClientPaymentInline(admin.TabularInline):
    model = ClientPayment
    extra = 0
    fields = ("amount", "payment_type", "payment_mode", "payment_date", "invoice_number", "notes")


class ClientNoteInline(admin.TabularInline):
    model = ClientNote
    extra = 0
    fields = ("note", "next_follow_up_date", "created_by", "created_at")
    readonly_fields = ("created_at",)


class ProjectProgressTaskInline(admin.TabularInline):
    model = ProjectProgressTask
    extra = 0
    fields = ("task_name", "status", "order", "updated_at")
    readonly_fields = ("updated_at",)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("business_name", "service_category", "contact_person", "phone", "email", "city", "lead_source", "communication_channel", "updated_at")
    list_filter = ("service_category", "lead_source", "communication_channel", "city", "created_at")
    search_fields = ("business_name", "contact_person", "phone", "email", "city")
    readonly_fields = ("created_at", "updated_at")
    inlines = (ClientProjectInline,)


@admin.register(ClientProject)
class ClientProjectAdmin(admin.ModelAdmin):
    list_display = ("client", "package_selected", "quoted_amount", "remaining_amount", "payment_status", "project_status", "priority", "start_date", "expected_delivery_date", "assigned_to")
    list_filter = ("client__service_category", "project_status", "payment_status", "priority", "start_date", "expected_delivery_date", "created_at")
    search_fields = ("client__business_name", "client__contact_person", "client__phone", "client__email", "client__city", "package_selected", "project_type")
    readonly_fields = ("created_at", "updated_at")
    inlines = (
        ClientContentStatusInline,
        ClientDomainHostingInline,
        ClientPaymentInline,
        ClientNoteInline,
        ProjectProgressTaskInline,
    )


@admin.register(ClientContentStatus)
class ClientContentStatusAdmin(admin.ModelAdmin):
    list_display = ("project", "logo_received", "photos_received", "service_details_received", "contact_details_received", "updated_at")
    list_filter = ("logo_received", "photos_received", "service_details_received", "contact_details_received", "updated_at")
    search_fields = ("project__client__business_name", "project__client__contact_person")
    readonly_fields = ("updated_at",)


@admin.register(ClientDomainHosting)
class ClientDomainHostingAdmin(admin.ModelAdmin):
    list_display = ("project", "domain_name", "domain_provider", "hosting_provider", "live_website_url", "stored_in_password_manager")
    list_filter = ("domain_required", "hosting_required", "access_given_by_client", "stored_in_password_manager")
    search_fields = ("project__client__business_name", "domain_name", "domain_provider", "hosting_provider", "live_website_url")


@admin.register(ClientPayment)
class ClientPaymentAdmin(admin.ModelAdmin):
    list_display = ("project", "amount", "payment_type", "payment_mode", "payment_date", "invoice_number", "created_at")
    list_filter = ("payment_type", "payment_mode", "payment_date", "created_at")
    search_fields = ("project__client__business_name", "invoice_number", "notes")
    readonly_fields = ("created_at",)


@admin.register(ClientNote)
class ClientNoteAdmin(admin.ModelAdmin):
    list_display = ("project", "next_follow_up_date", "created_by", "created_at")
    list_filter = ("next_follow_up_date", "created_at", "created_by")
    search_fields = ("project__client__business_name", "note")
    readonly_fields = ("created_at",)


@admin.register(ProjectProgressTask)
class ProjectProgressTaskAdmin(admin.ModelAdmin):
    list_display = ("project", "task_name", "status", "order", "updated_at")
    list_filter = ("status", "updated_at")
    search_fields = ("project__client__business_name", "task_name")
    list_editable = ("status", "order")
    readonly_fields = ("updated_at",)
