# -*- coding: utf-8 -*-
from django.db import transaction, IntegrityError, DatabaseError

from lib.exceptions import DuplicationError
from megawatts.models import MegaSite


class MegaSiteDjangoStorage(object):
    """ This storage interacts with PostgreSQL database directly

    Only the retrieve_sites function is provided. More methods including
    create_sites can be added

    """

    def wipe(self):
        MegaSite.objects.all().delete()

    def persist_site(self, site_name):
        try:
            site = MegaSite.objects.create(
                site_name=site_name
            )
        except (IntegrityError, DatabaseError) as err:
            transaction.rollback()
            raise DuplicationError(str(err))
        return self._serialize_site(site)

    def _serialize_site(self, obj):
        return {
            'id': obj.id,
            'site_name': obj.site_name,
        }

    def retrieve_sites(
        self,
        ids=None,
        site_names=None,
        limit=20,
        offset=0
    ):
        sites = MegaSite.objects.all()

        if ids:
            sites = sites.filter(id__in=ids)

        if site_names:
            sites = sites.filter(site_name__in=site_names)

        return (
            [
                self._serialize_site(site)
                for site in sites[offset:offset+limit]
            ],
            sites.count()
        )


class MegaSitePureMemoryStorage(object):

    sites = []
    next_site_id = 1

    def wipe(self):
        self.sites = []

    def persist_site(
        self,
        site_name
    ):
        site = {
            "id": self.next_site_id,
            "site_name": site_name
        }
        self.sites.append(site)

        self.next_site_id += 1
        return site

    def retrieve_sites(
        self,
        ids=None,
        site_names=None,
        limit=20,
        offset=0
    ):

        sites = self.sites

        if ids:
            sites = [
                site for site in self.sites
                if site['id'] in ids
            ]

        if site_names:
            sites = [
                site for site in self.sites
                if site['site_name'] in site_names
            ]

        count = len(sites)
        return sites[offset:offset+limit], count
