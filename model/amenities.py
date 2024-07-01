#!/usr/bin/python3
from datetime import datetime
from model.base import Base
from sqlalchemy import Column, String, DateTime
import uuid

class Amenities(Base):
    """
    A class representing amenities.
    """
    __tablename__ = 'amenities'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(100), nullable=False)
    create_time = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name):
        super().__init__()
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'create_time': self.create_time.isoformat(),
            'update_time': self.update_time.isoformat() if self.update_time else None
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.update_time = datetime.now()

    def delete(self):
        pass

    def __str__(self):
        return f"Amenity(ID: {self.id}, Name: {self.name}, Created: {self.create_time}, Last Updated: {self.update_time})"
