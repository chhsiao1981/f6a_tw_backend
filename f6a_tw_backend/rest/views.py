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
        the_limit = util._int(data.get('limit', 100))

        the_list = _query_data(the_str, the_limit)

        return Response({"success": True, "data": the_list}, status=status.HTTP_200_OK)


class MockQueryView(APIView):
    def get(self, request, format=None):
        data = request.GET.dict()
        the_str = data.get('str', '')
        the_limit = util._int(data.get('limit', 100))

        the_list = [
            {
                "color": "",
                "main_gradient": "N-ALKYO DIMETHYL BENZYL AMMONIUM CHLOREDE",
                "customs_no": "DHA00201429907",
                "process_address": "8316 WEST ROUTE 24, MAPLETON, ILLINOIS 61547 USA",
                "formulation": "原料藥溶液劑",
                "package2": "０．５公斤以上",
                "valid_date": "2014-12-16",
                "special": "",
                "size": "",
                "process_company": "LONZA INC.",
                "issue_date": "1995-01-16",
                "mark": "",
                "is_valid": "",
                "old_permit": "02009575",
                "usage": "",
                "indication": "消毒、殺菌",
                "type": "製劑原料",
                "process_company_country": "UNITED STATES",
                "invalidate_reason": "",
                "en_name": "HYAMINE 3500-(50%)",
                "apply_company": "國偉貿易有限公司",
                "apply_address": "台北市中山區松江路２９３號３樓３１１室",
                "memo2": "",
                "memo1": "",
                "name": "海亞敏３５００－５０％",
                "intl_id": "",
                "controlled_type": "",
                "invalidate_date": "",
                "package": "０．５公斤以上",
                "insurance_id": "",
                "smell": "",
                "process_company_address": "17-17 ROUTE 208, FAIR LAWN, N.J. 07410, USA",
                "permit_type": "原料藥",
                "apply_id": "30011460",
                "permit": "衛署藥輸字第014299號",
                "change_date": "2009-11-26",
                "procedure": "",
                "view": ""
            },
            {
                "color": "",
                "main_gradient": "N-ALKYO DIMETHYL BENZYL AMMONIUM CHLOREDE",
                "customs_no": "DHA00201430005",
                "process_address": "22-10 ROUTE 208, FAIR LAWN N.J. 07410",
                "formulation": "原料藥溶液劑",
                "package2": "０．５公斤以上",
                "valid_date": "2014-01-06",
                "special": "",
                "size": "",
                "process_company": "LONZA INC.",
                "issue_date": "1994-01-27",
                "mark": "",
                "is_valid": "",
                "old_permit": "02005461",
                "usage": "",
                "indication": "消毒、殺菌。",
                "type": "製劑原料",
                "process_company_country": "UNITED STATES",
                "invalidate_reason": "",
                "en_name": "HYAMINE 3500-(80%) CONCENTRATE",
                "apply_company": "國偉貿易有限公司",
                "apply_address": "台北市中山區松江路２９３號３樓３１１室",
                "memo2": "",
                "memo1": "",
                "name": "龍查 海亞敏３５００－８０％",
                "intl_id": "",
                "controlled_type": "",
                "invalidate_date": "",
                "package": "０．５公斤以上",
                "insurance_id": "",
                "smell": "",
                "process_company_address": "",
                "permit_type": "原料藥",
                "apply_id": "30011460",
                "permit": "衛署藥輸字第014300號",
                "change_date": "2008-12-29",
                "procedure": "",
                "view": ""
            },
        ]

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
    for idx in ["name", "en_name", "indication", "permit"]:
        query = {} if not the_str else {idx: {"$regex": the_str}}
        each_db_result = util.db_find('f6a_tw_backend', query)
        cfg.logger.debug('after db_find_it: idx: %s query: %s', idx, query)
        if the_limit:
            each_db_result = each_db_result[:the_limit]
        cfg.logger.debug('to list: idx: %s query: %s', idx, query)
        db_results += each_db_result
        cfg.logger.debug('after list: idx: %s query: %s', idx, query)

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
