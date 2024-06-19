#!usr/bin/python3
""" Class Place with the necessary attributes and methods."""

from datetime import datetime
from model.base import Base


class Place(Base):
    def __init__(self, name, description, address,
                 city, latitude, longitude, host_id,
                 number_of_rooms, number_of_bathrooms,
                 price_per_night, max_guests, amenities=[]):

        super().__init__()
        self.name = name
        self.description = description
        self.address = address
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.host_id = host_id
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenities = amenities

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'address': self.address,
            'city': self.city.to_dict() if self.city else None,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'host_id': self.host_id,
            'number_of_rooms': self.number_of_rooms,
            'number_of_bathrooms': self.number_of_bathrooms,
            'price_per_night': self.price_per_night,
            'max_guests': self.max_guests,
            'amenities': [amenity.to_dict() for amenity in self.amenities],
            'created_at': self.create_time.isoformat(),
            'updated_at': self.update_time.isoformat()
        }

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
