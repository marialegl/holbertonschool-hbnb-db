#!/usr/bin/python3
"""Unittest for City Endpoints"""

import unittest
import json
from api.api_country_city import app, data_manager
from model.city import City

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        data_manager.storage = {}

    def test_get_countries(self):
        response = self.app.get('/countries')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/json', response.content_type)

    def test_get_country_by_code(self):
        response = self.app.get('/countries/US')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['iso_3166_1_alpha_2'], 'US')

    def test_get_country_by_code_not_found(self):
        response = self.app.get('/countries/XX')
        self.assertEqual(response.status_code, 404)

    def test_add_city(self):
        city_data = {
            "name": "Test City",
            "population": 1000000,
            "country_code": "US"
        }
        response = self.app.post('/cities', data=json.dumps(city_data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Test City')

    def test_add_city_duplicate(self):
        city_data = {
            "name": "Test City",
            "population": 1000000,
            "country_code": "US"
        }
        self.app.post('/cities', data=json.dumps(city_data), content_type='application/json')
        response = self.app.post('/cities', data=json.dumps(city_data), content_type='application/json')
        self.assertEqual(response.status_code, 409)

    def test_get_city_by_id(self):
        city = City(name="Test City", population=100000, country_code="US")
        data_manager.save(city)

        response = self.app.get(f'/cities/{city.id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['name'], 'Test City')

    def test_delete_city(self):
        city = City(name="Test City", population=100000, country_code="US")
        data_manager.save(city)

        response = self.app.delete(f'/cities/{city.id}')
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(data_manager.get(city.id, 'City'))

if __name__ == '__main__':
    unittest.main()
