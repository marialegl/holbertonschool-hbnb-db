#!usr/bin/python3
from persistence.persistence_manager import IPersistenceManager
from persistence.database import db

class DataManager(IPersistenceManager):
    """
    Implements the persistence manager using SQLAlchemy for database operations.
    """
    
    def save(self, entity):
        db.session.add(entity)
        db.session.commit()

    def get(self, entity_type, entity_id):
        """
        Retrieves an entity by its ID and type.
        
        Args:
            entity_type: The type of the entity to retrieve.
            entity_id: The ID of the entity to retrieve.
            
        Returns:
            The entity instance or None if not found.
        """
        return db.session.get(entity_type, entity_id)

    def update(self, entity):
        """
        Updates an entity in the database.
        
        Args:
            entity: The entity instance with updated data.
        """
        db.session.commit()

    def delete(self, entity):
        """
        Deletes an entity from the database.
        
        Args:
            entity: The entity instance to delete.
        """
        db.session.delete(entity)
        db.session.commit()

    def query_all(self, entity_type):
        """
        Retrieves all entities of a specific type.
        
        Args:
            entity_type: The type of entities to retrieve.
            
        Returns:
            A list of entity instances.
        """
        return db.session.query(entity_type).all()

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
