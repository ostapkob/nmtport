import requests
import json
import time
from pprint import pprint
from datetime import datetime, timedelta
red_circle=u'\U0001F534'
yellow_circle=u'\U0001F7E1'

flag = True
try:
    import telebot
except:
    flag = False

def chech_values(ls, find, quantity):
    try:
        last_numbers = range(len(ls)-quantity, len(ls))
        values = [data[str(num)]['value'] for num in last_numbers]
    except:
        return False
    print("----->", name_mech, values)
    if values[0] == -1:
        return False
    if values[0] == find:
        return False
    if  all(el==find for el in values[1:]):
        return True
    return False

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
        [[-1, 0, 0, 0, 0], True],
         )

# for values, res in tests:
#     if chech_values(values, -1) != res:
#         print(values)

# print('===================')
# for values, res in tests:
#     if chech_values(values, 0) != res:
        # print(values)

host ="http://18.139.162.128"
type_mechanism = "usm"
TOKEN = "977352466:AAEgH-c6FFFGbv71pSBP8hbtu9oSS6JrY48"
if flag:
    bot = telebot.TeleBot(TOKEN)
while True:
    time.sleep(60)
    date_shift, shift = today_shift_date()
    date = date_shift.strftime('%d.%m.%Y')
    shift = str(shift)
    API = f"/api/v1.0/get_data/{type_mechanism}/{date}/{shift}"
    try:
        data = requests.get(host+API)
        mechanisms = json.loads(data.text)
    except:
        if flag:
            bot.send_message(226566335, 'Trouble with server')
            continue
    if not mechanisms:
        continue
    for mech, data_mech in mechanisms.items():
        data = data_mech['data']
        name_mech = data_mech['name']
        if chech_values(data, -1, 3):
            if flag:
                bot.send_message(226566335, f"{red_circle} {name_mech}")
        if chech_values(data, 0, 5):
            if flag:
                bot.send_message(226566335, f"{yellow_circle} {name_mech}")




