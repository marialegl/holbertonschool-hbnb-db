#!/usr/bin/python3
"""Unittest for City"""

import unittest
from datetime import datetime

from model.city import City


class TestCity(unittest.TestCase):

    def setUp(self):
        self.city = City(name="New York", state="New York", place="Manhattan")

    def test_initialization(self):
        self.assertEqual(self.city.name, "New York")
        self.assertEqual(self.city.state, "New York")
        self.assertEqual(self.city.place, "Manhattan")
        self.assertIsInstance(self.city.id, str)
        self.assertIsInstance(self.city.update_time, datetime)
        self.assertIsInstance(self.city.create_time, datetime)

    def test_update(self):
        self.city.update(name="Los Angeles", state="California")
        self.assertEqual(self.city.name, "Los Angeles")
        self.assertEqual(self.city.state, "California")
        self.assertNotEqual(self.city.update_time, self.city.create_time)

    def test_add_place(self):
        initial_update_time = self.city.update_time
        self.city.add_place("Brooklyn")
        self.assertIn("Brooklyn", self.city.place)
        self.assertNotEqual(self.city.update_time, initial_update_time)

    def test_remove_place(self):
        self.city.add_place("Brooklyn")
        self.city.remove_place("Manhattan")
        self.assertNotIn("Manhattan", self.city.place)
        self.assertIn("Brooklyn", self.city.place)

        # Test removing a place that does not exist
        self.city.remove_place("Queens")
        self.assertNotIn("Queens", self.city.place)

    def test_str_method(self):
        str_output = str(self.city)
        self.assertIn("City: New York", str_output)
        self.assertIn("State: New York", str_output)
        self.assertIn("Place(s): Manhattan", str_output)


if __name__ == '__main__':
    unittest.main()
