#!/usr/bin/python3
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from model.base import Base

# Cargar variables de entorno desde .env
load_dotenv()

# Crear la instancia de Flask
app = Flask(__name__)

# Seleccionar la configuración basada en el entorno
config_class = 'config.DevelopmentConfig' if os.getenv('ENV') == 'development' else 'config.ProductionConfig'
app.config.from_object(config_class)

try:
    app.config.from_object(config_class)
except ImportError as e:
    raise ImportError(f"Could not import '{config_class}': {e}")

# Crear la instancia de SQLAlchemy con la aplicacion
db = SQLAlchemy(app)

# Cerrar la sesión cuando la aplicación finaliza
@app.teardown_appcontext
def remove_session(exception=None):
    db.session.remove()

# Crear todas las tablas, asegurándose de importar después de que la app esté configurada
with app.app_context():
    db.create_all()
