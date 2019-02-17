import os
import logging
import sys
import psycopg2
from instance.config import app_config


config_name = os.getenv('APP_ENV')
config = app_config[config_name]


def db_conn():
    """ Intialize database connection."""
    database = config.DATABASE_NAME
    host = config.DATABASE_HOST
    user = config.DATABASE_USER
    password = config.DATABASE_PASSWORD
    port = config.DATABASE_PORT
    
    DSN = 'dbname={} user={} password={} host={} port={}'.format(
        database, user, password, host, port
    )

    try:
        conn = psycopg2.connect(DSN)

    except Exception as error:
        print('Error. Unable to establish Database connection')

        logger = logging.getLogger('database')
        logger.error(str(error))

        sys.exit(1)

    return conn




    # db_url = os.getenv('DATABASE_URL')
''' 
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


   