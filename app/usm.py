from functions import all_mechanisms_id
from app.model import Post, Mechanism
from app import db
from datetime import datetime, timedelta
from functions import HOURS
from functions import today_shift_date

def time_for_shift_usm(date_shift, shift):
    '''get dict with all minute's values for the period, name and total
    value is lever, value3 is speed roler,
    '''
    # get data from db
    shift = int(shift)
    all_mechs = all_mechanisms_id('usm')
    cursor = db.session.query(Post).filter(Post.date_shift == date_shift, Post.shift ==
                                           shift, Post.mechanism_id.in_(all_mechs)).order_by(Post.mechanism_id).all()
    # create dict all works mechanism in shift
    data_per_shift = {}
    for el in cursor:
        date_t = el.timestamp.replace(second=0, microsecond=0)
        date_t += timedelta(hours=HOURS)
        # date_t = date_t.strftime("%H:%M")
        el.value = -1 if el.value is None else el.value
        el.value3 = 0 if el.value3 is None else el.value3
        val_minute = 0 if el.value < 0.1 else el.value
        el.value = 0 if el.value3<10 else el.value # maybe more
        val_minute = 0 if el.value3<10 else el.value # maybe more

        if data_per_shift.get(el.mech.number):
            data_per_shift[el.mech.number]['data'][date_t] = val_minute, el.value3
            data_per_shift[el.mech.number]['total'] += el.value
        else:
            data_per_shift[el.mech.number] = {}
            data_per_shift[el.mech.number]['mechanism'] = el.mech
            data_per_shift[el.mech.number]['total'] = el.value
            data_per_shift[el.mech.number]['data'] = {}
            data_per_shift[el.mech.number]['data'][date_t] = val_minute, el.value3
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
    for key  in data_per_shift.keys():
        flag_start=True
        flag_finish = True
        time_by_minuts[key] = {}
        time_by_minuts[key]['name'] = data_per_shift[key]['mechanism'].name
        # translate hours into minutes and round
        time_by_minuts[key]['total'] = round(
            data_per_shift[key]['total'] / 60, 2)
        time_by_minuts[key]['data'] = {}
        delta_minutes = start
        for i in range(1, 60 * 12 + 1):
            date_t = delta_minutes.strftime("%H:%M")
            val_minute = data_per_shift[key]['data'].setdefault(delta_minutes, (-1, -1))
            time_by_minuts[key]['data'][i] = {'time': date_t, 'value': val_minute[0], "speed": val_minute[1]}
            delta_minutes += timedelta(minutes=1)
            today_date, today_shift = today_shift_date()
            if val_minute[0]>0 and flag_start:
                time_by_minuts[key]['start'] = date_t
                flag_start =False
            if val_minute[0] > 0:
                time_by_minuts[key]['finish'] = date_t
            if delta_minutes >= datetime.now() and date_shift == today_date and today_shift == shift:
                break
    return time_by_minuts
