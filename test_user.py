import unittest
from datetime import datetime
from Users import Users, Host, Guest


class TestUsers(unittest.TestCase):

    def setUp(self):
        Users.existing_email.clear()  # Clear existing emails before each test
        self.user = Users("1", "John", "Doe",
                          "john.doe@example.com", "password123")

    def test_create_user(self):
        self.assertEqual(self.user.id, "1")
        self.assertEqual(self.user.First_name, "John")
        self.assertEqual(self.user.Last_name, "Doe")
        self.assertEqual(self.user.email, "john.doe@example.com")
        self.assertEqual(self.user.password, "password123")
        self.assertIsInstance(self.user.create_time, datetime)
        self.assertIsInstance(self.user.update_time, datetime)

    def test_duplicate_email(self):
        with self.assertRaises(ValueError):
            Users("2", "Jane", "Doe", "john.doe@example.com", "password456")

    def test_update_user(self):
        self.user.update(First_name="Jane", email="jane.doe@example.com")
        self.assertEqual(self.user.First_name, "Jane")
        self.assertEqual(self.user.email, "jane.doe@example.com")

    def test_str_representation(self):
        self.assertEqual(str(self.user), "User(Id: 1, name: John,\
 email: john.doe@example.com)")

    def test_inherit(self):
        self.assertTrue(issubclass(Host, Users))
        self.assertTrue(issubclass(Guest, Users))


if __name__ == "__main__":
    unittest.main()
