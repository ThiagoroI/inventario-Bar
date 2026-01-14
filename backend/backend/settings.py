"""
Django settings for backend project.
"""

from pathlib import Path
import pymysql
from datetime import timedelta

pymysql.install_as_MySQLdb()

# ==============================
#   JWT CONFIGURATION
# ==============================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=8),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# ==============================
#   PATHS
# ==============================
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================
#   SECURITY
# ==============================
SECRET_KEY = 'django-insecure-*0z5c(yz#-m8ofd)kdhdlrj$ft3-0!-gb3-6j23&$how4ti3=z'

DEBUG = True

ALLOWED_HOSTS = ["*"]


# ==============================
#   INSTALLED APPS
# ==============================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'django_extensions',

    # CORS
    "corsheaders",

    # DRF
    "rest_framework",

    # Apps propias
    "apps.usuarios",
    "apps.inventario",
    "apps.mesas",
    "apps.pedidos",
]


# ==============================
#   MIDDLEWARE
# ==============================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOW_ALL_ORIGINS = True


# ==============================
#   URL + WSGI
# ==============================
ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"


# ==============================
#   DATABASE
# ==============================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "bar_inventario",
        "USER": "root",
        "PASSWORD": "Caballofeliz.28",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}


# ==============================
#   PASSWORD VALIDATION
# ==============================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# ==============================
#   INTERNATIONALIZATION
# ==============================
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# ==============================
#   DRF + JWT
# ==============================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],

    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],

    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}


# ==============================
#   STATIC FILES
# ==============================
STATIC_URL = "static/"


# ==============================
#   USER MODEL
# ==============================
AUTH_USER_MODEL = "usuarios.Usuario"


# ==============================
#   AUTO FIELD
# ==============================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
