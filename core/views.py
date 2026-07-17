import base64
import hashlib
import hmac
import json
import urllib.error
import urllib.request
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt

from .data import PACKAGES, PORTFOLIO, SERVICES
from .pricing import MARKETS, PRICE_BANDS, SPORTS_PACKAGE_SEEDS, price_band_key
from .forms import EnquiryForm, PaymentBookingForm, ReviewForm
from .models import (
    AboutProfile,
    Package,
    PaymentBooking,
    PortfolioProject,
    PackageMarketPrice,
    Review,
    Service,
)


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
    "wedding-event-planner-websites": {
        "audience": "wedding planners, event planners, decorators, party organizers, and event management brands",
        "sections": ["Elegant hero", "Services", "Portfolio gallery", "Packages", "Enquiry CTA"],
        "cta": "Show trust, past events, services, and enquiry options in a premium event-planning flow.",
        "vibe": "Luxury wedding and event enquiry page",
        "visual_items": ["Event gallery", "Service cards", "Packages", "Consultation CTA"],
        "package_focus": "wedding-event",
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
    "wedding-event": ["Wedding & Event Planner Websites"],
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
    "wedding-event": "Wedding & event planner website packages",
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
    "wedding-event-planner-website-demo": {
        "template": "portfolio_demos/wedding_event_planner_website_demo.html",
        "css": "css/portfolio_demos/wedding_event_planner_website_demo.css",
        "js": "js/portfolio_demos/wedding_event_planner_website_demo.js",
    },
    "web-design-agency-demo": {
        "template": "portfolio_demos/web_design_agency_demo.html",
        "css": "css/portfolio_demos/web_design_agency_demo.css",
        "js": "js/portfolio_demos/web_design_agency_demo.js",
    },
}


