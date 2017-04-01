# -*- coding: utf-8 -*-
import logging

from django.http import Http404

from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from megawatts.injection_setup import site_logic

logger = logging.getLogger(__name__)


class SiteSerializer(serializers.Serializer):

    resource_uri = serializers.SerializerMethodField()

    site_name = serializers.CharField(max_length=255)
    date = serializers.SerializerMethodField()

    a_value = serializers.SerializerMethodField()
    b_value = serializers.SerializerMethodField()

    def get_resource_uri(self, obj):
        if 'id' in obj:
            return '/sites/{0}'.format(obj['id'])
        else:
            return None

    def get_date(self, obj):
        return obj.get('date', None)

    def get_a_value(self, obj):
        return obj.get('a_value', None)

    def get_b_value(self, obj):
        return obj.get('b_value', None)


class Site(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]

    http_method_names = [
        'get',
    ]

    def list(self, request):
        Site.template_name = 'sites.html'

        sites, count = site_logic.get_sites()
        return Response({'sites':sites})

    def retrieve(self, request, pk=None):
        Site.template_name = 'site_details.html'

        try:
            site_id = int(pk)
        except ValueError:
            # Site ID was not an integer number.
            raise Http404

        sites_details, count = site_logic.get_site_details(
            site_id=site_id
        )

        return Response({'site_details':sites_details})

