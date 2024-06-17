#!/usr/bin/python3
"""Unittest for Data Manager"""


import unittest
from model.users import User
from persistence.data_manager import DataManager


class TestDataManager(unittest.TestCase):
    def setUp(self):
        """Setup initial conditions for tests"""
        self.dm = DataManager()
        self.user = User("Luis", "Dom", "luis12@gmai.com", "124")
    
    def test_save(self):
        """Test saving an entity"""
        self.dm.save(self.user)
        self.assertEqual(self.dm.get(self.user.id, 'User'), self.user.to_dict())

    def test_get(self):
        """Test retrieving an entity"""
        self.dm.save(self.user)
        self.assertEqual(self.dm.get(self.user.id, 'User'), self.user.to_dict())
        self.assertIsNone(self.dm.get('999', 'dict'))  # Testing non-existing entity

    def test_update(self):
        """Test updating an entity"""
        self.dm.save(self.user)
        self.user.first_name = "Jhon"
        self.user.last_name = "Doe"
        self.dm.update(self.user)
        user_old = self.dm.get(self.user.id, 'User')
        self.assertEqual(user_old.get('first_name'), self.user.first_name)
        self.assertEqual(user_old.get('last_name'), self.user.last_name)
        #self.assertEqual(user_old.get('email'), updated_user.email)
        #self.assertEqual(user_old.get('password'), updated_user.password)

    def test_delete(self):
        """Test deleting an entity"""
        self.dm.save(self.user)
        self.dm.delete('123', 'dict')
        self.assertIsNone(self.dm.get('123', 'dict'))

if __name__ == '__main__':
    unittest.main()
