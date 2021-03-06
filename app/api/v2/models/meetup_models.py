from datetime import datetime, timedelta
from .base_model import BaseModel


class MeetupModel(BaseModel):
    """ CLass for meetups model."""

    table = 'meetups'

    def save(self, data):
        """ save a new meetup."""
        tags = '{'
        
        for tag in data['tags']:
            tags += '"'+ tag +'",'
        tags = tags[:-1] + '}'

        query = "INSERT INTO {} (topic, description, tags, location, happeningOn) \
        VALUES ('{}','{}','{}','{}','{}') RETURNING *".format(self.table, data['topic'], data['description'], tags, data['location'], data['happeningOn']) 
        self.cur.execute(query)
        result = self.cur.fetchone()
        self.conn.commit()
        return result

    def exists(self, key, value):
        """ search item by key value pair."""
        query = "SELECT * FROM {} WHERE {} = '{}'".format(self.table, key, value)
        self.cur.execute(query)
        result = self.cur.fetchall()
        return len(result) > 0


    def getOne(self, id):
        """ Get a specific meetup."""
        meetup = self.where('id', id)
        return meetup

    def getAll(self):
        query = "SELECT * FROM {}".format(self.table)
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def where(self, key, value):
        query = "SELECT * FROM {} WHERE {} = '{}'".format(self.table, key, value)
        self.cur.execute(query)
        result = self.cur.fetchone()
        return result

    def delete(self, id):
        query = "DELETE FROM {} WHERE id = {}".format(self.table, id)
        self.cur.execute(query)
        self.conn.commit()
        return True

    def meetupTags(self, meetup_id, meetup_tags):
        """  update meetup tags """

        meetup = self.where('id', meetup_id)
        new_tags = list(set(meetup_tags + meetup['tags']))

        tags = '{'

        for tag in new_tags:
            tags += '"' + tag + '",'

        tags = tags[:-1] + '}'

        query = "UPDATE {} SET tags = '{}' WHERE id = '{}' \
        RETURNING *".format(self.table, tags, meetup_id)
        self.cur.execute(query)
        self.conn.commit()
        return self.cur.fetchone()

    def usersAttending(self, meetup_id):
        """ Get users attending an upcoming meetup."""
        query = "SELECT id, firstname, lastname, email FROM users WHERE \
        id IN ( SELECT user_id FROM rsvps WHERE meetup_id = '{}' AND response = 'yes')".format(meetup_id)

        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def getUpcomings(self):
        """ Get all upcoming meetups in the next 1 week """

        today = datetime.now().strftime('%d/%m/%Y')
        endWeek = (datetime.now() + timedelta(days=7)).strftime('%d/%m/%Y')
        query = "SELECT * FROM {} WHERE happeningOn BETWEEN '{}' AND '{}'".format(self.table, today, endWeek)
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def check_if_duplicate(self, data):
        """ Check for duplicate meetups."""

        query = "SELECT * FROM {} WHERE topic = '{}' AND location = '{}'\
        ".format(self.table, data['topic'], data['location'])
        self.cur.execute(query)
        result = self.cur.fetchone()

        if result:
            return True, 'Meetup with same topic at the same venue already exists'

        query = "SELECT * FROM {} WHERE happeningOn = '{}' AND location = '{}'\
        ".format(self.table, data['happeningOn'], data['location'])
        self.cur.execute(query)
        result = self.cur.fetchone()

        if result:
            return True, 'Meetup happening the same date at the same venue already exists'

        query = "SELECT * FROM {} WHERE topic = '{}' AND happeningOn = '{}'\
        ".format(self.table, data['topic'], data['happeningOn'])
        self.cur.execute(query)
        result = self.cur.fetchone()

        if result:
            return True, 'Meetup happening the same date with same topic \
            already exists'

        return False, None
    
         





