from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("demo/<int:service_id>/<slug:slug>/", views.service_demo, name="service_demo"),
    path("packages/", views.packages, name="packages"),
    path("portfolio/", views.portfolio, name="portfolio"),
    path("portfolio/demo/<int:project_id>/<slug:slug>/", views.portfolio_demo, name="portfolio_demo"),
    path("process/", views.process, name="process"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("faq/", views.faq, name="faq"),
    path("checkout/", views.checkout, name="checkout"),
    path("payment/pending/", views.payment_pending, name="payment_pending"),
    path("payment/success/", views.payment_success, name="payment_success"),
    path("payment/failed/", views.payment_failed, name="payment_failed"),
    path("payment/callback/", views.payment_callback, name="payment_callback"),
]
