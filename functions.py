from datetime import datetime, timedelta
from flask import render_template, flash
from app.model import Post, Mechanism
from app import db
from pprint import pprint
HOURS = 10


def today_shift_date():
    '''get date and shift'''
    hour = datetime.now().hour
    if hour >= 8 and hour < 20:
        date_shift = datetime.now()
        shift = 1
    elif hour < 8:
        date_shift = datetime.now() - timedelta(days=1)
        shift = 2
    else:
        date_shift = datetime.now()
        shift = 2
    return date_shift.date(), shift


def all_mechanisms_id(type=None):
    '''Find all mechanisms id'''
    if type == None:
        return [m.id for m in db.session.query(Mechanism).all()]
    return [m.id for m in db.session.query(Mechanism).filter(Mechanism.type == type).all()]

def all_mechanisms_type():
    '''Find all mechanisms type'''
    ls = [m.type for m in db.session.query(Mechanism).all()]
    return set(ls)

def all_number(type, number):
    '''Need to do then'''
    return [m.id for m in Mechanism.query.all()]

def multiple_5(date): #not use
    '''Return time multiple 5 minutes and remite microseconds'''
    global HOURS
    # date -= timedelta(minutes=5)
    date += timedelta(hours=HOURS)
    mul5 = date.minute - date.minute % 5
    date_n = date.replace(minute=mul5, second=0, microsecond=0)
    return date_n






def image_mechanism(value, type_mechanism, number, last_time):
    dt = datetime.now()- last_time
    dt =dt.total_seconds()/60
    if type_mechanism=="usm":
        if dt > 120.0:
            return './static/numbers/'+str(type_mechanism)+'/gray/'+str(number)+'.png'
        if dt >= 3.0:
            return './static/numbers/'+str(type_mechanism)+'/red/'+str(number)+'.png'
        if value<0.1:
            return './static/numbers/'+str(type_mechanism)+'/yellow/'+str(number)+'.png'
        else:
            return './static/numbers/'+str(type_mechanism)+'/green/'+str(number)+'.png'

    if type_mechanism=="kran":
        if dt > 120.0:
            return './static/numbers/'+str(type_mechanism)+'/gray/'+str(number)+'.png'
        if dt >= 5.0:
            return './static/numbers/'+str(type_mechanism)+'/red/'+str(number)+'.png'
        if value==1:
            return './static/numbers/'+str(type_mechanism)+'/black/'+str(number)+'.png'
        if value==2:
            return './static/numbers/'+str(type_mechanism)+'/blue/'+str(number)+'.png'
        else:
            return './static/numbers/'+str(type_mechanism)+'/yellow/'+str(number)+'.png'



# not use
def time_for_shift_list(date_shift, shift): #not use
    '''get dict with all minute's values for the period'''
    # get data from db
    cursor = db.session.query(Post).filter(
        Post.date_shift == date_shift, Post.shift == shift).order_by(Post.mechanism_id).all()

    # create dict all works mechanism in shift
    data_per_shift = {}
    for el in cursor:
        if data_per_shift.get(el.mech.name):
            data_per_shift[el.mech.name].append(el)
        else:
            data_per_shift[el.mech.name] = [el]

    # get start time for this shift
    start = datetime.combine(date_shift, datetime.min.time())
    if shift == 1:
        start = start.replace(hour=8, minute=0, second=0, microsecond=0)
    else:
        start = start.replace(hour=20, minute=0, second=0, microsecond=0)

    # create dict existing values by time
    existing_values = {}
    for key, values in data_per_shift.items():
        existing_values[key] = {}
        for val in values:
            date_t = val.timestamp.replace(second=0, microsecond=0)
            date_t += timedelta(hours=HOURS)
            existing_values[key][date_t] = val.value

    # create dict with all minutes to now if value is not return (-1) because
    # 0 may exist
    time_by_minuts = {}
    for key_m, values_m in existing_values.items():
        start_m = start
        time_by_minuts[key_m] = []
        for i in range(60 * 12 - 1):
            val_minutes = existing_values[key_m].setdefault(start_m, -1)
            if (val_minutes < 0.1 and val_minutes > 0):
                val_minutes = 0
            time_by_minuts[key_m].append(val_minutes)
            start_m += timedelta(minutes=1)
            if start_m >= datetime.now():
                break
    return time_by_minuts

def handle_date(date):
    day = month = year = None
    spl_date = date.split('.')
    if len(spl_date) >3:
        return redirect(url_for('index'))
    try:
        day = int(spl_date[0])
        month = int(spl_date[1])
        year = int(spl_date[2])
    except IndexError:
        print('ERR', day, month, year)
    if not year: year=datetime.now().year
    if not month: month=datetime.now().month
    if not day: day=datetime.now().day
    try:
        return datetime(year, month, day).date()
    except:
        flash('Enter correct shift')
        return datetime.now().date()

def add_post(post):
    # new_post = Post(value, latitude, longitude, mechanism_id)
    print(post)
    # print(post.value, post.latitude)
    # db.session.add(new_post)
    # db.session.commit()


# date_shift, shift = today_shift_date()
# print(date_shift, shift)
# dd = time_for_shift('usm', date_shift, shift)
# pprint(dd)




