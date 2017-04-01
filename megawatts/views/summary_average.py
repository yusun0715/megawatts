# -*- coding: utf-8 -*-
import logging

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response

from megawatts.injection_setup import site_logic

logger = logging.getLogger(__name__)


class SummaryAverageSerializer(serializers.Serializer):

    site_name = serializers.CharField(max_length=255)

    a_value = serializers.FloatField()
    b_value = serializers.FloatField()


class SummaryAverage(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    http_method_names = [
        'get',
    ]
    template_name = "summary-average.html"

    def list(self, request):
        #sites, count = site_logic.get_avg_through_django_orm()
        sites, count = site_logic.get_avg_through_python()

        serialized_sites = SummaryAverageSerializer(sites, many=True)
        return Response({'site_averages': sites})
