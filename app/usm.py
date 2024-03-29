from datetime import datetime, timedelta

from app import db, logger
from app.add_fio_1c import add_fio_and_grab_from_1c
from app.add_fio_rfid import add_fio_from_rfid
from app.add_resons_1c import add_resons_from_1c
from app.functions_for_all import (all_mechanisms_id, get_start_shift,
                                   id_and_number, today_shift_date)
from app.model import Post
from config import HOURS, usm_tons_in_hour

TYPE = 'usm'
ids_and_nums = id_and_number(TYPE)


def get_data_per_shift(cursor):
    '''create dict with all minutes to now if value is None return (-1) because  0 may exist'''
    data_per_shift = {}
    for item in cursor:
        item_value = item.value
        item_value3 = item.value3
        date_t = item.timestamp.replace(second=0, microsecond=0)
        date_t += timedelta(hours=HOURS)
        item_value = -1 if item_value is None else item_value
        item_value3 = 0 if item_value3 is None else item_value3
        val_min = 0 if item_value < 0.1 else item_value
        # maybe more, value3 is speed rool
        item_value = 0 if item_value3 < 4 else item_value
        val_min = 0 if item_value3 < 4 else item_value

        if data_per_shift.get(item.mech.number):
            # bad
            data_per_shift[item.mech.number]['data'][date_t] = val_min, item_value3, item_value
            data_per_shift[item.mech.number]['time_coal'] += item_value
            data_per_shift[item.mech.number]['total_time'] += 1
        else:
            data_per_shift[item.mech.number] = {}
            data_per_shift[item.mech.number]['mechanism'] = item.mech
            data_per_shift[item.mech.number]['time_coal'] = item_value
            data_per_shift[item.mech.number]['total_time'] = 1
            data_per_shift[item.mech.number]['data'] = {}
            data_per_shift[item.mech.number]['data'][date_t] = val_min, item_value3, item_value
        data_per_shift[item.mech.number].setdefault('work_time', 0)
        if item_value > 0:
            data_per_shift[item.mech.number]['work_time'] += 1
    return data_per_shift


def get_time_by_minuts(data_per_shift, date_shift, shift):
    start_shift = get_start_shift(date_shift, shift)
    time_by_minuts = {}
    for key in data_per_shift:
        flag_start = True
        mech = data_per_shift[key]['mechanism']
        time_by_minuts[key] = {}
        time_by_minuts[key]['name'] = mech.name
        time_by_minuts[key]['id'] = mech.id
        time_by_minuts[key]['number'] = mech.number
        time_by_minuts[key]['tons_in_hour'] = usm_tons_in_hour[mech.number]
        # translate hours into minutes and round
        time_by_minuts[key]['time_coal'] = round(
            data_per_shift[key]['time_coal'] / 60, 2)
        time_by_minuts[key]['total_time'] = round(
            data_per_shift[key]['total_time'] / 60, 1)
        time_by_minuts[key]['work_time'] = round(
            data_per_shift[key]['work_time'] / 60, 1)
        time_by_minuts[key]['data'] = {}
        delta_minutes = start_shift
        try:
            last_find_item = db.session.query(Post).filter(
                Post.mechanism_id == data_per_shift[key]['mechanism'].id).order_by(Post.timestamp.desc()).first()
            terminal = last_find_item.terminal
        except Exception as e:
            terminal = 8
            print('not found terminal', e)

        time_coal = 0
        for i in range(1, 60 * 12 + 1):
            date_t = delta_minutes.strftime("%H:%M")
            val_minute = data_per_shift[key]['data'].setdefault(
                delta_minutes, (-1, -1, 0))
            time_coal += val_minute[2] / 60
            time_by_minuts[key]['data'][i] = {'time': date_t,
                                              'value': val_minute[0],
                                              'speed': val_minute[1],
                                              'time_coal': round(time_coal, 2),
                                              'terminal': terminal,  # only last position
                                              }
            delta_minutes += timedelta(minutes=1)
            today_date, today_shift = today_shift_date()
            if val_minute[0] > 0 and flag_start:
                time_by_minuts[key]['start'] = date_t
                flag_start = False
            if val_minute[0] > 0:
                time_by_minuts[key]['finish'] = date_t
            if delta_minutes >= datetime.now() and date_shift == today_date and today_shift == shift:
                break
            time_by_minuts[key]['terminal'] = terminal
        # try:
            # resons = process_resons(get_resons(TYPE, date_shift, shift), ids_and_nums)
        # except Exception as e:
            # resons = {}
        # time_by_minuts[key]['resons'] = convert_resons_to_720minuts(resons.get(mech.number, None), start_shift)

    return time_by_minuts


def time_for_shift_usm(date_shift, shift):
    '''get dict with all minute's values for the period, name and total
    value is lever, value3 is speed roler,
    '''
    shift = int(shift)
    all_mechs = all_mechanisms_id(TYPE)  # TODO get not from db
    try:
        cursor = db.session.query(Post).filter(Post.date_shift == date_shift, Post.shift ==
                                               shift, Post.mechanism_id.in_(all_mechs)).order_by(Post.mechanism_id).all()
    except Exception as e:
        logger.debug(e)
        return None
    # create dict all works mechanism in shift
    data_per_shift = get_data_per_shift(cursor)
    if not data_per_shift:
        return {}
    time_by_minuts = get_time_by_minuts(data_per_shift, date_shift, shift)
    return time_by_minuts


def usm_periods(data):
    '''merge identical periods'''
    mechanisms_data = data
    if not mechanisms_data:
        return None
    for mech, data_mech in mechanisms_data.items():
        # pprint(data_mech)
        values_period = -1
        new_data = {}
        step = 0
        pre_time = ''  # data_mech['data'][1]['time']
        counter = 1
        # reson = resons.get(mech, None) and resons.get(mech, None).get(pre_time, None)
        tmp_time_coal = 0
        for value_number in data_mech['data'].values():
            value_min = get_values_min(value_number)
            if value_min != values_period:
                new_data[counter] = {'time': pre_time,
                                     'value': values_period,
                                     'step': step,
                                     'time_coal': value_number['time_coal']}
                step = 1
                values_period = value_min
                pre_time = value_number['time']
                counter += 1
                tmp_time_coal = value_number['time_coal']
            else:
                step += 1
        new_data[counter] = {'time': pre_time,
                             'value': values_period,
                             'step': step,
                             'time_coal': tmp_time_coal
                             }
        mechanisms_data[mech]['data'] = new_data
    return mechanisms_data


def get_values_min(value_number):
    if value_number['value'] >= 0 and value_number['value'] < 0.1:
        if value_number['speed'] <= 4:
            return 0  # yellow
        else:
            return 2  # dark yellow
    elif value_number['value'] >= 0.1:
        return 1  # blue
    else:
        return -1  # red


if __name__ == "__main__":
    import pickle

    from rich import print
    date_shift = datetime.now().date()
    date_shift -= timedelta(days=0)
    dates_shifts = [date_shift - timedelta(days=x) for x in range(18, 19)]
    shift = 2

    for date in dates_shifts:
        print(date)
        name_file_pickle = TYPE+'_'+str(date)+"_"+str(shift)
        # res = usm_periods(time_for_shift_usm(date, shift))
        # with open(name_file_pickle, 'wb') as f:
        #     pickle.dump(res, f)

        with open(name_file_pickle, 'rb') as f:
            load = pickle.load(f)

        data = add_fio_and_grab_from_1c(load, date, shift)
        data = add_fio_from_rfid(data, date, shift)
        data = add_resons_from_1c(data, date, shift)
        print(data[13]['resons'])
