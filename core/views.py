import base64
import hashlib
import hmac
import json
import urllib.error
import urllib.request

from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt

from .data import PACKAGES, PORTFOLIO, SERVICES
from .forms import EnquiryForm, PaymentBookingForm
from .models import AboutProfile, Package, PaymentBooking, PortfolioProject, Review, Service


DEMO_DETAILS = {
    "business-websites": {
        "audience": "cafes, restaurants, gyms, shops, clinics, salons, institutes, and local service businesses",
        "sections": ["Hero with clear offer", "Services/products", "Trust proof", "Gallery", "Contact and map"],
        "cta": "Turn visitors into calls, WhatsApp messages, and enquiries.",
        "vibe": "Local business command center",
        "visual_items": ["Service cards", "Offer strip", "Map block", "WhatsApp CTA"],
        "package_focus": "business",
    },
    "trips-tours-websites": {
        "audience": "travel agencies, tour planners, destination brands, and trip operators",
        "sections": ["Destination hero", "Trip packages", "Itinerary cards", "Gallery", "Booking enquiry"],
        "cta": "Show packages clearly and make trip enquiries easy.",
        "vibe": "Travel itinerary and destination board",
        "visual_items": ["Destination cards", "Day-wise itinerary", "Trip price row", "Booking enquiry"],
        "package_focus": "travel",
    },
    "restaurantcafe-websites": {
        "audience": "restaurants, cafes, cloud kitchens, bakeries, and food brands",
        "sections": ["Food hero", "Menu highlights", "Gallery", "Offers", "Location and WhatsApp"],
        "cta": "Help customers inspect food, location, timing, and contact fast.",
        "vibe": "Cafe menu and table booking flow",
        "visual_items": ["Coffee menu", "Chef special", "Gallery tiles", "Table enquiry"],
        "package_focus": "restaurant",
    },
    "shop-local-store-websites": {
        "audience": "retail stores, boutiques, electronics shops, local sellers, and showrooms",
        "sections": ["Store intro", "Product categories", "Offers", "Gallery", "Map and WhatsApp"],
        "cta": "Make local products easy to discover and enquire about.",
        "vibe": "Product shelf and offer display",
        "visual_items": ["Product grid", "Offer banner", "Store hours", "Location CTA"],
        "package_focus": "shop",
    },
    "digital-menu-qr-menu-websites": {
        "audience": "restaurants and cafes that need a fast QR menu experience",
        "sections": ["Menu categories", "Item prices", "Popular items", "Offers", "Call/WhatsApp actions"],
        "cta": "Give customers a clean mobile menu without app download friction.",
        "vibe": "QR menu on a phone screen",
        "visual_items": ["QR scan", "Menu tabs", "Item prices", "Order CTA"],
        "package_focus": "digital-menu",
    },
    "gym-fitness-websites": {
        "audience": "gyms, trainers, fitness studios, yoga classes, and transformation brands",
        "sections": ["Program hero", "Membership plans", "Trainer profiles", "Transformations", "Lead form"],
        "cta": "Convert fitness interest into trial sessions and membership leads.",
        "vibe": "Training dashboard with plans and progress",
        "visual_items": ["Dumbbell set", "Membership plans", "Trainer profile", "Transformation block"],
        "package_focus": "gym",
    },
    "real-estate-property-websites": {
        "audience": "property advisors, real estate consultants, builders, brokers, and rental agencies",
        "sections": ["Premium property hero", "Listings", "Locations served", "Consultation CTA", "Lead enquiry form"],
        "cta": "Build trust fast and turn property interest into serious calls and enquiries.",
        "vibe": "Premium property consultation and listing page",
        "visual_items": ["Property cards", "Location grid", "Trust numbers", "Consultation form"],
        "package_focus": "real-estate",
    },
    "salon-makeup-artist-websites": {
        "audience": "salons, makeup artists, bridal studios, beauty professionals, and personal care brands",
        "sections": ["Beauty hero", "Service packages", "Portfolio gallery", "Testimonials", "WhatsApp booking CTA"],
        "cta": "Show style, trust, services, and booking options in a premium beauty-focused flow.",
        "vibe": "Elegant bridal and salon booking page",
        "visual_items": ["Bridal package", "Service menu", "Gallery", "Booking CTA"],
        "package_focus": "salon",
    },
    "pet-shop-websites": {
        "audience": "pet shops, pet supply stores, grooming services, and pet care brands",
        "sections": ["Store hero", "Product categories", "Grooming/services", "Offers", "Map and WhatsApp enquiry"],
        "cta": "Show products, services, store trust, and enquiry options in a friendly local-shop flow.",
        "vibe": "Pet shop storefront and enquiry page",
        "visual_items": ["Product shelves", "Grooming CTA", "Offers", "Store map"],
        "package_focus": "pet-shop",
    },
    "hotel-websites": {
        "audience": "hotels, guest houses, lodges, boutique stays, banquet hotels, and resorts",
        "sections": ["Hotel hero", "Room categories", "Amenities", "Gallery", "Booking enquiry CTA"],
        "cta": "Show rooms, amenities, location, trust, and enquiry options in a premium hospitality flow.",
        "vibe": "Hotel room and booking enquiry page",
        "visual_items": ["Room cards", "Amenities", "Gallery", "Map CTA"],
        "package_focus": "hotel",
    },
    "web-design-agency-websites": {
        "audience": "freelancers, agencies, studios, consultants, and service brands selling website work",
        "sections": ["Agency hero", "Services", "Process", "Portfolio preview", "Quote CTA"],
        "cta": "Convince businesses that the service is professional, clear, and ready to launch.",
        "vibe": "Modern web design agency homepage",
        "visual_items": ["Service cards", "Process steps", "Work preview", "Quote form"],
        "package_focus": "business",
    },
    "landing-pages": {
        "audience": "offers, launches, events, lead campaigns, and focused service promotions",
        "sections": ["Single offer hero", "Benefits", "Proof", "FAQ", "Lead CTA"],
        "cta": "Keep one focused goal and push visitors toward action.",
        "vibe": "Focused campaign page",
        "visual_items": ["Offer headline", "Benefit stack", "Proof strip", "Lead form"],
        "package_focus": "landing",
    },
    "portfolio-websites": {
        "audience": "creators, freelancers, coaches, consultants, and personal brands",
        "sections": ["Personal intro", "Work showcase", "Services", "Testimonials", "Contact"],
        "cta": "Present your work clearly and make professional enquiries easier.",
        "vibe": "Personal brand portfolio wall",
        "visual_items": ["Profile hero", "Work cards", "Skill chips", "Contact CTA"],
        "package_focus": "portfolio",
    },
    "small-business-websites": {
        "audience": "service providers, clinics, consultants, repair services, tutors, and local professionals",
        "sections": ["Business intro", "Services", "Why choose us", "Gallery", "Contact"],
        "cta": "Create a simple, trustworthy online presence for local customers.",
        "vibe": "Small business trust page",
        "visual_items": ["Service list", "Trust badges", "Gallery row", "Enquiry form"],
        "package_focus": "small-business",
    },
    "website-redesign-improvement": {
        "audience": "businesses with an old site that needs better clarity, speed, and mobile experience",
        "sections": ["Before/after review", "UX fixes", "Mobile polish", "CTA cleanup", "Performance basics"],
        "cta": "Improve what already exists without starting from zero.",
        "vibe": "Before and after redesign board",
        "visual_items": ["Before audit", "After layout", "Speed notes", "CTA cleanup"],
        "package_focus": "redesign",
    },
    "responsive-website-development": {
        "audience": "brands that need one website to work smoothly on phone, tablet, and desktop",
        "sections": ["Responsive layout", "Mobile navigation", "Readable sections", "Fast interactions", "Device checks"],
        "cta": "Make every screen feel intentional and easy to use.",
        "vibe": "Desktop, tablet, and phone preview",
        "visual_items": ["Desktop layout", "Tablet view", "Phone nav", "Device checks"],
        "package_focus": "responsive",
    },
    "basic-seo-friendly-website-setup": {
        "audience": "small businesses that want clean search-friendly page structure",
        "sections": ["Page titles", "Meta descriptions", "Headings", "Alt text", "Internal links"],
        "cta": "Give your site a clean SEO foundation from launch.",
        "vibe": "Search result and page structure checklist",
        "visual_items": ["Title tags", "Meta preview", "Heading map", "Alt text"],
        "package_focus": "seo",
    },
    "domainhosting-setup-support": {
        "audience": "clients who need help connecting domain, hosting, SSL, and launch setup",
        "sections": ["Domain connection", "Hosting setup", "SSL", "Email basics", "Launch checks"],
        "cta": "Handle the technical launch steps with less confusion.",
        "vibe": "Launch setup control panel",
        "visual_items": ["Domain DNS", "Hosting", "SSL lock", "Launch checklist"],
        "package_focus": "launch",
    },
}


