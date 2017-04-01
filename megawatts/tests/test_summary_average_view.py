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

    def test_get_site_summary(self):
        site_data_1 = self.logic.create_site('A')['id']

        test_data_1 = {
            'site_id': site_data_1,
            'date': date(2015, 3, 21),
            'a_value': 15,
            'b_value': 43
        }
        test_data_2 = {
            'site_id': site_data_1,
            'date': date(2015, 3, 22),
            'a_value': 3,
            'b_value': 2
        }
        test_data_3 = {
            'site_id': site_data_1,
            'date': date(2015, 3, 24),
            'a_value': 2,
            'b_value': 2
        }

        self.logic.create_site_detail(**test_data_1)
        self.logic.create_site_detail(**test_data_2)
        self.logic.create_site_detail(**test_data_3)

        site_data_2 = self.logic.create_site('B')['id']
        test_data_4 = {
            'site_id': site_data_2,
            'date': date(2015, 3, 21),
            'a_value': 67,
            'b_value': 43
        }
        test_data_5 = {
            'site_id': site_data_2,
            'date': date(2015, 3, 22),
            'a_value': 6,
            'b_value': 23
        }
        test_data_6 = {
            'site_id': site_data_2,
            'date': date(2015, 3, 24),
            'a_value': 23,
            'b_value': 2
        }

        self.logic.create_site_detail(**test_data_4)
        self.logic.create_site_detail(**test_data_5)
        self.logic.create_site_detail(**test_data_6)

        response = self.api_client.get(
            '/summary-average',
        )

        self.assertEqual(response.status_code, 200)
        actual = response.data['site_averages']
        actual = sorted(actual, key=lambda k: k['site_name'])

        expected = [
            {
                'site_name': 'A',
                'a_value': 6.67,
                'b_value': 15.67
            },
            {
                'site_name': 'B',
                'a_value': 32,
                'b_value': 22.67
            }
        ]

        self.assertListEqual(actual, expected)
