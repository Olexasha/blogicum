from django.urls import path

from . import views

app_name: str = "blog"

urlpatterns: list = [
    path("", views.PostListView.as_view(), name="index"),
    path(
        "posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"
    ),
    path(
        "category/<slug:category_slug>/",
        views.CategoryListView.as_view(),
        name="category_posts",
    ),
    path(
        "posts/create/", views.PostCreateEditView.as_view(), name="create_post"
    ),
    path(
        "posts/<int:pk>/edit/",
        views.PostCreateEditView.as_view(),
        name="edit_post",
    ),
    path(
        "profile/<username>/", views.UserProfileView.as_view(), name="profile"
    ),
    path(
        "edit_profile/<int:pk>/",
        views.UserEditProfileView.as_view(),
        name="edit_profile",
    ),
    path(
        "posts/<int:pk>/delete/",
        views.PostDeleteView.as_view(),
        name="delete_post",
    ),
    path(
        "posts/<int:pk>/comment/",
        views.CommentCreateView.as_view(),
        name="add_comment",
    ),
    path(
        "posts/<int:post_id>/edit_comment/<int:pk>/",
        views.CommentUpdateView.as_view(),
        name="edit_comment",
    ),
    path(
        "posts/<int:post_id>/delete_comment/<int:pk>/",
        views.CommentDeleteView.as_view(),
        name="delete_comment",
    ),
]
