from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("demo/<int:service_id>/<slug:slug>/", views.service_demo, name="service_demo"),
    path("packages/", views.packages, name="packages"),
    path("packages/<slug:industry_slug>/", views.industry_packages, name="industry_packages"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("feedback/", views.feedback, name="feedback"),
    path("portfolio/demo/<int:project_id>/<slug:slug>/", views.portfolio_demo, name="portfolio_demo"),
    path("process/", views.process, name="process"),
    path("about/", views.about, name="about"),
    path("yuvraj-singh/", views.founder_portfolio, name="founder_portfolio"),
    path("contact/", views.contact, name="contact"),
    path("faq/", views.faq, name="faq"),
    path("checkout/", views.checkout, name="checkout"),
    path("payment/pending/", views.payment_pending, name="payment_pending"),
    path("payment/success/", views.payment_success, name="payment_success"),
    path("payment/failed/", views.payment_failed, name="payment_failed"),
    path("payment/callback/", views.payment_callback, name="payment_callback"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap_xml"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
    path("assistant/context/", views.assistant_context, name="assistant_context"),
    path("assistant/bootstrap/", views.assistant_bootstrap, name="assistant_bootstrap"),
    path("assistant/message/", views.assistant_message, name="assistant_message"),
    path("assistant/packages/", views.assistant_packages, name="assistant_packages"),
    path("assistant/pricing/", views.assistant_pricing, name="assistant_pricing"),
    path("assistant/demos/", views.assistant_demos, name="assistant_demos"),
    path("assistant/lead/", views.assistant_lead, name="assistant_lead"),
    # path("", include("core.urls")),

]
