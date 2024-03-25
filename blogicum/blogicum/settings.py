from pathlib import Path

BASE_DIR: Path = Path(__file__).resolve().parent.parent

SECRET_KEY: str = "django-insecure-kr*zdlb#&0j-sys#72hmlx9b7cg^jx0o3t_&vt&%e=)rij8@(6"

DEBUG: bool = True

ALLOWED_HOSTS: list = []

INSTALLED_APPS: list = [
    "blog.apps.BlogConfig",
    "pages.apps.PagesConfig",
    "core.apps.CoreConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE: list = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF: str = "blogicum.urls"

TEMPLATE_DIRS: list = [BASE_DIR / "templates"]

TEMPLATES: list = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": TEMPLATE_DIRS,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATIONL: str = "blogicum.wsgi.application"


DATABASES: dict = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS: list = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE: str = "ru-RU"

TIME_ZONE: str = "UTC"

USE_I18N: bool = True

USE_L10N: bool = True

USE_TZ: bool = True


STATIC_URL: str = "/static/"

STATICFILES_DIRS: list = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD: str = "django.db.models.BigAutoField"
