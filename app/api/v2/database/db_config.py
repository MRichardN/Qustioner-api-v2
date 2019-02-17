import os
import logging
import sys
import psycopg2
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash
from psycopg2.extras import RealDictCursor
from instance.config import app_config
from ..database.db_tables import tables, table_queries




class DbConnection:
    """ Connection to DB"""

    def db_conn(self, config_name):  
        """ initiate database connection."""

        config = app_config[config_name]
        database = config.DATABASE_NAME
        user = config.DATABASE_USER
        password = config.DATABASE_PASSWORD
        host = config.DATABASE_HOST
        port = config.DATABASE_PORT

        db_url = 'dbname={} user={} password={} host={} port={}'.format(
            database, user, password, host, port
        )

        try:
            global conn, cur

            conn = psycopg2.connect(db_url)
            cur = conn.cursor(cursor_factory=RealDictCursor)

        except Exception as error:
            print('Error. Unable to connect to the database!')

            logger = logging.getLogger('Database_connection')
            logger.error(str(error))

            sys.exit(1)

    def dropTables(self):
        """ Function to drop tables."""
        try:
            for table in tables:
                cur.execute('DROP TABLE IF EXISTS {} CASCADE'.format(table))
            conn.commit()
        except (Exception, psycopg2.Error):
            raise ValidationError('An error occured creating tables')   

    def createTables(self):
        """ Function to create tables."""
        for query in table_queries:
            cur.execute(query)
        conn.commit()    

    def seed(self):
        admin = "SELECT * FROM users WHERE isAdmin = True  AND username = 'RichardN'"
        cur.execute(admin)
        result = cur.fetchone()

        if not result:
            cur.execute("INSERT INTO users (firstname, lastname, username, email, password, isAdmin)\
                VALUES ('Richard', 'Mathenge', 'RichardN', 'richardn@gmail.com', '{}', True)\
                ".format(generate_password_hash('Rich@2019')))
            conn.commit()

    def truncate(self):
        """ Truncate database tables."""
        cur.execute('TRUNCATE TABLE ' + ','.join(tables) + ' CASCADE')
        conn.commit()
            
    def insert(self, query):
        """ Save an item to the database."""
        cur.execute(query)
        result = cur.fetchone()
        conn.commit()
        return result

    def fetchOne(self, query):
        """ fetch a single item from the database."""
        cur.execute(query)
        result = cur.fetchone()
        return result

    
    def fetchAll(self, query):
        cur.execute(query)
        result = cur.fetchall()
        return result
        
    def remove(self, query): 
        cur.execute(query)
        conn.commit()
           
'''

    def createTables(self):
        """ Function to create tables."""
        for query in table_queries:
            cur.execute(query)

        conn.commit()

    def seed(self):
        admin = "SELECT * FROM users WHERE isAdmin = True AND username = RichardN"
        cur.execute(admin)
        result = cur.fetchone()

        if not result:
            cur.execute("INSERT INTO users (firstname, lastname, username, email, password, isAdmin)\
                VALUES ('Richard', 'Mathenge', 'RichardN', 'richardn@gmail.com', '{}', True)\
                ".format(generate_password_hash('Rich@2019')))
            conn.commit()        




    # db_url = os.getenv('DATABASE_URL')

    db_url = 'dbname={} host={} user={} password={} port={}'.format(database, host, user, password, port)

    try:
        conn = psycopg2.connect(db_url)

    except (Exception, psycopg2.Error) as error:
        print('Unable to connect to the database', error)

         # create logger
        logger = logging.getLogger('Database_connection')
        logger.setLevel(logging.ERROR)

        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)

        #create formatter
        formatter = logging.Formatter('%(asctime)s  -   %(name)s    -   %(levelname)s - %(message)s')
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        # application code
        logger.error(str(error))

        sys.exit(1)
       
    return conn  

'''


   