def default_public_pricing_type(title):
    name = title.lower()
    if "system" in name:
        return Package.PublicPricingType.SCOPE_BASED
    if "premium" in name or "advanced" in name:
        return Package.PublicPricingType.TAILORED
    if "starter" in name or name.startswith("basic"):
        return Package.PublicPricingType.STARTING_ON_REQUEST
    return Package.PublicPricingType.CUSTOM_QUOTE


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
                public_pricing_type=default_public_pricing_type(item["title"]),
                order=index,
            )
            for index, item in enumerate(PACKAGES, start=1)
        )
    next_order = Package.objects.order_by("-order").values_list("order", flat=True).first() or 0
    for offset, item in enumerate(SPORTS_PACKAGE_SEEDS, start=1):
        Package.objects.get_or_create(
            title=item["title"],
            defaults={
                "category": "Sports & Community Websites",
                "price": "Internal custom quote",
                "short_description": item["description"],
                "included_features": "\n".join(item["features"]),
                "scope_limits": "\n".join(item["limits"]),
                "summary": item["description"],
                "is_featured": offset == 2,
                "public_pricing_type": Package.PublicPricingType.SCOPE_BASED if offset == 3 else Package.PublicPricingType.CUSTOM_QUOTE,
                "order": next_order + offset,
            },
        )
    for package in Package.objects.all():
        band = PRICE_BANDS[price_band_key(package)]
        for market_code, (minimum, maximum) in band.items():
            currency_code, currency_symbol, display_order = MARKETS[market_code]
            PackageMarketPrice.objects.get_or_create(
                package=package,
                market_code=market_code,
                defaults={
                    "currency_code": currency_code,
                    "currency_symbol": currency_symbol,
                    "min_price": minimum,
                    "max_price": maximum,
                    "pricing_mode": PackageMarketPrice.PricingMode.STARTING_FROM if maximum is None else PackageMarketPrice.PricingMode.RANGE,
                    "display_order": display_order,
                },
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


def package_best_for(package):
    return package_prefixed_value(package, "best for:")


def package_timeline(package):
    return package_prefixed_value(package, "timeline:")


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
            "services": Service.objects.all(),
            "packages": Package.objects.filter(is_featured=True)[:6],
            "projects": PortfolioProject.objects.all()[:3],
            "about_profile": AboutProfile.objects.filter(is_active=True).first(),
            "reviews": Review.objects.filter(status=Review.Status.APPROVED, is_featured=True)[:6],
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
    solution_definitions = [
        {
            "slug": "business-websites",
            "eyebrow": "Business Websites",
            "title": "Professional websites built to earn trust and enquiries.",
            "description": "For service businesses, hotels, local stores, pet-care brands and growing teams that need a clear, credible online presence.",
            "categories": {"Starter Business Website", "Professional Business Website", "Premium Business Website", "Hotel Websites", "Pet Shop Websites"},
        },
        {
            "slug": "restaurant-cafe-websites",
            "eyebrow": "Restaurant & Cafe Websites",
            "title": "Turn menus, ambience and location into a stronger customer journey.",
            "description": "From mobile-first digital menus to premium restaurant websites with reservations, offers and content management.",
            "categories": {"Digital Menu / Single Page Website", "Basic Restaurant Website", "Professional Restaurant Website", "Premium Restaurant Website"},
        },
        {
            "slug": "travel-tourism-websites",
            "eyebrow": "Travel & Tourism Websites",
            "title": "Present destinations and packages with clarity.",
            "description": "Structured travel websites for tour operators and planners who need itineraries, package discovery and booking enquiries.",
            "categories": {"Trips & Tours Website"},
        },
        {
            "slug": "beauty-personal-brand-websites",
            "eyebrow": "Beauty & Personal Brand Websites",
            "title": "Showcase expertise, results and services beautifully.",
            "description": "Portfolio-led websites for salons, makeup artists, wedding professionals and event brands with clear enquiry paths.",
            "categories": {"Salon & Makeup Artist Websites", "Wedding & Event Planner Websites"},
        },
        {
            "slug": "sports-community-websites",
            "eyebrow": "Sports & Community Websites",
            "title": "Bring teams, schedules and communities together online.",
            "description": "Custom solutions for leagues, academies, clubs and communities. Scope is prepared around teams, fixtures, registrations and admin needs.",
            "categories": {"Sports & Community Websites"},
        },
        {
            "slug": "custom-business-systems",
            "eyebrow": "Custom Business Systems",
            "title": "Custom workflows for operations that go beyond a standard website.",
            "description": "For bookings, payments, dashboards, admin controls, content management and tailored business workflows.",
            "categories": {"Advanced Business System", "Advanced Restaurant System"},
        },
    ]
    copy_replacements = {
        "A clean 3-5 section website for any small business that needs a professional online presence.": "A focused website for businesses that need a credible online presence and a clear way for customers to get in touch.",
        "A stronger multi-page website for service providers, shops, gyms, institutes, clinics, salons, and personal brands.": "A polished multi-page website designed to build trust and turn visitors into enquiries.",
        "A premium business website for brands that want stronger design, more trust sections, and a polished enquiry journey.": "A high-end website experience for businesses that need stronger branding, richer content, and custom functionality.",
        "A stronger digital menu with more items, photos, and section polish.": "A structured digital menu that presents more items, photography, and key customer information clearly.",
        "A more polished restaurant website with better gallery, offers, and content arrangement.": "A refined restaurant website with an engaging gallery, timely offers, and clearly organised content.",
        "A premium-looking restaurant website with stronger pages, enquiry flow, and mobile experience.": "A complete restaurant website designed to showcase the menu, build trust, and simplify customer enquiries across devices.",
        "Basic clean layout": "Clean, conversion-focused layout",
        "Slightly better mobile layout": "Enhanced mobile experience",
        "Best for simple businesses": "Designed for businesses establishing their online presence",
        "Extra charges apply": "Additional content can be quoted separately",
        "Content and photos provided by client": "Client-provided assets are organised and optimised for the website",
        "Photos and package details provided by client": "Final content requirements are confirmed before development",
        "Product photos and content provided by client": "Final product content and assets are confirmed before development",
    }

    def polish_copy(value):
        for weak, professional in copy_replacements.items():
            value = value.replace(weak, professional)
        return value

    best_for_by_title = {
        "Starter Business Website": "New businesses, solo professionals, and small local services.",
        "Professional Business Website": "Growing service businesses, clinics, salons, agencies, and personal brands.",
        "Premium Business Website": "Established businesses that need richer design, more pages, or custom functionality.",
        "Premium Plus Business Website": "Established brands planning a larger, highly tailored website experience.",
        "Custom Business System": "Teams that need admin controls, bookings, payments, or tailored workflows.",
        "Tour & Travel Website": "Tour operators, travel planners, and destination-based businesses.",
    }
    best_for_by_category = {
        "Digital Menu / Single Page Website": "Restaurants and cafes that need a fast, mobile-first menu experience.",
        "Basic Restaurant Website": "Independent restaurants and cafes establishing a professional web presence.",
        "Professional Restaurant Website": "Growing food businesses that need richer content and enquiry journeys.",
        "Premium Restaurant Website": "Established hospitality brands seeking a distinctive digital experience.",
        "Salon & Makeup Artist Websites": "Beauty professionals who need strong portfolio proof and booking enquiries.",
        "Hotel Websites": "Hotels, guest houses, boutique stays, and hospitality businesses.",
        "Pet Shop Websites": "Pet stores, grooming services, and local pet-care brands.",
        "Wedding & Event Planner Websites": "Wedding professionals, event planners, and creative service brands.",
    }

    package_list = list(Package.objects.prefetch_related("market_prices").all())
    solution_groups = []
    focus_slug_map = {
        "restaurant": "restaurant-cafe-websites", "digital-menu": "restaurant-cafe-websites",
        "travel": "travel-tourism-websites", "salon": "beauty-personal-brand-websites",
        "wedding-event": "beauty-personal-brand-websites", "business": "business-websites",
        "shop": "business-websites", "pet-shop": "business-websites", "hotel": "business-websites",
        "real-estate": "business-websites", "landing": "business-websites", "portfolio": "business-websites",
        "small-business": "business-websites", "redesign": "business-websites", "responsive": "business-websites",
        "seo": "business-websites", "launch": "business-websites", "gym": "sports-community-websites",
    }
    active_solution = focus_slug_map.get(focus, "")
    for definition in solution_definitions:
        matched = [package for package in package_list if package.category in definition["categories"]]
        items = []
        popular_index = 1 if len(matched) > 1 else 0
        for index, package in enumerate(matched):
            is_custom = package.public_pricing_type == Package.PublicPricingType.SCOPE_BASED
            if index == popular_index and len(matched) > 1:
                badge = "Most Popular"
            elif is_custom:
                badge = "Custom"
            elif index == 0:
                badge = "Starter"
            else:
                badge = "Premium"
            items.append({
                "package": package,
                "timeline": package_timeline(package),
                "best_for": package_best_for(package) or best_for_by_title.get(package.title) or best_for_by_category.get(package.category),
                "features": [polish_copy(item) for item in package_features(package)],
                "key_features": [polish_copy(item) for item in package_features(package)[:6]],
                "limits": [polish_copy(item) for item in package_limits(package)],
                "badge": badge,
                "is_popular": index == popular_index and len(matched) > 1,
                "is_custom": is_custom,
                "description": polish_copy(package.short_description),
                "market_prices": [price for price in package.market_prices.all() if price.is_active],
            })
        solution_groups.append({**definition, "items": items, "active": definition["slug"] == active_solution})
    return render(
        request,
        "packages.html",
        {
            "solution_groups": solution_groups,
            "package_focus": focus if active_solution else "",
            "package_focus_label": PACKAGE_FOCUS_LABELS.get(focus, ""),
            "active_solution": active_solution,
        },
    )


def portfolio(request):
    ensure_default_content()
    return render(request, "portfolio.html", {"projects": PortfolioProject.objects.all()})


def feedback(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.source = Review.Source.WEBSITE
            review.status = Review.Status.PENDING
            forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR", "")
            review.submitted_ip = forwarded_for.split(",")[0].strip() or request.META.get("REMOTE_ADDR")
            review.save()
            messages.success(request, "Thank you! Your feedback was saved and will appear on the homepage after approval.")
            return redirect("feedback")
    else:
        form = ReviewForm()
    return render(request, "feedback.html", {"form": form})


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
    selected_package = Package.objects.filter(pk=request.GET.get("package")).first() if request.GET.get("package") else None
    valid_markets = {value for value, label in PackageMarketPrice.Market.choices}
    selected_market = request.GET.get("market", PackageMarketPrice.Market.INDIA)
    if selected_market not in valid_markets:
        selected_market = PackageMarketPrice.Market.INDIA
    selected_market_price = None
    if selected_package:
        selected_market_price = selected_package.market_prices.filter(market_code=selected_market, is_active=True).first()
        if not selected_market_price:
            selected_market = PackageMarketPrice.Market.INDIA
            selected_market_price = selected_package.market_prices.filter(market_code=selected_market, is_active=True).first()
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save(commit=False)
            if selected_package:
                enquiry.package_interested_in = selected_package.title
                enquiry.selected_market = selected_market
                enquiry.displayed_price_context = selected_market_price.public_label if selected_market_price else ""
                if selected_market_price:
                    enquiry.preferred_currency = selected_market_price.currency_code
            enquiry.save()
            messages.success(request, "Your enquiry has been sent. I will reply shortly on WhatsApp/email.")
            return redirect("contact")
    else:
        initial = {"package_interested_in": selected_package.title} if selected_package else {}
        requested_service = request.GET.get("service", "").strip()
        enquiry_source = request.GET.get("source", "").strip()
        if requested_service and not selected_package:
            initial["package_interested_in"] = requested_service
            initial["business_type"] = "Sports / Cricket Organisation"
        if enquiry_source:
            initial["message"] = f"Enquiry source: {enquiry_source}"
        if selected_market_price:
            initial["preferred_currency"] = selected_market_price.currency_code
        form = EnquiryForm(initial=initial)
    return render(request, "contact.html", {"form": form, "selected_package": selected_package, "selected_market": selected_market, "selected_market_price": selected_market_price})


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


from django.http import HttpResponse
from django.urls import reverse


def sitemap_xml(request):
    base_url = "https://yuvicreates-production.up.railway.app"

    urls = [
        "/",
        "/about/",
        "/services/",
        "/packages/",
        "/portfolio/",
        "/contact/",
    ]

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for path in urls:
        xml.append("  <url>")
        xml.append(f"    <loc>{base_url}{path}</loc>")
        xml.append("    <priority>0.8</priority>")
        xml.append("  </url>")

    xml.append("</urlset>")

    return HttpResponse("\n".join(xml), content_type="application/xml")


from django.http import HttpResponse
from django.urls import reverse


def sitemap_xml(request):
    base_url = "https://yuvicreates-production.up.railway.app"

    urls = [
        "/",
        "/about/",
        "/services/",
        "/packages/",
        "/portfolio/",
        "/contact/",
    ]

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for path in urls:
        xml.append("  <url>")
        xml.append(f"    <loc>{base_url}{path}</loc>")
        xml.append("    <priority>0.8</priority>")
        xml.append("  </url>")

    xml.append("</urlset>")

    return HttpResponse("\n".join(xml), content_type="application/xml")


from django.http import HttpResponse

from django.urls import reverse

def sitemap_xml(request):
    base_url = "https://yuvicreates-production.up.railway.app"
    urls = [
        # Main public pages

        "/",
        "/services/",
        "/packages/",
        "/portfolio/",
        "/process/",
        "/about/",
        "/contact/",
        "/faq/",

        # Portfolio demo pages
        "/portfolio/demo/cafe-landing-page-demo/",
        "/portfolio/demo/gym-website-demo/",
        "/portfolio/demo/hotel-website-demo/",
        "/portfolio/demo/local-service-business-demo/",
        "/portfolio/demo/personal-portfolio-website/",
        "/portfolio/demo/pet-shop-website-demo/",
        "/portfolio/demo/pitchqi-demo/",
        "/portfolio/demo/real-estate-property-demo/",
        "/portfolio/demo/restaurant-website-demo/",
        "/portfolio/demo/salon-makeup-artist-demo/",
        "/portfolio/demo/shop-website-demo/",
        "/portfolio/demo/trips-tours-website-demo/",
        "/portfolio/demo/web-design-agency-demo/",
        "/portfolio/demo/wedding-event-planner-website-demo/",
    ]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for path in urls:
        xml.append("  <url>")
        xml.append(f"    <loc>{base_url}{path}</loc>")
        xml.append("    <priority>0.8</priority>")
        xml.append("  </url>")
    xml.append("</urlset>")
    return HttpResponse("\n".join(xml), content_type="application/xml")

def robots_txt(request):
    content = """User-agent: *
Allow: /
Sitemap: https://yuvicreates-production.up.railway.app/sitemap.xml

"""

    return HttpResponse(content, content_type="text/plain")
