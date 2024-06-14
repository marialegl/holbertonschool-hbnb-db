#!/usr/bin/python3
from datetime import datetime
from model.base import Base

class User(Base):
    """
        This class will inherit the atributes
        to the class Host and Guest
    """
    existing_email = set()

    def __init__(self, first_name, last_name, email, password):

        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'create_time': self.create_time.isoformat(),
            'update_time': self.update_time.isoformat()
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.update_time = datetime.now()

    def delete(self):
        del self

    def __str__(self):
        return f"User(Id: {self.id}, name: {self.first_name},\
 email: {self.email})"


class Host(User):

    def __init__(self, first_name, last_name, email, password):
        super().__init__(first_name, last_name, email, password)
        self.name_place = []
        self.amenities = []

    def add_place(self, place):
        self.name_place.append(place)

    def remove_place(self, place):
        self.name_place.remove(place)

    def add_amenities(self, amenities):
        self.amenities.append(amenities)

    def remove_amenities(self, amenities):
        self.amenities.remove(amenities)


class Guest(User):

    def __init__(self, first_name, last_name, email, password):
        super().__init__(first_name, last_name, email, password)
        self.comment = []

    def add_review(self, comment):
        self.comment.append(comment)

    def remove_review(self, comment):
        self.comment.remove(comment)
