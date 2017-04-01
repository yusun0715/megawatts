# -*- coding: utf-8 -*-
# pylint: disable=too-many-instance-attributes
from datetime import date

from django.test import TestCase

from rest_framework.test import APIClient

from megawatts.storage import MegaSiteDjangoStorage, MegaSiteDetailDjangoStorage
from megawatts.logic import MegaSiteLogic


class TestView(TestCase):

    site_storage = MegaSiteDjangoStorage()
    site_detail_storage = MegaSiteDetailDjangoStorage()

    logic = MegaSiteLogic(
        site_storage=site_storage,
        site_detail_storage=site_detail_storage
    )

    def setUp(self):
        self.site_storage.wipe()
        self.site_detail_storage.wipe()

        self.api_client = APIClient()

    def tearDown(self):
        super(TestCase, self).tearDown()

    def test_get_site_list(self):
        test_data = {
            'site_name': 'ABC',
        }

        site_id = self.logic.create_site(**test_data)['id']

        response = self.api_client.get(
            '/sites',
        )

        self.assertEqual(response.status_code, 200)
        actual = response.data['sites']

        test_data['id'] = site_id

        expected = test_data
        self.assertListEqual(actual, [expected])

    def test_get_site_detail(self):
        test_data = {
            'site_name': 'ABC',
        }

        site_id = self.logic.create_site(**test_data)['id']

        test_site_detail = {
            'date': date(2015, 3, 21),
            'a_value': 15,
            'b_value': 43,
            'site_id': site_id
        }

        site_detail_id = self.logic.create_site_detail(**test_site_detail)['id']

        response = self.api_client.get(
            '/sites/{}'.format(site_id),
        )

        self.assertEqual(response.status_code, 200)
        actual = response.data['site_details']

        test_site_detail['id'] = site_detail_id
        test_site_detail['site_name'] = 'ABC'
        del test_site_detail['site_id']

        expected = test_site_detail
        self.assertListEqual(actual, [expected])
