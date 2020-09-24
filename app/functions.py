from datetime import datetime, timedelta
from flask import render_template, flash
from app.model import Post, Mechanism, Work_1C_1
from app import db
from pprint import pprint
from random import choice

HOURS = 10 #your timezone


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

def data_from_1c(date_shift, shift):
    time_from = datetime.combine(date_shift, datetime.min.time())
    if shift==1:
        time_from += timedelta(hours=8)
    else:
        time_from += timedelta(hours=20)
    time_to = time_from + timedelta(hours=12)
    cursor = db.session.query(Work_1C_1).filter(Work_1C_1.data_nach>=time_from, Work_1C_1.data_nach<=time_to).all()
    data_1C = [x.get() for x in cursor]
    return data_1C

def data_from_1c_by_id(date_shift, shift, id_mech):
    time_from = datetime.combine(date_shift, datetime.min.time())
    if shift==1:
        time_from += timedelta(hours=8)
    else:
        time_from += timedelta(hours=20)
    time_to = time_from + timedelta(hours=12)
    cursor = db.session.query(Work_1C_1).filter(Work_1C_1.data_nach>=time_from, Work_1C_1.data_nach<time_to, Work_1C_1.inv_num==id_mech).all()
    data_1C = [x.get() for x in cursor]
    return data_1C

def fio_to_fi(item):
    fio = item[3].split()
    if not fio:
        return None
    return f'{fio[0].capitalize()} {fio[1][0]}.'

def add_fio(data_kran_period, date_shift, shift):
    ''' add fio and grab if it exec'''
    if not data_kran_period:
        return None
    for key, value in data_kran_period.items():
        id_mech = data_kran_period[key]['id']
        data_by_id_mech = data_from_1c_by_id(date_shift, shift, id_mech)
        if len(data_by_id_mech)<1:
            data_kran_period[key]['fio'] = None
            data_kran_period[key]['grab'] = None
        elif len(data_by_id_mech)==1:
            data_kran_period[key]['fio'] = fio_to_fi(data_by_id_mech[0])
            if data_by_id_mech[0][2] == 0:
                data_kran_period[key]['grab'] = None
            else:
                data_kran_period[key]['grab'] = data_by_id_mech[0][2]
        else:
            for operator in data_by_id_mech:
                data_kran_period[key]['fio'] = 'Two operators'
    return data_kran_period

def get_state():
    state = ['work', 'stay', 'no_power']
    return choice(state)

