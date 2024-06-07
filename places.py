#!usr/bin/python3
""" Class Place with the necessary attributes and methods."""

from datetime import datetime
import uuid


class Place():
    def __init__(self, id,  name, description, address,
                 city, latitude, longitude, host,
                 number_of_rooms, bathrooms, price_per_night, max_guests):
        self.id = str(uuid.uuid4())
        self_id = id
        self_name = name
        self_description = description
        self_address = address
        self_city = city
        self_latitude = latitude
        self_longitude = longitude
        self_host = host
        self_number_of_rooms = number_of_rooms
        self_bathrooms = bathrooms
        self_price_per_night = price_per_night
        self_max_guests = max_guests
        self.amenities = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def remove_amenity(self, amenity):
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
