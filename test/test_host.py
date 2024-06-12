#!/usr/bin/python3
"""Unittest for Host"""

import unittest
from datetime import datetime
from model.users import Users, Host


class TestHost(unittest.TestCase):

    def setUp(self):
        Users.existing_email.clear()
        self.host = Host("2", "Alice", "Smith",
                         "alice.smith@example.com", "password123")

    def test_create_host(self):
        self.assertEqual(self.host.id, "2")
        self.assertEqual(self.host.First_name, "Alice")
        self.assertEqual(self.host.Last_name, "Smith")
        self.assertEqual(self.host.email, "alice.smith@example.com")
        self.assertEqual(self.host.password, "password123")
        self.assertIsInstance(self.host.create_time, datetime)
        self.assertIsInstance(self.host.update_time, datetime)

    def test_add_place(self):
        self.host.add_place("Beach House")
        self.assertIn("Beach House", self.host.name_place)

    def test_remove_place(self):
        self.host.add_place("Beach House")
        self.host.remove_place("Beach House")
        self.assertNotIn("Beach House", self.host.name_place)

    def test_add_amenities(self):
        self.host.add_amenities("Pool")
        self.assertIn("Pool", self.host.amenities)

    def test_remove_amenities(self):
        self.host.add_amenities("Pool")
        self.host.remove_amenities("Pool")
        self.assertNotIn("Pool", self.host.amenities)


if __name__ == "__main__":
    unittest.main()
