#!/usr/bin/python3
from flask import Flask, jsonify, request, abort
from model.review import Review
from persistence.data_manager import DataManager
import uuid

app = Flask(__name__)
data_manager = DataManager()

def validate_review_data(data, is_update=False):
    """Validate review data ensuring all required fields are present and valid."""
    required_fields = ['user', 'text', 'rating']
    if not all(field in data for field in required_fields):
        abort(400, description="Missing required fields: user, text, rating")
    if not (1 <= data['rating'] <= 5):
        abort(400, description="Rating must be between 1 and 5")

@app.route('/places/<string:place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Create a new review for a specified place."""
    data = request.get_json()
    validate_review_data(data)
    review_id = str(uuid.uuid4())
    review = Review(user=data['user'], place=place_id, text=data['text'], rating=data['rating'])
    review.id = review_id  # Set the ID manually
    data_manager.save(review)
    return jsonify(review.to_dict()), 201

@app.route('/reviews/<string:review_id>', methods=['GET'])
def get_review(review_id):
    """Retrieve detailed information about a specific review."""
    review = data_manager.get(review_id, 'Review')
    if review is None or review.get('deleted'):
        abort(404, description=f"Review with ID '{review_id}' not found")
    return jsonify(review.to_dict()), 200

@app.route('/reviews/<string:review_id>', methods=['PUT'])
def update_review(review_id):
    """Update an existing review."""
    review_data = data_manager.get(review_id, 'Review')
    if review_data is None or review_data.get('deleted'):
        abort(404, description=f"Review with ID '{review_id}' not found")

    data = request.get_json()
    validate_review_data(data, is_update=True)

    review = Review.from_dict(review_data)
    review.update(**data)

    data_manager.update(review)

    return jsonify(review.to_dict()), 200

@app.route('/reviews/<string:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete a specific review."""
    review_data = data_manager.get(review_id, 'Review')
    if review_data is None or review_data.get('deleted'):
        abort(404, description=f"Review with ID '{review_id}' not found")

    review = Review.from_dict(review_data)
    review.delete()
    data_manager.update(review)

    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
