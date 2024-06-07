#!/usr/bin/python3
from datetime import datetime
import uuid


class City:
    """
    A class representing a city.
    """
    def __init__(self, name, country, place):
        self.id = str(uuid.uuid4())
        self.name = name
        self.country = country
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

    def add_place(self, additional_place):
        self.place += ", " + additional_place
        self.updated_at = datetime.now()

    def remove_place(self, removed_place):
        places = [p.strip() for p in self.place.split(",")]
        if removed_place in places:
            places.remove(removed_place)
            self.place = ", ".join(places)
            self.updated_at = datetime.now()
        else:
            print(f"{removed_place} not found in places")

    def __str__(self):
        return f"City: {self.name}, Country: {self.country}, Place(s): {self.place}, Last Updated: {self.updated_at}"
