from app.functions_for_all import all_mechanisms_id, today_shift_date
from config import HOURS, usm_tons_in_hour 
from app.model import Post
from app import db
from datetime import datetime, timedelta


def time_for_shift_usm(date_shift, shift):
    '''get dict with all minute's values for the period, name and total
    value is lever, value3 is speed roler,
    '''
    # get data from db
    shift = int(shift)
    all_mechs = all_mechanisms_id('usm')
    try:
        cursor = db.session.query(Post).filter(Post.date_shift == date_shift, Post.shift ==
                                               shift, Post.mechanism_id.in_(all_mechs)).order_by(Post.mechanism_id).all()
    except Exception as e:
        logger.debug(e)
    # create dict all works mechanism in shift
    data_per_shift = {}
    for el in cursor:
        date_t = el.timestamp.replace(second=0, microsecond=0)
        date_t += timedelta(hours=HOURS)
        # date_t = date_t.strftime("%H:%M")
        el.value = -1 if el.value is None else el.value
        el.value3 = 0 if el.value3 is None else el.value3
        val_min = 0 if el.value < 0.1 else el.value
        el.value = 0 if el.value3 < 5 else el.value  # maybe more, value3 is speed rool
        val_min = 0 if el.value3 < 5 else el.value

        if data_per_shift.get(el.mech.number):
            # bad
            data_per_shift[el.mech.number]['data'][date_t] = val_min, el.value3, el.value
            data_per_shift[el.mech.number]['time_coal'] += el.value
            data_per_shift[el.mech.number]['total_time'] += 1
        else:
            data_per_shift[el.mech.number] = {}
            data_per_shift[el.mech.number]['mechanism'] = el.mech
            data_per_shift[el.mech.number]['time_coal'] = el.value
            data_per_shift[el.mech.number]['total_time'] = 1
            data_per_shift[el.mech.number]['data'] = {}
            data_per_shift[el.mech.number]['data'][date_t] = val_min, el.value3, el.value
        data_per_shift[el.mech.number].setdefault('work_time', 0)
        if el.value > 0:
            data_per_shift[el.mech.number]['work_time'] += 1
    # get start time for this shift
    start = datetime.combine(date_shift, datetime.min.time())
    if shift == 1:
        start = start.replace(hour=8, minute=0, second=0, microsecond=0)
    else:
        start = start.replace(hour=20, minute=0, second=0, microsecond=0)

    if data_per_shift == {}:
        return None
    # create dict with all minutes to now if value is not return (-1) because
    # 0 may exist
    time_by_minuts = {}
    # pprint(data_per_shift)
    for key in data_per_shift.keys():
        flag_start = True
        mech = data_per_shift[key]['mechanism']
        time_by_minuts[key] = {}
        time_by_minuts[key]['name'] = mech.name
        time_by_minuts[key]['id'] = mech.id
        time_by_minuts[key]['number'] = mech.number
        time_by_minuts[key]['tons_in_hour'] =usm_tons_in_hour[mech.number]
        # translate hours into minutes and round
        time_by_minuts[key]['time_coal']  = round(data_per_shift[key]['time_coal'] / 60, 2)
        time_by_minuts[key]['total_time'] = round(data_per_shift[key]['total_time'] / 60, 1)
        time_by_minuts[key]['work_time']  = round(data_per_shift[key]['work_time'] / 60, 1)
        time_by_minuts[key]['data'] = {}
        delta_minutes = start
        try:
            last_find_item = db.session.query(Post).filter(Post.mechanism_id==data_per_shift[key]['mechanism'].id).order_by(Post.timestamp.desc()).first()
        except Exception as e:
            logger.debug(e)
        terminal = last_find_item.terminal
        time_coal = 0
        for i in range(1, 60 * 12 + 1):
            date_t = delta_minutes.strftime("%H:%M")
            val_minute = data_per_shift[key]['data'].setdefault(
                delta_minutes, (-1, -1, 0))
            if len(val_minute) < 3:
                print(val_minute)
            time_coal += val_minute[2] / 60
            time_by_minuts[key]['data'][i] = {'time': date_t,
                                              'value': val_minute[0],
                                              'speed': val_minute[1],
                                              'time_coal': round(time_coal, 2),
                                              'terminal': terminal,
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
    return time_by_minuts


def usm_periods(mechanisms_data):
    if not mechanisms_data:
        return None
    for mech, data_mech in mechanisms_data.items():
        # pprint(data_mech)
        values_period = -1
        new_data = {}
        step = 0
        pre_time = ''  # data_mech['data'][1]['time']
        counter = 1

        for number, value_number in data_mech['data'].items():
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
            else:
                step += 1
        new_data[counter] = {'time': pre_time,
                             'value': values_period, 
                             'step': step}
        mechanisms_data[mech]['data'] = new_data
    return mechanisms_data

def get_values_min(value_number):
    if value_number['value'] >= 0 and value_number['value'] < 0.1:
        if value_number['speed'] <= 5:
            return 0  # yellow
        else:
            # return 0  # yellow
            return 2 # dark yellow
    elif value_number['value'] >= 0.1:
        return  1  # blue
    else:
        return -1  # red


if __name__ == "__main__":
    from pprint import pprint
    # pprint(time_for_shift_usm(*today_shift_date()))
    pprint(usm_periods(time_for_shift_usm(*today_shift_date())))
