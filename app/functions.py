from datetime import datetime, timedelta
from flask import flash, redirect, url_for
from app.model import Post, Mechanism, Work_1C_1
from app import db
from config import TIME_PERIODS
from config import lines_krans, names_terminals
from app  import logger
from pymongo import MongoClient
from app.kran import  kran_periods, time_for_shift_kran
from app.usm import usm_periods, time_for_shift_usm
from config import HOURS
from app.functions_for_all import all_mechanisms_id, today_shift_date #  all_mechanisms_type, all_number, name_by_id

def multiple_5(date):  # not use
    '''Return time multiple 5 minutes and remite microseconds'''
    global HOURS
    # date -= timedelta(minutes=5)
    date += timedelta(hours=HOURS)
    mul5 = date.minute - date.minute % 5
    date_n = date.replace(minute=mul5, second=0, microsecond=0)
    return date_n


def image_mechanism(value, type_mechanism, number, last_time):
    dt = datetime.now() - last_time
    dt = dt.total_seconds() / 60
    if type_mechanism == "usm":
        if dt > 120.0:
            return './static/numbers/'+str(
                type_mechanism)+'/gray/'+str(number)+'.png'
        if dt >= 3.0:
            return './static/numbers/'+str(
                type_mechanism)+'/red/'+str(number)+'.png'
        if value < 0.1:
            return './static/numbers/'+str(
                type_mechanism)+'/yellow/'+str(number)+'.png'
        else:
            return './static/numbers/'+str(
                type_mechanism)+'/green/'+str(number)+'.png'

    if type_mechanism == "kran":
        if dt > 120.0:
            return './static/numbers/'+str(
                type_mechanism)+'/gray/'+str(number)+'.png'
        if dt >= 5.0:
            return './static/numbers/'+str(
                type_mechanism)+'/red/'+str(number)+'.png'
        if value == 1:
            return './static/numbers/'+str(
                type_mechanism)+'/black/'+str(number)+'.png'
        if value == 2:
            return './static/numbers/'+str(
                type_mechanism)+'/blue/'+str(number)+'.png'
        else:
            return './static/numbers/'+str(
                type_mechanism)+'/yellow/'+str(number)+'.png'


def time_for_shift_list(date_shift, shift):  # not use
    '''get dict with all minute's values for the period'''
    # get data from db
    cursor = db.session.query(Post).filter(
        Post.date_shift == date_shift,
        Post.shift == shift).order_by(Post.mechanism_id).all()

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
    if len(spl_date) > 3:
        return redirect(url_for('index'))
    try:
        day = int(spl_date[0])
        month = int(spl_date[1])
        year = int(spl_date[2])
    except IndexError:
        print('ERR', day, month, year)
    if not year:
        year = datetime.now().year
    if not month:
        month = datetime.now().month
    if not day:
        day = datetime.now().day
    try:
        return datetime(year, month, day).date()
    except ValueError:
        flash('Enter correct shift')
        return datetime.now().date()


def data_from_1c(date_shift, shift):
    time_from = datetime.combine(date_shift, datetime.min.time())
    if shift == 1:
        time_from += timedelta(hours=8)
    else:
        time_from += timedelta(hours=20)
    time_to = time_from + timedelta(hours=12)
    cursor = db.session.query(Work_1C_1).filter(
        Work_1C_1.data_nach >= time_from,
        Work_1C_1.data_nach <= time_to).all()
    data_1C = [x.get() for x in cursor]
    return data_1C


def data_from_1c_by_id(date_shift, shift, id_mech):
    # time_from = datetime.combine(date_shift, datetime.min.time())
    # if shift == 1:
    #     time_from += timedelta(hours=8)
    # else:
    #     time_from += timedelta(hours=20)
    # time_to = time_from + timedelta(hours=12)
    cursor = db.session.query(Work_1C_1).filter(
        # Work_1C_1. >= time_from,
        # Work_1C_1.data_nach < time_to,
        Work_1C_1.data_smen == date_shift,
        Work_1C_1.smena == shift,
        Work_1C_1.inv_num == id_mech
        ).all()
    data_1C = [x.get() for x in cursor]
    return data_1C


def fio_to_fi(item):
    fio = item[3].split()
    if not fio:
        return None
    return f'{fio[0].capitalize()} {fio[1][0]}.'


