from datetime import datetime, timedelta, date
from app.usm import time_for_shift_usm, usm_periods
from app.functions import today_shift_date
from pprint import pprint





date_shift, shift = today_shift_date()
# print(date_shift, shift)
d = date(2020,8, 13)
data = time_for_shift_usm(d, 2)
# for i in data.items():
#     print(i)
pprint(data[1])

pprint(usm_periods(data)[1])

