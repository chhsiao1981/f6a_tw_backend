# -*- coding: utf-8 -*-

from f6a_tw_backend.constants import *
from f6a_tw_backend.django_constants import *

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin

from f6a_tw_backend import cfg
from f6a_tw_backend import util
from f6a_tw_backend.rest import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin', include(admin.site.urls)),

    url(r'^api/', include('f6a_tw_backend.rest.urls')),

    url(r'^auth/', include('f6a_tw_backend.social_auth.urls')),

    url(r'', include('social.apps.django_app.urls', namespace='social'))

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
