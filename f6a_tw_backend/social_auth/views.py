# -*- coding: utf-8 -*-
# from https://github.com/omab/python-social-auth/blob/master/examples/django_example/example/app/views.py

from f6a_tw_backend.constants import *
from f6a_tw_backend.django_constants import *

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from social.apps.django_app.utils import psa
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login, REDIRECT_FIELD_NAME
from social.backends.oauth import BaseOAuth1, BaseOAuth2

from f6a_tw_backend import cfg
from f6a_tw_backend import util


@login_required
@require_POST
@csrf_protect
def logout(request, *args, **kwargs):
    auth_logout(request)

    redirect_url = getattr(settings, 'HOME_URL', '/')

    data = {"url": redirect_url}

    return HttpResponse(util.json_dumps(data), content_type='application/json')


@login_required
def profile(request, *args, **kwargs):
    cfg.logger.warning('start: kwargs: %s', kwargs)
    user = request.user
    cfg.logger.warning('user: %s', user)

    return HttpResponse(util.json_dumps({"username": user.username, "first_name": user.first_name, "last_name": user.last_name}), content_type='application/json')


@csrf_exempt
@psa('social:complete')
def complete(request, backend, *args, **kwargs):
    """Authentication complete view, override this view if transaction
    management doesn't suit your needs."""

    if isinstance(request.backend, BaseOAuth1):
        token = {
            'oauth_token': request.REQUEST.get('access_token'),
            'oauth_token_secret': request.REQUEST.get('access_token_secret'),
        }
    elif isinstance(request.backend, BaseOAuth2):
        token = request.REQUEST.get('access_token')
    else:
        raise HttpResponseBadRequest('Wrong backend type')
    user = request.backend.do_auth(token, ajax=True)
    login(request, user)

    redirect_url = request.REQUEST.get('next', getattr(settings, 'LOGIN_REDIRECT_URL', '/'))

    data = {'id': str(user.id), 'username': user.username, "first_name": user.first_name, "last_name": user.last_name, "url": redirect_url}

    return HttpResponse(util.json_dumps(data), content_type='application/json')
