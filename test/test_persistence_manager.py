#!/usr/bin/python3
"""pruebas para verificar que las implementaciones de IPersistenceManager
manejen las operaciones CRUD correctamente."""
from abc import ABC, abstractmethod

from model.city import City


class PersistenceManagerTestCase(ABC):
    """
    Base test case for any implementation of IPersistenceManager.
    """

    @classmethod
    @abstractmethod
    def setUpClass(cls):
        pass

    @classmethod
    @abstractmethod
    def tearDownClass(cls):
        pass

    def test_save_and_get_entity(self):
        city = City(name='TestCity', population=1000, country_code='TC')
        self.persistence_manager.save(city)
        retrieved_city = self.persistence_manager.get(City, city.id)
        self.assertIsNotNone(retrieved_city)
        self.assertEqual(retrieved_city.name, 'TestCity')

    def test_update_entity(self):
        city = City(name='UpdateCity', population=2000, country_code='UC')
        self.persistence_manager.save(city)
        city.name = 'UpdatedCity'
        self.persistence_manager.update(city)
        updated_city = self.persistence_manager.get(City, city.id)
        self.assertEqual(updated_city.name, 'UpdatedCity')

    def test_delete_entity(self):
        city = City(name='DeleteCity', population=3000, country_code='DC')
        self.persistence_manager.save(city)
        self.persistence_manager.delete(city)
        deleted_city = self.persistence_manager.get(City, city.id)
        self.assertIsNone(deleted_city)

    def test_query_all_entities(self):
        city1 = City(name='City1', population=1000, country_code='C1')
        city2 = City(name='City2', population=2000, country_code='C2')
        self.persistence_manager.save(city1)
        self.persistence_manager.save(city2)
        cities = self.persistence_manager.query_all(City)
        self.assertEqual(len(cities), 2)

    def test_query_all_by_filter(self):
        city1 = City(name='FilteredCity1', population=1000, country_code='FC1')
        city2 = City(name='FilteredCity2', population=2000, country_code='FC1')
        city3 = City(name='FilteredCity3', population=3000, country_code='FC2')
        self.persistence_manager.save(city1)
        self.persistence_manager.save(city2)
        self.persistence_manager.save(city3)
        cities = self.persistence_manager.query_all_by_filter(City, City.country_code == 'FC1')
        self.assertEqual(len(cities), 2)
