from django.http.response import HttpResponse
from django.shortcuts import render


def about(request) -> HttpResponse:
    """
    Обработчик страницы "О нас".
    :param request: Объект запроса.
    :return: HTTP ответ с результатом вызова.
    """
    template = "pages/about.html"
    return render(request, template)


def rules(request) -> HttpResponse:
    """
    Обработчик страницы "Правила".
    :param request: Объект запроса.
    :return: HTTP ответ с результатом вызова.
    """
    template = "pages/rules.html"
    return render(request, template)
