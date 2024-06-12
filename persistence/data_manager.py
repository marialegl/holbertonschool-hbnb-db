#!usr/bin/python3
from persistence_manager import IPersistenceManager


class DataManager(IPersistenceManager):
    """
    A concrete implementation of IPersistenceManager using in-memory storage.

    This class provides methods for saving, retrieving, updating, and deleting 
    entities in an in-memory storage dictionary. Each entity is stored based 
    on its type and a unique identifier.
    
    Attributes:
        storage (dict): A dictionary to store entities, organized by type.
    
    Methods:
        save(entity): Saves a new entity to the storage.
        get(entity_id, entity_type): Retrieves an entity by its ID and type.
        update(entity): Updates an existing entity in the storage.
        delete(entity_id, entity_type): Deletes an entity by its ID and type.
    """

    def __init__(self):
        """
        Initializes a new instance of DataManager with an empty storage dictionary.
        """
        self.storage = {}

    def save(self, entity):
        """
        Saves a new entity to the storage.

        The entity must have an 'id' field used as a unique identifier. Entities
        are stored in a nested dictionary structure, organized by their type and ID.
        
        Args:
            entity: The entity to be saved. It should be a dictionary-like object with
                    an 'id' key.
        
        Example:
            entity = {'id': '123', 'name': 'Alice'}
            data_manager.save(entity)
        """
        entity_id = entity.get('id')
        entity_type = type(entity).__name__
        if entity_type not in self.storage:
            self.storage[entity_type] = {}
        self.storage[entity_type][entity_id] = entity

    def get_all(self):
        """
        get s list of all users
        """
        return [entity for entity_type in self.storage.values()
                for entity in entity_type.values()] 

    def get(self, entity_id, entity_type):
        """
        Retrieves an entity from the storage by its ID and type.

        Args:
            entity_id: The unique identifier of the entity.
            entity_type: The type of the entity to retrieve.
        
        Returns:
            The entity if found, or None if not found.
        
        Example:
            entity = data_manager.get('123', 'dict')
        """
        return self.storage.get(entity_type, {}).get(entity_id, None)

    def update(self, entity):
        """
        Updates an existing entity in the storage.

        The entity must have an 'id' field used as a unique identifier. If the 
        entity exists in the storage, it will be updated with the new data.
        
        Args:
            entity: The entity with updated data. It should be a dictionary-like object 
                    with an 'id' key.
        
        Example:
            updated_entity = {'id': '123', 'name': 'Alice', 'age': 30}
            data_manager.update(updated_entity)
        """
        entity_id = entity.get('id')
        entity_type = type(entity).__name__
        if entity_type in self.storage and entity_id in self.storage[entity_type]:
            self.storage[entity_type][entity_id] = entity

    def delete(self, entity_id, entity_type):
        """
        Deletes an entity from the storage by its ID and type.

        Args:
            entity_id: The unique identifier of the entity.
            entity_type: The type of the entity to delete.
        
        Example:
            data_manager.delete('123', 'dict')
        """
        if entity_type in self.storage:
            self.storage[entity_type].pop(entity_id, None)
