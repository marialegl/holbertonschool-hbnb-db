#!/usr/bin/python3
from datetime import datetime
import uuid


class Amenities:
    """
    A class representing amenities.
    """
    def __init__(self, id=None, name='', place=''):
        self.id = id if id else str(uuid.uuid4())
        self.name = name
        self.place = place
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

    def delete(self):
        pass

    def __str__(self):
        return f"Amenity(ID: {self.id}, Name: {self.name}, Place: {self.place}, Created: {self.created_at}, Last Updated: {self.updated_at})"
    