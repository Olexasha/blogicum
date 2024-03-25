from blog.models import Category, Post
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

posts_dict: dict = {}


def index(request) -> HttpResponse:
    """
    Обработчик страницы "Главная".
    :param request: Объект запроса.
    :return: HTTP ответ с результатом вызова.
    """
    template = "blog/index.html"
    post_list = (
        Post.objects.exclude(pub_date__gt=timezone.now())
        .filter(is_published=1, category__is_published=1)
        .select_related("location", "author", "category")
        .order_by("-pub_date")
    )[:5]
    context = {"post_list": post_list}
    return render(request, template, context)


def post_detail(request, id) -> HttpResponse:
    """
    Обработчик страницы подробностей "Пост".
    :param request: Объект запроса.
    :param id: ID поста.
    :return: HTTP ответ с результатом вызова.
    """
    template = "blog/detail.html"
    post = get_object_or_404(
        Post,
        id=id,
        pub_date__lte=timezone.now(),
        is_published=1,
        category__is_published=1,
    )
    context = {"post": post}
    return render(request, template, context)


def category_posts(request, category_slug) -> HttpResponse:
    """
    Обработчик страницы "Категория".
    :param request: Объект запроса.
    :param category_slug: Наименование категории.
    :return: HTTP ответ с результатом вызова.
    """
    template = "blog/category.html"
    category = get_object_or_404(Category, slug=category_slug, is_published=1)
    post_list = (
        Post.objects.exclude(pub_date__gt=timezone.now())
        .filter(category_id=category.id, is_published=1)
        .select_related("location", "author", "category")
        .order_by("-pub_date")
    )
    context = {"category": category, "post_list": post_list}
    return render(request, template, context)
