from django.shortcuts import render
from django.views.generic import TemplateView


def page_not_found(request, exception):
    return render(request, "pages/404.html", status=404)


def server_error(exception, request=None):
    return render(request, "pages/500.html", status=500)


def csrf_failure(request, reason=""):
    return render(request, "pages/403csrf.html", status=403)


class AboutView(TemplateView):
    """Обработчик страницы "О нас"."""

    template_name = "pages/about.html"


class RulesView(TemplateView):
    """Обработчик страницы "Правила"."""

    template_name = "pages/rules.html"
