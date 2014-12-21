# -*- coding: utf-8 -*-

"""
Django settings for my_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mongoengine.django.mongo_auth',
    'rest_framework',
    'social.apps.django_app.me',
    'f6a_tw_backend',
    'f6a_tw_backend.rest',
    'f6a_tw_backend.social_auth',
    'corsheaders',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'f6a_tw_backend.urls'

WSGI_APPLICATION = 'f6a_tw_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/'

STATIC_ROOT = 'static/'

# rest framework
# http://www.django-rest-framework.org/

REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        # 'rest_framework.permissions.DjangoModelPermissions',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.YAMLRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),

    'FORM_METHOD_OVERRIDE': False,
    'FORM_CONTENT_OVERRIDE': False,

    'PAGINATE_BY': 10,
}

# CORS

CORS_ORIGIN_ALLOW_ALL = True

# mongo-engine

AUTH_USER_MODEL = 'mongo_auth.MongoUser'
MONGOENGINE_USER_DOCUMENT = 'mongoengine.django.auth.User'
SESSION_ENGINE = 'mongoengine.django.sessions'
SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'

# python-social-auth

SOCIAL_AUTH_STORAGE = 'social.apps.django_app.me.models.DjangoStorage'

AUTHENTICATION_BACKENDS = (
    # 'social.backends.google.GoogleOAuth2',
    # 'social.backends.twitter.TwitterOAuth',
    'social.backends.google.GooglePlusAuth',
    'mongoengine.django.auth.MongoEngineBackend',
)

SOCIAL_AUTH_GOOGLE_PLUS_KEY = ''
SOCIAL_AUTH_GOOGLE_PLUS_SECRET = ''
SOCIAL_AUTH_GOOGLE_PLUS_REDIRECT_URI = ''
SOCIAL_AUTH_GOOGLE_PLUS_USE_UNIQUE_USER_ID = True
