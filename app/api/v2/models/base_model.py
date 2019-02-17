from abc import ABC
from ..database.db_config import DbConnection



class BaseModel(ABC, DbConnection):
    """ Initialize db connection."""

    def __init__(self):
        pass

    @staticmethod
    def check_db_conn():
        pass
