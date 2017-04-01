# -*- coding: utf-8 -*-
import unittest

from megawatts.storage import (
    MegaSiteDetailDjangoStorage,
    MegaSiteDetailPureMemoryStorage,
    MegaSiteDjangoStorage,
    MegaSitePureMemoryStorage
)


class _CheckStorage(object):

    def setUp(self):
        self.storage.wipe()
        self.site_storage.wipe()

    def tearDown(self):
        self.storage.wipe()
        self.site_storage.wipe()

    def assertIDsEqual(self, result_list, expected_ids):
        actual_ids = [r['id'] for r in result_list]
        self.assertEqual(
            set(actual_ids),
            set(expected_ids),
        )

    def test_site_detail_persisted_correctly(self):
        site_id = self.site_storage.persist_site("ABC")['id']

        test_data = {
            "site_name": "ABC",
            "site_id": site_id,
            "date": "2015-02-13",
            "a_value": 15,
            "b_value": 30
        }

        actual = self.storage.persist_site_detail(**test_data)
        del test_data['site_id']
        expected = test_data

        self.assertTrue(isinstance(actual['id'], int))
        del actual['id']
        for key in expected:
            actual_value = actual[key]
            expected_value = expected[key]
            self.assertEqual(
                actual_value,
                expected_value,
                '%s: %s != %s (%s, %s)' % (
                    key,
                    actual_value,
                    expected_value,
                    type(actual_value),
                    type(expected_value),
                )
            )

    def test_get_sites_by_id(self):
        site_data_1 = self.site_storage.persist_site("A")['id']
        site_data_2 = self.site_storage.persist_site("B")['id']

        test_data_1 = {
            "site_name": "A",
            "site_id": site_data_1,
            "date": "2015-02-13",
            "a_value": 15,
            "b_value": 30
        }

        site_1_id = self.storage.persist_site_detail(**test_data_1)['id']

        test_data_2 = {
            "site_name": "B",
            "site_id": site_data_2,
            "date": "2015-02-14",
            "a_value": 15,
            "b_value": 30
        }
        self.storage.persist_site_detail(**test_data_2)

        actual, _ = self.storage.retrieve_site_details(site_ids=[site_data_1])
        self.assertIDsEqual(actual, [site_1_id])

    def test_get_sites_summary(self):
        site_data_1 = self.site_storage.persist_site("A")['id']
        site_data_2 = self.site_storage.persist_site("B")['id']

        test_data_1 = {
            "site_name": "A",
            "site_id": site_data_1,
            "date": "2015-02-13",
            "a_value": 15,
            "b_value": 30
        }
        test_data_2 = {
            "site_name": "A",
            "site_id": site_data_1,
            "date": "2015-02-15",
            "a_value": 14,
            "b_value": 32
        }
        self.storage.persist_site_detail(**test_data_1)
        self.storage.persist_site_detail(**test_data_2)

        test_data_3 = {
            "site_name": "B",
            "site_id": site_data_2,
            "date": "2015-02-13",
            "a_value": 5,
            "b_value": 3
        }
        test_data_4 = {
            "site_name": "B",
            "site_id": site_data_2,
            "date": "2015-02-15",
            "a_value": 4,
            "b_value": 2
        }
        self.storage.persist_site_detail(**test_data_3)
        self.storage.persist_site_detail(**test_data_4)

        expected_data_1 = {
            'site_name': 'A',
            'a_value': 14.5,
            'b_value': 31
        }
        expected_data_2 = {
            'site_name': 'B',
            'a_value': 4.5,
            'b_value': 2.5
        }
        actual, _ = self.storage.retrieve_site_details(is_avg=True)

        actual = sorted(actual, key=lambda k: k['site_name'])
        self.assertListEqual(actual, [expected_data_1, expected_data_2])

        expected_data_1 = {
            'site_name': 'A',
            'a_value': 29,
            'b_value': 62
        }
        expected_data_2 = {
            'site_name': 'B',
            'a_value': 9,
            'b_value': 5
        }
        actual, _ = self.storage.retrieve_site_details(is_sum=True)

        actual = sorted(actual, key=lambda k: k['site_name'])
        self.assertListEqual(actual, [expected_data_1, expected_data_2])


class TestMemoryStorage(_CheckStorage, unittest.TestCase):
    storage = MegaSiteDetailDjangoStorage()
    site_storage = MegaSiteDjangoStorage()


class TestDjangoStorage(_CheckStorage, unittest.TestCase):
    storage = MegaSiteDetailPureMemoryStorage()
    site_storage = MegaSitePureMemoryStorage()

    def setUp(self):
        super(TestDjangoStorage, self).setUp()

    def tearDown(self):
        super(TestDjangoStorage, self).tearDown()