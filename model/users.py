#!/usr/bin/python3
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from model.base import Base  # Asegúrate de tener db configurado en database.py

class User(db.Model):
    """
        This class will inherit the atributes
        to the class Host and Guest
    """
    __tablename__ = 'users'

    id = Column(String(36), primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

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
    __tablename__ = 'hosts'

    id = Column(String(36), primary_key=True)
    name_place = relationship("Place", back_populates="host")
    amenities = relationship("Amenities", secondary="user_amenities")

    def add_place(self, place):
        self.name_place.append(place)

    def remove_place(self, place):
        self.name_place.remove(place)

    def add_amenities(self, amenities):
        self.amenities.append(amenities)

    def remove_amenities(self, amenities):
        self.amenities.remove(amenities)


class Guest(User):
    __tablename__ = 'guests'

    id = Column(String(36), primary_key=True)
    comment = relationship("Review", back_populates="guest")

    def add_review(self, comment):
        self.comment.append(comment)

    def remove_review(self, comment):
        self.comment.remove(comment)
