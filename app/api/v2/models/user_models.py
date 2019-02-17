from werkzeug.security import generate_password_hash, check_password_hash

from .base_model import BaseModel




class UserModel(BaseModel):
    """ Users model."""
    
    table = 'users'
    
    @staticmethod   
    def checkpwdhash(hashed_pwd, pwd):
        """ Check password hashes match."""
        return check_password_hash(hashed_pwd, pwd)

    #taable users
    def save(self, data):
        """ Save new user."""
        query = "INSERT INTO {} (firstname, lastname, username, email, password)\
        VALUES('{}', '{}', '{}', '{}', '{}') RETURNING *".format(self.table, data['firstname'],
        data['lastname'], data['username'], data['email'], generate_password_hash(data['password']))
        return self.insert(query)

    def exists(self, key, value):
        """ Check if user exists."""
        query = "SELECT * from {} WHERE {} = '{}'".format(self.table, key, value)    
        result = self.fetchAll(query)
        return len(result) > 0

    def where(self, key, value):
        """ Fetch user."""
        query = "SELECT * FROM {} WHERE {} = '{}'".format(self.table, key, value)
        return self.fetchOne(query) 

    # def isAdmin(self, user_id):
    #     user = self.where('isAdmin', user_id) 
    #     return user['id']

    def isAdmin(self, user_id):
        user = self.where('id', user_id)
        return user['isadmin']    

       
    # def isAdmin(self, user_id):
    #     user = self.where('id', user_id) 
    #     print('########isAdmin##### at usermodels#####',user)
    #     return user['isAdmin']

    def getOne(self, id):
        """ Get user profile."""

        questions_query = "SELECT COUNT(DISTINCT id)\
        FROM questions WHERE user_id = '{}'".format(id)

        questions_asked = self.fetchOne(questions_query)

        comments_query = "SELECT COUNT(DISTINCT question_id)\
        FROM comments WHERE user_id = '{}'".format(id)

        questions_commented = self.fetchOne(comments_query)

        query = "SELECT users.id, users.firstname, users.lastname, users.username\
        FROM users WHERE id = '{}'".format(id)

        result = self.fetchOne(query)

        result.update({
            'questions_asked': questions_asked['count'],
            'questions_commented': questions_commented['count']
            })
        return result    

   



    

