# -*- coding: utf-8 -*-

from f6a_tw_backend.constants import *
from f6a_tw_backend.django_constants import *

from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from f6a_tw_backend import cfg
from f6a_tw_backend import util


class DefaultView(APIView):
    def get(self, request, format=None):
        return Response({"success": True}, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = _get_data(request)

        return Response({"success": True, "data": data}, status=status.HTTP_200_OK)


class DefaultDetailView(APIView):
    def get(self, request, pk, format=None):
        return Response({"success": True, "pk": pk}, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        data = _get_data(request)

        return Response({"success": True, "pk": pk, "data": data}, status=status.HTTP_200_OK)


class PathView(APIView):
    def get(self, request, path, format=None):
        return Response({"success": True, "path": path}, status=status.HTTP_200_OK)

    def post(self, request, path, format=None):
        data = _get_data(request)

        return Response({"success": True, "path": path, "data": data}, status=status.HTTP_200_OK)


def _get_data(request):
    data = {}
    try:
        data = request.DATA
    except Exception as e:
        cfg.logger.error('unable to get request.DATA: e: %s', e)
        data = request.POST.dict()

    return data
