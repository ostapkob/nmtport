from datetime import datetime, timedelta
from app import db
from functions import today_shift_date, all_mechanisms_id,  multiple_5, time_for_shift, time_for_shift_list
from app.model import Mechanism, Post
from pprint import pprint
import json
db.create_all()
date_shift, shift = today_shift_date()

dd = time_for_shift(date_shift, shift)
pprint(dd)
bb= time_for_shift_list(date_shift, shift)
print(bb)




