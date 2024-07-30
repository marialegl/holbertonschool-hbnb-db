#!/usr/bin/python3
from datetime import datetime

from flask_bcrypt import Bcrypt
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from model.base import Base, db

bcrypt = Bcrypt()


class User(Base):
    """
        This class will inherit the atributes
        to the class Host and Guest
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
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


# class Host(User):
#     __tablename__ = 'hosts'
#
#     id = Column(db.String(36), db.ForeignKey('users.id'), primary_key=True)
#     name_place = relationship("Place", back_populates="host")
#     amenities = relationship("Amenities", secondary="user_amenities")
#
#     def add_place(self, place):
#         self.name_place.append(place)
#
#     def remove_place(self, place):
#         self.name_place.remove(place)
#
#     def add_amenities(self, amenities):
#         self.amenities.append(amenities)
#
#     def remove_amenities(self, amenities):
#         self.amenities.remove(amenities)
#
#
# class Guest(User):
#     __tablename__ = 'guests'
#
#     id = Column(String(36), db.ForeignKey('users.id'), primary_key=True)
#     comment = relationship("Review", back_populates="guest")
#
#     def add_review(self, comment):
#         self.comment.append(comment)
#
#     def remove_review(self, comment):
#         self.comment.remove(comment)
