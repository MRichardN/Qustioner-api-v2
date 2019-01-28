import unittest
from app import create_app


class TestDevelopmentConfig(unittest.TestCase):
    """ Test class for Development config."""

    def setUp(self):
        """ Initialize app."""

        self.app = create_app('development')

    def test_app_is_development(self):
        """ Test app is in development configuration """

        self.assertEqual(self.app.config['DEBUG'], True)
        self.assertEqual(self.app.config['TESTING'], False)

    def tearDown(self):
        """ Clear initialized app """

        self.app = None


class TestTestingConfig(unittest.TestCase):
    """ Test class for Testing config """

    def setUp(self):
        """ Initialize Flask app """

        self.app = create_app('testing')

    def test_app_is_testing(self):
        """ Test app is in testing configuration """

        self.assertEqual(self.app.config['DEBUG'], False)
        self.assertEqual(self.app.config['TESTING'], True)

    def tearDown(self):
        """ Clear initialized app """

        self.app = None


class TestStagingConfig(unittest.TestCase):
    """ Test class for Staging config """

    def setUp(self):
        """ Initialize Flask app """

        self.app = create_app('staging')

    def test_app_is_staging(self):
        """ Test app is in staging configuration """

        self.assertEqual(self.app.config['DEBUG'], True)
        self.assertEqual(self.app.config['TESTING'], False)

    def tearDown(self):
        """ Clear initialized app """

        self.app = None


class TestProductionConfig(unittest.TestCase):
    """ Test class for Production config """

    def setUp(self):
        """ Initialize Flask app """

        self.app = create_app('production')

    def test_app_is_production(self):
        """ Test app is in production configuration """

        self.assertEqual(self.app.config['DEBUG'], False)
        self.assertEqual(self.app.config['TESTING'], False)

    def tearDown(self):
        """ Clear initialized app """

        self.app = None
