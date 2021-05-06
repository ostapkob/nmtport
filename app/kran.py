from app.functions_for_all import all_mechanisms_id, today_shift_date
from config import HOURS, names_terminals
from app.model import Post
from app import db
from datetime import datetime, timedelta
from app  import logger

def time_for_shift_kran(date_shift, shift):
    '''get dict with all minute's values for the period, name and total'''
    # get data from db
    shift = int(shift)
    all_mechs = all_mechanisms_id('kran')
    try:
        cursor = db.session.query(Post).filter(Post.date_shift == date_shift, Post.shift ==
                                               shift, Post.mechanism_id.in_(all_mechs)).order_by(Post.mechanism_id).all()
    except:
        None
    # create dict all works mechanism in shift
    data_per_shift = {}
    for el in cursor:
        date_t = el.timestamp.replace(second=0, microsecond=0)
        date_t += timedelta(hours=HOURS)
        if data_per_shift.get(el.mech.number): # if exist
            if el.value == 1 or el.value == 3:  # 123
                data_per_shift[el.mech.number]['total_90'] += 1
            if el.value == 2:
                data_per_shift[el.mech.number]['total_180'] += 1
                try:
                    data_per_shift[el.mech.number]['total_terminals_180'][str(el.terminal)] +=1
                except KeyError:
                    data_per_shift[el.mech.number]['total_terminals_180'][str(el.terminal)] = 1
            data_per_shift[el.mech.number]['data'][date_t] = el.value, el.count, el.terminal
            # pre_value=el.count # if will be problem with GPRS
        else:
            data_per_shift[el.mech.number] = {}
            data_per_shift[el.mech.number]['mechanism'] = el.mech
            data_per_shift[el.mech.number]['total_90'] = 0
            data_per_shift[el.mech.number]['total_180'] = 0
            data_per_shift[el.mech.number]['total_terminals_180'] = {}
            if el.value == 1:
                data_per_shift[el.mech.number]['total_90'] = 1
            if el.value == 2:
                data_per_shift[el.mech.number]['total_180'] = 1
                data_per_shift[el.mech.number]['total_terminals_180'][str(el.terminal)] = 1
            data_per_shift[el.mech.number]['data'] = {}
            data_per_shift[el.mech.number]['data'][date_t] = el.value, el.count, el.terminal
            # pre_value=el.count

    # get start time for this shift
    start = datetime.combine(date_shift, datetime.min.time())
    if shift == 1:
        start = start.replace(hour=8, minute=0, second=0, microsecond=0)
    else:
        start = start.replace(hour=20, minute=0, second=0, microsecond=0)

    if data_per_shift == {}:
        return None
    #---------------------------PART2------------------------------  i don't want 2 functions
    # create dict with all minutes to now if value is not return (-1) because 0 may exist
    time_by_minuts = {}
    for key, value in data_per_shift.items():
        flag_start = True
        time_by_minuts[key] = {}
        time_by_minuts[key]['name'] = data_per_shift[key]['mechanism'].name
        time_by_minuts[key]['number'] = data_per_shift[key]['mechanism'].number
        time_by_minuts[key]['id'] = data_per_shift[key]['mechanism'].id
        time_by_minuts[key]['total_terminals_180'] = data_per_shift[key]['total_terminals_180']
        # translate hours into minutes and round
        time_by_minuts[key]['total_180'] = round(data_per_shift[key]['total_180'], 2)
        time_by_minuts[key]['total_90'] = round(data_per_shift[key]['total_90'], 2)
        time_by_minuts[key]['data'] = {}
        delta_minutes = start
        last_find_item = db.session.query(Post).filter(Post.mechanism_id==data_per_shift[key]['mechanism'].id).order_by( Post.timestamp.desc()).first()
        tmp_terminal = last_find_item.terminal
        # time_by_minuts[key]['total_terminals_180'] = {str(tmp_terminal): 0} # str becouse mongo need str key
        for i in range(1, 60 * 12 + 1): # 720 minutes in shift
            date_t = delta_minutes.strftime("%H:%M")
            try:
                val_minute = data_per_shift[key]['data'][delta_minutes][0]
            except KeyError:
                val_minute = -1
            try:
                terminal = data_per_shift[key]['data'][delta_minutes][2]
                tmp_terminal = terminal
            except KeyError: # if item not exist get last found value
                terminal = tmp_terminal
            time_by_minuts[key]['data'][i] = {
                'time': date_t, 'value': val_minute, 'terminal': terminal}
            delta_minutes += timedelta(minutes=1)
            today_date, today_shift = today_shift_date()
            if val_minute > 0 and flag_start:
                time_by_minuts[key]['start'] = date_t
                flag_start = False
            if val_minute > 0:
                time_by_minuts[key]['finish'] = date_t
            if delta_minutes >= datetime.now() and date_shift == today_date and today_shift == shift: # if now moment 
                break

        # replace items from -1 to 0 if kran work
        pre_items = -1
        work_count = 0
        for number_item, data in time_by_minuts[key]['data'].items():
            if data['value'] == -1 and pre_items != -1 and work_count < 5:
                time_by_minuts[key]['data'][number_item]['value'] = 0
                work_count += 1
            else:
                work_count = 0
            pre_items = data['value']

    return time_by_minuts


def kran_periods(mechanisms_data):
    if not mechanisms_data:
        return None
    for mech, data_mech in mechanisms_data.items():
        period_value = -1
        new_data = {}
        step = 0 # number of duplicate values
        pre_time = ''
        counter = 1 #number items
        total_step = 0
        total_90_1 = 0  # if value=1
        total_180 = 0  # if value=2
        total_90_2 = 0  # if value=3
        terminal = None
        for number, value_number in data_mech['data'].items():
            value_minute = value_number['value']  
            terminal = value_number['terminal']
            if value_minute != period_value: #if previous value != current value
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
                else:
                    total_step

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
                step += 1 # if previous value == current value
        new_data[counter] = { # last value in data
                            'time': pre_time,
                            'value': period_value,
                            'step': step,
                            'total': total_step,
                            'terminal': terminal,
                            }
        mechanisms_data[mech]['data'] = new_data
    return mechanisms_data

# if __name__ == "__main__":
#     from pprint import pprint
#     pprint(time_for_shift_kran(*today_shift_date()))
