from datetime import datetime
from model.base import Base

class City(Base):
    """
    A class representing a city.
    """
    def __init__(self, name, population, country_code):
        super().__init__()
        self.name = name
        self.population = population
        self.country_code = country_code
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'population': self.population,
            'country_code': self.country_code,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __str__(self):
        return f"City: {self.name}, Population: {self.population}, Country Code: {self.country_code}, Last Updated: {self.updated_at}"
