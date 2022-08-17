from datetime import datetime, timedelta

from rich import print

from app import db, logger, mongodb
from app.add_fio_1c import add_fio_and_grab_from_1c
from app.add_fio_rfid import add_fio_from_rfid
from app.add_resons_1c import add_resons_from_1c
from app.functions_for_all import (  # all_mechanisms_type, all_number, name_by_id
    all_mechanisms_id,  today_shift_date)
from app.kran import kran_periods, time_for_shift_kran
from app.model import Mechanism, Post,  Work_1C_1
from app.sennebogen import sennebogen_periods, time_for_shift_sennebogen
from app.usm import time_for_shift_usm, usm_periods
from config import (HOURS, TIME_PERIODS, lines_krans, mechanisms_type,
                    names_terminals)
from flask import flash, redirect, url_for

from pymongo.errors import DuplicateKeyError


def multiple_5(date):  # not use
    '''Return time multiple 5 minutes and remite microseconds'''
    # global HOURS
    date += timedelta(hours=HOURS)
    mul5 = date.minute - date.minute % 5
    date_n = date.replace(minute=mul5, second=0, microsecond=0)
    return date_n


def time_for_shift_list(date_shift, shift):  # not use
    '''get dict with all minute's values for the period'''
    try:
        cursor = db.session.query(Post).filter(
            Post.date_shift == date_shift,
            Post.shift == shift).order_by(Post.mechanism_id).all()
    except Exception as e:
        cursor = {}
        logger.debug(e)

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
    for key_m in existing_values:
        start_m = start
        time_by_minuts[key_m] = []
        for _ in range(60 * 12 - 1):
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
    try:
        cursor = db.session.query(Work_1C_1).filter(
            Work_1C_1.data_nach >= time_from,
            Work_1C_1.data_nach <= time_to).all()
    except Exception as e:
        cursor = {}
        logger.debug(e)
    data_1C = [x.get() for x in cursor]
    return data_1C


def state_mech(el):
    type_mechanism = el.mech.type
    value = el.value
    value2 = el.value2
    value3 = el.value3
    last_time = el.timestamp + timedelta(hours=HOURS)
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
        if value == 5:
            return 'move'
        return 'err'

    if type_mechanism == 'usm':  # value - lever, value3 - roller
        if dt > 120.0:
            return 'long_no_power'
        if dt >= 3.0:
            return 'no_power'
        if value >= 0.1:
            return 'work'
        if value < 0.1 and value3 >= 5:
            return 'move'
        if value < 0.1 or value3 < 5:
            return 'stay'
        else:
            return 'err'

    if type_mechanism == "sennebogen":  # value - x, value2 - y
        if dt > 120.0:
            return 'long_no_power'
        if dt >= 3.0:
            return 'no_power'
        if value >= 500 or value2 >= 500:
            return 'work'
        else:
            return 'stay'
    return None


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


def is_alarm_sennebogen(args):
    """if last 15 minuts not work """
    return False


def get_status_alarm(mech_id, mech_type):
    try:
        # TODO redis
        last = db.session.query(Post).filter(
            Post.mechanism_id == mech_id).order_by(
            Post.timestamp.desc()).limit(20)
    except Exception as e:
        last = None
        logger.debug(e)
    now_hour = datetime.now().hour + datetime.now().minute/60
    cofe_time = any(now_hour > t1 and now_hour < t2 for t1, t2 in TIME_PERIODS)
    # logger.info(mech_type)
    if cofe_time:
        return False
    if mech_type == 'kran':
        return is_alarm_kran(last)
    elif mech_type == 'usm':
        return is_alarm_usm(last)
    elif mech_type == 'sennebogen':
        return is_alarm_sennebogen(last)
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
    return None, None


def get_terminal(latitude, longitude):
    '''matched values'''
    x = (longitude-132) / (latitude-42+0.0000001)
    if (x < 1.1):
        return 1
    else:
        return 2


def get_terminalGut(latitude, longitude):
    '''7.265 - matched value'''
    if 7.265 > (longitude-132)*10*(latitude-42):
        return 5
    return 4


def get_k1_b1_not_kran(latitude, longitude):
    terminal = get_terminal(latitude, longitude)
    latitude = int(latitude)
    longitude = int(longitude)
    if terminal == 1:
        return [0.593270908597224, 107.49050635162425]  # ut
    else:
        if get_terminalGut(latitude, longitude) == 5:
            return [1.696165886483065, 60.30071859473439]  # 5k
        else:
            return [0.339389423498601, 118.37599497658572]  # 4k


def which_terminal(type_mech, number, latitude, longitude):
    latitude = float(latitude)
    longitude = float(longitude)
    if type_mech == 'kran':
        k1, b1 = line_kran(int(number))
    else:
        k1, b1 = get_k1_b1_not_kran(latitude, longitude)

    k2, b2 = perpendicular_line_equation(
        k1, latitude, longitude)
    # print(k1, b1)
    nx, ny = intersection_point_of_lines(k1, b1, k2, b2)
    name_terminal = 78  # !make None
    for name, lon_max, lon_min in names_terminals:
        # print(name, lon_max, ny, lon_min)
        if ny < lon_max and ny > lon_min:
            name_terminal = name
    return name_terminal


