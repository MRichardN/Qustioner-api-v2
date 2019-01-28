
import unittest
from flask import g
from app import create_app
from app.api.v2.database.db_tables import dropTables, seed
from app.api.v2.models.base_model import BaseModel

class BaseTest(unittest.TestCase):
    """ Base class for testcases."""

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = BaseModel()
        self.client = self.app.test_client()

        seed(g.conn)
        response = self.client.post('/api/v2/auth/login/', json={'username':'RichardN', 'password':'Rich@2019'})
        data = response.get_json()
        self.access_token = data['access_token']        
        self.refresh_token = data['refresh_token']
        self.headers = {'Authorization': 'Bearer {}'.format(self.access_token)}

    def tearDown(self):
        """ drop tables."""
        dropTables(g.conn)    
