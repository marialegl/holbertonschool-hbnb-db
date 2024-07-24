#!/usr/bin/python3
from flask import Blueprint, jsonify, request
from model.users import User
from persistence.data_manager import DataManager
import re
from api import db
from uuid import UUID
from flask_jwt_extended import JWTManager


data_manager = DataManager()
bp = Blueprint('api_controller', __name__)

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


@bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    valid, message = validate_user_data(data)

    if not valid:
        return jsonify({"error": message}), 400

    existing_user = data_manager.query_all_by_filter(User, User.email == data["email"])
    if existing_user:
        return jsonify({"error": "Email already exists"}), 409


    user = User(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
    )
    user.set_password(data.get("password", ""))
    data_manager.save(user)
    return jsonify(user.to_dict()), 201


@bp.route("/users", methods=["GET"])
def get_users():
    if bp.config['USE_DATABASE']:
        users = User.query.all()
        users = [user.to_dict() for user in users]
    else:
        users = data_manager.get_all(User)
    return jsonify(users), 200


@bp.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    if bp.config['USE_DATABASE']:
        user = User.query.get(user_id)
    else:
        user = data_manager.get(user_id, "User") 

    if not is_valid_uuid(user_id):
        return jsonify({"error": "Invalid user ID"}), 400
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict() if bp.config['USE_DATABASE'] else user), 200 


@bp.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()

    if bp.config['USE_DATABASE']:
        user = User.query.get(user_id)
    else:
        user = data_manager.get(user_id, "User")

    if not is_valid_uuid(user_id):
        return jsonify({"error": "Invalid user ID"}), 400

    if user is None:
        return jsonify({"error": "User not found"}), 404

    valid, message = validate_user_data(data)

    if not valid:
        return jsonify({"error": message}), 400

    existing_user = data_manager.query_all_by_filter(User,
                User.email == data["email"], User.id != user_id)
    if existing_user:
        return jsonify({"error": "Email already exists"}), 409

    if bp.config['USE_DATABASE']:
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        if 'password' in data:
            user.set_password(data["password"])
        db.session.commit()
    else:
        updated_user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password=data.get("password", user["password"]),
        )
        updated_user.id = user_id
        data_manager.update(updated_user)
    return jsonify(user.to_dict()), 200
    

@bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    if not is_valid_uuid(user_id):
        return jsonify({"error": "Invalid user ID"}), 400

    if bp.config['USE_DATABASE']:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
    else:
        user = data_manager.get(User, user_id)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        data_manager.delete(user)
    return '', 204
