#!/usr/bin/python3
from datetime import datetime
import uuid
import os
from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates, sessionmaker
from persistence.database import db


# Definir una clase base que extienda de db.Model para compatibilidad con SQLAlchemy
class Base(db.Model):
    __abstract__ = True  # Esto indica a SQLAlchemy que no debe crear una tabla para esta clase
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

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
