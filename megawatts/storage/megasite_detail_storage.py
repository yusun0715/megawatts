# -*- coding: utf-8 -*-
from collections import Counter, defaultdict

from django.db import transaction, IntegrityError, DatabaseError
from django.db.models import Sum, Avg

from lib.exceptions import DuplicationError
from megawatts.models import MegaSiteDetail


class MegaSiteDetailDjangoStorage(object):
    """This storage interacts with PostgreSQL database directly

    Here only the method of retrieve_site_details is provided.
    More methods, such as create_site_details, update_site_details and
    delete_site_details can be easily added

    """

    SERIALIZATION_FUNCTION_MAPPING = {
        'SUM': '_serialize_aggregate',
        'AVG': '_serialize_aggregate',
        'OTHER': '_serialize_site_detail'
    }

    def wipe(self):
        MegaSiteDetail.objects.all().delete()

    def persist_site_detail(
        self,
        site_id,
        date,
        a_value,
        b_value,
        site_name=None
    ):
        try:
            site_detail = MegaSiteDetail.objects.create(
                site_id=site_id,
                date=date,
                a_value=a_value,
                b_value=b_value
            )
        except (IntegrityError, DatabaseError) as err:
            transaction.rollback()
            raise DuplicationError(str(err))
        return self._serialize_site_detail(site_detail)

    def _serialize_site_detail(self, obj):
        return {
            'id': obj.id,
            'date': obj.date,
            'site_name': obj.site.site_name,
            'a_value': float("{0:.2f}".format(obj.a_value)),
            'b_value': float("{0:.2f}".format(obj.b_value))
        }

    def _serialize_aggregate(self, obj):
        return {
            'site_name': obj['site__site_name'],
            'a_value': float("{0:.2f}".format(obj['a_value'])),
            'b_value': float("{0:.2f}".format(obj['b_value'])),
        }

    def retrieve_site_details(
        self,
        site_ids=None,
        is_sum=False,
        is_avg=False
    ):
        serialization_type = 'OTHER'
        if is_sum:

            # Get the sum values for all sites using Django ORM
            site_details = MegaSiteDetail.objects.values(
                'site__site_name'
            ).annotate(
                a_value=Sum('a_value')
            ).annotate(
                b_value=Sum('b_value')
            )
            serialization_type = 'SUM'

        elif is_avg:

            # Get the average values for all sites using Django ORM
            site_details = MegaSiteDetail.objects.values(
                'site__site_name'
            ).annotate(
                a_value=Avg('a_value')
            ).annotate(
                b_value=Avg('b_value')
            )
            serialization_type = 'AVG'

        else:
            site_details = MegaSiteDetail.objects.all()
            if site_ids:
                site_details = site_details.filter(site__in=site_ids)

        func_name = self.SERIALIZATION_FUNCTION_MAPPING[serialization_type]
        function = getattr(self, func_name)

        return (
            [
                function(site_detail)
                for site_detail in site_details
            ],
            site_details.count()
        )


class MegaSiteDetailPureMemoryStorage(object):

    site_details = []
    next_site_detail_id = 1

    def wipe(self):
        self.site_details = []

    def persist_site_detail(
        self,
        date,
        a_value,
        b_value,
        site_name,
        site_id
    ):

        site_detail = {
            'id': self.next_site_detail_id,
            'date': date,
            'a_value': a_value,
            'b_value': b_value,
            'site_name': site_name,
            'site_id': site_id
        }

        self.site_details.append(site_detail)
        self.next_site_detail_id += 1

        return site_detail

    def retrieve_site_details(
        self,
        site_ids=None,
        is_sum=False,
        is_avg=False
    ):
        if is_sum:
            sites_summary = defaultdict(Counter)
            for site in self.site_details:
                sites_summary[site['site_name']].update(
                    a_value=site['a_value'],
                    b_value=site['b_value'],
                    counter=1
                )
            return [
                {
                    'site_name': key,
                    'a_value': float("{0:.2f}".format(value['a_value'])),
                    'b_value': float("{0:.2f}".format(value['b_value']))
                } for key, value in sites_summary.items()
            ], len(sites_summary)

        elif is_avg:
            sites_summary = defaultdict(Counter)
            for site in self.site_details:
                sites_summary[site['site_name']].update(
                    a_value=site['a_value'],
                    b_value=site['b_value'],
                    counter=1
                )
            return [
                {
                    'site_name': key,
                    'a_value': float("{0:.2f}".format(value['a_value']/value['counter'])),
                    'b_value': float("{0:.2f}".format(value['b_value']/value['counter']))
                } for key, value in sites_summary.items()
            ], len(sites_summary)

        else:
            site_details = self.site_details

            if site_ids:
                site_details = [
                    site_detail for site_detail in site_details
                    if site_detail['site_id'] in site_ids
                ]
            for site_detail in site_details:
                del site_detail['site_id']

            return site_details, len(site_details)
