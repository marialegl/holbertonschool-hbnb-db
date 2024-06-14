#!/usr/bin/python3
"""Unittest for Review"""


import unittest
from datetime import datetime
from model.review import Review


class TestReview(unittest.TestCase):

    def setUp(self):
        """Setup a default Review instance for testing."""
        self.review = Review(
            user="Test User",
            place="Test Place",
            text="Great place to stay!",
            rating=5
        )

    def test_review_creation(self):
        """Test that a Review instance is created correctly."""
        self.assertEqual(self.review.user, "Test User")
        self.assertEqual(self.review.place, "Test Place")
        self.assertEqual(self.review.text, "Great place to stay!")
        self.assertEqual(self.review.rating, 5)
        self.assertIsNotNone(self.review.id)
        self.assertIsInstance(self.review.created_at, datetime)
        self.assertIsInstance(self.review.updated_at, datetime)

    def test_update_review(self):
        """Test updating the attributes of a review."""
        previous_updated_at = self.review.updated_at
        self.review.update(text="Amazing experience!", rating=4)
        self.assertEqual(self.review.text, "Amazing experience!")
        self.assertEqual(self.review.rating, 4)
        self.assertNotEqual(self.review.updated_at, previous_updated_at)

    def test_review_str(self):
        """Test the string representation of the review."""
        expected_str = f"Review({self.review.id}, Test User, Test Place, 5)"
        self.assertEqual(str(self.review), expected_str)

    def test_invalid_rating(self):
        """Test that a rating must be within an acceptable range."""
        with self.assertRaises(ValueError):
            Review(user="Test User", place="Test Place", text="Nice!", rating=6)

    def test_delete_review(self):
        """Test deleting the review."""
        self.review.delete()
        self.assertTrue(self.review.deleted)

if __name__ == "__main__":
    unittest.main()