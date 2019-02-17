from .base_test import BaseTest


class TestComments(BaseTest):
    """ Test class for comments."""

    def setUp(self):
        super().setUp()

        self.meetup = {
            'topic': 'Postgres Database',
            'description': 'Unable to connect to postgres as postgres',
            'location': 'TRM',
            'happeningOn': '20/01/2019',
            'tags': ['Python']
        }

        self.question = {
            'title': 'Psycopg2',
            'body': 'What is pyscopg2 used for?',
            'meetup_id': 1
        }

        self.comment1 = {
            'body': 'Why cant we use an ORM like SQLAlchemy'
        }

        self.comment2 = {
            'body': 'Learning to do things from scratch is the best thing'
        }
        
        self.client.post('/api/v2/meetup/', json=self.meetup, headers=self.headers)
        self.client.post('/api/v2/question/', json=self.question, headers=self.headers)

    def tearDown(self):
        super().tearDown()

###########failed not found
    def test_post_comment(self):
        """ Test post a comment."""
        print('######self.quiz', self.question)
        
        res = self.client.post('/api/v2/question/1/comments/', json=self.comment1, headers=self.headers)
        data = res.get_json()
        print('####### post data', data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(data['status'], 201)
        self.assertEqual(data['message'], 'Comment posted')


    def test_getAll_comments(self):
        """ Test get all comments for a specific question."""
        self.client.post('/api/v2/question/1/comments/', json=self.comment1,
                         headers=self.headers)
        self.client.post('/api/v2/question/1/comments/', json=self.comment2,
                         headers=self.headers)

        res = self.client.get('/api/v2/question/1/comments/')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 2)
'''
    ###########failed not found
    def test_post_comment_for__no_data_sent(self):
        """ Test post comment with no data sent."""

        res = self.client.post('/api/v2/question/<int:question_id>/comments/', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')    

    ###########failed not found url check
    def test_post_comment_for_nonexistent__question(self):
        """ Test post comment for non existent question."""

        
        res = self.client.post('/api/v2/question/8/comments/', headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Question not found')
    

    def test_post_comment_question_empty_data(self):
        """ Test post comment with empty data."""

        self.comment1.clear()

        res = self.client.post('/api/v2/question/1/comments/', json=self.comment1, headers=self.headers)
        data = res.get_json()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['status'], 400)
        self.assertEqual(data['message'], 'No data provided')

   
###########failed not found
    def test_getAll_comments_question_not_posted(self):
        """ Test get all comments for question not found."""

        res = self.client.get('/api/v2/question/22/comments/')
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['status'], 404)
        self.assertEqual(data['message'], 'Question not found')


    ###########failed not found
    def test_getAll_comments_for_question_without_comment(self):
        res = self.client.get('/api/v2/question/1/comments/')
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['status'], 200)
        self.assertEqual(len(data['data']), 0)
'''