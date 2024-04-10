from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from blog.models import (
    Category,
    Comment,
    Post,
)
from blogicum.urls import handler404

from .forms import (
    CommentForm,
    PostForm,
)
from .utils import CreateUpdateView

User = get_user_model()

# Имена URL
INDEX_URL = "blog:index"
PROFILE_URL = "blog:profile"
POST_DETAIL_URL = "blog:post_detail"

# Константы URL
INDEX = reverse_lazy(INDEX_URL)
PROFILE = reverse_lazy(PROFILE_URL)
POST_DETAIL = reverse_lazy(POST_DETAIL_URL)


class PostFieldsMixin:
    """Миксин, определяющий общие поля для представлений создания и
    редактирования постов.
    """

    model = Post
    template_name = "blog/create.html"
    success_url = INDEX

    def check_if_user_is_author(self, request, *args, **kwargs):
        """Проверяет, является ли текущий пользователь автором
        поста.
        """
        post_to_delete = get_object_or_404(Post, id=kwargs["pk"])
        if request.user.id != post_to_delete.author.id:
            return redirect(POST_DETAIL_URL, pk=post_to_delete.pk)
        else:
            return super().dispatch(request, *args, **kwargs)


class PostCreateEditView(
    LoginRequiredMixin, PostFieldsMixin, CreateUpdateView
):
    """Представление для создания и редактирования постов."""

    form_class = PostForm

    def form_valid(self, form):
        """Проверяет валидность формы и устанавливает текущего
        пользователя в качестве автора поста.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        """Возвращает URL для перенаправления после успешного
        создания/редактирования поста.
        """
        return reverse(PROFILE_URL, args=[self.request.user.username])

    def dispatch(self, request, *args, **kwargs):
        """Перехватывает запрос и проверяет, может ли текущий
        пользователь редактировать пост.
        """
        if "edit/" in self.request.path:
            post_to_delete = get_object_or_404(Post, id=kwargs["pk"])
            if request.user.id != post_to_delete.author.id:
                return redirect("blog:post_detail", pk=post_to_delete.pk)
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, PostFieldsMixin, DeleteView):
    """Представление для удаления поста."""

    def dispatch(self, request, *args, **kwargs):
        """
        Перехватывает запрос и проверяет, может ли текущий пользователь
        удалить пост.
        """
        return self.check_if_user_is_author(request, *args, **kwargs)


class ListingMixin:
    """Миксин, определяющий общие поля для представлений списка постов."""

    model = Post
    ordering = "-pub_date"
    paginate_by = 10


class PostListView(ListingMixin, ListView):
    """Представление списка постов."""

    template_name = "blog/index.html"
    queryset = (
        Post.objects.select_related("location", "author", "category")
        .exclude(pub_date__gt=timezone.now())
        .filter(is_published=1, category__is_published=1)
        .annotate(comment_count=Count("comments"))
    )


class CategoryListView(ListingMixin, ListView):
    """Представление списка постов в категории."""

    template_name = "blog/category.html"

    def get_queryset(self):
        """Получает отфильтрованный список постов в выбранной категории."""
        queryset = super().get_queryset()
        category = get_object_or_404(
            Category, slug=self.kwargs["category_slug"], is_published=1
        )
        return (
            queryset.select_related("category")
            .exclude(pub_date__gt=timezone.now())
            .filter(category=category, is_published=1)
            .annotate(comment_count=Count("comments"))
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет выбранную категорию в контекст."""
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(
            Category, slug=self.kwargs["category_slug"], is_published=1
        )
        return context


