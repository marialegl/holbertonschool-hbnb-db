#!usr/bin/python3
from abc import ABC, abstractmethod


class IPersistenceManager(ABC):
    """
    Abstract interface for managing the persistence of entities.

    This class defines abstract methods that must be implemented by any class 
    wishing to handle data persistence to a data source, such as a database, 
    files, etc.
    """

    @abstractmethod
    def save(self, entity):
        pass

    @abstractmethod
    def get(self, entity_type, entity_id):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete(self, entity):
        pass

    @abstractmethod
    def get_all(self, entity_type):
        pass

    @abstractmethod
    def query_all_by_filter(self, entity_type, filter_condition):
        pass
