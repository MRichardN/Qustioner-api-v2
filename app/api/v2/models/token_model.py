from .base_model import BaseModel


class RevokedTokenModel(BaseModel):
    """ Revoked tokens model."""

    table = 'revoked_tokens'

    def save(self, jti):
        """ Function to save new jti """

        query = "INSERT INTO {} (jti) VALUES ('{}')".format(self.table, jti)
        self.cur.execute(query)
        self.conn.commit()

    def blacklistedTokens(self, jti):
        """ check if jti is blacklisted """

        query = "SELECT * FROM {} where jti = '{}'".format(self.table, jti)
        self.cur.execute(query)
        result = self.cur.fetchone()
        return bool(result)
