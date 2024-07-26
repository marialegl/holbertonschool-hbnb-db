from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from model.base import Base


class Country(Base):
    """
    A class representing a country.
    """
    __tablename__ = 'countries'

    id = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    states = relationship('State', back_populates='country')

    def __init__(self, name, states=None):
        super().__init__()
        self.name = name
        self.states = states if states else []

    def add_state(self, state):
        if state not in self.states:
            self.states.append(state)

    def remove_state(self, state):
        if state in self.states:
            self.states.remove(state)

    def update(self, new_name):
        self.name = new_name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'states': [state.to_dict() for state in self.states]
        }

    def __str__(self):
        states_str = ', '.join([state.name for state in self.states])
        return f"Country(ID: {self.id}, Name: {self.name}, States: [{states_str}])"
