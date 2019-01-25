from .base_model import BaseModel

class CommentModel(BaseModel):
    """ Comments model."""

    table = 'comments'


    
    def getAll(self, id):
        """ Get all question comments."""

        query = "SELECT * FROM {} WHERE question_id = {}".format(self.table, id)
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def save(self, data):
        """ Save new comment."""

        query = "INSERT INTO {} (body, question_id, user_id) \
        VALUES ('{}', '{}', '{}') RETURNING *".format(
            self.table, data['body'], data['question_id'], data['user_id'])

        self.cur.execute(query)
        result = self.cur.fetchone()
        self.conn.commit()
        return result