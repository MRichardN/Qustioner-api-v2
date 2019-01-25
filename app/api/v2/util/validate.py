
import re
import time
from datetime import datetime
from marshmallow import ValidationError


def password(pwd):
    """ check password meets requirements."""
    if len(pwd) not in range(6, 13):
        raise ValidationError('password must be between 6 and 12 characters')

    if not re.search('[a-z]',pwd):
        raise ValidationError('password must atleast have a lower case character')

    if not re.search('[A-Z]', pwd):
        raise ValidationError('password must contain an upper case letter') 

    if not re.search('[0-9]', pwd):
        raise ValidationError('password must contain a numeric character') 


def email(value):
    """ check email format."""
    if not re.match(r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)", value):
        raise ValidationError('Invalid email format')
    return value

def required(value):
    """Check a field does not contain null entries."""

    if isinstance(value, str):
        if not value.strip(' '):
            raise ValidationError('This parameter cannot be null')
        return value
    return value

def date_checker(new_date):
    """ check date format(dd/mm/yyyy) or (dd-mm-yyyy) or (dd.mm.yyyy)."""
    if not re.match(r'^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d$', new_date):
        raise ValidationError('Invalid date format. Use (dd/mm/yyyy) or (dd-mm-yyyy) or (dd.mm.yyyy)')  
    future = time.strptime(new_date, "%d/%m/%Y" )
    present = time.strptime("25/01/2019", "%d/%m/%Y")
    if future < present:
        raise ValidationError('YOu cannot input date from the past')  

    # date1 = "31/12/2015"
    # date2 = "01/01/2016"
    # newdate1 = time.strptime(date1, "%d/%m/%Y")
    # newdate2 = time.strptime(date2, "%d/%m/%Y")

    # newdate1 > newdate2 will return False
    # newdate1 < newdate2 will return True

def notString(value):
    """ Check non unicode characters."""
    if type(value) is not str:
        raise ValidationError('Invalid string')
    return value    

def tag(tags):
    """ Validate meetup tags are present """

    if not tags and not len(tags) > 0:
        raise ValidationError('You need to pass atleast 1 tag for the meetup')

      




   
        