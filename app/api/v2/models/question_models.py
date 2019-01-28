from .base_model import BaseModel
    
class QuestionModel(BaseModel):
    """ Question Model."""
    
    table = 'questions'

    
    def save(self, data):
        """ Save a new question."""
        query = "INSERT INTO {} (title, body, meetup_id, user_id) \
        VALUES('{}','{}','{}', '{}') RETURNING *".format(self.table, data['title'], data['body'], data['meetup_id'], data['user_id'])
        self.cur.execute(query)
        result = self.cur.fetchone()
        self.conn.commit()
        return result

    def upvote(self, question_id):
        """ Upvote a question."""
        question = self.where('id', question_id)
        votes = question['votes'] + 1
        query = "UPDATE {} SET votes = '{}' WHERE id = '{}' RETURNING *".format(self.table, votes, question_id)
        self.cur.execute(query)
        self.conn.commit()
        return self.cur.fetchone()

    def downvote(self, question_id):
        """ Downvote a question."""
        question = self.where('id', question_id)
        votes = question['votes'] - 1
        query = "UPDATE {} SET votes = '{}' WHERE id = '{}' RETURNING *".format(self.table, votes, question_id)
        self.cur.execute(query)
        self.conn.commit()
        return self.cur.fetchone()
    
    def exist(self, key, value):
        """ check whether it exists."""
        query = "SELECT * FROM {} WHERE {} = '{}'".format(self.table, key, value)
        self.cur.execute(query)
        result = self.cur.fetchall()
        return len(result) > 0


    def where(self, key, value):
        query = "SELECT * FROM {} WHERE {} = '{}'".format(self.table, key, value)
        self.cur.execute(query) 
        result = self.cur.fetchone()
        return result

    
    def getOne(self, id):
        question = self.where('id', id)
        return question

    def getAll(self, id):
        """ get all questions for a meetup."""
        query = "SELECT * FROM {} WHERE meetup_id = {}".format(self.table, id)
        self.cur.execute(query)
        result = self.cur.fetchall()   
        return result 

    def delete(self, id):
        """ delete a question."""
        query = "DELETE FROM {} WHERE question_id = {}".format(self.table, id)
        self.cur.execute(query)
        self.conn.commit()
        return True
        



