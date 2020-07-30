from datetime import datetime, timedelta, date
from app.usm import time_for_shift_usm
from app.functions import today_shift_date
from pprint import pprint





date_shift, shift = today_shift_date()
# print(date_shift, shift)
d = date(2020,7, 18)
data = time_for_shift_usm(d, 1)
# for i in data.items():
#     print(i)
pprint(data)

pprint(usm_periods(data))

