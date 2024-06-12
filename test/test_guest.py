#!/usr/bin/python3
"""Unittest for Guest"""

import unittest
from datetime import datetime
from model.users import Users, Guest


class TestGuest(unittest.TestCase):

    def setUp(self):
        Users.existing_email.clear()
        self.guest = Guest("3", "Bob", "Brown",
                           "bob.brown@example.com", "password123")

    def test_created_guest(self):
        self.assertEqual(self.guest.id, "3")
        self.assertEqual(self.guest.First_name, "Bob")
        self.assertEqual(self.guest.Last_name, "Brown")
        self.assertEqual(self.guest.email, "bob.brown@example.com")
        self.assertEqual(self.guest.password, "password123")
        self.assertIsInstance(self.guest.create_time, datetime)
        self.assertIsInstance(self.guest.update_time, datetime)

    def test_add_review(self):
        self.guest.add_review("Great place!")
        self.assertIn("Great place!", self.guest.comment)

    def test_remove_review(self):
        self.guest.add_review("Great place!")
        self.guest.remove_review("Great place!")
        self.assertNotIn("Great place!", self.guest.comment)


if __name__ == "__main__":
    unittest.main()
