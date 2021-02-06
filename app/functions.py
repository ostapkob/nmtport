from datetime import datetime, timedelta
from flask import flash, redirect, url_for
from app.model import Post, Mechanism, Work_1C_1
from app import db
from config import TIME_PERIODS
from config import lines_krans, names_terminals
HOURS = 10  # your timezone


def today_shift_date():
    '''get date and shift'''
    hour = datetime.now().hour
    if hour >= 8 and hour < 20:
        date_shift = datetime.now()
        shift = 1
    elif hour < 8:
        date_shift = datetime.now() - timedelta(days=1)
        shift = 2
    else:
        date_shift = datetime.now()
        shift = 2
    return date_shift.date(), shift


def all_mechanisms_id(type=None):
    '''Find all mechanisms id'''
    if type is None:
        try:
            return [m.id for m in db.session.query(Mechanism).all()]
        except:
            return []
    try:
        return [m.id for m in db.session.query(Mechanism).filter(
            Mechanism.type == type).all()]
    except:
        return []


def all_mechanisms_type():
    '''Find all mechanisms type'''
    ls = [m.type for m in db.session.query(Mechanism).all()]
    return set(ls)


def all_number(type, number):
    '''Need to do then'''
    return [m.id for m in Mechanism.query.all()]


def name_by_id(id):
    '''Need to do then'''
    return Mechanism.query.filter(Mechanism.id == id).first().name


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
        Work_1C_1.inv_num == id_mech).all()
    data_1C = [x.get() for x in cursor]
    return data_1C


def fio_to_fi(item):
    fio = item[3].split()
    if not fio:
        return None
    return f'{fio[0].capitalize()} {fio[1][0]}.'


def add_fio(data_kran_period, date_shift, shift):
    ''' add fio and grab if it exec'''
    if not data_kran_period:
        return None
    for key, value in data_kran_period.items():
        id_mech = data_kran_period[key]['id']
        data_by_id_mech = data_from_1c_by_id(date_shift, shift, id_mech)
        if len(data_by_id_mech) < 1:
            data_kran_period[key]['fio'] = None
            data_kran_period[key]['grab'] = None
            data_kran_period[key]['contract'] = None
        elif len(data_by_id_mech) == 1:
            data_kran_period[key]['fio'] = fio_to_fi(data_by_id_mech[0])
            data_kran_period[key]['contract'] = data_by_id_mech[0][8]
            if data_by_id_mech[0][2] == 0:
                data_kran_period[key]['grab'] = None
            else:
                data_kran_period[key]['grab'] = data_by_id_mech[0][2]
        else:
            for operator in data_by_id_mech:
                data_kran_period[key]['fio'] = 'Два оператора'
                data_kran_period[key]['contract'] = 1
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
        if value == 0:  # 123
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
    # print(dt,  values_14_10, values_9_0)
    if sum(values_9_0) > 0:
        return False

    if sum(values_14_10) <= 0:
        return False

    return True


def get_status_alarm(mech_id):
    last = db.session.query(Post).filter(
        Post.mechanism_id == mech_id).order_by(
        Post.timestamp.desc()).limit(15)
    now_hour = datetime.now().hour + datetime.now().minute/60
    result = any(now_hour > t1 and now_hour < t2 for t1, t2 in TIME_PERIODS)
    if result:
        return False
    return is_alarm(last)


def straight_line_equation(x1, y1, x2, y2):
    k = (y1 - y2) / (x1 - x2)
    b = y2 - k * x2
    return k, b


def perpendicular_line_equation(k1, b1, mx, my):
    k2 = - (1/k1)
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


def which_terminal(latitude, longitude, flag=True):
    k1, b1 = 0.5932709085972241, 107.49050635162425
    k2, b2 = perpendicular_line_equation(
        k1, b1, float(latitude), float(longitude))
    nx, ny = intersection_point_of_lines(k1, b1, k2, b2)
    name_terminal = 9
    for name, lon in names_terminals:
        if ny < lon:
            if not flag:
                print(name,  ny,  '<',  lon)
            name_terminal = name
            # print(names_terminals, )
    return name_terminal


if __name__ == "__main__":
    x1, y1 = 42.80691726848499, 132.88660505374455
    x2, y2 = 42.81408152044796, 132.89085539601604
    # x1, y1 = 42.807735079133295, 132.88577535577383
    # x2, y2 = 42.81760201722565, 132.89163529190128
    # x1, y1 = 42.81381686151741, 132.89146624081198
    # x2, y2 = 42.81697813067333, 132.89335636137457
    # print(straight_line_equation(x1, y1, x2, y2))
    print()

    test = [
        [9, [132.89194679066017, 42.81736550995399]], [9, [132.89257462348414, 42.81589379423502]], [9, [132.88986696392485, 42.81595748772176]], [9, [132.89161522194811, 42.81419894232471]], [9, [132.88916770035377, 42.81475478530103]], [9, [132.88917668763676, 42.81476989016062]], [9, [132.89137483936300, 42.81404213350927]], [9, [132.88990317783382, 42.81615568248341]], [9, [132.89020564075590, 42.81567523049253]], [9, [132.89042573840710, 42.81522114523636]], [9, [132.89058743687528, 42.81483370688806]], [9, [132.89074913534347, 42.81444626611244]], [9, [132.89103938675726, 42.81413754727080]], [9, [132.88905238171193, 42.81472577146314]], [9, [132.88948020966708, 42.81484054704739]], [9, [132.89005630963496, 42.81503972041025]], [9, [132.89073024692019, 42.81518359284351]], [9, [132.89136573255382, 42.81520790672962]], [9, [132.89210231604280, 42.81531973361439]], [11, [132.8891646231937, 42.81419314664282]], [11, [132.8888248696648, 42.81370081717350]], [11, [132.88991758824514, 42.81333378283207]], [11, [132.8895013421617, 42.813106384954210]], [
            11, [132.88857236403388, 42.81319772391066]], [11, [132.88782603382631, 42.81261228981140]], [11, [132.88907575397195, 42.81246977997844]], [11, [132.88835626010132, 42.81204749736881]], [11, [132.88918006475876, 42.81154327759049]], [13, [132.88840048662553, 42.81101999945392]], [13, [132.88784625048788, 42.81111158159720]], [13, [132.8872512688971, 42.811370787187370]], [13, [132.88699984920487, 42.81098755490390]], [13, [132.88792165710373, 42.81072675441268]], [13, [132.88861605517303, 42.81055594248610]], [13, [132.88789764724106, 42.81025352816530]], [13, [132.88712132692385, 42.81008988483347]], [13, [132.88638900987576, 42.81011825912287]], [13, [132.88747955657874, 42.80951143862879]], [15, [132.88535149641822, 42.80849242190669]], [15, [132.88586498710285, 42.80856846706237]], [15, [132.88661262650422, 42.80805425483484]], [15, [132.88658177371104, 42.80713661372471]], [15, [132.88585086990005, 42.80700994885330]], [15, [132.8864242215921, 42.808406576413830]], [15, [132.88706787750513, 42.80854399911098]]
    ]

    for ans, [y, x] in test:
        # print(x, y)
        if ans != which_terminal(x, y):
            print(ans, which_terminal(x, y, False))
