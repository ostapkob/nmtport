from datetime import datetime, timedelta
from app.model import Post, Mechanism
from app import db
from pprint import pprint
HOURS = 10
def today_shift_date():
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
    if type==None:
        return [m.id for m in db.session.query(Mechanism).all()]
    return [m.id for m in db.session.query(Mechanism).filter(Mechanism.type==type).all()]


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

def time_for_shift(type_mechanism, date_shift, shift):
    '''get dict with all minute's values for the period, name and total'''
    #get data from db
    shift=int(shift)
    all_mechs = all_mechanisms_id(type_mechanism)
    cursor = db.session.query(Post).filter(Post.date_shift == date_shift, Post.shift == shift, Post.mechanism_id.in_(all_mechs)).order_by(Post.mechanism_id).all()
    #create dict all works mechanism in shift
    data_per_shift = {}
    for el in cursor:
        date_t = el.timestamp.replace(second=0, microsecond=0)
        date_t+=timedelta(hours=10)
        # date_t = date_t.strftime("%H:%M")
        val_minute = 0 if el.value < 0.1 else el.value

        if data_per_shift.get(el.mech.number):
            data_per_shift[el.mech.number]['data'][date_t]=val_minute
            data_per_shift[el.mech.number]['total'] += el.value
        else:
            data_per_shift[el.mech.number]={}
            data_per_shift[el.mech.number]['mechanism'] = el.mech
            data_per_shift[el.mech.number]['total'] = el.value
            data_per_shift[el.mech.number]['data'] = {}
            data_per_shift[el.mech.number]['data'] [date_t] = val_minute

    # get start time for this shift
    start = datetime.combine(date_shift, datetime.min.time())
    if shift == 1:
        start=start.replace(hour=8, minute=0, second=0, microsecond=0)
    else:
        start=start.replace(hour=20, minute=0, second=0, microsecond=0)

    if data_per_shift=={}: return None
    #create dict with all minutes to now if value is not return (-1) because 0 may exist
    time_by_minuts = {}
    for key, value in data_per_shift.items():
        time_by_minuts[key]={}
        time_by_minuts[key]['name'] = data_per_shift[key]['mechanism'].name
        time_by_minuts[key]['total'] = round(data_per_shift[key]['total'] /60, 2) #translate hours into minutes and round
        time_by_minuts[key]['data'] = {}
        delta_minutes = start
        for i in range(1, 60*12+1):
            date_t =delta_minutes.strftime("%H:%M")
            val_minute = data_per_shift[key]['data'].setdefault(delta_minutes, -1)
            time_by_minuts[key]['data'][i]={'time':date_t, 'value':val_minute}
            delta_minutes+=timedelta(minutes=1)
            today_date, today_shift = today_shift_date()
            if delta_minutes>=datetime.now() and date_shift==today_date and today_shift == shift:
                break
    return time_by_minuts


# not use
def time_for_shift_list(date_shift, shift):
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
            date_t+=timedelta(hours=HOURS)
            existing_values[key][date_t]=val.value

    #create dict with all minutes to now if value is not return (-1) because 0 may exist
    time_by_minuts ={}
    for key_m, values_m in existing_values.items():
        start_m=start
        time_by_minuts[key_m] = []
        for i in range(60*12-1):
            val_minutes = existing_values[key_m].setdefault(start_m, -1)
            if (val_minutes  < 0.1 and val_minutes > 0): val_minutes = 0
            time_by_minuts[key_m].append(val_minutes    )
            start_m+=timedelta(minutes=1)
            if start_m>=datetime.now():
                break
    print(shift)
    return time_by_minuts

# date_shift, shift = today_shift_date()
# print(date_shift, shift)
# dd = time_for_shift('usm', date_shift, shift)
# pprint(dd)