def add_fio(data_kran_period, date_shift, shift):
    ''' add fio and grab if it exec '''
    if not data_kran_period:
        return None
    for key, value in data_kran_period.items():
        id_mech = data_kran_period[key]['id']
        data_by_id_mech = data_from_1c_by_id(date_shift, shift, id_mech)
        # last_find_item = db.session.query(Work_1C_1).filter(Work_1C_1.inv_num==id_mech, Work_1C_1.greifer_vol>0 ).first()
        if len(data_by_id_mech) < 1:
            data_kran_period[key]['fio'] = None
            data_kran_period[key]['grab'] = None
            data_kran_period[key]['contract'] = None
        elif len(data_by_id_mech) == 1:
            data_kran_period[key]['fio'] = fio_to_fi(data_by_id_mech[0])
            data_kran_period[key]['contract'] = data_by_id_mech[0][8]
            if data_by_id_mech[0][2]:
                data_kran_period[key]['grab'] = float(data_by_id_mech[0][2])
            else:
                data_kran_period[key]['grab'] = None
        else:
            for operator in data_by_id_mech:
                data_kran_period[key]['fio'] = 'Два оператора'
                data_kran_period[key]['contract'] = 1
            if data_by_id_mech[0][2]: # dublicate
                data_kran_period[key]['grab'] = float(data_by_id_mech[0][2])
            else:
                data_kran_period[key]['grab'] = None

        # if grab not write then find last item
        if data_kran_period[key]['grab'] == None and id_mech in all_mechanisms_id('kran'):
            try:
                last_find_item = db.session.query(Work_1C_1).filter(Work_1C_1.inv_num==id_mech, Work_1C_1.greifer_vol> 0 ).order_by(Work_1C_1.data_nach.desc()).first()
                data_kran_period[key]['grab'] = float(last_find_item.greifer_vol)
            except AttributeError:
                data_kran_period[key]['grab'] = None
    return data_kran_period


def get_state():
    return 'work'


# def state_mech(args):
#     values = list(x.value == -1 for x in args.values())
#     result = all(values[1:])
#     print(values, result)
#     if result:
#         return 'no_power'

#     values = list(x.value <= .1 for x in args.values())
#     result = all(values[1:])
#     if result:
#         return 'stay'

#     return 'work'


def state_mech(type_mechanism, value, value3, last_time):
    dt = datetime.now() - last_time
    dt = dt.total_seconds() / 60
    if type_mechanism == 'kran':
        if dt > 120.0:
            return 'long_no_power'
        if dt >= 6.0:
            return 'no_power'
        if value == 0 or value == 4:  # 123 4
            return 'stay'
        if value == 2:
            return '180'
        if value == 1:
            return '90_1'
        if value == 3:
            return '90_2'
        else:
            return 'err'

    if type_mechanism == 'usm':
        if dt > 120.0:
            return 'long_no_power'
        if dt >= 3.0:
            return 'no_power'
        if value < 0.1 or not value3:
            return 'stay'
        if value >= 0.1:
            return 'work'
        else:
            return 'err'


def is_alarm(args):
    """if last 10 minuts not values > 1 but 15 minutes ago mechanism worked"""
    values_14_10 = []
    values_9_0 = []
    dt = datetime.now()
    for el in args:
        dt = datetime.now() - (el.timestamp + timedelta(hours=HOURS))
        dt = dt.total_seconds() / 60
        if dt > 10 and dt <= 15:
            values_14_10.append(el.value)
        elif dt <= 10:
            values_9_0.append(el.value)
        else:
            pass
    if sum(values_9_0) > 0:
        return False
    if sum(values_14_10) <= 0:
        return False
    return True


def is_alarm_kran(args):
    """if last 15 minuts not work """
    values_19_15 = []
    values_14_0 = []
    dt = datetime.now()
    for el in args:
        dt = datetime.now() - (el.timestamp + timedelta(hours=HOURS))
        dt = dt.total_seconds() / 60
        if dt > 15 and dt <= 20:
            values_19_15.append(el.value)
        elif dt <= 15:
            values_14_0.append(el.value)
        else:
            pass
    if sum(values_14_0) > 0:
        return False
    if sum(values_19_15) <= 0:
        return False
    return any(x == 2 for x in values_19_15)  # if work 180 degress


def is_alarm_usm(args):
    """if last 15 minuts not work """
    values_19_15 = []
    values_14_0 = []
    dt = datetime.now()
    for el in args:
        dt = datetime.now() - (el.timestamp + timedelta(hours=HOURS))
        dt = dt.total_seconds() / 60
        if dt > 15 and dt <= 20:
            values_19_15.append(el.value)
        elif dt <= 15:
            values_14_0.append(el.value)
        else:
            pass
    # logger.info(dt,  values_19_15, values_14_0)
    # logger.info(any(x == 2 for x in values_19_15))  # if work 180 degress
    if sum(values_14_0) > 0:
        return False
    if sum(values_19_15) <= 0:
        return False
    return True


def get_status_alarm(mech_id, mech_type):
    last = db.session.query(Post).filter(
        Post.mechanism_id == mech_id).order_by(
        Post.timestamp.desc()).limit(20)
    now_hour = datetime.now().hour + datetime.now().minute/60
    cofe_time = any(now_hour > t1 and now_hour < t2 for t1, t2 in TIME_PERIODS)
    # logger.inf o(mech_type)
    if cofe_time:
        return False
    if mech_type == 'kran':
        return is_alarm_kran(last)
    elif mech_type == 'usm':
        return is_alarm_usm(last)
    else:
        return False


