#!/usr/bin/python3
"""clases de prueba específicas que hereden de PersistenceManagerTestCase y proporcionen 
una implementación concreta de la interfaz para el sistema de persistencia"""
import unittest

from persistence.database import db, app
from tests.test_persistence_manager import PersistenceManagerTestCase

from persistence.data_manager import DataManager


class SQLAlchemyDataManagerTestCase(PersistenceManagerTestCase, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        db.create_all()
        cls.persistence_manager = DataManager()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
