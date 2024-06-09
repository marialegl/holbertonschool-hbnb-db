#!usr/bin/python3
""" Class State with the necessary attributes and methods."""

from datetime import datetime
import uuid


class State:
    def __init__(self, name, country):
        self.id = str(uuid.uuid4())
        self.name = name
        self.country = country
        self.cities = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        if not name:
            raise ValueError("Name cannot be empty")
        if not country:
            raise ValueError("Country cannot be empty")

    def add_city(self, city):
        self.cities.append(city)

    def remove_city(self, city):
        self.cities.remove(city)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

    def delete(self):
        del self

    def __str__(self):
        return f"State({self.id}, {self.name}, {self.country})"
