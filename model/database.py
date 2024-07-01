#!/usr/bin/python3
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

DB_TYPE = os.getenv('DB_TYPE', 'sqlite')
DB_URI = {
    'sqlite': 'sqlite:///mydatabase.db',
    'postgresql': 'postgresql://username:password@localhost/mydatabase'
}

# Crear el motor de la base de datos
engine = create_engine(DB_URI[DB_TYPE])

# Crear una sesión de base de datos
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# Crear todas las tablas, asegurándose de importar después de que el motor esté configurado
from model.base import Base
Base.metadata.create_all(engine)

# Cerrar la sesión cuando la aplicación finaliza
def remove_session():
    Session.remove()
