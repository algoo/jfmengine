# JSSG - Jtremesay's Static Site Generator
# Copyright (C) 2024 Jonathan Tremesaygues
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.
"""Django settings for proj project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from django.core.management.commands.runserver import Command as runserver

from os import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-+lnz3sdad49!x)zq6fg_fah1qdw-01!7y!8)dahyw7hxjgnl$0"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = environ.get("DJANGO_DEBUG", "false") == "true"

ALLOWED_HOSTS = ["exemple.org", "localhost"]
runserver.default_port = '8000'
runserver.default_addr = '127.0.0.1'

# JSSG
JFME_DOMAIN = "www.galae.net"
JFME_CONTENT_DIRS = [BASE_DIR / "content"] + [BASE_DIR / "galae-content"] + [BASE_DIR / "common-content"]
JFME_PAGES_DIRS = [path / "pages" for path in JFME_CONTENT_DIRS]
JFME_POSTS_DIRS = [path / "posts" for path in JFME_CONTENT_DIRS]
JFME_TEMPLATES_DIRS = [path / "templates" for path in JFME_CONTENT_DIRS]
JFME_STATIC_DIRS = [path / "static" for path in JFME_CONTENT_DIRS]
JFME_DEFAULT_METADATA_DICT = {"slug": "index", }                        # The order of include is : JFME_DEFAULT_METADATA_DICT then JFME_DEFAULT_METADATA_FILEPATH then page metadata
JFME_DEFAULT_METADATA_FILEPATH = BASE_DIR / "jssg" / "default_metadata.txt" # If a metadata is specified more than once, the last included is retained
JFME_NUMBER_OF_POSTS_BY_PAGE = 3
JFME_CONTENT_REQUIRED_METADATA = ["title", "slug", "lang", "description"]
JFME_SITEMAP_LASTMOD_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S%z" # %Y:YYYY, %m:MM, %d:DD, %z:+/-HHMM

#Django sites and sitemap app
SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    "jssg",
    "django_jinja_markdown",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django_distill",
    "django_vite_plugin",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "jssg.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.jinja2.Jinja2",
        "DIRS": [path / "jinja2" for path in JFME_TEMPLATES_DIRS],
        "APP_DIRS": True,
        "OPTIONS": {
            "environment": "jssg.jinja2.environment",
            "extensions": ["django_jinja_markdown.extensions.MarkdownExtension"]
        },
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [path / "django" for path in JFME_TEMPLATES_DIRS],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]

# Do we really need this?
ASGI_APPLICATION = "jssg.asgi.application"
WSGI_APPLICATION = "jssg.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []

STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.ManifestStaticFilesStorage",
    },
}


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = "/static/"

DIST_DIR = BASE_DIR / "dist"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = JFME_STATIC_DIRS

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

VITE_MANIFEST_FILE = STATIC_ROOT / ".vite" / "manifest.json"
if not DEBUG and not VITE_MANIFEST_FILE.exists():
    VITE_MANIFEST_FILE.parent.mkdir(parents=True, exist_ok=True)
    VITE_MANIFEST_FILE.write_text("{}")

DJANGO_VITE_PLUGIN = {
    "MANIFEST": VITE_MANIFEST_FILE,
}

import re
from django.template import base
base.tag_re = re.compile(base.tag_re.pattern, re.DOTALL)
