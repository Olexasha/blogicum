from django.urls import path

from . import views

app_name: str = "pages"

urlpatterns: list = [
    path("about/", views.about, name="about"),
    path("rules/", views.rules, name="rules"),
]
