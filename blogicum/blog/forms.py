from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    """
    Форма для добавления поста.
    """
    class Meta:
        model = Post
        exclude = (
            "author",
            "is_published",
        )
        widgets = {
            "pub_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class CommentForm(forms.ModelForm):
    """
    Форма для добавления комментария к посту.
    """

    class Meta:
        model = Comment
        fields = ("text",)
