from .base_model import BaseModel


class RsvpModel(BaseModel):
    """ rsvp model."""

    table = 'rsvps'

    def save(self, data):
        """ Save rsvp for a question."""

        query = "INSERT INTO {} (meetup_id, user_id, response) \
        VALUES('{}', '{}', '{}') RETURNING *".format(
            self.table, data['meetup_id'], data['user_id'], data['response']
        )
        return self.insert(query)

    def exists(self, meetup_id, user_id):
        """ Check if user has rsvped."""

        query = "SELECT * FROM {} WHERE user_id = '{}' AND meetup_id = '{}'\
        ".format(self.table, user_id, meetup_id)

        result = self.fetchOne(query)
        return bool(result)

    def usersAttending(self, meetup_id):
        """ Function to get number of attendees for a meetup """

        query = "SELECT * FROM {} WHERE meetup_id = '{}' AND response = '{}'\
        ".format(self.table, meetup_id, 'yes')
        #include Yes and YES

        result = self.fetchAll(query)
        return len(result)