def mech_periods(type_mechanism, date, shift):
    data = None
    if type_mechanism == 'usm':
        data = usm_periods(time_for_shift_usm(date, shift))
    elif type_mechanism == 'kran':
        data = kran_periods(time_for_shift_kran(date, shift))
    elif type_mechanism == 'sennebogen':
        data = sennebogen_periods(time_for_shift_sennebogen(date, shift))
        # logger.info(data)
    return data


def hash_all_last_data_state():
    # start = datetime.now()
    try:
        last_data_mech = [db.session.query(Post).filter(Post.mechanism_id == x).order_by(
            Post.timestamp.desc()).first() for x in all_mechanisms_id()]
    except Exception as e:
        last_data_mech = {}
        logger.debug(e)
    last_data_mech = filter(lambda x: x is not None, last_data_mech)
    data = {el.mech.type + str(el.mech.number): {'id': el.mech.id,
                                                 'name': el.mech.name,
                                                 'type': el.mech.type,
                                                 'number': el.mech.number,
                                                 # if roller not work
                                                 # !need function
                                                 'value': round(el.value, 2) if not el.value3 else 0,
                                                 'value2': el.value2,
                                                 'value3': el.value3,
                                                 'latitude': el.latitude,
                                                 'longitude': el.longitude,
                                                 'state': state_mech(el),
                                                 'alarm': get_status_alarm(el.mech.id, el.mech.type),
                                                 'terminal': el.terminal,
                                                 'time': el.timestamp + timedelta(hours=HOURS)
                                                 }
            for el in last_data_mech
            }
    posts = mongodb['hash']
    if data is not None:
        data["_id"] = "last_data"
        posts.delete_one({"_id": "last_data"})
        try:
            posts.insert_one(data)
        except DuplicateKeyError:
            print("thread already use")
    else:
        return


def hash_now(type_mechanism):
    date, shift = today_shift_date()
    data = mech_periods(type_mechanism, date, shift)
    data = add_fio_and_grab_from_1c(data, date, shift)
    data = add_fio_from_rfid(data, date, shift)
    data = add_resons_from_1c(data, date, shift)

    posts = mongodb[type_mechanism]
    if data is not None:
        # convert int key to str
        mongo_data = {str(key): value for key, value in data.items()}
        for key, value in data.items():
            mongo_data[str(key)]['data'] = {
                str(k): v for k, v in value['data'].items()}
        mongo_data['_id'] = "now"
        posts.delete_one({"_id": "now"})
        try:
            posts.insert_one(mongo_data)
        except DuplicateKeyError:
            print("thread already use")
    else:
        mongo_data = {}
        mongo_data['_id'] = "now"
        posts.delete_one({"_id": "now"})
        posts.insert_one(mongo_data)


def get_dict_mechanisms_id_by_number():
    dict_mechanisms = {mech_type: {} for mech_type in mechanisms_type}
    for mech_type in mechanisms_type:
        try:
            dict_mechanisms[mech_type] = {m.number: m.id for m in db.session.query(
                Mechanism).filter(Mechanism.type == mech_type).all()}
        except Exception as e:
            logger.debug(e)
    return dict_mechanisms


def get_dict_mechanisms_number_by_id():
    dict_mechanisms = {mech_type: {} for mech_type in mechanisms_type}
    for mech_type in mechanisms_type:
        try:
            dict_mechanisms[mech_type] = {m.id: m.number for m in db.session.query(
                Mechanism).filter(Mechanism.type == mech_type).all()}
        except Exception as e:
            logger.debug(e)
    return dict_mechanisms


def dez10_to_dez35C(n: str) -> str:
    '''
        convert rfid_id to "text_format" rfid
        https://guardsaas.com/ru/content/keycode
    '''
    import re
    n = re.sub("[^0-9]", "", n)
    n = str(n).zfill(10)
    hex_n = hex(int(n)).split('x')[-1]
    hex_n = hex_n.zfill(6)
    left = str(int(hex_n[:2], 16))
    left = left.zfill(3)
    right = str(int(hex_n[2:], 16))
    right = right.zfill(5)
    return left+','+right
    # return str(int(left))+','+right


if __name__ == "__main__":
    # type_mech = 'sennebogen'
    # number = 1
    # lat=43.805052
    # lon=132.905318
    # res = which_terminal(type_mech, number, lat, lon)
    # print(res)
    # type_mech = 'kran'
    # number = 1
    # for term, degress in tests:
    #     latitude = degress[1]
    #     longitude = degress[0]
    date_shift = datetime.now().date()
    # date_shift -= timedelta(days=1)
    type_mechanism = 'usm'
    shift = 1
    rfid_ids = [
        '36/59956',
        '240/01548',
        '15/23422',
    ]

    data = mech_periods(type_mechanism, date_shift, shift)
    data = add_fio_from_rfid(data, date_shift, shift)
    # print(data)
