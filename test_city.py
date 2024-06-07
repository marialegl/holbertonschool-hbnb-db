import unittest
from datetime import datetime
from city import City 

class TestCity(unittest.TestCase):

    def setUp(self):
        self.city = City(name="New York", country="USA", place="Manhattan")

    def test_initialization(self):
        self.assertEqual(self.city.name, "New York")
        self.assertEqual(self.city.country, "USA")
        self.assertEqual(self.city.place, "Manhattan")
        self.assertIsInstance(self.city.id, str)
        self.assertIsInstance(self.city.updated_at, datetime)

    def test_update(self):
        self.city.update(name="Los Angeles", country="USA")
        self.assertEqual(self.city.name, "Los Angeles")
        self.assertEqual(self.city.country, "USA")
        self.assertNotEqual(self.city.updated_at, self.city.created_at)

    def test_add_place(self):
        initial_updated_at = self.city.updated_at
        self.city.add_place("Brooklyn")
        self.assertIn("Brooklyn", self.city.place)
        self.assertNotEqual(self.city.updated_at, initial_updated_at)

    def test_remove_place(self):
        self.city.add_place("Brooklyn")
        self.city.remove_place("Manhattan")
        self.assertNotIn("Manhattan", self.city.place)
        self.assertIn("Brooklyn", self.city.place)
        
        # Test removing a place that does not exist
        self.city.remove_place("Queens")
        self.assertNotIn("Queens", self.city.place)

    def test_str_method(self):
        self.assertIn("City: New York", str(self.city))
        self.assertIn("Country: USA", str(self.city))
        self.assertIn("Place(s): Manhattan", str(self.city))


if __name__ == '__main__':
    unittest.main()
