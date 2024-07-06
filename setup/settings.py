from pathlib import Path
import os
from django.conf.urls import handler404


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = "django-insecure-w^2#8hy^y&&lk1arec79a$je#qzhu&iiq8qht5)aq(1gr07w2q"

DEBUG = True

if DEBUG:
    def custom_500_view(request, *args, **kwargs):
        from django.views import debug
        from django.http import HttpResponseServerError

        # Use Django's default debug view to render the error
        response = debug.technical_500_response(request, *args, **kwargs)
        # Wrap the response to return as an HTTP response
        return HttpResponseServerError(response.content)

    # Set handler500 to the custom view
    handler500 = 'donations.custom_500_view'
handler404 = 'donations.custom_404_view'


ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '0.0.0.0', '192.168.6.87']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "donations.apps.DonationsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


#Definindo customUser com usuário padrão
AUTH_USER_MODEL = "donations.CustomUser"

ROOT_URLCONF = "setup.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "setup.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
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


# Internationalization

LANGUAGE_CODE = "pt-pt"

TIME_ZONE = "GMT"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
