from django.db import migrations


def seed_content(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    Package = apps.get_model("core", "Package")
    PortfolioProject = apps.get_model("core", "PortfolioProject")

    services = [
        ("Restaurant/Cafe Websites", "Premium, mobile-friendly restaurant websites with menu, gallery, location, and WhatsApp flow.", "01"),
        ("Digital Menu / QR Menu Websites", "Fast-loading digital menus that customers can open from a QR code and use easily on phones.", "02"),
        ("Landing Pages", "Focused single-page websites for offers, launches, services, and lead generation.", "03"),
        ("Portfolio Websites", "Personal brand websites for creators, professionals, coaches, and freelancers.", "04"),
        ("Small Business Websites", "Clean websites for shops, gyms, service providers, and local businesses.", "05"),
        ("Website Redesign / Improvement", "Improve layout, mobile experience, clarity, speed, and conversion flow.", "06"),
        ("Responsive Website Development", "Websites built to work smoothly across desktop, tablet, and mobile screens.", "07"),
        ("Basic SEO-Friendly Website Setup", "Clean page structure, titles, descriptions, alt text, and search-friendly basics.", "08"),
        ("Domain/Hosting Setup Support", "Guidance for connecting domain, hosting, SSL, and launch setup.", "09"),
    ]
    if not Service.objects.exists():
        Service.objects.bulk_create(
            Service(title=title, description=description, icon=icon, order=index)
            for index, (title, description, icon) in enumerate(services, start=1)
        )

    packages = [
        ("Digital Menu / Single Page Website", "Starter Digital Menu", "₹10,000", "A clean single-page digital menu for smaller restaurants and cafes.", "1 single page website\nUp to 5 menu categories\nUp to 40 menu items\nBasic item names + prices\nOpening hours\nGoogle Map location\nCall button\nWhatsApp button\nMobile-friendly design\nBasic clean layout\n1 round minor revision", "Single page only\nUp to 40 menu items\n1 round minor revision", False),
        ("Digital Menu / Single Page Website", "Standard Digital Menu", "₹12,000", "A stronger digital menu with more items, photos, and section polish.", "Everything in Starter Digital Menu\nUp to 8 menu categories\nUp to 70 menu items\nBetter section design\nUp to 10 food/photos setup\nSlightly better mobile layout\n2 rounds minor revisions", "Single page digital menu\nUp to 70 menu items\n2 rounds minor revisions", False),
        ("Digital Menu / Single Page Website", "Advanced Digital Menu / Landing Page", "₹16,000", "A premium digital menu landing page with hero, offers, gallery, and stronger CTA flow.", "Everything in Standard Digital Menu\nUp to 100 menu items\nHero section\nOffers/specials section\nGallery section\nBetter premium layout\nBasic SEO title/description\nStrong WhatsApp/call CTA\nGoogle Map section\n2-3 rounds revisions", "Up to 100 menu items\nExtra charges apply above 100 items\n2-3 rounds revisions", True),
        ("Basic Restaurant Website", "Basic Website", "₹18,000", "A compact restaurant website covering the core pages customers expect.", "Home\nMenu\nGallery\nAbout\nLocation/Contact\nWhatsApp/call button\nGoogle Map\nMobile responsive design\nBasic SEO-friendly structure\nUp to 5 pages/sections\nUp to 60 menu items\nUp to 15 photos\n2 rounds minor revisions", "Up to 5 pages/sections\nUp to 60 menu items\nUp to 15 photos\n2 rounds minor revisions", False),
        ("Basic Restaurant Website", "Basic Plus", "₹22,000-₹25,000", "A more polished restaurant website with better gallery, offers, and content arrangement.", "Everything in Basic Website\nUp to 80-100 menu items\nMore polished layout\nBetter gallery setup\nOffers/highlights section\nMore content arrangement\nBetter mobile spacing\n2-3 rounds revisions", "Up to 80-100 menu items\n2-3 rounds revisions\nFinal quote depends on content and design level", False),
        ("Professional Restaurant Website", "Professional Website", "₹30,000", "A premium-looking restaurant website with stronger pages, enquiry flow, and mobile experience.", "Premium-looking homepage\nFull menu sections\nGallery\nOffers/Specials section\nAbout section\nLocation + Google Map\nContact/enquiry flow\nWhatsApp/call button\nBetter mobile experience\nBasic SEO-friendly structure\nUp to 6-7 pages/sections\nUp to 100 menu items\nUp to 25 photos\n3 rounds revisions", "Up to 6-7 pages/sections\nUp to 100 menu items\nUp to 25 photos\n3 rounds revisions", True),
        ("Professional Restaurant Website", "Professional Plus", "₹35,000-₹45,000", "A more custom professional website with animations, richer sections, and speed basics.", "Everything in Professional Website\nMore custom design\nMore sections/pages\nLarger gallery\nMore detailed menu layout\nBasic animations\nBetter CTA flow\nContent arrangement help\nSpeed/basic performance optimization", "Final scope depends on custom sections\nContent and gallery size confirmed before quote", False),
        ("Premium Restaurant Website", "Premium Website", "₹50,000", "A custom premium restaurant website experience with strong brand story, reservation flow, and launch support.", "Custom premium design\nFull restaurant website experience\nHome page with strong hero section\nAdvanced menu layout\nGallery\nOffers/Specials section\nAbout/brand story section\nLocation section with Google Map\nContact section\nReservation/enquiry form\nWhatsApp/call CTA\nStrong call-to-action flow\nBetter mobile user experience\nSpeed optimization\nBasic SEO-friendly structure\nDomain/hosting setup support\nLaunch/setup support\nUp to 8 pages/sections\nUp to 120 menu items\nUp to 35 photos\n3 rounds revisions", "Up to 8 pages/sections\nUp to 120 menu items\nUp to 35 photos\n3 rounds revisions", False),
        ("Premium Restaurant Website", "Premium Plus", "₹60,000-₹75,000", "An elevated custom build with richer animations, events/offers, testimonials, and deeper polish.", "Everything in Premium Website\nMore custom sections\nMore premium animations\nLarger menu\nLarger gallery\nMore detailed reservation/enquiry flow\nTestimonials/reviews section\nEvents/offers page\nBetter performance optimization\nMore design polish\nMore revision support", "Final quote depends on pages, menu size, photos, design level, content, and extra features", False),
        ("Advanced Restaurant System", "Advanced Restaurant System", "₹80,000+", "A custom restaurant system for teams that need admin controls, ordering, bookings, payments, or content management.", "Admin panel\nMenu update system\nMulti-branch pages\nOnline table booking system\nOnline ordering flow\nPayment integration\nCustomer enquiry management\nBlog/news/offers management\nCustom backend", "Custom quote required\nDomain and hosting charges are separate if required\nPayment gateway keys and provider setup are added only during real integration", True),
    ]
    if not Package.objects.exists():
        Package.objects.bulk_create(
            Package(
                category=category,
                title=title,
                price=price,
                short_description=description,
                summary=description,
                included_features=features,
                scope_limits=limits,
                is_featured=featured,
                order=index,
            )
            for index, (category, title, price, description, features, limits, featured) in enumerate(packages, start=1)
        )

    projects = [
        ("Restaurant Website Demo", "A polished restaurant concept with menu, gallery, location, and WhatsApp enquiry flow.", "Django, HTML, CSS, JavaScript"),
        ("Cafe Landing Page Demo", "A warm cafe landing page designed for offers, ambience, menu highlights, and visits.", "HTML, CSS, JavaScript"),
        ("Gym Website Demo", "A conversion-focused gym website with plans, trainer highlights, and mobile CTA.", "Django, CSS, JavaScript"),
        ("Personal Portfolio Website", "A clean personal brand portfolio with services, case studies, and enquiry flow.", "Django, HTML, CSS"),
        ("Cricket Project: PitchQI", "A cricket intelligence project presented with dashboard-style content and structured insights.", "Python, Django, JavaScript"),
    ]
    if not PortfolioProject.objects.exists():
        PortfolioProject.objects.bulk_create(
            PortfolioProject(title=title, description=description, tech_stack=stack, order=index)
            for index, (title, description, stack) in enumerate(projects, start=1)
        )


def unseed_content(apps, schema_editor):
    Service = apps.get_model("core", "Service")
    Package = apps.get_model("core", "Package")
    PortfolioProject = apps.get_model("core", "PortfolioProject")
    Service.objects.all().delete()
    Package.objects.all().delete()
    PortfolioProject.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_content, unseed_content),
    ]
