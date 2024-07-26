#!/usr/bin/python3
"""relaciones estén bien gestionadas."""
import unittest

from persistence.database import db, app

from model.city import City
from model.country import Country
from persistence.json_data_manager import DataManager


class RelationshipTestCase(unittest.TestCase):
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

    def test_country_city_relationship(self):
        country = Country(name='TestCountry', iso_code='TC')
        city = City(name='TestCity', population=1000, country_code='TC')
        country.cities.append(city)
        self.data_manager.save(country)
        self.data_manager.save(city)

        retrieved_country = self.data_manager.get(Country, country.id)
        self.assertEqual(len(retrieved_country.cities), 1)
        self.assertEqual(retrieved_country.cities[0].name, 'TestCity')


if __name__ == '__main__':
    unittest.main()
