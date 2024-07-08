#!/usr/bin/python3
"""Verifica que el sistema pueda cambiar entre almacenamiento en archivo y base de datos."""
import unittest
import os
from persistence.data_manager import DataManager
from model.city import City
from model.country import Country
from persistence.database import db, app

class PersistenceSwitchingTestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        db.create_all()
        self.data_manager = DataManager()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_sqlite_persistence(self):
        city = City(name='SQLiteCity', population=1000, country_code='SC')
        self.data_manager.save(city)
        retrieved_city = self.data_manager.get(City, city.id)
        self.assertIsNotNone(retrieved_city)
        self.assertEqual(retrieved_city.name, 'SQLiteCity')

    def test_postgresql_persistence(self):
        os.environ['DATABASE_TYPE'] = 'postgresql'
        os.environ['DATABASE_URL'] = 'postgresql://username:password@localhost/mydatabase'
        app.config.from_object('config.ProductionConfig')
        db.create_all()

        city = City(name='PostgresCity', population=2000, country_code='PC')
        self.data_manager.save(city)
        retrieved_city = self.data_manager.get(City, city.id)
        self.assertIsNotNone(retrieved_city)
        self.assertEqual(retrieved_city.name, 'PostgresCity')

        # Cleanup PostgreSQL
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()