PACKAGE_FOCUS_CATEGORIES = {
    "business": [
        "Starter Business Website",
        "Professional Business Website",
        "Premium Business Website",
        "Advanced Business System",
    ],
    "travel": ["Trips & Tours Website"],
    "restaurant": [
        "Digital Menu / Single Page Website",
        "Basic Restaurant Website",
        "Professional Restaurant Website",
        "Premium Restaurant Website",
        "Advanced Restaurant System",
    ],
    "digital-menu": ["Digital Menu / Single Page Website"],
    "salon": ["Salon & Makeup Artist Websites"],
    "pet-shop": ["Pet Shop Websites"],
    "hotel": ["Hotel Websites"],
}

for focus_key in ("shop", "gym", "real-estate", "landing", "portfolio", "small-business", "redesign", "responsive", "seo", "launch"):
    PACKAGE_FOCUS_CATEGORIES[focus_key] = PACKAGE_FOCUS_CATEGORIES["business"]

PACKAGE_FOCUS_LABELS = {
    "business": "Business website packages",
    "shop": "Shop and local store website packages",
    "gym": "Gym and fitness website packages",
    "real-estate": "Real estate website packages",
    "salon": "Salon & Makeup Artist Websites",
    "pet-shop": "Pet shop website packages",
    "hotel": "Hotel website packages",
    "landing": "Landing page website packages",
    "portfolio": "Portfolio website packages",
    "small-business": "Small business website packages",
    "redesign": "Website redesign packages",
    "responsive": "Responsive website development packages",
    "seo": "SEO-friendly website setup packages",
    "launch": "Domain and hosting setup packages",
    "travel": "Trips & tours packages",
    "restaurant": "Restaurant and cafe packages",
    "digital-menu": "Digital menu packages",
}


