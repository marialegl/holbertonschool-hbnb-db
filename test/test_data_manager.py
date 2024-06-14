#!/usr/bin/python3
"""Unittest for Data Manager"""


import unittest
from persistence.data_manager import DataManager


class TestDataManager(unittest.TestCase):
    def setUp(self):
        """Setup initial conditions for tests"""
        self.dm = DataManager()
        self.user = {'id': '123', 'name': 'John'}
    
    def test_save(self):
        """Test saving an entity"""
        self.dm.save(self.user)
        self.assertEqual(self.dm.get('123', 'dict'), self.user)

    def test_get(self):
        """Test retrieving an entity"""
        self.dm.save(self.user)
        self.assertEqual(self.dm.get('123', 'dict'), self.user)
        self.assertIsNone(self.dm.get('999', 'dict'))  # Testing non-existing entity

    def test_update(self):
        """Test updating an entity"""
        self.dm.save(self.user)
        updated_user = {'id': '123', 'name': 'John Doe'}
        self.dm.update(updated_user)
        self.assertEqual(self.dm.get('123', 'dict')['name'], 'John Doe')

    def test_delete(self):
        """Test deleting an entity"""
        self.dm.save(self.user)
        self.dm.delete('123', 'dict')
        self.assertIsNone(self.dm.get('123', 'dict'))

if __name__ == '__main__':
    unittest.main()
