#!/usr/bin/python3
from flask import Flask, jsonify, request
from model.users import User, bcrypt
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,get_jwt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///development.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret'

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
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

@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@app.route('/admin', methods=['GET'])
@jwt_required()
def admin():
    current_user = get_jwt_identity()
    if not current_user['is_admin']:
        return jsonify({"msg": "Admin access required"}), 403
    return jsonify(logged_in_as=current_user), 200

@app.route('/admin/data', methods=['POST', 'DELETE'])
@jwt_required()
def admin_data():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

if __name__ == "__main__":
    app.run(debug=True)
