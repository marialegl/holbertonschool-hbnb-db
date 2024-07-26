#!/usr/bin/python3
"""Unittest for Amenities Endpoints"""

import unittest

from api.api_amenities import app
from model.amenities import Amenities


class TestAmenitiesAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = app.test_client()
        cls.app.testing = True
        cls.data_manager = app.config['data_manager']

    def setUp(self):
        self.data_manager.storage = {}

    def test_delete_amenity(self):
        """Test deleting an amenity"""
        amenity = Amenities(name='Pool')
        self.data_manager.save(amenity)

        response = self.app.delete(f'/amenities/{amenity.id}')
        self.assertEqual(response.status_code, 204)

        # Verify the amenity has been deleted
        response = self.app.get(f'/amenities/{amenity.id}')
        self.assertEqual(response.status_code, 404)

    def test_create_amenity(self):
        """Test creating a new amenity"""
        response = self.app.post('/amenities', json={'name': 'Pool'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('Pool', data['name'])

    def test_get_amenities(self):
        """Test retrieving all amenities"""
        amenity1 = Amenities(name='Pool')
        amenity2 = Amenities(name='Gym')
        self.data_manager.save(amenity1)
        self.data_manager.save(amenity2)

        response = self.app.get('/amenities')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertIn('Pool', data[0]['name'])
        self.assertIn('Gym', data[1]['name'])

    def test_get_amenity(self):
        """Test retrieving a specific amenity"""
        amenity = Amenities(name='Pool')
        self.data_manager.save(amenity)

        response = self.app.get(f'/amenities/{amenity.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('Pool', data['name'])

    def test_update_amenity(self):
        """Test updating an amenity"""
        amenity = Amenities(name='Pool')
        self.data_manager.save(amenity)

        response = self.app.put(f'/amenities/{amenity.id}', json={'name': 'Spa', 'place': 'Basement'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('Spa', data['name'])
        self.assertIn('Basement', data['place'])

    def test_update_amenity_with_existing_name(self):
        """Test updating an amenity to a name that already exists"""
        amenity1 = Amenities(name='Pool')
        amenity2 = Amenities(name='Spa')
        self.data_manager.save(amenity1)
        self.data_manager.save(amenity2)

        response = self.app.put(f'/amenities/{amenity2.id}', json={'name': 'Pool'})
        self.assertEqual(response.status_code, 409)

    def test_create_duplicate_amenity(self):
        """Test creating an amenity with a duplicate name"""
        amenity = Amenities(name='Pool')
        self.data_manager.save(amenity)

        response = self.app.post('/amenities', json={'name': 'Pool'})
        self.assertEqual(response.status_code, 409)


if __name__ == '__main__':
    unittest.main()
