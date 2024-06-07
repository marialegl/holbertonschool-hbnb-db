#!/usr/bin/python3

import uuid


class Country:
    """
    A class representing a country.
    """

    def __init__(self, id, name, cities=None):
        self.id = str(uuid.uuid4())
        self.id = id
        self.name = name
        self.cities = cities if cities else []

    def addCity(self, city):
        self.cities.append(city)

    def removeCity(self, city):
        if city in self.cities:
            self.cities.remove(city)
        else:
            print(f"{city} not found in cities")

    def update(self, new_name):
        self.name = new_name

    def delete(self):
        pass

    def __str__(self):
        cities_str = ', '.join(self.cities)
        return f"Country(ID: {self.id}, Name: {self.name}, Cities: [{cities_str}])"
