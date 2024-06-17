#!/usr/bin/python3
from datetime import datetime
import uuid


class Base:
    """
        This class will inherit the atributes
        to the class Host and Guest
    """

    def __init__(self):

        self.id = str(uuid.uuid4())
        self.create_time = datetime.now()
        self.update_time = datetime.now()
