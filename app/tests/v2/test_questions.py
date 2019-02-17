from .base_test import BaseTest


class TestQuestion(BaseTest):
    """ Test class for question."""

    def setUp(self):
        super().setUp()

        self.meetup = {
            'topic': 'TDD',
            'description': 'Software development the TDD way is very crucial',
            'location': 'Moringa School',
            'happeningOn': '27/01/2019',
            'tags': ['Python', 'Tests']
        }

        self.question1 = {
            'title': 'TDD way',
            'body': 'Are we supposed to write tests or code?',
            'meetup_id': 1
        }

        self.question2 = {
            'title': 'Test_db',
            'body': 'Do we create a separate db for tests?',
            'meetup_id': 1,
        }

        test = self.client.post('/api/v2/meetup/', json=self.meetup, headers=self.headers)

        print('### test-post meetup::', test)

    def tearDown(self):
        super().tearDown()

    def test_post_question_meetup_not_created(self):
        """ Test post question to meetup that doesn't exist """

        self.question1.update({'meetup_id': 115})

        res = self.client.post('/api/v2/question/', json=self.question1,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Meetup not found')

    def test_post_question_without_meetup_id(self):
        """ Test post question to meetup without meetup id """

        self.question1.pop('meetup_id', None)

        res = self.client.post('/api/v2/question/', json=self.question1,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data.')

    def post_question_no_data(self):
        """ Test post question with no data sent """

        res = self.client.post('/api/v2/question/', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data sent')

    def test_post_question_empty_data(self):
        """ Test post question with empty data sent """

        self.question1.clear()

        res = self.client.post('/api/v2/question/', json=self.question1,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

    def test_post_question_missing_fields(self):
        """ Test post question with missing fields in data sent """

        self.question1.pop('body', None)

        res = self.client.post('/api/v2/question/', json=self.question1,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'Invalid data.')

    def test_post_question(self):
        """ Test post question successfully """

        res = self.client.post('/api/v2/question/', json=self.question1,
                               headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Question posted successfully')

    def test_fetch_all_questions_meetup_not_created(self):
        """ Test fetch all questions for a meetup that doesn't exist """

        res = self.client.get('/api/v2/meetups/99/questions/')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Meetup not found')

    def test_fetch_all_questions_empty(self):
        """ Test fetch all questions for a meetup with none posted """

        res = self.client.get('/api/v2/meetups/1/questions/')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 0)

    def test_fetch_all_questions(self):
        """ Test fetch all questions for a meetup """

        self.client.post('/api/v2/question/', json=self.question1,
                         headers=self.headers)
        self.client.post('/api/v2/question/', json=self.question2,
                         headers=self.headers)

        res = self.client.get('/api/v2/meetups/1/questions/')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 2)

    def test_upvote_question_not_posted(self):
        """ Test upvote for question that hasn't been posted """

        res = self.client.patch('/api/v2/question/3/upvote/',
                                headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Question not found')

    def test_upvote_question(self):
        """ Test upvote question successfully """

        self.client.post('/api/v2/question/', json=self.question1, headers=self.headers)

        res = self.client.patch('/api/v2/question/1/upvote/', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Question up-voted')
        self.assertEqual(data['data']['votes'], 1)                    

    def test_downvote_question_not_posted(self):
        """ Test downvote for question that hasn't been posted """

        res = self.client.patch('/api/v2/question/10/downvote/',
                                headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['error'], 'Question not found')

    def test_downvote_question(self):
        """ Test downvote question successfully """

        self.client.post('/api/v2/question/', json=self.question1,
                         headers=self.headers)

        res = self.client.patch('/api/v2/question/1/downvote/',
                                headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(data['message'], 'Question down-voted')
        self.assertEqual(data['data']['votes'], -1)
 