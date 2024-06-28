#!/usr/bin/python3
from flask import Flask, jsonify, request, abort
from model.review import Review
from model.place import Place
from model.users import User
from persistence.data_manager import DataManager
from datetime import datetime

app = Flask(__name__)
data_manager = DataManager()

@app.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    data = request.get_json()
    user_id = data.get('user_id')
    rating = data.get('rating')
    comment = data.get('comment')
    
    # Validaciones
    if not user_id or not rating or not comment:
        abort(400, description="Missing required fields")
    if not 1 <= rating <= 5:
        abort(400, description="Rating must be between 1 and 5")
    if not data_manager.get(user_id, "User"):
        abort(404, description="User not found")
    if not data_manager.get(place_id, "Place"):
        abort(404, description="Place not found")
    place = data_manager.get(place_id, "Place")
    if place["host_id"] == user_id:
        abort(400, description="Hosts cannot review their own place")
    
    review = Review(place_id=place_id, user_id=user_id, rating=rating, comment=comment)
    data_manager.save(review)
    return jsonify(review.to_dict()), 201

@app.route('/users/<user_id>/reviews', methods=['GET'])
def get_user_reviews(user_id):
    if not data_manager.get(user_id, "User"):
        abort(404, description="User not found")
    reviews = [review for review in data_manager.get_all("Review") if review["user_id"] == user_id]
    return jsonify(reviews), 200

@app.route('/places/<place_id>/reviews', methods=['GET'])
def get_place_reviews(place_id):
    if not data_manager.get(place_id, "Place"):
        abort(404, description="Place not found")
    reviews = [review for review in data_manager.get_all("Review") if review["place_id"] == place_id]
    return jsonify(reviews), 200

@app.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = data_manager.get(review_id, "Review")
    if not review:
        abort(404, description="Review not found")
    return jsonify(review), 200

@app.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):

    review = data_manager.get(review_id, 'Review')
    if not review:
        abort(404, description="Review not found")
    
    data = request.get_json()
    review['rating'] = data.get('rating', review['rating'])
    review['comment'] = data.get('comment', review['comment'])
    
    if review['rating'] < 1 or review['rating'] > 5:
        abort(400, description="Rating must be between 1 and 5")

    review['updated_at'] = datetime.now().isoformat()
    
    updated_review = Review(
        place_id=review['place_id'],
        user_id=review['user_id'],
        rating=review['rating'],
        comment=review['comment']
    )
    updated_review.id = review['id']
    updated_review.create_time = datetime.fromisoformat(review['created_at'])
    updated_review.update_time = datetime.fromisoformat(review['updated_at'])
    
    data_manager.update(updated_review)
    
    return jsonify(updated_review.to_dict()), 200

@app.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    if not data_manager.get(review_id, "Review"):
        abort(404, description="Review not found")
    data_manager.delete(review_id, "Review")
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
