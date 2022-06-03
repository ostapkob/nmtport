from app.functions_for_all import *
from config import HOURS
from app.model import Post
from app import db
from datetime import datetime, timedelta

TYPE = 'sennebogen'
ids_and_nums = id_and_number(TYPE)

def get_data_per_shift(cursor: dict) -> dict:
    '''create dict with all minutes to now if value is None return (-1) because  0 may exist'''
    data_per_shift = {}
    for el in cursor:
        date_t = el.timestamp.replace(second=0, microsecond=0)
        date_t += timedelta(hours=HOURS)
        x = -1 if el.value is None else el.value
        y = -1 if el.value2 is None else el.value2

        #acselerometer
        if x< 500 and y < 500: # and change state_mech in function
        # if (x>300 and y > 300) or x>700 or y>700 :  
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
    return data_per_shift


def get_time_by_minuts(data_per_shift: dict, date_shift: datetime, shift: int):
    start_shift = get_start_shift(date_shift, shift)
    time_by_minuts = {}
    for key in data_per_shift.keys():
        flag_start = True
        mech = data_per_shift[key]['mechanism']
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
        delta_minutes = start_shift
        try:
            # ! maybe is slower request
            last_find_item = db.session.query(Post).filter(Post.mechanism_id==data_per_shift[key]['mechanism'].id).order_by(Post.timestamp.desc()).first()
        except Exception as e:
            logger.debug(e)
        terminal = last_find_item.terminal
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
        # try:
        #     resons = process_resons(get_resons(TYPE, date_shift, shift), ids_and_nums)
        # except Exception as e:
        #     resons = {}
        # time_by_minuts[key]['resons'] = convert_resons_to_720minuts(resons.get(mech.number, None), start_shift)

    return time_by_minuts



def time_for_shift_sennebogen(date_shift: datetime, shift: int) -> dict:
    '''get dict with all minute's values for the period, name and total
    value is lever, value3 is speed roler,
    '''
    shift = int(shift)
    all_mechs = all_mechanisms_id(TYPE)
    start_shift = get_start_shift(date_shift, datetime.min.time())
    try:
        cursor = db.session.query(Post).filter(Post.date_shift == date_shift, Post.shift ==
                                               shift, Post.mechanism_id.in_(all_mechs)).order_by(Post.mechanism_id).all()
    except Exception as e:
        logger.debug(e)

    data_per_shift = get_data_per_shift(cursor) # create dict all works mechanism in shift

    if data_per_shift == {}:
        return {}

    time_by_minuts =  get_time_by_minuts(data_per_shift, date_shift, shift)
    return time_by_minuts


def sennebogen_periods(mechanisms_data: dict) -> dict:
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



if __name__ == "__main__":
    from pprint import pp
    import pickle
    date_shift = datetime.now().date()
    date_shift -= timedelta(days=3)
    shift = 1

    before_resons = sennebogen_periods(time_for_shift_sennebogen(date_shift, shift))
    # pp(before_resons)

    name_file_pickle = TYPE+'_'+str(date_shift)+"_"+str(shift)
    # with open(name_file_pickle, 'wb') as f:
    #     pickle.dump(before_resons, f)

    with open(name_file_pickle, 'rb') as f:
        load = pickle.load(f)

    pp(load==before_resons)



