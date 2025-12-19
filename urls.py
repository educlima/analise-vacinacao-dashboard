from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("api/", include("vaccine.urls")),
    path("", TemplateView.as_view(template_name="dashboard.html"), name="dashboard"),
]
