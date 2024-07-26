from datetime import datetime

from sqlalchemy import Column, String, Integer

from model.base import Base


class City(Base):
    """
    A class representing a city.
    """
    __tablename__ = 'cities'

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    population = Column(Integer, nullable=False)
    country_code = Column(String(5), nullable=False)

    def __init__(self, name, population, country_code):
        super().__init__()
        self.name = name
        self.population = population
        self.country_code = country_code

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.update_time = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'population': self.population,
            'country_code': self.country_code,
            'created_at': self.create_time.isoformat(),
            'updated_at': self.update_time.isoformat()
        }

    def __str__(self):
        return f"City: {self.name}, Population: {self.population}, Country Code: {self.country_code}, Last Updated: {self.update_time}"
