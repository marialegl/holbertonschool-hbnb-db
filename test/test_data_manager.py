#!/usr/bin/python3
"""Pruebas para cada operación CRUD en tu DataManager"""
import unittest
from persistence.data_manager import DataManager
from model.city import City
from model.country import Country
from persistence.database import db, app

class DataManagerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        db.create_all()
        cls.data_manager = DataManager()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()

    def test_save_and_get_city(self):
        city = City(name='TestCity', population=1000, country_code='TC')
        self.data_manager.save(city)
        retrieved_city = self.data_manager.get(City, city.id)
        self.assertIsNotNone(retrieved_city)
        self.assertEqual(retrieved_city.name, 'TestCity')

    def test_update_city(self):
        city = City(name='UpdateCity', population=2000, country_code='UC')
        self.data_manager.save(city)
        city.name = 'UpdatedCity'
        self.data_manager.update(city)
        updated_city = self.data_manager.get(City, city.id)
        self.assertEqual(updated_city.name, 'UpdatedCity')

    def test_delete_city(self):
        city = City(name='DeleteCity', population=3000, country_code='DC')
        self.data_manager.save(city)
        self.data_manager.delete(city)
        deleted_city = self.data_manager.get(City, city.id)
        self.assertIsNone(deleted_city)

    def test_query_all_cities(self):
        city1 = City(name='City1', population=1000, country_code='C1')
        city2 = City(name='City2', population=2000, country_code='C2')
        self.data_manager.save(city1)
        self.data_manager.save(city2)
        cities = self.data_manager.query_all(City)
        self.assertEqual(len(cities), 2)

if __name__ == '__main__':
    unittest.main()
