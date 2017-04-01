# -*- coding: utf-8 -*-
# pylint: disable=too-many-instance-attributes
from datetime import date

from django.test import TestCase

from megawatts.storage import MegaSiteDjangoStorage, MegaSiteDetailDjangoStorage
from megawatts.logic import MegaSiteLogic


class TestLogic(TestCase):

    site_storage = MegaSiteDjangoStorage()
    site_detail_storage = MegaSiteDetailDjangoStorage()

    logic = MegaSiteLogic(
        site_storage=site_storage,
        site_detail_storage=site_detail_storage
    )

    def assertDictsEqual(self, dic_1, dic_2):
        for key in dic_2:
            self.assertEqual(
                dic_1[key],
                dic_2[key],
                '%s: %s != %s (%s, %s)' % (
                    key,
                    dic_1[key],
                    dic_2[key],
                    type(dic_1[key]),
                    type(dic_2[key]),
                )
            )

    def setUp(self):
        self.site_storage.wipe()
        self.site_detail_storage.wipe()

    def tearDown(self):
        self.site_storage.wipe()
        self.site_detail_storage.wipe()

    def test_create_and_get_sites(self):
        test_data = {
            'site_name': 'ABC'
        }

        created_site = self.logic.create_site(**test_data)
        fetched_site, count = self.logic.get_sites()

        self.assertEqual(count, 1)

        del created_site['id']
        del fetched_site[0]['id']

        self.assertDictEqual(fetched_site[0], test_data)
        self.assertDictEqual(created_site, test_data)

    def test_create_and_get_site_details(self):
        site_data = self.logic.create_site(site_name='ABC')

        test_data = {
            'site_id': site_data['id'],
            'date': date(2015, 3, 22),
            'a_value': 3,
            'b_value': 2
        }

        site_detail = self.logic.create_site_detail(**test_data)

        site_details, count = self.logic.get_site_details(site_id=site_data['id'])

        self.assertEqual(count, 1)

        del test_data['site_id']
        test_data['site_name'] = site_data['site_name']

        del site_detail['id']
        del site_details[0]['id']

        self.assertDictsEqual(site_detail, test_data)
        self.assertDictsEqual(site_details[0], test_data)

    def test_get_summary(self):
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

        sum_from_django, _ = self.logic.get_sum_through_django_orm()
        sum_from_django = sorted(sum_from_django, key=lambda k: k['site_name'])

        sum_from_python, _ = self.logic.get_sum_through_python()
        sum_from_python = sorted(sum_from_python, key=lambda k: k['site_name'])

        expected = [
            {
                'site_name': 'A',
                'a_value': 20,
                'b_value': 47
            },
            {
                'site_name': 'B',
                'a_value': 96,
                'b_value': 68
            }
        ]

        self.assertListEqual(sum_from_django, expected)
        self.assertListEqual(sum_from_python, expected)

    def test_get_summary_average(self):
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

        avg_from_django, _ = self.logic.get_avg_through_django_orm()
        avg_from_django = sorted(avg_from_django, key=lambda k: k['site_name'])

        avg_from_python, _ = self.logic.get_avg_through_python()
        avg_from_python = sorted(avg_from_python, key=lambda k: k['site_name'])

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

        self.assertListEqual(avg_from_python, expected)
        self.assertListEqual(avg_from_django, expected)
