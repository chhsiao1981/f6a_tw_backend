# -*- coding: utf-8 -*-
"""
WSGI config for my_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

application = None


def init_django_settings_module(settings):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)


def init_application():
    global application
    application = get_wsgi_application()
