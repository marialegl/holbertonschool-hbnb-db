#!usr/bin/python3
from flask import current_app, json
from persistence.persistence_manager import IPersistenceManager
from api import db


class DataManager(IPersistenceManager):
    """
    Implements the persistence manager using SQLAlchemy for database operations.
    """
    def __init__(self, file_path="data.json"):
        self.file_path = file_path
        if not current_app.config['USE_DATABASE']:
            self.storage = self.load_from_file()
        else:
            self.storage = None

    def load_from_file(self):
        """
        Loads data from the JSON file if it exists, otherwise returns an empty dictionary.
        """
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_to_file(self):
        """
        Saves the current storage dictionary to the JSON file
        """
        with open(self.file_path, "w") as file:
            json.dump(self.storage, file, indent=4, default=str)

    
    def save(self, entity):

        if current_app.config['USE_DATABASE']:
            db.session.add(entity)
            db.session.commit()
        else:
            entity_type = type(entity).__name__
            if entity_type not in self.storage:
                self.storage[entity_type] = {}
            self.storage[entity_type][entity.id] = entity.to_dict()
            self.save_to_file()


    def get(self, entity_type, entity_id):
        """
        Retrieves an entity by its ID and type.
        
        Args:
            entity_type: The type of the entity to retrieve.
            entity_id: The ID of the entity to retrieve.
            
        Returns:
            The entity instance or None if not found.
        """
        if current_app.config['USE_DATABASE']:
            return db.session.query(entity_type).get(entity_id)
        else:
            return self.storage.get(entity_type, {}).get(entity_id, None)

    def update(self, entity):
        """
        Updates an entity in the database.
        
        Args:
            entity: The entity instance with updated data.
        """
        if current_app.config['USE_DATABASE']:
            db.session.merge(entity)
            db.session.commit()
        else:
            entity_type = type(entity).__name__
            if entity_type in self.storage and entity.id in self.storage[entity_type]:
                self.storage[entity_type][entity.id] = entity.to_dict()
                self.save_to_file()

    def delete(self, entity_id, entity_type):
        """
        Deletes an entity from the database.
        
        Args:
            entity: The entity instance to delete.
        """
        if current_app.config['USE_DATABASE']:
            entity = db.session.query(entity_type).get(entity_id)
            if entity:
                db.session.delete(entity)
                db.session.commit()
        else:
            if entity_type in self.storage:
                self.storage[entity_type].pop(entity_id, None)
                self.save_to_file()

    def get_all(self, entity_type):
        """
        Retrieves all entities of a specific type.
        
        Args:
            entity_type: The type of entities to retrieve.
            
        Returns:
            A list of entity instances.
        """
        if current_app.config['USE_DATABASE']:
            return db.session.query(entity_type).all()
        else:
            if entity_type:
                return [entity for entity_type_key, entities in self.storage.items()
                        if entity_type_key == entity_type
                        for entity in entities.values()]
            else:
                return [entity for entities in self.storage.values()
                        for entity in entities.values()]

    def query_all_by_filter(self, entity_type, filter_condition):
        """
        Retrieves all entities of a specific type that match the filter condition.
        
        Args:
            entity_type: The type of entities to retrieve.
            filter_condition: A SQLAlchemy filter condition.
            
        Returns:
            A list of entity instances that match the filter condition.
        """
        return db.session.query(entity_type).filter(filter_condition).all()
