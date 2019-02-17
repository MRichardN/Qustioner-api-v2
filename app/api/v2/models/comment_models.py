from ..database.db_config import DbConnection



class CommentModel(DbConnection):
    """ Comments model."""

    table = 'comments'


    
    def getAll(self, id):
        """ Get all question comments."""

        query = "SELECT * FROM {} WHERE question_id = {}".format(self.table, id)
        return self.fetchAll(query)

    def save(self, data):
        """ Save new comment."""

        query = "INSERT INTO {} (body, question_id, user_id) \
        VALUES ('{}', '{}', '{}') RETURNING *".format(
            self.table, data['body'], data['question_id'], data['user_id'])
        
        return self.insert(query)

    def where(self, key, value):
        query = "SELECT * FROM {} WHERE {} = '{}'".format(
            self.table, key, value)
        return self.fetchOne(query)

    def exist(self, key, value):
        """ check whether it exists."""
        query = "SELECT * FROM {} WHERE {} = '{}'".format(self.table, key, value)
        result = self.fetchAll(query)
        return len(result) > 0

    def check_duplicate(self, question_id, body):
        """ Function to check if comment is a duplicate """

        if self.exist('question_id', question_id):
            comment = self.where('question_id', question_id)

            if comment['body'] == body:
                return True

        return False    