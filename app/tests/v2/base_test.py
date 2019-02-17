import unittest
from app import create_app
from app.api.v2.database.db_config import DbConnection

class BaseTest(unittest.TestCase):
    """ Base class for testcases."""

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
                
        res = self.client.post('/api/v2/auth/login/', json={'username':'RichardN', 'password':'Rich@2019'})
        #data = res.get_json
        self.access_token = res.get_json()['access_token']        
        self.refresh_token = res.get_json()['refresh_token']
        self.headers = {'Authorization': 'Bearer {}'.format(self.access_token)}

        print('## self.app::', self.app)
        print('## self.client::', self.client)
        print('## res::', res)
        print('## self.access-token::', self.access_token)
        print('## self.refresh_token::', self.refresh_token)
        print('## self.headers::', self.headers)

    def tearDown(self):
        """ drop database tables."""
        db_conn = DbConnection()
        print('###db_conn::', db_conn)
        db_conn.db_conn('testing')
        db_conn.dropTables()
