from django.db import migrations


INDUSTRIES = [
    ("Coaching & Institutes", "coaching-institute", "ED", "Admission Ready", "Present courses, faculty, results and admissions in one credible learning experience.", "EDUCATION WEBSITE SOLUTIONS", "Turn Student Interest Into Confident Admissions.", "Give learners and parents a clear view of programmes, faculty, outcomes and the next step to enrol.", "#d3a943"),
    ("Car Dealers & Auto Showrooms", "car-dealer", "AU", "Test Drive Focused", "Show inventory, brands, finance options and test-drive enquiries professionally.", "AUTOMOTIVE WEBSITE SOLUTIONS", "Move Buyers From Browsing to the Driver's Seat.", "Present vehicles with confidence and make finance, availability and test-drive enquiries effortless.", "#c56f3c"),
    ("Construction & Interior Design", "construction-interior", "IN", "Project Led", "Showcase completed spaces, services and consultations through a refined portfolio.", "BUILD & INTERIOR WEBSITE SOLUTIONS", "Turn Your Best Spaces Into Your Strongest Sales Story.", "Build trust with projects, before-and-after work, services and a focused consultation journey.", "#b56b46"),
    ("Jewellery Stores", "jewellery-store", "JE", "Luxury Retail", "A premium digital showcase for collections, craftsmanship and private appointments.", "JEWELLERY WEBSITE SOLUTIONS", "Make Every Collection Feel Worth Discovering.", "Present signature pieces, bridal collections and craftsmanship through an elegant luxury experience.", "#a77a31"),
    ("Corporate Businesses", "corporate-business", "CO", "Authority Focused", "Position expertise, services, case studies and leadership with authority.", "CORPORATE WEBSITE SOLUTIONS", "Build Confidence Before the First Conversation.", "Present capabilities, industries, proof and leadership in a polished experience built for serious business enquiries.", "#4736c9"),
]

PACKAGES = {
    "coaching-institute": [
        ("Starter Coaching Website", 20000, ["Professional homepage", "Courses overview", "About institute", "Admissions enquiry", "Contact and WhatsApp", "Mobile responsive", "Basic SEO"]),
        ("Professional Coaching Website", 38000, ["Everything in Starter", "Course detail pages", "Faculty profiles", "Student results", "Gallery", "FAQ", "Admin-saved enquiries"]),
        ("Premium Institute Website", 60000, ["Everything in Professional", "Programme comparison", "Success stories", "Events and updates", "Rich admissions flow", "Content management", "Advanced polish"]),
        ("Custom Education Platform", 85000, ["Custom student workflow", "Online registration", "Admin dashboard", "Course management", "Custom modules", "Integration planning", "Launch support"]),
    ],
    "car-dealer": [
        ("Starter Auto Showroom Website", 28000, ["Premium homepage", "Featured vehicles", "Brands section", "Showroom details", "Test-drive enquiry", "Mobile responsive", "Basic SEO"]),
        ("Professional Car Dealer Website", 48000, ["Everything in Starter", "Vehicle inventory", "Vehicle detail pages", "Finance information", "Gallery", "Testimonials", "Admin-saved leads"]),
        ("Premium Automotive Website", 75000, ["Everything in Professional", "Inventory filters", "Compare-ready structure", "Finance enquiry flow", "Offers and launches", "Content management", "Advanced polish"]),
        ("Custom Dealer Inventory System", 120000, ["Custom inventory admin", "Lead dashboard", "Test-drive workflow", "Vehicle availability", "Custom integrations", "Multi-location support", "Launch support"]),
    ],
    "construction-interior": [
        ("Starter Construction Website", 25000, ["Professional homepage", "Services overview", "Selected projects", "About company", "Consultation CTA", "Mobile responsive", "Basic SEO"]),
        ("Professional Interior Portfolio", 45000, ["Everything in Starter", "Project case studies", "Interior portfolio", "Before and after", "Process section", "Testimonials", "Admin-saved enquiries"]),
        ("Premium Design & Build Website", 72000, ["Everything in Professional", "Rich project galleries", "Service detail pages", "Project categories", "Consultation flow", "Content management", "Advanced polish"]),
        ("Custom Project Management Website", 110000, ["Custom project workflow", "Client enquiry dashboard", "Project management modules", "Document planning", "Custom integrations", "Multi-team support", "Launch support"]),
    ],
    "jewellery-store": [
        ("Starter Jewellery Website", 24000, ["Luxury homepage", "Featured collections", "Brand story", "Craftsmanship section", "Appointment enquiry", "Mobile responsive", "Basic SEO"]),
        ("Professional Jewellery Catalogue", 42000, ["Everything in Starter", "Collection pages", "Product showcase", "Wedding collection", "Testimonials", "Store information", "Admin-saved enquiries"]),
        ("Premium Jewellery Experience", 70000, ["Everything in Professional", "Luxury collection storytelling", "Product detail layouts", "Private appointment flow", "Rich editorial gallery", "Content management", "Advanced polish"]),
        ("Custom Jewellery Commerce System", 100000, ["Custom catalogue admin", "Product enquiry workflow", "Collection management", "Appointment dashboard", "Commerce planning", "Custom integrations", "Launch support"]),
    ],
    "corporate-business": [
        ("Starter Corporate Website", 30000, ["Professional homepage", "Company overview", "Services section", "Industries served", "Contact enquiry", "Mobile responsive", "Basic SEO"]),
        ("Professional Corporate Website", 55000, ["Everything in Starter", "Service detail pages", "Leadership profiles", "Process section", "Case studies", "FAQ", "Admin-saved enquiries"]),
        ("Premium Enterprise Website", 85000, ["Everything in Professional", "Industry solution pages", "Rich case studies", "Insights section", "Team and careers", "Content management", "Advanced polish"]),
        ("Custom Corporate Platform", 140000, ["Custom business workflows", "Admin dashboard", "Multi-department content", "Lead routing", "Custom modules", "Integration planning", "Launch support"]),
    ],
}