def straight_line_equation(x1, y1, x2, y2):
    k = (y1 - y2) / (x1 - x2)
    b = y2 - k * x2
    return k, b


def perpendicular_line_equation(k1, mx, my):
    k2 = - (1/k1) * 1.9
    b2 = my - (k2*mx)
    return k2, b2


def intersection_point_of_lines(k1, b1, k2, b2):
    nx = (b2 - b1) / (k1-k2)
    ny = nx*k2 + b2
    return nx, ny


def line_kran(number):
    for el in lines_krans:
        if number in el['numbers']:
            return el['k1'], el['b1']


def which_terminal(latitude, longitude):
    k1, b1 = 0.5932709085972241, 107.49050635162425
    k2, b2 = perpendicular_line_equation(
        k1, float(latitude), float(longitude))
    nx, ny = intersection_point_of_lines(k1, b1, k2, b2)
    name_terminal = None
    for name, lon_max, lon_min in names_terminals:
        if ny < lon_max and ny > lon_min:
            name_terminal = name
    return name_terminal


def mech_periods(type_mechanism, date, shift):
    if type_mechanism == 'usm':
        data = usm_periods(time_for_shift_usm(date, shift))
    elif type_mechanism == 'kran':
        data = kran_periods(time_for_shift_kran(date, shift))
        # logger.info(data)
    else:
        data = None
    return data

# not to use
# def add_to_mongo(data, date, shift):
#     if data is not None:
#         today_date, today_shift = today_shift_date()
#         # convert int key to str
#         mongo_data = {str(key): value for key, value in data.items()}
#     for key, value in data.items():
#         mongo_data[str(key)]['data'] = {
#             str(k): v for k, v in value['data'].items()}
#     if today_date == date and today_shift == shift:
#         print('No')
#         pass
#     else:
#         mongo_data['_id'] = f'{date_shift}|{shift}'
#         posts = db[type_mechanism]
#         posts.insert_one(mongo_data)

def hash_all_last_data_state():
    start = datetime.now()
    last_data_mech = [db.session.query(Post).filter(Post.mechanism_id == x).order_by(
        Post.timestamp.desc()).first() for x in all_mechanisms_id()]
    last_data_mech = filter(lambda x: x is not None, last_data_mech)
    data = {el.mech.type + str(el.mech.number): {'id': el.mech.id,
                                                 'name': el.mech.name,
                                                 'type': el.mech.type,
                                                 'number': el.mech.number,
                                                 # if roller not work
                                                 'value': round(el.value, 2) if not el.value3 else 0,
                                                 'value2': el.value2,
                                                 'value3': el.value3,
                                                 'latitude': el.latitude,
                                                 'longitude': el.longitude,
                                                 'state': state_mech(el.mech.type, el.value, el.value3, el.timestamp + timedelta(hours=HOURS)),
                                                 'alarm': get_status_alarm(el.mech.id, el.mech.type),
                                                 # 'alarm': True,
                                                 # 'alarm': False,
                                                 'terminal': el.terminal,
                                                 'time': el.timestamp + timedelta(hours=HOURS)} for el in last_data_mech}
    client = MongoClient('mongodb://localhost:27017')
    mongodb = client['HashShift']
    posts = mongodb['hash']
    # logger.debug(data)
    if data is not None:
        data['_id'] = 'last_data'
        posts.delete_one({"_id":"last_data"})
        posts.insert_one(data)


def hash_now(type_mechanism):
    date, shift = today_shift_date()
    data = mech_periods(type_mechanism, date, shift)
    data = add_fio(data, date, shift)
    client = MongoClient('mongodb://localhost:27017')
    mongodb = client['HashShift']
    posts = mongodb[type_mechanism]
    # logger.debug(data)
    if data is not None:
        # convert int key to str
        mongo_data = {str(key): value for key, value in data.items()}
        for key, value in data.items():
            mongo_data[str(key)]['data'] = {
                str(k): v for k, v in value['data'].items()}
        mongo_data['_id'] = "now"
        posts.delete_one({"_id": "now"})
        posts.insert_one(mongo_data)


if __name__ == "__main__":
    x1, y1 = 42.80691726848499, 132.88660505374455
    x2, y2 = 42.81408152044796, 132.89085539601604
    # x1, y1 = 42.807735079133295, 132.88577535577383
    # x2, y2 = 42.81760201722565, 132.89163529190128
    # x1, y1 = 42.81381686151741, 132.89146624081198
    # x2, y2 = 42.81697813067333, 132.89335636137457
    # print(straight_line_equation(x1, y1, x2, y2))
