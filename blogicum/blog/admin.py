from django.contrib import admin

from .models import Category, Comment, Location, Post

admin.site.empty_value_display = "Не задано"


class PostInline(admin.TabularInline):
    model = Post
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "slug")
    list_filter = ("title",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "pub_date", "author", "category")
    list_filter = ("pub_date", "author", "category")
    search_fields = ("title", "text", "author__username")
    date_hierarchy = "pub_date"
    empty_value_display = "-пусто-"

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_published=1)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


class CommentInline(admin.TabularInline):
    model = Post
    extra = 1


class CommentAdmin(admin.ModelAdmin):
    list_display = ("text", "created_at", "author")
    list_filter = ("created_at", "author")
    search_fields = ("text", "author__username")
    date_hierarchy = "created_at"
    empty_value_display = "-пусто-"


class LocationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Location, LocationAdmin)
