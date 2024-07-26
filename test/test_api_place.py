#!/usr/bin/python3
import json
import unittest

from api.api_place import app, data_manager
from model.amenities import Amenities
from model.city import City


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Create test data for city and amenities
        self.city = City(name="Test City", population=1000000, country_code="US")
        data_manager.save(self.city)

        self.amenity1 = Amenities(name="WiFi", place="apartmen")
        self.amenity2 = Amenities(name="Parking", place="Basement")
        data_manager.save(self.amenity1)
        data_manager.save(self.amenity2)

    def tearDown(self):
        # Clear the data manager storage
        data_manager.storage = {}

    def test_create_place(self):
        place_data = {
            "name": "Beautiful Beach House",
            "description": "A lovely house by the beach.",
            "address": "123 Ocean Drive",
            "city_id": self.city.id,
            "latitude": 34.0194,
            "longitude": -118.4912,
            "host_id": "host_uuid_123",
            "number_of_rooms": 3,
            "number_of_bathrooms": 2,
            "price_per_night": 150.00,
            "max_guests": 6,
            "amenity_ids": [self.amenity1.id, self.amenity2.id]
        }
        response = self.app.post('/places', data=json.dumps(place_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertIn('id', data)
        self.assertEqual(data['name'], "Beautiful Beach House")

    def test_get_places(self):
        place_data = {
            "name": "Beautiful Beach House",
            "description": "A lovely house by the beach.",
            "address": "123 Ocean Drive",
            "city_id": self.city.id,
            "latitude": 34.0194,
            "longitude": -118.4912,
            "host_id": "host_uuid_123",
            "number_of_rooms": 3,
            "number_of_bathrooms": 2,
            "price_per_night": 150.00,
            "max_guests": 6,
            "amenity_ids": [self.amenity1.id, self.amenity2.id]
        }
        self.app.post('/places', data=json.dumps(place_data), content_type='application/json')

        response = self.app.get('/places')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], "Beautiful Beach House")

    def test_get_place(self):
        place_data = {
            "name": "Beautiful Beach House",
            "description": "A lovely house by the beach.",
            "address": "123 Ocean Drive",
            "city_id": self.city.id,
            "latitude": 34.0194,
            "longitude": -118.4912,
            "host_id": "host_uuid_123",
            "number_of_rooms": 3,
            "number_of_bathrooms": 2,
            "price_per_night": 150.00,
            "max_guests": 6,
            "amenity_ids": [self.amenity1.id, self.amenity2.id]
        }
        post_response = self.app.post('/places', data=json.dumps(place_data), content_type='application/json')
        place_id = json.loads(post_response.data.decode())['id']

        response = self.app.get(f'/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data['id'], place_id)
        self.assertEqual(data['name'], "Beautiful Beach House")

    def test_update_place(self):
        place_data = {
            "name": "Beautiful Beach House",
            "description": "A lovely house by the beach.",
            "address": "123 Ocean Drive",
            "city_id": self.city.id,
            "latitude": 34.0194,
            "longitude": -118.4912,
            "host_id": "host_uuid_123",
            "number_of_rooms": 3,
            "number_of_bathrooms": 2,
            "price_per_night": 150.00,
            "max_guests": 6,
            "amenity_ids": [self.amenity1.id, self.amenity2.id]
        }
        post_response = self.app.post('/places', data=json.dumps(place_data), content_type='application/json')
        place_id = json.loads(post_response.data.decode())['id']

        updated_data = {
            "name": "Updated Beach House",
            "description": "An updated lovely house by the beach.",
            "address": "123 New Ocean Drive",
            "city_id": self.city.id,
            "latitude": 34.0194,
            "longitude": -118.4912,
            "host_id": "host_uuid_123",
            "number_of_rooms": 4,
            "number_of_bathrooms": 3,
            "price_per_night": 200.00,
            "max_guests": 8,
            "amenity_ids": [self.amenity1.id, self.amenity2.id]
        }

        response = self.app.put(f'/places/{place_id}', data=json.dumps(updated_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data['name'], "Updated Beach House")
        self.assertEqual(data['number_of_rooms'], 4)
        self.assertEqual(data['price_per_night'], 200.00)

    def test_delete_place(self):
        place_data = {
            "name": "Beautiful Beach House",
            "description": "A lovely house by the beach.",
            "address": "123 Ocean Drive",
            "city_id": self.city.id,
            "latitude": 34.0194,
            "longitude": -118.4912,
            "host_id": "host_uuid_123",
            "number_of_rooms": 3,
            "number_of_bathrooms": 2,
            "price_per_night": 150.00,
            "max_guests": 6,
            "amenity_ids": [self.amenity1.id, self.amenity2.id]
        }
        post_response = self.app.post('/places', data=json.dumps(place_data), content_type='application/json')
        place_id = json.loads(post_response.data.decode())['id']

        response = self.app.delete(f'/places/{place_id}')
        self.assertEqual(response.status_code, 204)

        get_response = self.app.get(f'/places/{place_id}')
        self.assertEqual(get_response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
