"""
Django settings for metadata project.

Generated by 'django-admin startproject' using Django 2.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import sys
import logging

from .. import __version__

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SERVICE_SECRET_KEY", '=p1@hhp5m4v0$c#eba3a+rx!$9-xk^q*7cb9(cd!wn1&_*osyc')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("CHORD_DEBUG", "true").lower() == "true"

ALLOWED_HOSTS = [os.environ.get("CHORD_HOST", "localhost")]
if DEBUG:
    ALLOWED_HOSTS = list(set(ALLOWED_HOSTS + ["localhost", "127.0.0.1", "[::1]"]))

APPEND_SLASH = False


# CHORD-specific settings

CHORD_URL = os.environ.get("CHORD_URL", None)  # Leave None if not specified, for running in other contexts

# SECURITY WARNING: Don't run with CHORD_PERMISSIONS turned off in production,
# unless an alternative permissions system is in place.
CHORD_PERMISSIONS = os.environ.get("CHORD_PERMISSIONS", str(not DEBUG)).lower() == "true"

CHORD_SERVICE_TYPE = "ca.c3g.chord:metadata:{}".format(__version__)
CHORD_SERVICE_ID = os.environ.get("SERVICE_ID", CHORD_SERVICE_TYPE)

# SECURITY WARNING: don't run with AUTH_OVERRIDE turned on in production!
AUTH_OVERRIDE = not CHORD_PERMISSIONS


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'chord_metadata_service.chord',
    'chord_metadata_service.experiments.apps.ExperimentsConfig',
    'chord_metadata_service.patients.apps.PatientsConfig',
    'chord_metadata_service.phenopackets.apps.PhenopacketsConfig',
    'chord_metadata_service.mcode.apps.McodeConfig',
    'chord_metadata_service.restapi',

    'rest_framework',
    'django_nose',
    'rest_framework_swagger',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'chord_lib.auth.django_remote_user.CHORDRemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chord_metadata_service.metadata.urls'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'chord_metadata_service.metadata.wsgi.application'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
        },
    },
    'loggers': {
        '': {
            'level': 'INFO',
            'handlers': ['console'],
        },
    },
}

# if we are running the test suite, only log CRITICAL messages
if len(sys.argv) > 1 and sys.argv[1] == 'test':
    logging.disable(logging.CRITICAL)

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("POSTGRES_DATABASE", 'metadatadevelop'),
        'USER': os.environ.get("POSTGRES_USER", 'admin'),
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD", 'admin'),

        # Use sockets if we're inside a CHORD container / as a priority
        'HOST': os.environ.get("POSTGRES_SOCKET_DIR", os.environ.get("POSTGRES_HOST", "localhost")),
        'PORT': os.environ.get("POSTGRES_PORT", "5432"),
    }
}

FHIR_INDEX_NAME = 'fhir_metadata'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'chord_lib.auth.django_remote_user.CHORDRemoteUserAuthentication'
    ],
    'DEFAULT_PARSER_CLASSES': (
        # allows serializers to use snake_case field names, but parse incoming data as camelCase
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
    ),
    'DEFAULT_PERMISSION_CLASSES': ['chord_metadata_service.chord.permissions.OverrideOrSuperUserOnly'],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTHENTICATION_BACKENDS = ["chord_lib.auth.django_remote_user.CHORDRemoteUserBackend"] + (
    ["django.contrib.auth.backends.ModelBackend"] if DEBUG else [])


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
