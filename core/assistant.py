import re
from urllib.parse import urlencode

from .models import AboutProfile, Industry, PackageMarketPrice, PortfolioProject, Service


MARKETS = {
    "IN": ("India — INR", "INR", ("india", "inr", "rupee", "rupees", "₹")),
    "US_INTL": ("USA / International — USD", "USD", ("usa", "us", "international", "usd", "dollar")),
    "UK": ("United Kingdom — GBP", "GBP", ("uk", "britain", "gbp", "pound")),
    "AU": ("Australia — AUD", "AUD", ("australia", "australian", "aud", "a$")),
    "CA": ("Canada — CAD", "CAD", ("canada", "canadian", "cad", "c$")),
}

PUBLIC_ABOUT = {
    "why_started": "Yuvi Creates was started with a simple idea: every business deserves a website that feels connected to its identity, not like a generic template copied from somewhere else.",
    "approach": "The work starts by understanding the business, its audience and the action visitors should take, then shaping a clean, responsive and practical experience around those goals.",
    "project_types": "Business websites, landing pages, industry-focused websites and custom web systems.",
    "core_stack": "Python, Django, HTML, CSS, JavaScript, databases, API integration, GitHub, deployment and responsive web design.",
}

INDUSTRY_ALIASES = {
    "restaurant-cafe": ("restaurant", "cafe", "bakery", "cloud kitchen", "food", "digital menu"),
    "cricket-sports": ("cricket", "league", "academy", "tournament", "sports", "team"),
    "real-estate": ("real estate", "property", "broker", "builder", "agent"),
    "clinic-healthcare": ("clinic", "doctor", "dentist", "skin clinic", "physio", "healthcare", "medical"),
    "travel-tourism": ("travel", "tour", "trip", "destination"),
    "beauty-salon": ("salon", "makeup", "beauty", "spa"),
    "gym-fitness": ("gym", "fitness", "trainer", "yoga"),
    "hotels-hospitality": ("hotel", "resort", "hospitality", "room"),
    "wedding-events": ("wedding", "event", "planner", "photographer"),
    "shops-products": ("shop", "store", "retail", "catalogue", "ecommerce", "e-commerce", "product"),
    "pet-services": ("pet", "grooming", "veterinary"),
    "local-services": ("local service", "electrician", "cleaning", "plumber", "repair"),
    "personal-portfolios": ("portfolio", "student", "creator", "influencer", "personal brand"),
    "creative-agencies": ("agency", "creative studio", "design agency"),
    "business-services": ("business", "service provider", "company"),
    "custom-systems": ("custom system", "dashboard", "user login", "api", "inventory"),
}

INTENT_NAMES = (
"greeting|time_greeting|what_is_yuvi_creates|who_is_yuvraj|founder|founder_work|is_developer|design_services|technologies|speak_to_yuvraj|location|remote_work|international_clients|show_work|show_services|choose_help|simple_website|professional_website|premium_website|custom_system|landing_page|one_page|multi_page|existing_website|redesign|broken_website|slow_website|mobile_friendly|more_enquiries|online_bookings|admin_panel|user_login|dashboard|api_integration|payment_integration|whatsapp_integration|email_forms|blog|multilingual|site_search|cafe_website|cafe_starter|cafe_professional|cafe_premium|cafe_custom|restaurant_website|bakery_website|cloud_kitchen|food_ordering|digital_menu|cricket_league|cricket_academy|cricket_team|tournament|live_score|fixtures_results|points_table|player_profiles|team_registration|sponsor_section|real_estate|property_starter|property_professional|property_premium|property_admin|multiple_agents|lead_assignment|property_filters|map_integration|clinic_website|clinic_starter|clinic_professional|clinic_premium|multiple_doctors|appointment_request|realtime_appointment|dentist|skin_clinic|physiotherapy|medical_compliance|travel_website|tour_management|travel_booking|destination_pages|salon_website|makeup_artist|spa_website|gym_website|trainer_website|class_schedule|membership_enquiry|hotel_website|resort_website|room_enquiry|room_inventory|wedding_website|event_company|photographer|shop_website|product_catalogue|ecommerce|inventory_management|pet_business|local_service|electrician|cleaning_company|personal_portfolio|student_portfolio|creator_website|agency_website|pricing_general|pricing_india|pricing_us|pricing_uk|pricing_australia|pricing_canada|niche_price|tier_price|compare_prices|price_final|custom_quote|discount|low_budget|part_payment|advance|tax|domain_price|hosting_price|domain_ownership|handover|source_code|responsive|seo|ranking|google_business|speed|security|content_writing|images|branding|timeline|urgent|revisions|support|maintenance|demo_request|no_demo|unlisted_feature|submit_enquiry|unknown"
).split("|")

