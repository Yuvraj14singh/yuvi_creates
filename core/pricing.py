MARKETS = {
    "IN": ("INR", "₹", 1),
    "US_INTL": ("USD", "$", 2),
    "UK": ("GBP", "£", 3),
    "AU": ("AUD", "A$", 4),
    "CA": ("CAD", "C$", 5),
}

SPORTS_PACKAGE_SEEDS = [
    {
        "title": "Starter Sports & Community Website",
        "description": "A focused website for teams, academies and communities that need a credible home for updates, schedules and enquiries.",
        "features": ["Custom homepage", "Team or academy profile", "Programs or services", "Schedule or fixtures section", "Gallery", "Enquiry form", "Responsive design"],
        "limits": ["Final pages and content volume confirmed in the proposal", "Advanced registrations and live data quoted separately"],
    },
    {
        "title": "Professional Sports Organisation Website",
        "description": "A structured multi-page platform for leagues and sports organisations that need richer content, teams, fixtures and registration journeys.",
        "features": ["Premium homepage", "Teams and profiles", "Fixtures and results sections", "News or updates", "Registration enquiry flow", "Gallery and sponsors", "Admin-saved enquiries"],
        "limits": ["Data update workflow confirmed before development", "Live scoring integrations quoted separately"],
    },
    {
        "title": "Advanced Sports Platform",
        "description": "A tailored sports system for organisations that need admin workflows, registrations, dashboards or custom competition management.",
        "features": ["Custom application architecture", "Admin dashboard", "Team and player management", "Fixtures and competition workflows", "Registration system", "Role-based access planning", "Custom reporting modules"],
        "limits": ["Scope-based engagement", "Third-party data, payment and live scoring services quoted separately"],
    },
]

# Manually configured commercial bands; these are not currency conversions.
PRICE_BANDS = {
    "business_starter": {"IN": (18000, 30000), "US_INTL": (450, 700), "UK": (350, 550), "AU": (700, 1100), "CA": (600, 950)},
    "business_professional": {"IN": (35000, 65000), "US_INTL": (850, 1400), "UK": (650, 1100), "AU": (1300, 2200), "CA": (1150, 1900)},
    "business_premium": {"IN": (70000, 140000), "US_INTL": (1600, 3000), "UK": (1250, 2400), "AU": (2500, 4700), "CA": (2200, 4100)},
    "digital_starter": {"IN": (10000, 16000), "US_INTL": (280, 450), "UK": (220, 350), "AU": (450, 700), "CA": (380, 600)},
    "digital_standard": {"IN": (16000, 25000), "US_INTL": (450, 700), "UK": (350, 550), "AU": (700, 1100), "CA": (600, 950)},
    "digital_advanced": {"IN": (25000, 40000), "US_INTL": (700, 1100), "UK": (550, 850), "AU": (1100, 1700), "CA": (950, 1500)},
    "restaurant_professional": {"IN": (35000, 70000), "US_INTL": (900, 1600), "UK": (700, 1250), "AU": (1400, 2500), "CA": (1200, 2200)},
    "restaurant_premium": {"IN": (70000, 140000), "US_INTL": (1700, 3200), "UK": (1300, 2500), "AU": (2600, 5000), "CA": (2300, 4300)},
    "travel": {"IN": (35000, 75000), "US_INTL": (900, 1700), "UK": (700, 1350), "AU": (1400, 2700), "CA": (1250, 2300)},
    "beauty_starter": {"IN": (18000, 30000), "US_INTL": (450, 750), "UK": (350, 600), "AU": (700, 1150), "CA": (600, 1000)},
    "beauty_professional": {"IN": (35000, 65000), "US_INTL": (850, 1500), "UK": (650, 1200), "AU": (1300, 2300), "CA": (1150, 2000)},
    "beauty_premium": {"IN": (65000, 120000), "US_INTL": (1500, 2800), "UK": (1200, 2200), "AU": (2300, 4400), "CA": (2000, 3800)},
    "sports_starter": {"IN": (25000, 45000), "US_INTL": (650, 1100), "UK": (500, 850), "AU": (1000, 1700), "CA": (900, 1500)},
    "sports_professional": {"IN": (50000, 100000), "US_INTL": (1200, 2300), "UK": (950, 1800), "AU": (1900, 3600), "CA": (1650, 3100)},
    "sports_advanced": {"IN": (120000, None), "US_INTL": (3000, None), "UK": (2400, None), "AU": (4700, None), "CA": (4100, None)},
    "custom_system": {"IN": (100000, None), "US_INTL": (2500, None), "UK": (2000, None), "AU": (3900, None), "CA": (3400, None)},
}


def price_band_key(package):
    title = package.title.lower()
    category = package.category
    if "system" in title:
        return "custom_system"
    if category == "Trips & Tours Website":
        return "travel"
    if category == "Digital Menu / Single Page Website":
        return "digital_advanced" if "advanced" in title else "digital_standard" if "standard" in title else "digital_starter"
    if "Restaurant Website" in category:
        if category == "Premium Restaurant Website": return "restaurant_premium"
        if category == "Professional Restaurant Website": return "restaurant_professional"
        return "digital_advanced" if "plus" in title else "digital_standard"
    if category == "Salon & Makeup Artist Websites":
        return "beauty_premium" if "premium" in title else "beauty_professional" if "professional" in title else "beauty_starter"
    if category == "Sports & Community Websites":
        return "sports_advanced" if "advanced" in title else "sports_professional" if "professional" in title else "sports_starter"
    if "premium" in title: return "business_premium"
    if "professional" in title: return "business_professional"
    return "business_starter"
