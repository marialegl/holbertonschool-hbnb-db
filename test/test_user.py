#!/usr/bin/python3
"""Unittest for Users"""

import unittest
from datetime import datetime
from model.users import User, Host, Guest


class TestUsers(unittest.TestCase):

    def setUp(self):
        User.existing_email.clear()  # Clear existing emails before each test
        self.user = User("John", "Doe",
                          "john.doe@example.com", "password123")

    def test_create_user(self):
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.email, "john.doe@example.com")
        self.assertEqual(self.user.password, "password123")
        self.assertIsInstance(self.user.create_time, datetime)
        self.assertIsInstance(self.user.update_time, datetime)

    def test_update_user(self):
        self.user.update(first_name="Jane", email="jane.doe@example.com")
        self.assertEqual(self.user.first_name, "Jane")
        self.assertEqual(self.user.email, "jane.doe@example.com")

    def test_str_representation(self):
        self.assertTrue(str(self.user).startswith("User(Id: ") and
                        str(self.user).endswith(", name: John, email: john.doe@example.com)"))

    def test_inherit(self):
        self.assertTrue(issubclass(Host, User))
        self.assertTrue(issubclass(Guest, User))


if __name__ == "__main__":
    unittest.main()