assert len(INTENT_NAMES) == 150

PHRASES = {
    "greeting": ("hi", "hello", "hey", "namaste"), "time_greeting": ("good morning", "good afternoon", "good evening"),
    "what_is_yuvi_creates": ("what is yuvi creates", "yuvi creates kya"), "who_is_yuvraj": ("who is yuvraj", "yuvraj kaun"),
    "founder": ("who founded", "founder"), "founder_work": ("what does yuvraj do", "yuvraj kya karte"), "design_services": ("why was yuvi creates started", "why yuvi creates", "how do you work", "your process"), "technologies": ("technology", "technologies", "tech stack", "django", "python"),
    "speak_to_yuvraj": ("speak", "talk", "contact yuvraj", "yuvraj se baat"), "show_work": ("show work", "portfolio", "demo dikhao"),
    "show_services": ("services", "what do you do"), "choose_help": ("dont know", "don't know", "help choosing", "find a package", "samajh nahi"),
    "simple_website": ("simple website", "basic website"), "professional_website": ("professional website", "proper business website"),
    "premium_website": ("premium website",), "landing_page": ("landing page",), "one_page": ("one page", "single page"), "multi_page": ("multi page", "multipage"),
    "redesign": ("redesign", "revamp"), "broken_website": ("website broken", "site broken"), "slow_website": ("website slow", "site slow"),
    "mobile_friendly": ("mobile friendly", "responsive nahi"), "more_enquiries": ("more enquiries", "more leads"),
    "online_bookings": ("online booking", "bookings"), "admin_panel": ("admin panel", "content update", "khud update"),
    "user_login": ("user login", "customer login"), "dashboard": ("dashboard",), "api_integration": ("api integration", "api"),
    "payment_integration": ("payment integration", "payment gateway"), "whatsapp_integration": ("whatsapp integration", "whatsapp"),
    "email_forms": ("email form", "enquiry form"), "blog": ("blog",), "multilingual": ("multilingual", "multiple language"), "site_search": ("search functionality", "site search"),
    "pricing_general": ("price", "pricing", "cost", "rate", "kitna"), "price_final": ("final price", "price final"), "discount": ("discount",),
    "low_budget": ("low budget", "small budget", "budget kam"), "part_payment": ("pay in parts", "installment"), "advance": ("advance",), "tax": ("gst", "tax"),
    "domain_price": ("domain price", "domain cost"), "hosting_price": ("hosting price", "hosting cost"), "domain_ownership": ("domain ownership", "own domain"),
    "handover": ("handover",), "source_code": ("source code",), "responsive": ("responsive",), "seo": ("seo",), "ranking": ("guaranteed ranking", "rank guarantee"),
    "google_business": ("google business",), "speed": ("website speed", "performance"), "security": ("security", "secure"), "content_writing": ("content writing",),
    "images": ("images", "photos"), "branding": ("logo", "branding"), "timeline": ("timeline", "how long", "kitne din"), "urgent": ("urgent", "asap"),
    "revisions": ("revision",), "support": ("support after", "post launch"), "maintenance": ("maintenance",), "demo_request": ("demo", "example"),
    "submit_enquiry": ("submit enquiry", "get quote", "quotation"),
}

VARIANTS = {
    "greeting": ["Hi! I can help you compare packages, demos and pricing, or plan a custom website.", "Hello — what would you like to build? I can narrow down the right package and demo.", "Namaste! Website type bata dijiye; main matching package, demo aur pricing check kar dunga."],
    "pricing_general": ["Sure — tell me the business type and the market you want pricing for.", "I can check the current price. Which niche is this for, and should I show INR, USD, GBP, AUD or CAD?", "Let me narrow it down. What kind of website do you need, and which country’s pricing should I use?"],
    "unknown": ["I may have misunderstood that. Are you asking about pricing, package features, demos or a custom website?", "I couldn’t confidently match that to current website information. You can rephrase it, or I can connect you with Yuvraj.", "I don’t want to guess. Is this about a package, demo, feature, price or enquiry?"],
}

def normalise(text):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9₹$£]+", " ", (text or "").lower())).strip()

def detect_market(text, current=""):
    value = normalise(text)
    for code, (_, _, aliases) in MARKETS.items():
        if any(f" {normalise(alias)} " in f" {value} " for alias in aliases): return code
    return current if current in MARKETS else ""

def detect_industry(text, current=""):
    value = normalise(text)
    for slug, aliases in INDUSTRY_ALIASES.items():
        if any(f" {normalise(alias)} " in f" {value} " for alias in aliases): return slug
    return current

def detect_tier(text, current=""):
    value = normalise(text)
    for tier in ("starter", "professional", "premium", "custom"):
        if tier in value: return tier
    return current

