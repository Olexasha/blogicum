from django.contrib import admin
from django.urls import include, path

urlpatterns: list = [
    path("", include("blog.urls", namespace="blog")),
    path("pages/", include("pages.urls", namespace="pages")),
    path("admin/", admin.site.urls),
]
