#!/usr/bin/python3
from datetime import datetime
from model.base import Base


class Amenities(Base):
    """
    A class representing amenities.
    """

    def __init__(self, name):
        super().__init__()
        self.name = name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.update_time = datetime.now()

    def delete(self):
        pass

    def __str__(self):
        return f"Amenity(ID: {self.id}, Name: {self.name},\
 Created: {self.create_time}, Last Updated: {self.update_time})"
