#!/usr/bin/python3
"""Unittest for Place"""

import unittest
from datetime import datetime

from model.place import Place


class TestPlace(unittest.TestCase):

    def setUp(self):
        """Setup a default Place instance for testing."""
        self.place = Place(
            name="Test Place",
            description="A cozy place",
            address="123 Test St",
            city="Testville",
            latitude=34.05,
            longitude=-118.25,
            host=None,
            number_of_rooms=3,
            bathrooms=2,
            price_per_night=100,
            max_guests=4
        )

    def test_place_creation(self):
        """Test that a Place instance is created correctly."""
        self.assertEqual(self.place.name, "Test Place")
        self.assertEqual(self.place.city, "Testville")
        self.assertIsNotNone(self.place.id)
        self.assertIsInstance(self.place.create_time, datetime)
        self.assertIsInstance(self.place.update_time, datetime)

    def test_unique_host(self):
        """Test that a place can only have one host."""
        with self.assertRaises(ValueError):
            Place(
                name="Test Place 2",
                description="Another cozy place",
                address="456 Test Ave",
                city="Testville",
                latitude=34.05,
                longitude=-118.25,
                host="Existing Host",
                number_of_rooms=2,
                bathrooms=1,
                price_per_night=80,
                max_guests=2
            )

    def test_add_amenity(self):
        """Test adding amenities to a place."""
        self.place.add_amenity("WiFi")
        self.assertIn("WiFi", self.place.amenities)

    def test_remove_amenity(self):
        """Test removing amenities from a place."""
        self.place.add_amenity("WiFi")
        self.place.remove_amenity("WiFi")
        self.assertNotIn("WiFi", self.place.amenities)

    def test_update_attributes(self):
        """Test updating the attributes of a place."""
        self.place.update(name="Updated Place", price_per_night=150)
        self.assertEqual(self.place.name, "Updated Place")
        self.assertEqual(self.place.price_per_night, 150)

    def test_update_timestamp(self):
        """Test that the update_time timestamp is updated on attribute update."""
        previous_update_time = self.place.update_time
        self.place.update(name="Updated Place")
        self.assertNotEqual(self.place.update_time, previous_update_time)

    def test_place_str(self):
        """Test the string representation of the place."""
        self.assertEqual(str(self.place), f"Place({self.place.id}, Test Place, Testville, None)")


if __name__ == "__main__":
    unittest.main()
