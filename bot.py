import requests
import telebot
import json
import time
from pprint import pprint
from datetime import datetime

def chech_values(ls, num):
    if ls[0] == num:
        return False
    return( all(el==num for el in ls[1:]))

def today_shift_date():
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

tests = ( [[1, -1, -1, -1, -1], True],
        [[0, -1, -1, -1, -1], True],
        [[1, -1, -1, -1], True],
        [[-1, -1, -1, -1, -1], False],
        [[1, 1, -1, -1, -1], False],
        [[1, -1, 1, -1, -1], False],
        [[1, 1, -1, -1, -1], False],
        [[1, 1, -1, -1, -1], False],
        [[1, -1, -1, 1, -1], False],
        [[1, -1, -1, 1, -1], False],
        [[1, -1, -1, 1, -1], False],
        [[1, -1, -1, 1, -1], False],
        [[1, -1, -1, 1, -1], False],
        [[-1, -1, 1, -1], False],
        [[0,-1, -1, 1, -1], False],
        [[0.5, 0, -1, 1, -1], False],
        [[-1, 0, 0, 0, 0], False],
         )

# for values, res in tests:
#     if chech_values(values, -1) != res:
#         print(values)

# print('===================')
# for values, res in tests:
#     if chech_values(values, 0) != res:
        # print(values)

host ="http://35.241.126.216"
type_mechanism = "usm"
date_shift, shift = today_shift_date()
date = date_shift.strftime('%d.%m.%Y')
shift = str(shift)
API = f"/api/v1.0/get_data/{type_mechanism}/{date}/{shift}"
TOKEN = "977352466:AAEgH-c6FFFGbv71pSBP8hbtu9oSS6JrY48"
amount_elements = 5
bot = telebot.TeleBot(TOKEN)
while True:
    data = requests.get(host+API)
    mechanisms = json.loads(data.text)
    for mech, data_mech in mechanisms.items():
        data = data_mech['data']
        name_mech = data_mech['name']
        last_numbers = range(len(data)-amount_elements, len(data))
        values_last_5_minutes = [data[str(num)]['value'] for num in last_numbers]
        if chech_values(values_last_5_minutes, -1):
            bot.send_message(226566335, "-1" + name_mech)
            print("-1 -bo---->", name_mech)
        if chech_values(values_last_5_minutes, 0):
            bot.send_message(226566335, "0" + name_mech)
            print("0 ----->", name_mech)
    time.sleep(31)




