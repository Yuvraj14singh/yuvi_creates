from django.urls import path

from . import views


app_name = "leads"

urlpatterns = [
    path("login/", views.staff_login, name="login"),
    path("logout/", views.staff_logout, name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("leads/", views.lead_dashboard, name="lead_dashboard"),
    path("leads/all/", views.lead_list, name="list"),
    path("leads/add/", views.lead_create, name="add"),
    path("leads/follow-ups/", views.follow_ups, name="follow_ups"),
    path("leads/archived/", views.archived_leads, name="archived"),
    path("leads/<int:pk>/", views.lead_detail, name="detail"),
    path("leads/<int:pk>/edit/", views.lead_edit, name="edit"),
    path("leads/<int:pk>/activity/add/", views.activity_add, name="activity_add"),
    path("leads/<int:pk>/attachment/add/", views.attachment_add, name="attachment_add"),
    path("attachments/<int:pk>/download/", views.attachment_download, name="attachment_download"),
    path("leads/<int:pk>/action/<slug:action>/", views.lead_action, name="action"),
]
