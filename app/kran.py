"""Its module work whith kran logigs"""
from datetime import datetime, timedelta, date
from rich import print

# from app import logger
from app import db
from app.model import Post

from app.functions_for_all import (
    all_mechanisms_id, get_start_shift, id_and_number, today_shift_date)
from config import HOURS

TYPE = 'kran'
ids_and_nums = id_and_number(TYPE)


def get_data_per_shift(cursor: list) -> dict:
    ''' create dict all works mechanism in shift '''
    data_per_shift = {}
    for item in cursor:
        date_t = item.timestamp.replace(second=0, microsecond=0)
        # use hours because count word time You can FIX it
        date_t += timedelta(hours=HOURS)
        if data_per_shift.get(item.mech.number):  # if exist
            if item.value in (1, 3):
                data_per_shift[item.mech.number]['total_90'] += 1
            if item.value == 2:
                data_per_shift[item.mech.number]['total_180'] += 1
                try:
                    data_per_shift[item.mech.number]['total_terminals_180'][str(
                        item.terminal)] += 1
                except KeyError:
                    data_per_shift[item.mech.number]['total_terminals_180'][str(
                        item.terminal)] = 1
            data_per_shift[item.mech.number]['data'][date_t] = item.value, item.count, item.terminal
        else:
            data_per_shift[item.mech.number] = {}
            data_per_shift[item.mech.number]['mechanism'] = item.mech
            data_per_shift[item.mech.number]['total_90'] = 0
            data_per_shift[item.mech.number]['total_180'] = 0
            data_per_shift[item.mech.number]['total_terminals_180'] = {}
            if item.value in (1, 3):  # 1 turn to bearch 3  turn to sea
                data_per_shift[item.mech.number]['total_90'] = 1
            if item.value == 2:
                data_per_shift[item.mech.number]['total_180'] = 1
                data_per_shift[item.mech.number]['total_terminals_180'][str(
                    item.terminal)] = 1
            data_per_shift[item.mech.number]['data'] = {}
            data_per_shift[item.mech.number]['data'][date_t] = item.value, item.count, item.terminal
    return data_per_shift


def get_time_by_minuts(data_per_shift: dict, date_shift: date, shift: int) -> dict:
    '''add empty minutes how -1'''
    start_shift = get_start_shift(date_shift, shift)
    time_by_minuts = {}
    terminal = 78
    for key in data_per_shift.keys():
        flag_start = True
        mech = data_per_shift[key]['mechanism']
        time_by_minuts[key] = {}
        time_by_minuts[key]['name'] = mech.name
        time_by_minuts[key]['id'] = mech.id
        time_by_minuts[key]['number'] = mech.number
        time_by_minuts[key]['total_terminals_180'] = data_per_shift[key]['total_terminals_180']
        # translate hours into minutes and round
        time_by_minuts[key]['total_180'] = round(
            data_per_shift[key]['total_180'], 2)
        time_by_minuts[key]['total_90'] = round(
            data_per_shift[key]['total_90'], 2)
        time_by_minuts[key]['data'] = {}
        delta_minutes = start_shift
        try:
            last_find_item = db.session.query(Post).filter(
                Post.mechanism_id == data_per_shift[key]['mechanism'].id).order_by(
                    Post.timestamp.desc()).first()
            tmp_terminal = last_find_item.terminal
        except Exception as err:
            print(err)
            tmp_terminal = 78

        for i in range(1, 60 * 12 + 1):  # 720 minutes in shift
            date_t = delta_minutes.strftime("%H:%M")
            try:
                val_minute = data_per_shift[key]['data'][delta_minutes][0]
            except KeyError:
                val_minute = -1
            try:
                terminal = data_per_shift[key]['data'][delta_minutes][2]
                tmp_terminal = terminal
            except KeyError:  # if item not exist get last found value
                terminal = tmp_terminal
            if val_minute == 4:  # show 4 how 0 look get api
                val_minute = 0
            time_by_minuts[key]['data'][i] = {
                'time': date_t,
                'value': val_minute,
                'terminal': terminal  # every step
            }
            delta_minutes += timedelta(minutes=1)
            today_date, today_shift = today_shift_date()
            if val_minute > 0 and flag_start:
                time_by_minuts[key]['start'] = date_t
                flag_start = False
            if val_minute > 0:
                time_by_minuts[key]['finish'] = date_t
            if delta_minutes >= datetime.now()\
                    and date_shift == today_date\
                    and today_shift == shift:  # if now moment
                break
        time_by_minuts[key]['data'] = add_4_minutes(
            time_by_minuts[key]['data'])
        # try:
        #     resons = process_resons(get_resons(TYPE, date_shift, shift), ids_and_nums)
        # except Exception as e:
        #     resons = {}
        # time_by_minuts[key]['resons'] = convert_resons_to_720minuts(
        # resons.get(mech.number, None), start_shift)
        time_by_minuts[key]['terminal'] = terminal  # last item
    return time_by_minuts


