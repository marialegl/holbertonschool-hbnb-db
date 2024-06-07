#!/usr/bin/python3
from datetime import datetime
import uuid


class Users:
    """
        This class will inherit the atributes
        to the class Host and Guest
    """
    existing_email = set()

    def __init__(self, id_user, First_name, Last_name, email, password):

        if email in Users.existing_email:
            raise ValueError("This email already exists")

        self.id = str(uuid.uuid4())
        self.id = id_user
        self.First_name = First_name
        self.Last_name = Last_name
        self.email = email
        Users.existing_emails.add(email)
        self.password = password
        self.create_time = datetime.now()
        self.update_time = datetime.now()
        
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now() 

    def delete(self):
        del self

    def __str__(self):
        return f"User(Id:{self.id}, name:{self.First_name}, email:{self.email})"

class Host(Users):

    def __init__(self, id_user):
        super().__init__(id_user)
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

class Guest(Users):

    def __init__(self, id_user):

        super().__init__(id_user)
        self.comment = []

    def add_review(self, comment):
        self.comment.append(comment)
        

    def remove_review(self, comment):
        self.comment.remove(comment)
