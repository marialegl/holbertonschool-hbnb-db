#!/usr/bin/python3

from datetime import datetime


class Amenities:
    """
    A class representing amenities.
    """
    def __init__(self, id, name, place, create_time=None, update_time=None):
        self.id = id
        self.name = name
        self.place = place
        self.create_time = self.get_current_time(create_time)
        self.update_time = self.get_current_time(update_time)

    def get_current_time(self, time):
        return time if time else datetime.now()

    def update(self, new_name, new_place):
        self.name = new_name
        self.place = new_place
        self.update_time = self.get_current_time(None)

    def delete(self):
        pass

    def __str__(self):
        return f"Amenity(ID: {self.id}, Name: {self.name}, Place: {self.place}, Created: {self.create_time}, Last Updated: {self.update_time})"
