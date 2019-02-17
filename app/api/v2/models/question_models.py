from .base_model import BaseModel

    
class QuestionModel(BaseModel):
    """ Question Model."""
    
    table = 'questions'

    
    def save(self, data):
        """ Save a new question."""
        query = "INSERT INTO {} (title, body, meetup_id, user_id) \
        VALUES('{}','{}','{}', '{}') RETURNING *".format(self.table, data['title'], data['body'], data['meetup_id'], data['user_id'])
        return self.insert(query)

    def upvote(self, question_id):
        """ Upvote a question."""
        question = self.where('id', question_id)
        votes = question['votes'] + 1
        query = "UPDATE {} SET votes = '{}' WHERE id = '{}' RETURNING *".format(self.table, votes, question_id)
        return self.insert(query)

    def downvote(self, question_id):
        """ Downvote a question."""
        question = self.where('id', question_id)
        votes = question['votes'] - 1
        query = "UPDATE {} SET votes = '{}' WHERE id = '{}' RETURNING *".format(self.table, votes, question_id)
        return self.insert(query)
    
    def exist(self, key, value):
        """ check whether it exists."""
        query = "SELECT * FROM {} WHERE {} = '{}'".format(self.table, key, value)
        result = self.fetchAll(query)
        return len(result) > 0


    def where(self, key, value):
        query = "SELECT * FROM {} WHERE {} = '{}'".format(self.table, key, value)
        return self.fetchOne(query)

    
    # def getOne(self, id):
    #     question = self.where('id', id)
    #     return question

    def getAll(self, id):
        """ fetch all questions for a specific meetup."""
        """ get all questions for a meetup."""
        query = "SELECT * FROM {} WHERE meetup_id = {}".format(self.table, id)
        return self.fetchAll(query)
        
    # def delete(self, id):
    #     """ delete a question."""
    #     query = "DELETE FROM {} WHERE question_id = {}".format(self.table, id)
    #     self.remove(query)
    #     return True
        

    def checkIfDuplicate(self, meetup_id, body):
        """ check for duplicate questions."""
        if self.exist('meetup_id', meetup_id):
            question = self.where('meetup_id', meetup_id)
            print('####### Q body', question)
            print('####### R body', body)
            if question['body'] == body:
                return True
        return False