class UserProfileView(ListingMixin, ListView):
    """Представление профиля пользователя."""

    template_name = "blog/profile.html"
    queryset = Post.objects.select_related("author").annotate(
        comment_count=Count("comments")
    )

    def get_queryset(self):
        """Получает отфильтрованный список постов пользователя."""
        author = get_object_or_404(User, username=self.kwargs["username"])
        queryset = super().get_queryset()
        queryset = queryset.filter(author=author)
        if author.id != self.request.user.id:
            queryset = queryset.filter(
                is_published=1, category__is_published=1
            ).exclude(pub_date__gt=timezone.now())
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        """Добавляет профиль пользователя в контекст."""
        context = super().get_context_data(**kwargs)
        author_id = get_object_or_404(
            User, username=self.kwargs["username"]
        ).id
        context["profile"] = get_object_or_404(User, id=author_id)
        return context


class UserEditProfileView(LoginRequiredMixin, UpdateView):
    """Представление редактирования профиля пользователя."""

    model = User
    template_name = "blog/user.html"
    fields = ["first_name", "last_name", "username", "email", "about_me"]

    def get_queryset(self):
        """
        Получает отфильтрованный запрос для редактирования профиля
        пользователя.
        """
        return super().get_queryset().filter(id=self.kwargs["pk"])

    def get_success_url(self, *args, **kwargs):
        """Возвращает URL для перенаправления после успешного
        редактирования профиля.
        """
        username = get_object_or_404(User, id=self.kwargs["pk"]).username
        return reverse_lazy(PROFILE_URL, args=[username])


class PostDetailView(DetailView):
    """Представление для детального просмотра поста."""

    model = Post
    template_name = "blog/detail.html"

    def is_post_accessible(self, post, user):
        """Проверяет, доступен ли пост для просмотра текущему
        пользователю.
        """
        return (
                post.is_published
                and post.category.is_published
                and post.pub_date <= timezone.now()
        ) or user == post.author

    def dispatch(self, request, *args, **kwargs):
        """Перехватывает запрос и проверяет, доступен ли пост
        текущему пользователю.
        """
        try:
            post = self.get_object()
            if not self.is_post_accessible(post, request.user):
                raise Http404(
                    "Такого поста не существует или у вас нет доступа к нему."
                )
        except Http404 as error:
            return handler404(request, exception=str(error))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Добавляет форму комментариев и список комментариев в контекст."""
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        context["comments"] = self.object.comments.select_related("post")
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Представление для создания комментариев."""

    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        """Проверяет валидность формы и устанавливает текущего
        пользователя в качестве автора комментария.
        """
        post = get_object_or_404(Post, id=self.kwargs["pk"])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def form_invalid(self, form):
        """Перенаправляет на страницу поста в случае невалидной формы."""
        return HttpResponseRedirect(
            self.model.get_absolute_url(self.kwargs["pk"])
        )


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования комментариев."""

    model = Comment
    template_name = "blog/comment.html"
    form_class = CommentForm

    def dispatch(self, request, *args, **kwargs):
        comment_to_delete = get_object_or_404(Comment, id=self.kwargs["pk"])
        if request.user.id != comment_to_delete.author.id:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Проверяет валидность формы и устанавливает текущего
        пользователя в качестве автора комментария.
        """
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def form_invalid(self, form):
        """Перенаправляет на страницу поста в случае невалидной формы."""
        return HttpResponseRedirect(
            self.model.get_absolute_url(self.kwargs["pk"])
        )


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """Представление для удаления комментариев."""

    model = Comment
    template_name = "blog/comment.html"

    def dispatch(self, request, *args, **kwargs):
        """Перехватывает запрос и проверяет, может ли текущий
        пользователь удалить комментарий.
        """
        comment_to_delete = get_object_or_404(Comment, id=self.kwargs["pk"])
        if request.user.id != comment_to_delete.author.id:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        """Возвращает URL для перенаправления после успешного
        удаления комментария.
        """
        post = get_object_or_404(Post, id=self.kwargs["post_id"])
        return reverse(POST_DETAIL_URL, kwargs={"pk": post.pk})

    def form_invalid(self, form):
        """Перенаправляет на страницу поста в случае невалидной формы."""
        return HttpResponseRedirect(self.get_success_url())
