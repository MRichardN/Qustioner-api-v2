from .base_test import BaseTest


class TestUser(BaseTest):
    """ Test class for users."""

    def setUp(self):
        super().setUp()

        self.user = {
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'MrBean',
            'email': 'mrbean@gmail.com',
            'password': 'MrB3@nadf'
        }
    def tearDown(self):
        super().tearDown()

    def test_sign_up_no_data(self):
        """ Test signup with no data sent """

        res = self.client.post('/api/v2/auth/register/')
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_sign_up_empty_data(self):
        """ Test sign up sending empty data """

        self.user.clear()

        res = self.client.post('/api/v2/auth/register/', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_sign_up_empty_fields(self):
        """ Test sign up empty fields """

        self.user.update({'firstname': ' '})

        res = self.client.post('/api/v2/auth/register/', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data')

    def test_sign_up_invalid_password(self):
        """ Test sign up with an invalid password """

        self.user.update({'password': '12345'})

        res = self.client.post('/api/v2/auth/register/', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data')

    def test_sign_up_invalid_email(self):
        """ Test sign up with an invalid email """

        self.user.update({'email': 'mrbean.com'})

        res = self.client.post('/api/v2/auth/register/', json=self.user)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data')


