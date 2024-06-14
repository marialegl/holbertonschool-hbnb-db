#!/usr/bin/python3
"""Unittest for User, Host, and Guest"""

import unittest
from datetime import datetime
from model.users import User, Host, Guest


class TestUser(unittest.TestCase):

    def setUp(self):
        User.existing_email.clear()  # Clear existing emails before each test
        self.user = User("John", "Doe", "john.doe@example.com", "password123")

    def test_create_user(self):
        self.assertEqual(self.user.first_name, "John")
        self.assertEqual(self.user.last_name, "Doe")
        self.assertEqual(self.user.email, "john.doe@example.com")
        self.assertEqual(self.user.password, "password123")
        self.assertIsInstance(self.user.create_time, datetime)
        self.assertIsInstance(self.user.update_time, datetime)
        self.assertIn("john.doe@example.com", User.existing_email)

    def test_duplicate_email(self):
        with self.assertRaises(ValueError):
            User("Jane", "Doe", "john.doe@example.com", "password456")

    def test_update_user(self):
        self.user.update(first_name="Jane", email="jane.doe@example.com")
        self.assertEqual(self.user.first_name, "Jane")
        self.assertEqual(self.user.email, "jane.doe@example.com")
        self.assertIsInstance(self.user.update_time, datetime)

    def test_to_dict(self):
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict['first_name'], "John")
        self.assertEqual(user_dict['last_name'], "Doe")
        self.assertEqual(user_dict['email'], "john.doe@example.com")
        self.assertEqual(user_dict['password'], "password123")
        self.assertIn('create_time', user_dict)
        self.assertIn('update_time', user_dict)

    def test_str_representation(self):
        expected_str = f"User(Id: {self.user.id}, name: John, email: john.doe@example.com)"
        self.assertEqual(str(self.user), expected_str)

    def test_delete_user(self):
        email = self.user.email
        self.user.delete()
        self.assertNotIn(email, User.existing_email)


class TestHost(unittest.TestCase):

    def setUp(self):
        User.existing_email.clear()  # Clear existing emails before each test
        self.host = Host("Alice", "Smith", "alice.smith@example.com", "hostpassword")

    def test_create_host(self):
        self.assertEqual(self.host.first_name, "Alice")
        self.assertEqual(self.host.last_name, "Smith")
        self.assertEqual(self.host.email, "alice.smith@example.com")
        self.assertEqual(self.host.password, "hostpassword")
        self.assertIsInstance(self.host.name_place, list)
        self.assertIsInstance(self.host.amenities, list)

    def test_add_and_remove_place(self):
        self.host.add_place("Apartment in NY")
        self.assertIn("Apartment in NY", self.host.name_place)
        self.host.remove_place("Apartment in NY")
        self.assertNotIn("Apartment in NY", self.host.name_place)

    def test_add_and_remove_amenities(self):
        self.host.add_amenities("WiFi")
        self.assertIn("WiFi", self.host.amenities)
        self.host.remove_amenities("WiFi")
        self.assertNotIn("WiFi", self.host.amenities)


class TestGuest(unittest.TestCase):

    def setUp(self):
        User.existing_email.clear()  # Clear existing emails before each test
        self.guest = Guest("Bob", "Brown", "bob.brown@example.com", "guestpassword")

    def test_create_guest(self):
        self.assertEqual(self.guest.first_name, "Bob")
        self.assertEqual(self.guest.last_name, "Brown")
        self.assertEqual(self.guest.email, "bob.brown@example.com")
        self.assertEqual(self.guest.password, "guestpassword")
        self.assertIsInstance(self.guest.comment, list)

    def test_add_and_remove_review(self):
        self.guest.add_review("Great host!")
        self.assertIn("Great host!", self.guest.comment)
        self.guest.remove_review("Great host!")
        self.assertNotIn("Great host!", self.guest.comment)


if __name__ == "__main__":
    unittest.main()
