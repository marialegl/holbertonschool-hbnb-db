#!/usr/bin/python3
from flask import Flask, jsonify, request
from model.users import User
from persistence.data_manager import DataManager
from persistence.database import session
import re
from uuid import UUID

app = Flask(__name__)
data_manager = DataManager(session)


def validate_email(email):
    email_regex = r"^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$"
    return re.match(email_regex, email)


def validate_name(name):
    return isinstance(name, str) and name.strip() != ""


def validate_user_data(data):
    if not validate_email(data.get("email", "")):
        return False, "Invalid email format."
    if not validate_name(data.get("first_name", "")):
        return False, "First name cannot be empty."
    if not validate_name(data.get("last_name", "")):
        return False, "Last name cannot be empty."
    return True, ""


def is_valid_uuid(val):
    try:
        UUID(str(val))
        return True
    except ValueError:
        return False


@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    valid, message = validate_user_data(data)

    if not valid:
        return jsonify({"error": message}), 400

    existing_user = User.query.filter_by(email=data["email"]).first()
    if existing_user:
        return jsonify({"error": "Email already exists"}), 409

    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        password=data.get("password", ""),
    )
    data_manager.save(user)
    return jsonify(user.to_dict()), 201


@app.route("/users", methods=["GET"])
def get_users():
    users = data_manager.get_all('User')
    return jsonify([user for user in users]), 200


@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    if not is_valid_uuid(user_id):
        return jsonify({"error": "Invalid user ID"}), 400
    user = data_manager.get(user_id, 'User')
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200


@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()

    if not is_valid_uuid(user_id):
        return jsonify({"error": "Invalid user ID"}), 400

    user = data_manager.get(user_id, 'User')

    if user is None:
        return jsonify({"error": "User not found"}), 404

    valid, message = validate_user_data(data)

    if not valid:
        return jsonify({"error": message}), 400

    existing_user =  data_manager.get_all('User')
    if any(u['email'] == data["email"] and u['id'] != user_id for u in existing_user):
        return jsonify({"error": "Email already exists"}), 409

    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.email = data["email"]
    user.password = data.get("password", user.password)
    
    data_manager.update(user)
    return jsonify(user.to_dict()), 200


@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    if not is_valid_uuid(user_id):
        return jsonify({"error": "Invalid user ID"}), 400

    user = data_manager.get(user_id, 'User')
    if user is None:
        return jsonify({"error": "User not found"}), 404

    data_manager.delete(user_id, 'User')
    return '', 204


if __name__ == "__main__":
    app.run(debug=True)
