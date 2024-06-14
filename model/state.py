#!usr/bin/python3
""" Class State with the necessary attributes and methods."""

from datetime import datetime
from model.base import Base

class State(Base):
    def __init__(self, name, country):
        super().__init__()
        self.name = name
        self.country = country
        self.cities = []
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
        self.update_time = datetime.now()

    def delete(self):
        del self

    def __str__(self):
        return f"State({self.id}, {self.name}, {self.country})"
