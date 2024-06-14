#!/usr/bin/python3
from datetime import datetime
from .base import Base

class Amenities(Base):
    """
    A class representing amenities.
    """
    def __init__(self, name='', place=''):
        self.name = name
        self.place = place

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

    def delete(self):
        pass

    def __str__(self):
        return f"Amenity(ID: {self.id}, Name: {self.name}, Place: {self.place},\
 Created: {self.created_at}, Last Updated: {self.updated_at})"
    