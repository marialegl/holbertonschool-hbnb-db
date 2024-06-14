#!/usr/bin/python3

from datetime import datetime
from model.base import Base


class City(Base):
    """
    A class representing a city.
    """
    def __init__(self, name, state, place):
        super().__init__()
        self.name = name
        self.state = state
        self.place = place

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.update_time = datetime.now()

    def delete(self):
        pass

    def add_place(self, additional_place):
        self.place += ", " + additional_place
        self.update_time = datetime.now()

    def remove_place(self, removed_place):
        places = [p.strip() for p in self.place.split(",")]
        if removed_place in places:
            places.remove(removed_place)
            self.place = ", ".join(places)
            self.update_time = datetime.now()
        else:
            print(f"{removed_place} not found in places")

    def __str__(self):
        return f"City: {self.name}, State: {self.state},\
 Place(s): {self.place}, Last Updated: {self.update_time}"
