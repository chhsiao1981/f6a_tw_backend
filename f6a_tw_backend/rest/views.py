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


class QueryView(APIView):
    def get(self, request, format=None):
        data = request.GET.dict()
        the_str = data.get('str', '')
        the_limit = data.get('limit', 0)

        the_list = _query_data(the_str, the_limit)

        return Response({"success": True, "data": the_list}, status=status.HTTP_200_OK)


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


def _query_data(the_str, the_limit):
    cfg.logger.debug('the_str: (%s, %s), the_limit: (%s, %s)', the_str, the_str.__class__.__name__, the_limit, the_limit.__class__.__name__)

    db_results = []
    query = {} if not the_str else {"$regex": "/" + the_str + "/"}
    for idx in ["name", "en_name", "indication", "permit"]:
        each_db_result_it = util.db_find_it('f6a_tw_backend', {idx: query})
        if the_limit:
            each_db_result_it = each_db_result_it.limit(the_limit)
        db_results += list(each_db_result_it)

    if the_limit:
        db_results = db_results[:the_limit]

    cfg.logger.debug('the_str: %s the_limit: %s db_results: %s', the_str, the_limit, len(db_results))

    return db_results


def _get_data(request):
    data = {}
    try:
        data = request.DATA
    except Exception as e:
        cfg.logger.error('unable to get request.DATA: e: %s', e)
        data = request.POST.dict()

    return data