def add_4_minutes(mech_data: dict) -> dict:
    """
    if kran not spining around then it sent one value in 5 minutes,
    another minutes fill empty values
    """
    pre_items = -1
    work_count = 0
    last_value = 0
    for number_item, data in mech_data.items():
        if data['value'] == -1 and pre_items != -1 and work_count < 5:
            mech_data[number_item]['value'] = last_value
            work_count += 1
        else:
            last_value = 0
            if data['value'] == 5:  # if kran move
                last_value = 5
            work_count = 0
        pre_items = data['value']
    return mech_data


def time_for_shift_kran(date_shift: date, shift: int):
    '''get dict with all minute's values for the period, name and total'''
    # get data from db
    shift = int(shift)
    all_mechs = all_mechanisms_id(TYPE)
    try:
        cursor = db.session.query(Post).filter(Post.date_shift == date_shift,
                                               Post.shift == shift,
                                               Post.mechanism_id.in_(all_mechs)
                                               ).order_by(Post.mechanism_id).all()
        data_per_shift = get_data_per_shift(cursor)
    except Exception as err:
        print(err)
        return None
    time_by_minuts = get_time_by_minuts(data_per_shift, date_shift, shift)

    return time_by_minuts


def kran_periods(mechanisms_data):
    '''combine equal values of minutes'''
    if not mechanisms_data:
        return None
    for mech, data_mech in mechanisms_data.items():
        period_value = -1
        new_data = {}
        step = 0  # number of duplicate values
        pre_time = ''
        counter = 1  # number items
        total_step = 0
        total_90_1 = 0  # if value=1
        total_180 = 0  # if value=2
        total_90_2 = 0  # if value=3
        terminal = None
        for value_number in data_mech['data'].values():
            value_minute = value_number['value']
            terminal = value_number['terminal']
            if value_minute != period_value:  # if previous value != current value
                # this part by accumulated total
                if period_value == 1:
                    total_90_1 += step
                    total_step = total_90_1
                elif period_value == 2:
                    total_180 += step
                    total_step = total_180
                elif period_value == 3:
                    total_90_2 += step
                    total_step = total_90_2

                new_data[counter] = {
                    'time': pre_time,
                    'value': period_value,
                    'step': step,
                    'total': total_step,
                    'terminal': terminal,
                }
                step = 1
                period_value = value_minute
                pre_time = value_number['time']
                counter += 1
            else:
                step += 1  # if previous value == current value
        new_data[counter] = {  # last value in data
            'time': pre_time,
            'value': period_value,
            'step': step,
            'total': total_step,
            'terminal': terminal,
        }
        mechanisms_data[mech]['data'] = new_data
    return mechanisms_data


if __name__ == "__main__":
    # import pickle
    DATE_SHIFT = datetime.now().date()
    DATE_SHIFT -= timedelta(days=2)
    SHIFT = 1

    before_resons = kran_periods(time_for_shift_kran(DATE_SHIFT, SHIFT))

    # name_file_pickle = TYPE+'_'+str(date_shift)+"_"+str(shift)
    # with open(name_file_pickle, 'wb') as f:
    #     pickle.dump(before_resons, f)

    # with open(name_file_pickle, 'rb') as f:
    #     load = pickle.load(f)

    # print(load==before_resons)
