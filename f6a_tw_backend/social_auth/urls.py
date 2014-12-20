# -*- coding: utf-8 -*-

from f6a_tw_backend.constants import *
from f6a_tw_backend.django_constants import *

from django.conf.urls import patterns, url

from f6a_tw_backend.rest import views

urlpatterns = patterns(
    '',
    url(r'^logout/?$', 'f6a_tw_backend.social_auth.views.logout'),
    url(r'^profile/?$', 'f6a_tw_backend.social_auth.views.profile'),
    url(r'^complete/(?P<backend>' + DJANGO_URL_NO_SLASH_REGEX + r')/?$', 'f6a_tw_backend.social_auth.views.complete'),
)
