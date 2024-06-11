#!/usr/bin/python3
from flask import Flask, jsonify, request
from users import Users
from data_manager import DataManager
import re
import uuid
from uuid import UUID

app = Flask(__name__)
data_manager = DataManager()

def validate_email(email):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

def validate_name(name):
    return isinstance(name, str) and name.strip() != ""

def validate_user_data(data):
    if not validate_email(data.get('email', '')):
        return False, "Invalid email format."
    if not validate_name(data.get('first_name', '')):
        return False, "First name cannot be empty."
    if not validate_name(data.get('last_name', '')):
        return False, "Last name cannot be empty."
    return True, ""

def is_valid_uuid(val):
    try:
        UUID(str(val))
        return True
    except ValueError:
        return False

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    valid, message = validate_user_data(data)

    if not valid:
        return jsonify({'error': message}), 400
    
    if any(user['email'] == data['email'] for user in data_manager.storage.get('Users', {}).values()):
        return jsonify({'error': 'Email already exists'}), 409
    
    user = Users(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data.get('password', '')
    )
    data_manager.save(user.to_dict())
    return jsonify(user.to_dict()), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = list(data_manager.storage.get('Users', {}).values())
    return jsonify(users), 200

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    if not is_valid_uuid(user_id):
        return jsonify({'error': 'Invalid user ID'}), 400
    user = data_manager.get(user_id, 'Users')
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    if not is_valid_uuid(user_id):
        return jsonify({'error': 'Invalid user ID'}), 400
    
    user = data_manager.get(user_id, 'Users')

    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    valid, message = validate_user_data(data)

    if not valid:
        return jsonify({'error': message}), 400
    
    if any(user['email'] == data['email'] and user['id'] != user_id for user in data_manager.storage.get('Users', {}).values()):
        return jsonify({'error': 'Email already exists'}), 409
    
    updated_user = Users(
        id_user=user_id,
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password=data.get('password', user['password'])
    )
    data_manager.update(updated_user.to_dict())
    return jsonify(updated_user.to_dict()), 200

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if not is_valid_uuid(user_id):
        return jsonify({'error': 'Invalid user ID'}), 400
    
    user = data_manager.get(user_id, 'Users')
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    
    data_manager.delete(user_id, 'Users')
    return jsonify({}), 204

if __name__ == '__main__':
    app.run(debug=True)