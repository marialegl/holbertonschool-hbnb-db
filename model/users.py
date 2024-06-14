#!/usr/bin/python3
from datetime import datetime
import uuid  # Para generar IDs únicos
from .base import Base

class User(Base):
    """
    This class will inherit the attributes
    to the class Host and Guest
    """
    existing_email = set()

    def __init__(self, first_name, last_name, email, password):
        if email in User.existing_email:
            raise ValueError("Email already exists")
        self.id = str(uuid.uuid4())  # Generar un ID único
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.create_time = datetime.now()
        self.update_time = datetime.now()
        User.existing_email.add(email)

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
        self.update_time = datetime.now()  # Corregido de `self.updated_at`

    def delete(self):
        User.existing_email.discard(self.email)
        # Normalmente, se manejaría con lógica de eliminación de la base de datos

    def __str__(self):
        return f"User(Id: {self.id}, name: {self.first_name}, email: {self.email})"

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
