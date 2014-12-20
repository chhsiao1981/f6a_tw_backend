# -*- coding: utf-8 -*-

from f6a_tw_backend.constants import *
from f6a_tw_backend.django_constants import *

from django.conf.urls import patterns, url

from f6a_tw_backend.rest import views

urlpatterns = patterns(
    '',
    url(r'^default/$', views.DefaultView.as_view()),
    url(r'^default$', views.DefaultView.as_view()),
    url(r'^default/detail/(?P<pk>' + DJANGO_URL_VAR_REGEX + r')/$', views.DefaultDetailView.as_view()),
    url(r'^default/detail/(?P<pk>' + DJANGO_URL_VAR_REGEX + r')$', views.DefaultDetailView.as_view()),
    url(r'^(?P<path>' + DJANGO_URL_PATH_REGEX + r')$', views.PathView.as_view()),
)
