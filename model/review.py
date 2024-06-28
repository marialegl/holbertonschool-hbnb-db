#!usr/bin/python3
""" Class Review with the necessary attributes and methods."""

from datetime import datetime
from model.base import Base


class Review(Base):
    def __init__(self, user_id, place_id, rating, comment):
        super().__init__()
        self.user_id = user_id
        self.place_id = place_id
        self.rating = rating
        self.comment = comment
        self.deleted = False
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

    def to_dict(self):
        return{
            'id': self.id,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'rating': self.rating,
            'comment': self.comment,
            'created_at': self.create_time.isoformat(),
            'updated_at': self.update_time.isoformat()
        }


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