PORTFOLIO_DEMO_DETAILS = {
    "restaurant-website-demo": {
        "template": "portfolio_demos/restaurant_website_demo.html",
        "css": "css/portfolio_demos/restaurant_website_demo.css",
        "js": "js/portfolio_demos/restaurant_website_demo.js",
    },
    "cafe-landing-page-demo": {
        "template": "portfolio_demos/cafe_landing_page_demo.html",
        "css": "css/portfolio_demos/cafe_landing_page_demo.css",
        "js": "js/portfolio_demos/cafe_landing_page_demo.js",
    },
    "gym-website-demo": {
        "template": "portfolio_demos/gym_website_demo.html",
        "css": "css/portfolio_demos/gym_website_demo.css",
        "js": "js/portfolio_demos/gym_website_demo.js",
    },
    "personal-portfolio-website": {
        "template": "portfolio_demos/personal_portfolio_website.html",
        "css": "css/portfolio_demos/personal_portfolio_website.css",
        "js": "js/portfolio_demos/personal_portfolio_website.js",
    },
    "cricket-intelligence-dashboard-demo": {
        "template": "portfolio_demos/pitchqi_demo.html",
        "css": "css/portfolio_demos/pitchqi_demo.css",
        "js": "js/portfolio_demos/pitchqi_demo.js",
    },
    "cricket-project-pitchqi": {
        "template": "portfolio_demos/pitchqi_demo.html",
        "css": "css/portfolio_demos/pitchqi_demo.css",
        "js": "js/portfolio_demos/pitchqi_demo.js",
    },
    "trips-tours-website-demo": {
        "template": "portfolio_demos/trips_tours_website_demo.html",
        "css": "css/portfolio_demos/trips_tours_website_demo.css",
        "js": "js/portfolio_demos/trips_tours_website_demo.js",
    },
    "local-service-business-demo": {
        "template": "portfolio_demos/local_service_business_demo.html",
        "css": "css/portfolio_demos/local_service_business_demo.css",
        "js": "js/portfolio_demos/local_service_business_demo.js",
    },
    "shop-website-demo": {
        "template": "portfolio_demos/shop_website_demo.html",
        "css": "css/portfolio_demos/shop_website_demo.css",
        "js": "js/portfolio_demos/shop_website_demo.js",
    },
    "real-estate-property-demo": {
        "template": "portfolio_demos/real_estate_property_demo.html",
        "css": "css/portfolio_demos/real_estate_property_demo.css",
        "js": "js/portfolio_demos/real_estate_property_demo.js",
    },
    "salon-makeup-artist-demo": {
        "template": "portfolio_demos/salon_makeup_artist_demo.html",
        "css": "css/portfolio_demos/salon_makeup_artist_demo.css",
        "js": "js/portfolio_demos/salon_makeup_artist_demo.js",
    },
    "pet-shop-website-demo": {
        "template": "portfolio_demos/pet_shop_website_demo.html",
        "css": "css/portfolio_demos/pet_shop_website_demo.css",
        "js": "js/portfolio_demos/pet_shop_website_demo.js",
    },
    "hotel-website-demo": {
        "template": "portfolio_demos/hotel_website_demo.html",
        "css": "css/portfolio_demos/hotel_website_demo.css",
        "js": "js/portfolio_demos/hotel_website_demo.js",
    },
    "web-design-agency-demo": {
        "template": "portfolio_demos/web_design_agency_demo.html",
        "css": "css/portfolio_demos/web_design_agency_demo.css",
        "js": "js/portfolio_demos/web_design_agency_demo.js",
    },
}


