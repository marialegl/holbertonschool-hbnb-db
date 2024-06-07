#!usr/bin/python3
""" Class Review with the necessary attributes and methods."""

from datetime import datetime
import uuid


class Review:
    def __init__(self, user, place, text, rating):
        self.id = str(uuid.uuid4())
        self.user = user
        self.place = place
        self.text = text
        self.rating = rating
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.deleted = False
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

    def update(self, **kwargs):
        if self.deleted:
            raise ValueError("Cannot update a deleted review.")
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()

    def delete(self):
        self.deleted = True

    def __str__(self):
        return f"Review({self.id}, {self.user}, {self.place}, {self.rating})"
