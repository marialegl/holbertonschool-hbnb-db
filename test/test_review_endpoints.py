#!/usr/bin/python3
import unittest

from api.api_review import app
from model.review import Review
from persistence.json_data_manager import DataManager


class ReviewAPITestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and initialize the data manager."""
        self.app = app.test_client()
        self.app.testing = True
        self.data_manager = DataManager()
        self.data_manager.storage.clear()  # Clear storage before each test

    def test_create_review(self):
        """Test creating a new review."""
        response = self.app.post('/places/place-123/reviews', json={
            'user': 'user-123',
            'rating': 4,
            'text': 'Great place!'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('user', response.json)
        self.assertIn('place', response.json)
        self.assertIn('rating', response.json)
        self.assertIn('text', response.json)
        self.assertEqual(response.json['user'], 'user-123')
        self.assertEqual(response.json['place'], 'place-123')
        self.assertEqual(response.json['rating'], 4)
        self.assertEqual(response.json['text'], 'Great place!')

    def test_get_review(self):
        """Test retrieving a review by its ID."""
        review = Review(user='user-123', place='place-123', text='Great place!', rating=4)
        review.id = 'review-123'
        self.data_manager.save(review)

        response = self.app.get('/reviews/review-123')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['user'], 'user-123')
        self.assertEqual(response.json['place'], 'place-123')
        self.assertEqual(response.json['rating'], 4)
        self.assertEqual(response.json['text'], 'Great place!')

    def test_update_review(self):
        """Test updating an existing review."""
        review = Review(user='user-123', place='place-123', text='Great place!', rating=4)
        review.id = 'review-123'
        self.data_manager.save(review)

        response = self.app.put('/reviews/review-123', json={
            'text': 'Updated text',
            'rating': 5
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['text'], 'Updated text')
        self.assertEqual(response.json['rating'], 5)

    def test_delete_review(self):
        """Test deleting a review."""
        review = Review(user='user-123', place='place-123', text='Great place!', rating=4)
        review.id = 'review-123'
        self.data_manager.save(review)

        response = self.app.delete('/reviews/review-123')
        self.assertEqual(response.status_code, 204)

        # Verify that the review is marked as deleted
        deleted_review = self.data_manager.get('review-123', 'Review')
        self.assertTrue(deleted_review['deleted'])

    def test_get_non_existent_review(self):
        """Test retrieving a review that does not exist."""
        response = self.app.get('/reviews/non-existent-review')
        self.assertEqual(response.status_code, 404)

    def test_update_non_existent_review(self):
        """Test updating a review that does not exist."""
        response = self.app.put('/reviews/non-existent-review', json={
            'text': 'Should not work',
            'rating': 3
        })
        self.assertEqual(response.status_code, 404)

    def test_delete_non_existent_review(self):
        """Test deleting a review that does not exist."""
        response = self.app.delete('/reviews/non-existent-review')
        self.assertEqual(response.status_code, 404)

    def test_create_review_invalid_rating(self):
        """Test creating a review with an invalid rating."""
        response = self.app.post('/places/place-123/reviews', json={
            'user': 'user-123',
            'rating': 6,  # Invalid rating
            'text': 'This should fail'
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_missing_fields(self):
        """Test creating a review with missing required fields."""
        response = self.app.post('/places/place-123/reviews', json={
            'user': 'user-123',
            'rating': 4
            # Missing 'text'
        })
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()
