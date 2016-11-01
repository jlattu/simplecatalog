import unittest
import catapp.catalog as catalog
from catapp.catalog import *


class TestStringMethods(unittest.TestCase):
    # When running these tests, it's expected that test data filler that catalog.py uses contains at least 100 products

    def test_opening_the_database_connection(self):
        resp = open_database_connection(catalog, testing=True)
        self.assertEqual(resp, "Connection to temporary database in memory opened")

    def test_adding_test_data(self):
        open_database_connection(catalog, testing=True)
        resp = populate_test_data()
        self.assertGreater(resp, 0)
        # When trying again, result won't be the same anymore as shirts exist already
        resp = populate_test_data()
        self.assertNotEqual(resp, 500)
        self.assertEqual(resp, 0)

    def test_getting_shirts(self):
        open_database_connection(catalog, testing=True)
        resp = get_shirts()
        self.assertEqual(len(resp), 0)
        resp = populate_test_data()
        self.assertGreater(resp, 99)

    def test_getting_total_count_of_shirts(self):
        open_database_connection(catalog, testing=True)
        populate_test_data()
        resp = get_shirt_count()
        self.assertGreater(resp, 99)

    def test_adding_new_shirt(self):
        open_database_connection(catalog, testing=True)
        resp = add_shirt("Lorem ipsum", "Blue", "XL", 5, 14)
        self.assertEqual(resp, 1)
        resp = add_shirt("Lorem ipsum", "Blue", "XL", 5, 14)
        self.assertEqual(resp, 2)

    def test_updating_a_shirt(self):
        open_database_connection(catalog, testing=True)
        add_shirt("Lorem ipsum", "Blue", "XL", 5, 14)
        resp = update_shirt(1, "Lorem ipsum", "Green", "XL", 5, 14)
        self.assertEqual(resp, 1)
        resp = update_shirt(-1, "Lorem ipsum de vitae", "Green", "XL", 5, 14)
        self.assertEqual(resp, 0)

    def test_deleting_a_shirt(self):
        open_database_connection(catalog, testing=True)
        shirt_id = add_shirt("Lorem ipsum", "Blue", "XL", 5, 14)
        resp = get_shirts()
        self.assertEqual(len(resp), 1)
        resp = delete_shirt(shirt_id)
        self.assertEqual(resp, 1)
        resp = get_shirts()
        self.assertEqual(len(resp), 0)

    def test_deleting_all_shirts(self):
        open_database_connection(catalog, testing=True)
        populate_test_data()
        shirt_count = get_shirt_count()
        self.assertGreater(shirt_count, 99)
        resp = delete_all_shirts()
        self.assertEqual(resp, shirt_count)


if __name__ == '__main__':
    unittest.main()