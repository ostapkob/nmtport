from datetime import datetime, timedelta
from app.model import Post, Mechanism
def shift_date():
    hour = datetime.now().hour
    if hour > 8 and hour < 20:
        date_shift = datetime.now()
        shift = 1
    elif hour < 8:
        date_shift = datetime.now() - timedelta(days=1)
        shift = 2
    else:
        date_shift = datetime.now()
        shift = 2
    return date_shift.date(), shift

def all_mechanisms_id():
    'Find all mechanisms id'''
    return [m.id for m in Mechanism.query.all()]


def all_number(type, number):
    '''Need to do then'''
    return [m.id for m in Mechanism.query.all()]

def in_hours(n):
    return round(n*600/7200, 3)


