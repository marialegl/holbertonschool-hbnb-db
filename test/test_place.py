#!/usr/bin/python3
"""Unittest for Place"""

import unittest
from datetime import datetime
from model.place import Place


class TestPlace(unittest.TestCase):

    def setUp(self):
        """Setup a default Place instance for testing."""
        self.place = Place(
            id=None,
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
        self.assertIsInstance(self.place.created_at, datetime)
        self.assertIsInstance(self.place.updated_at, datetime)

    def test_unique_host(self):
        """Test that a place can only have one host."""
        with self.assertRaises(ValueError):
            Place(
                id=None,
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
        """Test that the updated_at timestamp is updated on attribute update."""
        previous_updated_at = self.place.updated_at
        self.place.update(name="Updated Place")
        self.assertNotEqual(self.place.updated_at, previous_updated_at)

    def test_place_str(self):
        """Test the string representation of the place."""
        self.assertEqual(str(self.place), f"Place({self.place.id}, Test Place, Testville, None)")

if __name__ == "__main__":
    unittest.main()
