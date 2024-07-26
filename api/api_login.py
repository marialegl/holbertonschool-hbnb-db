#!/usr/bin/python3
from flask import Blueprint, jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

from model.users import User, bcrypt

bcrypt = Bcrypt()
bp = Blueprint('api_login', __name__)


@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        additional_claims = {"is_admin": user.is_admin}
        access_token = create_access_token(identity=user.id,
                                           additional_claims=additional_claims)
        return jsonify(access_token=access_token), 200
    return 'Wrong username or password', 401


@bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@bp.route('/admin', methods=['GET'])
@jwt_required()
def admin():
    current_user = get_jwt_identity()
    if not current_user['is_admin']:
        return jsonify(message="Admin access required"), 403
    return jsonify(logged_in_as=current_user), 200


@bp.route('/admin/data', methods=['POST', 'DELETE'])
@jwt_required()
def admin_data():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
