#!/usr/bin/python3
"""Operaciones CRUD y Gestión de Relaciones"""
import unittest
from model.base import Base
from model.city import City
from model.country import Country
from persistence.database import db, app

class CRUDOperationsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self):
        with app.app_context():
            self.city = City(name='TestCity', population=1000, country_code='TC')
            self.country = Country(name='TestCountry', iso_code='TC')
            self.country.cities.append(self.city)
            db.session.add(self.country)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_city(self):
        with app.app_context():
            city = City(name='NewCity', population=2000, country_code='NC')
            city.save()
            self.assertIsNotNone(City.query.filter_by(name='NewCity').first())

    def test_read_city(self):
        with app.app_context():
            city = City.query.filter_by(name='TestCity').first()
            self.assertIsNotNone(city)
            self.assertEqual(city.name, 'TestCity')

    def test_update_city(self):
        with app.app_context():
            city = City.query.filter_by(name='TestCity').first()
            city.name = 'UpdatedCity'
            city.save()
            self.assertEqual(City.query.filter_by(name='UpdatedCity').first().name, 'UpdatedCity')

    def test_delete_city(self):
        with app.app_context():
            city = City.query.filter_by(name='TestCity').first()
            city.delete()
            self.assertIsNone(City.query.filter_by(name='TestCity').first())

    def test_country_city_relationship(self):
        with app.app_context():
            country = Country.query.filter_by(name='TestCountry').first()
            self.assertEqual(len(country.cities), 1)
            self.assertEqual(country.cities[0].name, 'TestCity')

if __name__ == '__main__':
    unittest.main()
