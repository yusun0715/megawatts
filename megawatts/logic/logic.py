# -*- coding: utf-8 -*-
from __future__ import division

from collections import Counter, defaultdict
import logging


logger = logging.getLogger('megasite')


class MegaSiteLogic(object):

    def __init__(self, site_storage, site_detail_storage):
        self.site_storage = site_storage
        self.site_detail_storage = site_detail_storage

    def create_site(
        self,
        site_name,

    ):
        site = self.site_storage.persist_site(site_name=site_name)
        return site

    def create_site_detail(
        self,
        site_id,
        date,
        a_value,
        b_value
    ):
        site_detail = self.site_detail_storage.persist_site_detail(
            site_id=site_id,
            date=date,
            a_value=a_value,
            b_value=b_value
        )
        return site_detail

    def get_site_details(self, site_id):
        """ Return site details for a particular site

        Args:
            site_id: (int): The ID of the site to be retrieved.

        Returns:
            list: A list representation of site details
        """
        return self.site_detail_storage.retrieve_site_details(
            site_ids=[site_id]
        )

    def get_sites(
        self,
        ids=None,
        site_names=None,
        limit=20,
        offset=0
    ):
        """ Retrieve Site Information, filtering based on passed in parameters

        Args:
            ids (:obj:`list`, optional): A list of IDs of MegaSites to be
                returned.
            site_names (:obj:`list`, optional): A list of Site Names of MegaSites
                to be returned
            limit (:obj:`int`, optional): The number of megasites to be
                returned. Default is 20
            offset (:obj:`int`, optional): Used in paginating the retrieval of
                megasites.

        Returns:
            list: A list representation of sites

        """
        return self.site_storage.retrieve_sites(
            ids=ids,
            site_names=site_names,
            limit=limit,
            offset=offset
        )

    def get_sum_through_django_orm(self):
        """ Return the sum results of all sites through
        Django ORM query

        """
        return self.site_detail_storage.retrieve_site_details(
            is_sum=True
        )

    def get_avg_through_django_orm(self):
        """ Return the average results of all sites through
        Django ORM query

        """
        return self.site_detail_storage.retrieve_site_details(
            is_avg=True
        )

    def _get_summary_data(self):
        sites, _ = self.site_detail_storage.retrieve_site_details()

        # Pure python library, additional optimisation and no overhead
        sites_summary = defaultdict(Counter)

        for site in sites:
            sites_summary[site['site_name']].update(
                a_value=site['a_value'],
                b_value=site['b_value'],
                counter=1
            )
        return sites_summary

    def get_sum_through_python(self):
        """Return the sum results of all sites through Python
        calculations

        """
        sites = self._get_summary_data()
        return [
            {
                'site_name': key,
                'a_value': float("{0:.2f}".format(value['a_value'])),
                'b_value': float("{0:.2f}".format(value['b_value']))
            } for key, value in sites.items()
        ], len(sites)

    def get_avg_through_python(self):
        """Return the average results of all sites through Python
        calculations

        """
        sites = self._get_summary_data()
        return [
            {
                'site_name': key,
                'a_value': float("{0:.2f}".format(
                    value['a_value']/value['counter'])
                ),
                'b_value': float("{0:.2f}".format(
                    value['b_value']/value['counter'])
                ),
            } for key, value in sites.items()
        ], len(sites)
