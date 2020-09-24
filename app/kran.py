from app.functions import all_mechanisms_id, today_shift_date
from app.functions import HOURS
from app.model import Post, Mechanism
from app import db
from datetime import datetime, timedelta
from collections import UserDict



def time_for_shift_kran(date_shift, shift):
    '''get dict with all minute's values for the period, name and total'''
    # get data from db
    shift = int(shift)
    all_mechs = all_mechanisms_id('kran')
    cursor = db.session.query(Post).filter(Post.date_shift == date_shift, Post.shift ==
                                           shift, Post.mechanism_id.in_(all_mechs)).order_by(Post.mechanism_id).all()
    # create dict all works mechanism in shift
    data_per_shift = {}
    for el in cursor:
        date_t = el.timestamp.replace(second=0, microsecond=0)
        date_t += timedelta(hours=HOURS)
        if data_per_shift.get(el.mech.number):
            data_per_shift[el.mech.number]['data'][date_t] = el.value, el.count
            if el.value==1:
                data_per_shift[el.mech.number]['total_90'] += 1
            if el.value==2:
                data_per_shift[el.mech.number]['total_180'] += 1
            # pre_value=el.count
        else:
            data_per_shift[el.mech.number] = {}
            data_per_shift[el.mech.number]['mechanism'] = el.mech
            data_per_shift[el.mech.number]['total_90'] = 0
            data_per_shift[el.mech.number]['total_180'] = 0
            if el.value==1:
                data_per_shift[el.mech.number]['total_90'] = 1
            if el.value==2:
                data_per_shift[el.mech.number]['total_180'] = 1
            data_per_shift[el.mech.number]['data'] = {}
            data_per_shift[el.mech.number]['data'][date_t] = el.value, el.count
            # pre_value=el.count

    # get start time for this shift
    start = datetime.combine(date_shift, datetime.min.time())
    if shift == 1:
        start = start.replace(hour=8, minute=0, second=0, microsecond=0)
    else:
        start = start.replace(hour=20, minute=0, second=0, microsecond=0)

    if data_per_shift == {}:
        return None
    # create dict with all minutes to now if value is not return (-1) because 0 may exist
    # time_by_minuts = {'date_shift': date_shift, 'shift': shift}
    time_by_minuts = {}
    for key, value in data_per_shift.items():
        flag_start=True
        flag_finish = True
        time_by_minuts[key] = {}
        time_by_minuts[key]['name'] = data_per_shift[key]['mechanism'].name
        time_by_minuts[key]['id'] = data_per_shift[key]['mechanism'].id
        # translate hours into minutes and round
        time_by_minuts[key]['total_180'] = round(data_per_shift[key]['total_180'], 2)
        time_by_minuts[key]['total_90'] = round(data_per_shift[key]['total_90'], 2)
        time_by_minuts[key]['data'] = {}
        delta_minutes = start
        for i in range(1, 60 * 12 + 1):
            date_t = delta_minutes.strftime("%H:%M")
            try:
                val_minute = data_per_shift[key]['data'][delta_minutes][0]
                # pre_value =  data_per_shift[key]['data'][delta_minutes][1]
            except KeyError:
                val_minute = -1
            time_by_minuts[key]['data'][i] = {'time': date_t, 'value': val_minute}
            delta_minutes += timedelta(minutes=1)
            today_date, today_shift = today_shift_date()
            if val_minute>0 and flag_start:
                time_by_minuts[key]['start'] = date_t
                flag_start =False
            if val_minute > 0:
                time_by_minuts[key]['finish'] = date_t
            if delta_minutes >= datetime.now() and date_shift == today_date and today_shift == shift:
                break

        # replace items from -1 to 0 if kran work
        pre_items = -1
        work_count = 0
        for number_item, data in time_by_minuts[key]['data'].items():
            if data['value'] == -1 and pre_items !=-1 and work_count<5:
                time_by_minuts[key]['data'][number_item]['value']=0
                work_count+=1
            else:
                work_count =0
            pre_items = data['value']


    return time_by_minuts


def kran_periods(mechanisms_data):
    if not mechanisms_data:
        return None
    for mech, data_mech in mechanisms_data.items():
        values_period = -1
        new_data ={}
        step = 0
        pre_time = ''
        counter = 1
        total_step = 0
        total_90_1 = 0 # 1
        total_180 = 0 # 2
        total_90_2 = 0 # 1
        for number, value_number in data_mech['data'].items():
            value_min = value_number['value'] # yellow
            if value_min !=values_period:
                # this part by accumulated total
                if values_period==1:
                    total_90_1+= step
                    total_step=total_90_1
                elif values_period == 2:
                    total_180 += step
                    total_step = total_180
                elif values_period == 3:
                    total_90_2 += step
                    total_step = total_90_2
                else:
                    total_step

                new_data[counter]={'time': pre_time, 'value': values_period, 'step':step, 'total': total_step}
                step=1
                values_period = value_min
                pre_time = value_number['time']
                counter +=1
            else:
                step +=1
        new_data[counter]={'time': pre_time, 'value': values_period, 'step':step}
        mechanisms_data[mech]['data'] = new_data
    return mechanisms_data
