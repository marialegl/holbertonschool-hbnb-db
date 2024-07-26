#!/usr/bin/python3
import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()
# bcrypt = Bcrypt()
# jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # Configuración de la aplicación
    if os.environ.get('ENV') == 'production':
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['USE_DATABASE'] = True
    app.config['JWT_SECRET_KEY'] = 'super-secret'

    db.init_app(app)
    # bcrypt.init_app(app)
    # jwt.init_app(app)

    from api.api_controller import bp as api_user_bp
    from api.api_login import bp as api_login_bp
    app.register_blueprint(api_user_bp)
    # app.register_blueprint(api_login_bp)

    with app.app_context():
        if config.USE_DB and os.environ.get('DATABASE_TYPE') == 'sqlite':
            db.create_all()

    return app
