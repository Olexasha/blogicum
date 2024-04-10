# Generated by Django 3.2.16 on 2024-04-08 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Снимите галочку, чтобы скрыть публикацию.",
                        verbose_name="Опубликовано",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Добавлено"
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=256, verbose_name="Заголовок"),
                ),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "slug",
                    models.SlugField(
                        help_text="Идентификатор страницы для URL; разрешены символы латиницы, цифры, дефис и подчёркивание.",
                        unique=True,
                        verbose_name="Идентификатор",
                    ),
                ),
            ],
            options={
                "verbose_name": "категория",
                "verbose_name_plural": "Категории",
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Снимите галочку, чтобы скрыть публикацию.",
                        verbose_name="Опубликовано",
                    ),
                ),
                ("text", models.TextField(verbose_name="Текст комментария")),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Создан"
                    ),
                ),
            ],
            options={
                "verbose_name": "комментарий",
                "verbose_name_plural": "Комментарии",
                "ordering": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Снимите галочку, чтобы скрыть публикацию.",
                        verbose_name="Опубликовано",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Добавлено"
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=256, verbose_name="Название места"
                    ),
                ),
            ],
            options={
                "verbose_name": "местоположение",
                "verbose_name_plural": "Местоположения",
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Снимите галочку, чтобы скрыть публикацию.",
                        verbose_name="Опубликовано",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Добавлено"
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=256, verbose_name="Заголовок"),
                ),
                ("text", models.TextField(verbose_name="Текст")),
                (
                    "pub_date",
                    models.DateTimeField(
                        help_text="Если установить дату и время в будущем — можно делать отложенные публикации.",
                        verbose_name="Дата и время публикации",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="blog/",
                        verbose_name="Фото",
                    ),
                ),
            ],
            options={
                "verbose_name": "публикация",
                "verbose_name_plural": "Публикации",
            },
        ),
    ]
