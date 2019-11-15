from datetime import datetime, timedelta
from app.model import Post, Mechanism
from app import db

HOURS = 10
def today_shift_date():
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
    '''Find all mechanisms id'''
    return [m.id for m in Mechanism.query.all()]


def all_number(type, number):
    '''Need to do then'''
    return [m.id for m in Mechanism.query.all()]

# def in_hours(n):
#     return round(n/60, 3)

def multiple_5(date):
    '''Return time multiple 5 minutes and remite microseconds'''
    global HOURS
    # date -= timedelta(minutes=5)
    date += timedelta(hours=HOURS)
    mul5=date.minute-date.minute%5
    date_n = date.replace(minute=mul5, second=0, microsecond=0)
    return date_n

def time_for_shift(date_shift, shift):
    '''get dict with all minute's values for the period'''
    #get data from db
    cursor = db.session.query(Post).filter( Post.date_shift == date_shift, Post.shift == shift).order_by(Post.mechanism_id).all()

    #create dict all works mechanism in shift
    data_per_shift = {}
    for el in cursor:
        if data_per_shift.get(el.mech.name):
            data_per_shift[el.mech.name].append(el)
        else:
            data_per_shift[el.mech.name] = [el]


    # get start time for this shift
    start = datetime.combine(date_shift, datetime.min.time())
    if shift == 1:
        start=start.replace(hour=8, minute=0, second=0, microsecond=0)
    else:
        start=start.replace(hour=20, minute=0, second=0, microsecond=0)

    #create dict existing values by time
    existing_values = {}
    for key, values in data_per_shift.items():
        existing_values[key]={}
        for val in values:
            date_t = val.timestamp.replace(second=0, microsecond=0)
            date_t+=timedelta(hours=10)
            existing_values[key][date_t]=val.value

    #create dict with all minutes to now if value is not return (-1) because 0 may exist
    time_by_minuts ={}
    for key_m, values_m in existing_values.items():
        start_m=start
        time_by_minuts[key_m] = {}
        for i in range(60*12-1):
            start_m+=timedelta(minutes=1)
            time_by_minuts[key_m][start_m]= existing_values[key_m].setdefault(start_m, -1)
            if start_m>datetime.now():
                break

    return time_by_minuts





