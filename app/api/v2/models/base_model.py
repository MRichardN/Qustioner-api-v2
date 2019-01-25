from flask import g
from psycopg2.extras import RealDictCursor
from ..database.db_config import db_conn



class BaseModel():
    """ Initialize db connection."""

    def __init__(self):
        self.conn = self.check_db_conn()
        self.cur = self.conn.cursor(cursor_factory=RealDictCursor)

    @staticmethod
    def check_db_conn():
        """ Check if db_connection exists."""
        if 'conn' not in g:
            g.conn = db_conn()
            return g.conn
        return g.conn 
