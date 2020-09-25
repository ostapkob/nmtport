from datetime import datetime, timedelta, date
from app.usm import time_for_shift_usm, usm_periods
from app.functions import all_mechanisms_id, today_shift_date, data_from_1c, data_from_1c_by_id, add_fio
from app.kran import time_for_shift_kran, kran_periods
from app.model import Post, Work_1C_1
from app import db
from pprint import pprint
from columnar import columnar


date_shift, shift = today_shift_date()
date_shift -= timedelta(days=1)
shift = 2


headers = ['INV_NUM', 'GREIFER_NUM', 'GREIFER_VOL', 'FIO','DATA_NACH', 'DATA_KON']
cursor = data_from_1c(date_shift, shift)
table = columnar(cursor, headers, no_borders=True)
# data_kran_period = kran_periods(time_for_shift_kran(date_shift, shift))
print(date_shift, shift)
print(table)