def ensure_default_content():
    for index, (title, description, icon) in enumerate(SERVICES, start=1):
        Service.objects.get_or_create(
            title=title,
            defaults={"description": description, "icon": icon, "order": index},
        )
    if not Package.objects.exists():
        Package.objects.bulk_create(
            Package(
                title=item["title"],
                category=item["category"],
                price=item["price"],
                short_description=item["short_description"],
                included_features="\n".join(item["included_features"]),
                scope_limits="\n".join(item["scope_limits"]),
                summary=item.get("summary", item["short_description"]),
                is_featured=item.get("is_featured", False),
                order=index,
            )
            for index, item in enumerate(PACKAGES, start=1)
        )
    for index, (title, description, stack) in enumerate(PORTFOLIO, start=1):
        PortfolioProject.objects.get_or_create(
            title=title,
            defaults={"description": description, "tech_stack": stack, "order": index},
        )
    PortfolioProject.objects.filter(title="Cricket Project: PitchQI").update(
        title="Cricket Intelligence Dashboard Demo"
    )


def package_features(package):
    return [line.strip() for line in package.included_features.splitlines() if line.strip()]


def package_prefixed_value(package, prefix):
    prefix = prefix.lower()
    for line in package.scope_limits.splitlines():
        clean_line = line.strip()
        if clean_line.lower().startswith(prefix):
            return clean_line.split(":", 1)[1].strip()
    return ""


def package_timeline(package):
    return package_prefixed_value(package, "timeline:")


def package_best_for(package):
    return package_prefixed_value(package, "best for:")


def package_limits(package):
    return [
        line.strip()
        for line in package.scope_limits.splitlines()
        if line.strip()
        and not line.strip().lower().startswith("timeline:")
        and not line.strip().lower().startswith("best for:")
    ]


