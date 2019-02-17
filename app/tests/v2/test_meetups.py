from .base_test import BaseTest


class TestMeetup(BaseTest):
    """ Test class for meetups."""

    def setUp(self):
        super().setUp()

        self.user = {
            'firstname': 'John',
            'lastname': 'Doe',
            'username': 'Mr Bean',
            'email': 'mrbean@gmail.com',
            'password': 'MrB3@n',
            'phoneNumber': '0700000000'
        }

        self.meetup1 = {
            'topic': 'TDD',
            'description': 'SOftware development the TDD way is very crucial',
            'location': 'Moringa School',
            'happeningOn': '27/01/2019',
            'tags': ['Python', 'pytest']
        }

        self.meetup2 = {
            'topic': 'Postgres',
            'description': 'Insering data with INSERT statement',
            'location': 'PAC',
            'happeningOn': '28/01/2019',
            'tags': ['python', 'databases']
        }

    def tearDown(self):
        super().tearDown()

  
    def test_create_meetup_with_empty_data(self):
        """ Test create meetup with no data sent."""

        self.meetup1.clear()

        res = self.client.post('/api/v2/meetup/', json=self.meetup1,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_create_meetup_with_missing_fields(self):
        """ Test create meetup with missing fields in request """

        self.meetup1.pop('location', None)

        res = self.client.post('/api/v2/meetup/', json=self.meetup1,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data')

    def test_create_meetup_With_empty_fields(self):
        """ Test create meetup with empty fields."""

        self.meetup1.update({'desciption': ''})

        res = self.client.post('/api/v2/meetup/', json=self.meetup1,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data')

    def test_create_meetup(self):
        """ Test create meetup successfully """

        res = self.client.post('/api/v2/meetup/', json=self.meetup1,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Meetup created')

    def test_create_meetup_invalid_email(self):
        """ Test create meetup with an invalid email."""

        self.meetup1.update({'email': 'mrbean.com'})

        res = self.client.post('/api/v2/meetup/', json=self.meetup1,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data')

    def test_create_meetup_with_past_date(self):
        """ Test create meetup with a past date."""

        self.meetup1.update({'happeningOn': '01/01/1940'})

        res = self.client.post('/api/v2/meetup/', json=self.meetup1,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data')

    def test_create_meetup_by_not_admin(self):
        """ Test create meetup not admin user."""

        resp = self.client.post('/api/v2/auth/register/', json=self.user)
        token = resp.get_json()['access_token']
        self.headers.update({'Authorization': 'Bearer {}'.format(token)})

        res = self.client.post('/api/v2/meetup/', json=self.meetup1,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['status'], 401)
        self.assertEqual(data['message'], 'You are not authorized')

    ##################
    def test_getAll_meetups_no_data(self):
        """ Test get all non existent meetups."""

        res = self.client.get('/api/v2/meetups/upcoming/')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 0)

    def test_getAll_meetups(self):
        """ Test get all meetups """

        self.client.post('/api/v2/meetup/', json=self.meetup1,
                         headers=self.headers)
        self.client.post('/api/v2/meetup/', json=self.meetup2,
                         headers=self.headers)

        res = self.client.get('/api/v2/meetups/upcoming/')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 2)

    def test_get_upcoming_meetups_nonexistent(self):
        """ Test get upcoming non-existent meetups."""

        res = self.client.get('/api/v2/meetups/upcoming/')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 0)

    def test_get_specific_upcoming_meetup(self):
        """ Test get  upcoming meetups """

        self.client.post('/api/v2/meetup/', json=self.meetup1,
                         headers=self.headers)

        res = self.client.get('/api/v2/meetups/1/')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 1)
    ####
    def test_get_upcoming_meetups_notexists(self):
        """ Test get upcoming meetups with none in the next 1 week"""

        self.meetup1.update({'happeningOn': '12/03/2019'})

        self.client.post('/api/v2/meetup/', json=self.meetup1,
                         headers=self.headers)
        self.client.post('/api/v2/meetup/', json=self.meetup2,
                         headers=self.headers)

        res = self.client.get('/api/v2/meetups/upcoming/')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 0)

    
    def test_get_non_existent_meetup(self):
        """ Test get a non existent meetup."""

        res = self.client.get('/api/v2/meetups/55/')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Meetup does not exist')

    def test_delete_meetup_not_eixists(self):
        """ Test delete non existent meetup."""

        res = self.client.delete('/api/v2/meetup/10/',
                                 headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Meetup not found')

    def test_delete_meetup(self):
        """ Test delete meetup successfully """

        self.client.post('/api/v2/meetup/', json=self.meetup1,
                         headers=self.headers)

        res = self.client.delete('/api/v2/meetup/1/', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Meetup Deleted')

    def test_delete_meetup_by_non_admin(self):
        """ Test delete meetup non authorized user."""

        resp = self.client.post('/api/v2/auth/register/', json=self.user)
        token = resp.get_json()['access_token']
        self.headers.update({'Authorization': 'Bearer {}'.format(token)})

        self.client.post('/api/v2/meetup/', json=self.meetup1,
                         headers=self.headers)

        res = self.client.delete('/api/v2/meetup/1/', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['status'], 401)
        self.assertEqual(data['message'], 'Unauthorized')

    def test_rsvps_for_meetup_not_created(self):
        """ Test RSVP for non-existent meetup."""

        res = self.client.post('/api/v2/meetups/3/yes/', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Meetup does not exist')

    def test_rsvps_meetup_for_invalid_rsvp(self):
        """ Test RSVP for invalid rsvp."""

        self.client.post('/api/v2/meetup/', json=self.meetup1,
                         headers=self.headers)

        res = self.client.post('/api/v2/meetups/1/notsure/',
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid rsvp')

    def test_rsvps_yes(self):
        """ Test RSVPs yes to a meetup."""

        self.client.post('/api/v2/meetup/', json=self.meetup1, headers=self.headers)

        res = self.client.post('/api/v2/meetups/1/yes/', headers=self.headers)
        data = res.get_json()

        print('################Check in test rsvps , line 280:: {}'.format(data))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Responded successfully')
        self.assertEqual(data['data']['response'], 'yes')

    def test_rsvps_no(self):
        """ Test RSVPs no to a meetup."""

        self.client.post('/api/v2/meetup/', json=self.meetup1,
                         headers=self.headers)

        res = self.client.post('/api/v2/meetups/1/no/', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Responded successfully')
        self.assertEqual(data['data']['response'], 'no')

    def test_rsvps_maybe(self):
        """ Test RSVPs maybe to a meetup."""

        self.client.post('/api/v2/meetup/', json=self.meetup1,
                         headers=self.headers)

        res = self.client.post('/api/v2/meetups/1/maybe/', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Responded successfully')
        self.assertEqual(data['data']['response'], 'maybe')

    def test_rsvps_already_responded(self):
        """ Test RSVPs for a meetup already responded to."""

        self.client.post('/api/v2/meetup/', json=self.meetup1,
                         headers=self.headers)
        self.client.post('/api/v2/meetups/1/yes/', headers=self.headers)

        res = self.client.post('/api/v2/meetups/1/yes/', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['status'], 403)
        self.assertEqual(data['message'], 'Already responded')
