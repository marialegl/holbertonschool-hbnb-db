#!/usr/bin/python3

from datetime import datetime

class City:
    """
    A class representing a city.
    """
    def __init__(self, name, country, place, create_time=None, update_time=None):
        self.name = name
        self.country = country
        self.place = place
        self.create_time = self.get_current_time(create_time)
        self.update_time = self.get_current_time(update_time)

    def get_current_time(self, time):
        return time if time else datetime.now()

    def update(self, new_place):
        self.place = new_place
        self.update_time = self.get_current_time(None)

    def delete(self):
        pass

    def add_place(self, additional_place):
        self.place += ", " + additional_place
        self.update_time = self.get_current_time(None)

    def remove_place(self, removed_place):
        places = [p.strip() for p in self.place.split(",")]
        if removed_place in places:
            places.remove(removed_place)
            self.place = ", ".join(places)
            self.update_time = self.get_current_time(None)
        else:
            print(f"{removed_place} not found in places")

    def __str__(self):
        return f"City: {self.name}, Country: {self.country}, Place: {self.place}"