def match_intent(text):
    value = normalise(text)
    best, score = "unknown", 0
    for key, phrases in PHRASES.items():
        for phrase in phrases:
            p = normalise(phrase)
            candidate = 100 + len(p) if value == p else len(p) if p in value else 0
            if candidate > score: best, score = key, candidate
    if best != "unknown": return best
    tokens = set(value.split())
    for key in INTENT_NAMES:
        overlap = len(tokens & set(key.split("_")))
        if overlap > score: best, score = key, overlap
    return best if score else "unknown"

def public_founder():
    profile = AboutProfile.objects.filter(is_active=True).first()
    if not profile: return None
    return {"name": profile.name, "role": profile.role, "headline": profile.headline, "bio": profile.bio, "highlights": [x for x in (profile.highlight_one, profile.highlight_two, profile.highlight_three) if x]}

def industry_data(slug):
    return Industry.objects.filter(slug=slug, is_active=True).prefetch_related("packages__market_prices", "demos").first()

def package_for(industry, tier):
    packages = list(industry.packages.all()) if industry else []
    if not packages: return None
    if tier:
        match = next((p for p in packages if tier in p.title.lower()), None)
        if match: return match
    return packages[0]

def buttons(*items):
    return [{"label": label, "url": url} for label, url in items if url]

