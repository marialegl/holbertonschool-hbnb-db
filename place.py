#!usr/bin/python3
""" Class Place with the necessary attributes and methods."""

from datetime import datetime
import uuid


class Place():
    def __init__(self, id, name, description, address,
                 city, latitude, longitude, host,
                 number_of_rooms, bathrooms, price_per_night, max_guests):
        self.id = str(uuid.uuid4())
        self.name = name
        self.description = description
        self.address = address
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.number_of_rooms = number_of_rooms
        self.bathrooms = bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenities = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
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
        self.updated_at = datetime.now()

    def delete(self):
        del self

    def __str__(self):
        return f"Place({self.id}, {self.name}, {self.city}, {self.host})"