PRICES = {
    "coaching-institute": [(450,380,720,620),(850,720,1350,1170),(1350,1150,2150,1850),(1900,1600,3000,2600)],
    "car-dealer": [(650,550,1040,900),(1100,930,1750,1510),(1700,1450,2750,2350),(2700,2250,4300,3700)],
    "construction-interior": [(575,485,920,795),(1025,865,1640,1415),(1650,1390,2630,2270),(2475,2090,3950,3410)],
    "jewellery-store": [(550,465,880,760),(950,805,1520,1310),(1600,1340,2550,2200),(2250,1900,3600,3100)],
    "corporate-business": [(680,575,1090,940),(1250,1050,2000,1725),(1950,1650,3120,2690),(3150,2650,5000,4310)],
}

DEMOS = {
    "coaching-institute": ("Coaching Website Demo", "A premium institute website with courses, faculty, results, admissions and student success stories.", "Education Website"),
    "car-dealer": ("Car Dealer Website Demo", "A premium automotive showroom experience with inventory, finance and test-drive enquiries.", "Automotive Website"),
    "construction-interior": ("Construction & Interior Design Demo", "A refined design and build portfolio featuring projects, interiors and consultations.", "Construction Website"),
    "jewellery-store": ("Luxury Jewellery Website Demo", "An elegant jewellery concept with collections, craftsmanship and private appointments.", "Luxury Retail Website"),
    "corporate-business": ("Corporate Business Website Demo", "A high-authority corporate concept with services, industries, case studies and leadership.", "Corporate Website"),
}


def seed(apps, schema_editor):
    Industry = apps.get_model("core", "Industry")
    Package = apps.get_model("core", "Package")
    Price = apps.get_model("core", "PackageMarketPrice")
    Demo = apps.get_model("core", "PortfolioProject")
    market_meta = [("IN","INR","₹"),("US_INTL","USD","$"),("UK","GBP","£"),("AU","AUD","A$"),("CA","CAD","C$")]
    base_order = (Package.objects.order_by("-order").values_list("order", flat=True).first() or 0) + 1
    for industry_order, values in enumerate(INDUSTRIES, 17):
        title, slug, icon, badge, short, eyebrow, heading, text, accent = values
        industry, _ = Industry.objects.get_or_create(slug=slug, defaults={"title":title,"icon":icon,"badge":badge,"short_description":short,"eyebrow":eyebrow,"hero_heading":heading,"hero_text":text,"accent":accent,"order":industry_order,"faq":"Can every section be customized?|Yes. Content, colours, sections and enquiry flows are tailored to the confirmed scope.\nCan the website be managed later?|Content management and admin tools can be included in Professional, Premium or Custom scopes."})
        demo_title, description, stack = DEMOS[slug]
        demo, _ = Demo.objects.get_or_create(title=demo_title, defaults={"description":description,"tech_stack":stack,"order":industry_order})
        industry.demos.add(demo)
        for index, (package_title, inr, features) in enumerate(PACKAGES[slug]):
            package, _ = Package.objects.get_or_create(title=package_title, defaults={"category":title,"price":f"Starting from ₹{inr:,}","short_description":f"A focused {title.lower()} solution designed around credibility, enquiries and growth.","included_features":"\n".join(features),"scope_limits":"Final scope depends on confirmed content and requirements.\nThird-party costs are quoted separately.","summary":f"Premium {title.lower()} website package.","is_featured":index==1,"public_pricing_type":"SCOPE_BASED" if index==3 else "CUSTOM_QUOTE","order":base_order})
            base_order += 1
            industry.packages.add(package)
            values_by_market = [inr] + list(PRICES[slug][index])
            for display_order, ((market, currency, symbol), amount) in enumerate(zip(market_meta, values_by_market), 1):
                Price.objects.update_or_create(package=package, market_code=market, defaults={"currency_code":currency,"currency_symbol":symbol,"min_price":amount,"max_price":None,"pricing_mode":"STARTING_FROM","is_active":True,"display_order":display_order})


def unseed(apps, schema_editor):
    apps.get_model("core", "Industry").objects.filter(slug__in=[row[1] for row in INDUSTRIES]).delete()
    apps.get_model("core", "Package").objects.filter(title__in=[row[0] for items in PACKAGES.values() for row in items]).delete()
    apps.get_model("core", "PortfolioProject").objects.filter(title__in=[row[0] for row in DEMOS.values()]).delete()


class Migration(migrations.Migration):
    dependencies = [("core", "0022_industries_and_clinic_experience")]
    operations = [migrations.RunPython(seed, unseed)]