def response_for(intent, text, context, used):
    industry = industry_data(context.get("industry"))
    market = context.get("market") or "IN"
    tier = context.get("tier")
    package = package_for(industry, tier)
    is_hinglish = any(word in normalise(text).split() for word in ("kya", "ka", "ki", "hai", "mujhe", "chahiye", "kitna", "dikhao"))
    if intent in ("who_is_yuvraj", "founder", "founder_work", "is_developer", "design_services", "technologies"):
        founder = public_founder()
        if not founder: return "I don’t have a confirmed public detail for that, but I can connect you with Yuvraj.", buttons(("Contact Yuvraj", "/contact/?source=Assistant"))
        if intent == "technologies":
            answer = "The public Yuvi Creates technology stack includes " + PUBLIC_ABOUT["core_stack"]
        elif intent == "design_services":
            answer = PUBLIC_ABOUT["why_started"] + " " + PUBLIC_ABOUT["approach"]
        elif intent == "founder_work":
            answer = f"{founder['name']} is {founder['role']} at Yuvi Creates. The work includes {PUBLIC_ABOUT['project_types']}"
        else:
            answer = f"{founder['name']} is {founder['role']} at Yuvi Creates. {founder['headline']} {founder['bio']}"
        return answer[:700], buttons(("About Yuvi Creates", "/about/"), ("View Demos", "/portfolio/"), ("Contact Yuvraj", "/contact/?source=Assistant"))
    if intent in ("what_is_yuvi_creates", "show_services"):
        services = list(Service.objects.all().values_list("title", flat=True)[:6])
        return "Yuvi Creates designs and develops modern websites, landing pages and custom web systems. Current services include: " + ", ".join(services) + ".", buttons(("Explore Services", "/services/"), ("View Demos", "/portfolio/"))
    if intent == "choose_help":
        return "Tell me your business type and the main result you want—for example enquiries, bookings, registrations or sales. I’ll narrow down a suitable package and demo.", buttons(("Browse Packages", "/packages/"), ("View Demos", "/portfolio/"))
    if intent in ("show_work", "demo_request", "no_demo") or intent.endswith("_website"):
        if industry:
            demos = list(industry.demos.all()[:3]); names = ", ".join(d.title for d in demos)
            reply = f"For {industry.title}, the closest current demo option{'s are' if len(demos)!=1 else ' is'} {names}." if demos else "There isn’t an exact public demo for that niche yet, but a custom concept can be planned."
            return reply, buttons(("View Demos", "/portfolio/?search=" + industry.slug), ("View Packages", industry.get_absolute_url()))
        return "You can explore complete website concepts by industry on the Demos page.", buttons(("Explore Demos", "/portfolio/"))
    price_intents = {"pricing_general","pricing_india","pricing_us","pricing_uk","pricing_australia","pricing_canada","niche_price","tier_price","compare_prices","price_final"}
    if intent in price_intents or any(x in normalise(text) for x in ("price", "pricing", "cost", "rate", "kitna")):
        if not industry: return ("Kaunsi business category ke liye pricing chahiye?" if is_hinglish else "Which business category should I check pricing for?"), []
        if not context.get("market"): return ("Kaunsa market dikhau—India, USA/International, UK, Australia ya Canada?" if is_hinglish else "Which market should I show—India, USA/International, UK, Australia or Canada?"), []
        if not package: return "I couldn’t confirm a current package for that combination, so I won’t guess.", buttons(("Request a Quote", "/contact/?source=Assistant"))
        price = package.market_prices.filter(market_code=market, is_active=True).first()
        if not price: return "That package does not currently have a public price for this market. I can help you request a custom quotation.", buttons(("Request Quote", "/contact/?source=Assistant"))
        reply = f"For {MARKETS[market][0]}, {package.title} is currently listed at {price.public_label}. The final quote depends on confirmed pages, features, content, integrations and delivery requirements."
        return reply, buttons(("View Package", industry.get_absolute_url()+"?market="+market), ("Request Quote", "/contact/?"+urlencode({"industry":industry.slug,"package":package.pk,"market":market,"source":"Assistant"})))
    if industry and tier and package and intent not in ("unknown", "greeting", "time_greeting"):
        features = [line.strip(" •-") for line in package.included_features.splitlines() if line.strip()][:5]
        limits = [line.strip(" •-") for line in package.scope_limits.splitlines() if line.strip()][:3]
        details = "; ".join(features)
        if limits:
            details += ". Scope notes: " + "; ".join(limits)
        return f"The current {package.title} scope includes {details}.", buttons(("View Full Package", industry.get_absolute_url()), ("Request Quote", "/contact/?"+urlencode({"industry":industry.slug,"package":package.pk,"market":market,"source":"Assistant"})))
    if industry and (intent not in ("unknown", "greeting", "time_greeting")):
        packages = list(industry.packages.all()[:4]); names = ", ".join(p.title for p in packages)
        return f"For {industry.title}, the current starting options are {names}. Tell me the tier or feature you want to compare, and I’ll use the live package details.", buttons(("View Packages", industry.get_absolute_url()), ("View Demo", "/portfolio/?search="+industry.slug))
    feature_answers = {
        "admin_panel":"Yes, an admin panel can be included. The right scope depends on whether you need to manage content, enquiries, listings, schedules or products.",
        "payment_integration":"Payment gateway integration can be planned after confirming the provider, payment flow and account requirements. Third-party charges are separate unless explicitly quoted.",
        "online_bookings":"There are two options: a simple booking enquiry form, or a real-time booking system/integration. The second is custom scope.",
        "responsive":"Current website builds follow a responsive approach for mobile, tablet and desktop.",
        "seo":"SEO scope depends on the selected package. Standard builds include a clean technical structure; rankings are never guaranteed.",
        "ranking":"No ethical developer can guarantee a Google ranking. Yuvi Creates can implement sound technical structure, but results also depend on content, competition and ongoing SEO.",
        "domain_ownership":"The domain should normally remain registered in the client’s own account so ownership stays clear.",
        "domain_price":"Domain registration is a separate third-party cost unless a proposal explicitly includes it.",
        "hosting_price":"Hosting depends on traffic, storage, backend and deployment requirements. I won’t invent a fixed price without the confirmed scope.",
        "timeline":"Delivery time depends on pages, content readiness, revisions and integrations. Share the niche and scope for a realistic timeline.",
        "revisions":"Revision limits are package-specific. Select an industry and tier and I’ll read the current scope rather than guess.",
        "medical_compliance":"The website can present approved clinic information, but I can’t claim legal or medical compliance without a formal requirements review.",
        "discount":"I can’t promise a discount. Yuvraj can review the confirmed scope and propose the most suitable option.",
        "location":"I don’t have a confirmed public location detail to quote here, so I won’t guess. You can contact Yuvraj directly for current information.",
        "remote_work":"Yes, project discussion and delivery can be handled remotely. Final availability is confirmed during the enquiry.",
        "international_clients":"Yuvi Creates supports public pricing markets for India, USA/International, UK, Australia and Canada. A final proposal is still based on the confirmed scope.",
    }
    if intent in feature_answers: return feature_answers[intent], buttons(("Discuss Requirements", "/contact/?source=Assistant"))
    variants = VARIANTS.get(intent) or VARIANTS.get("greeting" if intent in ("greeting","time_greeting") else "unknown")
    index = (used.get(intent, -1) + 1) % len(variants); used[intent] = index
    return variants[index], buttons(("View Packages", "/packages/"), ("View Demos", "/portfolio/"), ("Talk to Yuvraj", "/contact/?source=Assistant"))

def answer_message(text, session):
    context = session.get("assistant_context", {})
    used = session.get("assistant_variants", {})
    context["industry"] = detect_industry(text, context.get("industry", ""))
    detected_market = detect_market(text, context.get("market", ""))
    if detected_market: context["market"] = detected_market
    context["tier"] = detect_tier(text, context.get("tier", ""))
    intent = match_intent(text)
    reply, actions = response_for(intent, text, context, used)
    context["previous_question"] = text[:500]; context["last_intent"] = intent
    session["assistant_context"] = context; session["assistant_variants"] = used
    return {"intent": intent, "reply": reply, "actions": actions, "context": context}
