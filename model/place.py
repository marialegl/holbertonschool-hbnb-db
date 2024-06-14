#!usr/bin/python3
""" Class Place with the necessary attributes and methods."""

from datetime import datetime
from model.base import Base


class Place(Base):
    def __init__(self, name, description, address,
                 city, latitude, longitude, host,
                 number_of_rooms, number_bathrooms,
                 price_per_night, max_guests, amenities=[]):

        super().__init__()
        self.name = name
        self.description = description
        self.address = address
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenities = amenities
        self.host = host
        if self.host is not None:
            raise ValueError("This place already has a host")

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        if amenity in self.amenities:
            self.amenities.remove(amenity)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.update_time = datetime.now()

    def delete(self):
        del self

    def __str__(self):
        return f"Place({self.id}, {self.name}, {self.city}, {self.host})"
