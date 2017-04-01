# -*- coding: utf-8 -*-
import unittest

from megawatts.storage import MegaSiteDjangoStorage, MegaSitePureMemoryStorage


class _CheckStorage(object):

    def setUp(self):
        self.storage.wipe()

    def tearDown(self):
        self.storage.wipe()

    def assertIDsEqual(self, result_list, expected_ids):
        actual_ids = [r['id'] for r in result_list]
        self.assertEqual(
            set(actual_ids),
            set(expected_ids),
        )

    def test_site_persisted_correctly(self):
        test_data = {
            "site_name": "ABC"
        }

        actual = self.storage.persist_site(**test_data)
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
        site_1_id = self.storage.persist_site(site_name='A')['id']
        self.storage.persist_site(site_name='B')

        actual, _ = self.storage.retrieve_sites(ids=[site_1_id])
        self.assertIDsEqual(actual, [site_1_id])

    def test_get_sites_by_site_name(self):
        site_1_id = self.storage.persist_site(site_name='A')['id']
        self.storage.persist_site(site_name='B')

        actual, _ = self.storage.retrieve_sites(site_names=['A'])
        self.assertIDsEqual(actual, [site_1_id])

    def get_limit_and_offset(self):
        self.storage.persist_site(site_name='A')
        site_2_id = self.storage.persist_site(site_name='B')['id']
        site_3_id = self.storage.persist_site(site_name='C')['id']

        actual, _ = self.storage.retrieve_sites(
            offset=1,
            limit=2
        )
        self.assertIDsEqual(actual, [site_2_id, site_3_id])


class TestMemoryStorage(_CheckStorage, unittest.TestCase):
    storage = MegaSitePureMemoryStorage()


class TestDjangoStorage(_CheckStorage, unittest.TestCase):
    storage = MegaSiteDjangoStorage()

    def setUp(self):
        super(TestDjangoStorage, self).setUp()

    def tearDown(self):
        super(TestDjangoStorage, self).tearDown()