#!/usr/bin/python3
import uuid
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()


# Definir una clase base que extienda de db.Model para compatibilidad con SQLAlchemy
class Base(db.Model):
    __abstract__ = True  # Esto indica a SQLAlchemy que no debe crear una tabla para esta clase
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @validates('create_time', 'update_time')
    def convert_datetime(self, key, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value

    def save(self):
        """Save the object to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the object from the database."""
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """Convert the object to a dictionary."""
        return {
            'id': self.id,
            'create_time': self.create_time.isoformat(),
            'update_time': self.update_time.isoformat()
        }
