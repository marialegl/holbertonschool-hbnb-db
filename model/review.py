#!usr/bin/python3
""" Class Review with the necessary attributes and methods."""

from datetime import datetime
from model.base import Base

class Review(Base):
    def __init__(self, user, place, text, rating):
        super().__init__()
        self.user = user
        self.place = place
        self.text = text
        self.rating = rating
        self.deleted = False
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

    def update(self, **kwargs):
        if self.deleted:
            raise ValueError("Cannot update a deleted review.")
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.update_time = datetime.now()

    def delete(self):
        self.deleted = True

    def __str__(self):
        return f"Review({self.id}, {self.user}, {self.place}, {self.rating})"
