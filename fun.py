from datetime import datetime, timedelta, date
from app.usm import time_for_shift_usm, usm_periods
from app.kran import time_for_shift_kran
from app.functions import today_shift_date
from pprint import pprint




def kran_periods(mechanisms_data):
    for mech, data_mech in mechanisms_data.items():
        values_period = -1
        new_data ={}
        step = 0
        pre_time = ''
        counter = 1
        for number, value_number in data_mech['data'].items():
            value_min = value_number['value'] # yellow

            if value_min !=values_period:
                new_data[counter]={'time': pre_time, 'value': values_period, 'step':step}
                step=1
                values_period = value_min
                pre_time = value_number['time']
                counter +=1
            else:
                step +=1
        new_data[counter]={'time': pre_time, 'value': values_period, 'step':step}
        mechanisms_data[mech]['data'] = new_data
    return mechanisms_data

date_shift, shift = today_shift_date()
# print(date_shift, shift)
d = date(2020,9, 12)
data = time_for_shift_kran(d, 2)
for i in data.items():
    print(i)

# pprint(data[1])

pprint(kran_periods(data))

