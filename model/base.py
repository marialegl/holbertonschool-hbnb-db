#!/usr/bin/python3
from datetime import datetime
import uuid
import os
from sqlalchemy import Column, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates, sessionmaker


# Determinar el motor de base de datos a utilizar
db_type = os.getenv('DB_TYPE', 'sqlite')
if db_type == 'postgresql':
    engine = create_engine('postgresql://username:password@localhost/mydatabase')
else:
    engine = create_engine('sqlite:///mydatabase.db')

Base = declarative_base(bind=engine)

class Base:
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    @validates('create_time', 'update_time')
    def convert_datetime(self, key, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value

    def save(self, session):
        """Save the object to the database."""
        session.add(self)
        session.commit()

    def delete(self, session):
        """Delete the object from the database."""
        session.delete(self)
        session.commit()

    def to_dict(self):
        """Convert the object to a dictionary."""
        return {
            'id': self.id,
            'create_time': self.create_time.isoformat(),
            'update_time': self.update_time.isoformat()
        }

Base.metadata.create_all(engine)
