#!/usr/bin/python3
from datetime import datetime

from flask import Flask, jsonify, request, abort
from persistence.database import db

from model.place import Place
from model.review import Review
from model.users import User
from persistence.data_manager import DataManager

app = Flask(__name__)
data_manager = DataManager()


def validate_review_data(data):
    """Validates the input data for creating or updating a review."""
    if 'user_id' not in data or 'place_id' not in data or 'rating' not in data:
        abort(400, description="Missing required fields: user_id, place_id, rating")
    if not data_manager.get(User, data['user_id']):
        abort(404, description=f"User with ID '{data['user_id']}' not found")
    if not data_manager.get(Place, data['place_id']):
        abort(404, description=f"Place with ID '{data['place_id']}' not found")
    if not isinstance(data['rating'], int) or not (1 <= data['rating'] <= 5):
        abort(400, description="Rating must be an integer between 1 and 5")


@app.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()
    validate_review_data(data)
    new_review = Review(
        user_id=data['user_id'],
        place_id=data['place_id'],
        rating=data['rating'],
        comment=data.get('comment')
    )
    data_manager.save(new_review)
    return jsonify(new_review.to_dict()), 201


@app.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = data_manager.query_all(Review)
    return jsonify([review.to_dict() for review in reviews]), 200


@app.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = data_manager.get(Review, review_id)
    if not review:
        abort(404, description="Review not found")
    return jsonify(review.to_dict()), 200


@app.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    review = data_manager.get(Review, review_id)
    if not review:
        abort(404, description="Review not found")

    data = request.get_json()
    if 'rating' in data:
        validate_review_data({'user_id': review.user_id, 'place_id': review.place_id, 'rating': data['rating']})
    review.rating = data.get('rating', review.rating)
    review.comment = data.get('comment', review.comment)
    review.updated_at = datetime.now()

    data_manager.update(review)
    return jsonify(review.to_dict()), 200


@app.route('/users/<user_id>/reviews', methods=['GET'])
def get_user_reviews(user_id):
    user = data_manager.get(User, user_id)
    if not user:
        abort(404, description="User not found")
    reviews = data_manager.query_all_by_filter(Review, Review.user_id == user_id)
    return jsonify([review.to_dict() for review in reviews]), 200


@app.route('/places/<place_id>/reviews', methods=['GET'])
def get_place_reviews(place_id):
    place = data_manager.get(Place, place_id)
    if not place:
        abort(404, description="Place not found")
    reviews = data_manager.query_all_by_filter(Review, Review.place_id == place_id)
    return jsonify([review.to_dict() for review in reviews]), 200


@app.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = data_manager.get(Review, review_id)
    if not review:
        abort(404, description="Review not found")
    data_manager.delete(review)
    return '', 204


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crear todas las tablas dentro del contexto de la aplicación
    app.run(debug=True)
