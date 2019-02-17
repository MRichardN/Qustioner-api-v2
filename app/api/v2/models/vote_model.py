#from .base_model import BaseModel
from app.api.v2.models.base_model import BaseModel
#from ..database.db_config import DbConnection


class VotesModel(BaseModel):
    """ class for votes model."""

    table = 'votes'

    def checkVote(self, question_id, user_id):
        """ check whether user has voted."""
        query = "SELECT * FROM {} WHERE question_id = '{}' AND user_id = '{}'".format(self.table, question_id, user_id)
        return self.fetchOne(query)

    def addNewVote(self, data):
        """ add new vote."""
        query = "INSERT INTO {} (question_id, user_id, vote)\
        VALUES('{}', '{}','{}') RETURNING *".format(self.table, data['question_id'], 
                                        data['user_id'], data['vote'])
        self.insert(query)

    def changeVote(self, data):
        """ change Current Vote """
        query = "UPDATE {} SET vote = '{}' WHERE question_id = '{}' AND user_id = '{}' RETURNING *".format(self.table, data['vote'], data['question_id'], data['user_id'])
        return self.insert(query)
  