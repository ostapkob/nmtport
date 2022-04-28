from pymongo import MongoClient
from datetime import datetime, timedelta
from pprint import pp
from collections import defaultdict
from dateutil.parser import parse
import json
'''
this Template
not use 
'''

client = MongoClient('mongodb://localhost:27017')
mongodb = client['HashShift']

kransUT = [45, 34, 53, 69, 21, 37, 4, 41, 5, 36, 40, 32, 25, 11, 33, 20, 8, 22, 12, 13, 6, 26, 47, 54, 14, 16, 82]
kransGUT = [28, 18, 1, 35, 31, 17, 58, 60, 49, 38, 39, 23, 48, 72, 65, 10]

def minutes_from_start(times, start_shift):
    return [(x - start_shift).seconds // 60 for x in times]

def minutes_to_finish(times, start_shift):
    finish_shift = start_shift + timedelta(hours=12)
    return [(finish_shift - x ).seconds // 60 for x in times]

def avg_minutes(minutes):
    if minutes:
        return int(sum(minutes) / len(minutes))
    return 0

def get_time_start_and_stop(req, date_shift, shift):
    gut_start  = []
    gut_finish = []
    ut_start   = []
    ut_finish  = []

    start_shift = get_start_shift(date_shift, shift) # 2022-01-01 08:00:00
    for mech in req.values():
        assert mech != None
        start = mech.get('start', None)
        finish = mech.get('finish', None)
        if start is None:
            continue
        if mech['number'] in kransUT:
            ut_start.append ( add_time_to_date_shift(date_shift, start) ) #  datetime.datetime(2022, 1, 1, 8, 27), ...
            ut_finish.append( add_time_to_date_shift(date_shift, finish) )
        else:
            gut_start.append( add_time_to_date_shift(date_shift, start) )
            gut_finish.append( add_time_to_date_shift(date_shift, finish) )

    minutes_ut_start   = minutes_from_start(ut_start, start_shift) # [27, 29, 659, 23, 31, 426, 471, 133, 17, 17, 19, 383]
    minutes_ut_finish  = minutes_to_finish(ut_finish, start_shift)
    minutes_gut_start  = minutes_from_start(gut_start, start_shift)
    minutes_gut_finish = minutes_to_finish(gut_finish, start_shift)
   
    minutes_ut_start   = [x for x in minutes_ut_start   if x<90] # [27, 29, 23, 31, 17, 17, 19]
    minutes_ut_finish  = [x for x in minutes_ut_finish  if x<90]
    minutes_gut_start  = [x for x in minutes_gut_start  if x<90]
    minutes_gut_finish = [x for x in minutes_gut_finish if x<90]

    result = {
            'ut': {
                'start' : avg_minutes(minutes_ut_start),
                'finish' : avg_minutes(minutes_ut_finish),
            },
            'gut': {
                'start' : avg_minutes(minutes_gut_start),
                'finish' : avg_minutes(minutes_gut_finish),
            }
    }
    return result

def add_time_to_date_shift(date_shift: datetime, time: str) -> datetime:
    date_shift = datetime.combine(date_shift, datetime.min.time())
    h, m = time.split(':')
    h= int(h)
    m = int(m)
    if h<8:
        return date_shift.replace(hour=h, minute=m) + timedelta(days=1)
    else:
        return date_shift.replace(hour=h, minute=m)


def get_start_shift(date_shift, shift):
    start_shift = datetime.combine(date_shift, datetime.min.time())
    if shift == 1:
        return start_shift.replace(hour=8, minute=0, second=0, microsecond=0)
    else:
        return start_shift.replace(hour=20, minute=0, second=0, microsecond=0)

def get_avr_time(times):
    if not times:
        return 0
    mysum = timedelta()
    for i in times:
        h = i.hour
        m = i.minute
        mysum += timedelta(hours=int(h), minutes=int(m))
    return mysum/len(times)



def diapozone_time_work(date_start, date_finish):
    date_shift = date_start
    result = defaultdict(dict)
    while date_shift <= date_finish:
        for shift in range(1,3):
            date_str = date_shift.strftime("%d.%m.%Y")
            mongo_request = mongodb[type_mechanism].find_one({"_id": f"{date_str}|{shift}"})
            if not mongo_request:
                continue
            del mongo_request["_id"]
            start_stop_for_shift = get_time_start_and_stop(mongo_request, date_shift, shift)
            result[ date_shift.strftime("%Y-%m-%d") ] [shift] = start_stop_for_shift
        date_shift += timedelta(days=1)
    return result


date_start  = datetime(2022, 3,  1).date()
date_finish = datetime(2022, 3, 8).date()
type_mechanism = 'kran'

data=diapozone_time_work(date_start, date_finish)
# pp(data)
for k,v in data.items():
    us1, uf1 = v[1]['ut']['start'],  v[1]['ut']['finish']
    # gs1, gf1 = v[1]['gut']['start'], v[1]['gut']['finish']

    try:
        us2, uf2 = v[2]['ut']['start'],  v[2]['ut']['finish']
    except:
        print(k)
    # gs2, gf2 = v[2]['gut']['start'], v[2]['gut']['finish']

    print(k, 1 , 'UT',  us1, uf1)
    # print(k, 1 , 'GUT', gs1, gf1)
    print(k, 2 , 'UT',  us2, uf2)
    # print(k, 2 , 'GUT', gs2, gf2)

# with open("data.json", "w") as f:
#     json.dump(data, f, indent=4, sort_keys=True, default=str)


