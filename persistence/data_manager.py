from config import config
from persistence.db_data_manager import DbDataManager
from persistence.json_data_manager import JsonDataManager
from persistence.persistence_manager import IPersistenceManager


class DataManager:

    __db_manager = None
    __json_manager = None

    def get_data_manager(self) -> IPersistenceManager:
        if config.USE_DB:
            if not self.__db_manager:
                self.__db_manager = DbDataManager()
            return self.__db_manager
        else:
            if not self.__json_manager:
                self.__json_manager = JsonDataManager()
            return self.__json_manager
