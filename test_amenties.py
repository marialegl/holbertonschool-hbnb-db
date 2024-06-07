import unittest
from datetime import datetime
from amenities import Amenities
import time

class TestAmenities(unittest.TestCase):

    def test_initialization(self):
        amenity = Amenities(name="Pool", place="Hotel")
        self.assertEqual(amenity.name, "Pool")
        self.assertEqual(amenity.place, "Hotel")
        self.assertIsNotNone(amenity.id)
        self.assertIsInstance(amenity.created_at, datetime)
        self.assertIsInstance(amenity.updated_at, datetime)

    def test_initialization_with_id(self):
        amenity = Amenities(id="1234", name="Pool", place="Hotel")
        self.assertEqual(amenity.id, "1234")
        self.assertEqual(amenity.name, "Pool")
        self.assertEqual(amenity.place, "Hotel")

    def test_update(self):
        amenity = Amenities(name="Pool", place="Hotel")
        old_updated_at = amenity.updated_at
        time.sleep(1)
        amenity.update(name="Gym", place="Resort")
        self.assertEqual(amenity.name, "Gym")
        self.assertEqual(amenity.place, "Resort")
        self.assertGreater(amenity.updated_at, old_updated_at)

    def test_str_representation(self):
        amenity = Amenities(name="Pool", place="Hotel")
        expected_str = f"Amenity(ID: {amenity.id}, Name: {amenity.name}, Place: {amenity.place}, Created: {amenity.created_at}, Last Updated: {amenity.updated_at})"
        self.assertEqual(str(amenity), expected_str)

if __name__ == '__main__':
    unittest.main()
