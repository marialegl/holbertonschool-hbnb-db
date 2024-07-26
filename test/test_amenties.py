#!/usr/bin/python3
"""Unittest for Amenities"""

import time
import unittest
from datetime import datetime

from model.amenities import Amenities


class TestAmenities(unittest.TestCase):

    def test_initialization(self):
        amenity = Amenities(name="Pool", place="Hotel")
        self.assertEqual(amenity.name, "Pool")
        self.assertEqual(amenity.place, "Hotel")
        self.assertIsNotNone(amenity.id)
        self.assertIsInstance(amenity.create_time, datetime)
        self.assertIsInstance(amenity.update_time, datetime)

    def test_initialization_with_id(self):
        amenity = Amenities(name="Pool", place="Hotel")
        self.assertEqual(amenity.name, "Pool")
        self.assertEqual(amenity.place, "Hotel")

    def test_update(self):
        amenity = Amenities(name="Pool", place="Hotel")
        old_update_time = amenity.update_time
        time.sleep(1)
        amenity.update(name="Gym", place="Resort")
        self.assertEqual(amenity.name, "Gym")
        self.assertEqual(amenity.place, "Resort")
        self.assertGreater(amenity.update_time, old_update_time)

    def test_str_representation(self):
        amenity = Amenities(name="Pool", place="Hotel")
        expected_str = f"Amenity(ID: {amenity.id}, Name: {amenity.name}, Place: {amenity.place}, Created: {amenity.create_time}, Last Updated: {amenity.update_time})"
        self.assertEqual(str(amenity), expected_str)


if __name__ == '__main__':
    unittest.main()