def razorpay_is_configured():
    return bool(settings.RAZORPAY_API_KEY and settings.RAZORPAY_KEY_SECRET)


def create_razorpay_order(booking):
    payload = {
        "amount": booking.payment_amount_paise,
        "currency": "INR",
        "receipt": f"booking_{booking.pk}",
        "notes": {
            "booking_id": str(booking.pk),
            "package": booking.selected_package,
            "client": booking.client_name,
        },
    }
    request = urllib.request.Request(
        "https://api.razorpay.com/v1/orders",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": "Basic "
            + base64.b64encode(f"{settings.RAZORPAY_API_KEY}:{settings.RAZORPAY_KEY_SECRET}".encode()).decode(),
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))


def verify_razorpay_signature(order_id, payment_id, signature):
    digest = hmac.new(
        settings.RAZORPAY_KEY_SECRET.encode("utf-8"),
        f"{order_id}|{payment_id}".encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(digest, signature)


def home(request):
    ensure_default_content()
    return render(
        request,
        "home.html",
        {
            "services": Service.objects.all()[:6],
            "packages": Package.objects.filter(is_featured=True)[:6],
            "projects": PortfolioProject.objects.all()[:3],
            "about_profile": AboutProfile.objects.filter(is_active=True).first(),
            "reviews": Review.objects.filter(is_featured=True)[:3],
        },
    )


def services(request):
    ensure_default_content()
    return render(request, "services.html", {"services": Service.objects.all()})


def service_demo(request, service_id, slug):
    ensure_default_content()
    service = get_object_or_404(Service, pk=service_id)
    demo_slug = slugify(service.title)
    details = DEMO_DETAILS.get(
        demo_slug,
        {
            "audience": "businesses that need a clean, professional website",
            "sections": ["Clear hero", "Useful sections", "Trust proof", "Contact flow", "Mobile-friendly layout"],
            "cta": "Make the website easier to understand, trust, and act on.",
            "vibe": "Business-ready website preview",
            "visual_items": ["Hero", "Sections", "Proof", "Contact CTA"],
            "package_focus": "business",
        },
    )
    package_focus = details.get("package_focus", "business")
    return render(
        request,
        "demos/service_demo.html",
        {
            "service": service,
            "demo_slug": demo_slug,
            "details": details,
            "package_url": f"{reverse('packages')}?focus={package_focus}",
            "demo_css": f"css/demos/{demo_slug}.css",
            "demo_js": f"js/demos/{demo_slug}.js",
        },
    )


def packages(request):
    ensure_default_content()
    focus = request.GET.get("focus", "")
    focus_categories = PACKAGE_FOCUS_CATEGORIES.get(focus)
    package_list = list(Package.objects.all())
    grouped = {}
    for package in package_list:
        if focus_categories and package.category not in focus_categories:
            continue
        grouped.setdefault(package.category, []).append(
            {
                "package": package,
                "timeline": package_timeline(package),
                "best_for": package_best_for(package),
                "features": package_features(package),
                "limits": package_limits(package),
            }
        )
    return render(
        request,
        "packages.html",
        {
            "grouped_packages": grouped,
            "package_focus": focus if focus_categories else "",
            "package_focus_label": PACKAGE_FOCUS_LABELS.get(focus, ""),
        },
    )


def portfolio(request):
    ensure_default_content()
    return render(request, "portfolio.html", {"projects": PortfolioProject.objects.all()})


def portfolio_demo(request, project_id, slug):
    ensure_default_content()
    project = get_object_or_404(PortfolioProject, pk=project_id)
    project_slug = slugify(project.title)
    demo = PORTFOLIO_DEMO_DETAILS.get(project_slug, PORTFOLIO_DEMO_DETAILS["restaurant-website-demo"])
    return render(
        request,
        demo["template"],
        {
            "project": project,
            "project_slug": project_slug,
            "demo_css": demo["css"],
            "demo_js": demo["js"],
        },
    )


def process(request):
    return render(request, "process.html")


def about(request):
    return render(request, "about.html", {"about_profile": AboutProfile.objects.filter(is_active=True).first()})


def faq(request):
    return render(request, "faq.html")


def contact(request):
    ensure_default_content()
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your enquiry has been sent. I will reply shortly on WhatsApp/email.")
            return redirect("contact")
    else:
        form = EnquiryForm()
    return render(request, "contact.html", {"form": form})


def checkout(request):
    ensure_default_content()
    selected_package = get_object_or_404(Package, pk=request.GET.get("package")) if request.GET.get("package") else Package.objects.first()
    payment_context = None

    if request.method == "POST":
        form = PaymentBookingForm(request.POST, selected_package=selected_package)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.selected_package = selected_package.title
            booking.package_price = selected_package.price
            booking.payment_method = PaymentBooking.PaymentMethod.RAZORPAY
            booking.payment_amount_paise = form.cleaned_data["payable_amount"] * 100
            booking.save()

            if not razorpay_is_configured():
                messages.error(request, "Razorpay keys are missing in .env.")
                return redirect(reverse("payment_failed") + f"?booking={booking.pk}")
            if booking.payment_amount_paise <= 0:
                messages.error(request, "This package needs an exact payable amount before online payment.")
                return redirect(reverse("payment_failed") + f"?booking={booking.pk}")

            try:
                order = create_razorpay_order(booking)
            except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
                booking.payment_status = PaymentBooking.PaymentStatus.FAILED
                booking.save(update_fields=["payment_status"])
                messages.error(request, "Razorpay order could not be created. Please try again.")
                return redirect(reverse("payment_failed") + f"?booking={booking.pk}")

            booking.razorpay_order_id = order["id"]
            booking.save(update_fields=["razorpay_order_id"])
            payment_context = {
                "booking": booking,
                "amount_rupees": booking.payment_amount_paise // 100,
                "razorpay_key": settings.RAZORPAY_API_KEY,
                "razorpay_order_id": booking.razorpay_order_id,
                "callback_url": request.build_absolute_uri(reverse("payment_callback")),
            }
    else:
        form = PaymentBookingForm(selected_package=selected_package)

    return render(
        request,
        "checkout.html",
        {
            "form": form,
            "selected_package": selected_package,
            "features": package_features(selected_package),
            "limits": package_limits(selected_package),
            "payment": payment_context,
        },
    )


def payment_pending(request):
    booking_id = request.GET.get("booking")
    booking = PaymentBooking.objects.filter(pk=booking_id).first() if booking_id else None
    return render(request, "payment_pending.html", {"booking": booking})


def payment_success(request):
    booking_id = request.GET.get("booking")
    booking = PaymentBooking.objects.filter(pk=booking_id).first() if booking_id else None
    return render(request, "payment_success.html", {"booking": booking})


def payment_failed(request):
    booking_id = request.GET.get("booking")
    booking = PaymentBooking.objects.filter(pk=booking_id).first() if booking_id else None
    return render(request, "payment_failed.html", {"booking": booking})


@csrf_exempt
def payment_callback(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid payment callback.")

    order_id = request.POST.get("razorpay_order_id", "")
    payment_id = request.POST.get("razorpay_payment_id", "")
    signature = request.POST.get("razorpay_signature", "")
    booking = PaymentBooking.objects.filter(razorpay_order_id=order_id).first()

    if not booking or not order_id or not payment_id or not signature:
        return redirect("payment_failed")

    booking.razorpay_payment_id = payment_id
    booking.razorpay_signature = signature

    if verify_razorpay_signature(order_id, payment_id, signature):
        booking.payment_status = PaymentBooking.PaymentStatus.PAID
        booking.transaction_id = payment_id
        booking.save(
            update_fields=[
                "razorpay_payment_id",
                "razorpay_signature",
                "payment_status",
                "transaction_id",
            ]
        )
        return redirect(reverse("payment_success") + f"?booking={booking.pk}")

    booking.payment_status = PaymentBooking.PaymentStatus.FAILED
    booking.save(update_fields=["razorpay_payment_id", "razorpay_signature", "payment_status"])
    return redirect(reverse("payment_failed") + f"?booking={booking.pk}")
