from app.functions_for_all import all_mechanisms_id, today_shift_date
from config import HOURS
from app.model import Post
from app import db
from datetime import datetime, timedelta


def time_for_shift_sennebogen(date_shift, shift):
    '''get dict with all minute's values for the period, name and total
    value is lever, value3 is speed roler,
    '''
    # get data from db
    shift = int(shift)
    all_mechs = all_mechanisms_id('sennebogen')
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
        x = -1 if el.value is None else el.value
        y = -1 if el.value2 is None else el.value2
        if x< 500 and y < 500: # and change state_mech in function
        # if y < 750: # and change state_mech in function
            value_minute = 0
        else:
            value_minute = 1

        if data_per_shift.get(el.mech.number):
            data_per_shift[el.mech.number]['data'][date_t] = value_minute, x, y # ? x, y
            data_per_shift[el.mech.number]['total_time'] += 1

        else:
            data_per_shift[el.mech.number] = {}
            data_per_shift[el.mech.number]['mechanism'] = el.mech
            data_per_shift[el.mech.number]['total_time'] = 1
            data_per_shift[el.mech.number]['data'] = {}
            data_per_shift[el.mech.number]['data'][date_t] = value_minute, x, y
        data_per_shift[el.mech.number].setdefault('work_time', 0)
        if value_minute != 0:
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
    #---------------------------PART2------------------------------  i don't want 2 functions
    time_by_minuts = {}
    # pprint(data_per_shift)
    for key in data_per_shift.keys():
        flag_start = True
        # flag_finish = True
        time_by_minuts[key] = {}
        time_by_minuts[key]['name'] = data_per_shift[key]['mechanism'].name
        time_by_minuts[key]['id'] = data_per_shift[key]['mechanism'].id
        time_by_minuts[key]['number'] = data_per_shift[key]['mechanism'].number
        # translate hours into minutes and round
        time_by_minuts[key]['total_time'] = round(
            data_per_shift[key]['total_time'] / 60, 1)
        time_by_minuts[key]['work_time'] = round(
            data_per_shift[key]['work_time'] / 60, 1)
        time_by_minuts[key]['data'] = {}
        delta_minutes = start
        time_move = 0
        for i in range(1, 60 * 12 + 1):
            date_t = delta_minutes.strftime("%H:%M")
            val_minute = data_per_shift[key]['data'].setdefault(
                delta_minutes, (-1, 0, 0))
            if val_minute[0] != -1:
                time_move +=val_minute[0] / 60
            time_by_minuts[key]['data'][i] = {'time': date_t,
                                              'value': val_minute[0],
                                              'x': val_minute[1],
                                              'y': val_minute[2],
                                              'time_move': round(time_move, 2),
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
    return time_by_minuts


def sennebogen_periods(mechanisms_data):
    if not mechanisms_data:
        return None
    for mech, data_mech in mechanisms_data.items():
        values_period = -1
        new_data = {}
        step = 0
        pre_time = ''  # data_mech['data'][1]['time']
        counter = 1

        for number, value_number in data_mech['data'].items():
            if value_number['value'] == 0:
                value_min = 0  # yellow
            elif value_number['value'] == 1:
                value_min = 1  # blue
            else:
                value_min = -1  # red

            if value_min != values_period:
                if values_period > 0:
                    values_period = 1
                new_data[counter] = {'time': pre_time,
                                     'value': values_period,
                                     'step': step,
                                     'time_move': value_number['time_move']}
                step = 1
                values_period = value_min
                pre_time = value_number['time']
                counter += 1
            else:
                step += 1
        new_data[counter] = {'time': pre_time,
                             'value': values_period, 'step': step}
        mechanisms_data[mech]['data'] = new_data
    return mechanisms_data

# from pprint import pprint

# pprint(time_for_shift_sennebogen(*today_shift_date()))
# pprint(sennebogen_periods(time_for_shift_sennebogen(*today_shift_date())))
