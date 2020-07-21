from datetime import datetime, timedelta
from app.usm import time_for_shift_usm
from app.functions import today_shift_date
from pprint import pprint
def usm_periods(mechanisms_data):
    for mech, data_mech in mechanisms_data.items():
        vaues_period = -1
        new_data ={}
        step = 0
        pre_time = data_mech['data'][1]['time']
        counter = 1
        for number, value_number in data_mech['data'].items():
            if value_number['value'] !=vaues_period:
                if vaues_period>0:
                    vaues_period=1
                new_data[counter]={'time': pre_time, 'value': vaues_period, 'step':step}
                step=1
                vaues_period = value_number['value']
                pre_time = value_number['time']
                counter +=1
            else:
                step +=1

        mechanisms_data[mech]['data'] = new_data
    return mechanisms_data




date_shift, shift = today_shift_date()
# print(date_shift, shift)
data = time_for_shift_usm(date_shift, shift)
# for i in data.items():
#     print(i)
pprint(usm_periods(data))

