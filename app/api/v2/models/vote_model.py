#from .base_model import BaseModel
from app.api.v2.models.base_model import BaseModel


class VotesModel(BaseModel):
    """ class for votes model."""

    table = 'votes'

    def checkVote(self, question_id, user_id):
        """ check whether user has voted."""
        query = "SELECT * FROM {} WHERE question_id = '{}' AND user_id = '{}'".format(self.table, question_id, user_id)
        self.cur.execute(query)
        result = self.cur.fetchone()
        return result

    def addNewVote(self, data):
        """ add new vote."""
        query = "INSERT INTO {} (question_id, user_id, vote) \
        VALUES('{}', '{}','{}')".format(self.table, data['question_id'], data['user_id'], data['vote'])
        self.cur.execute(query)
        self.conn.commit()
  