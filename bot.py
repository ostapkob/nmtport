import requests
import telebot
import json
import time
from pprint import pprint

def chech_values(ls, num):
    if ls[0] == num:
        return False
    return( all(el==num for el in ls[1:]))


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





server_ip ="http://35.241.126.216"
type_mechanism = "usm"
date_shift = "17.01.2020"
shift = "1"
API = f"/api/v1.0/get_data/{type_mechanism}/{date_shift}/{shift}"
TOKEN = "977352466:AAEgH-c6FFFGbv71pSBP8hbtu9oSS6JrY48"
amount_elements = 5
data = requests.get(server_ip+API)
mechanisms = json.loads(data.text)
# pprint(mechanisms)
bot = telebot.TeleBot(TOKEN)


bot.send_message(226566335, 'start')


for mech, data_mech in mechanisms.items():
    data = data_mech['data']
    name_mech = data_mech['name']
    last_numbers = range(len(data)-amount_elements, len(data))
    values_last_5_minutes = [data[str(num)]['value'] for num in last_numbers]
    print(values_last_5_minutes)
    if chech_values(values_last_5_minutes, -1):
        bot.send_message(226566335, name_mech)
        print("-1 -bo---->", name_mech)
    if chech_values(values_last_5_minutes, 0):
        bot.send_message(226566335, name_mech)
        print("0 ----->", name_mech)
