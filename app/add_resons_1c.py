#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rich import print
from datetime import datetime, timedelta
from app import db
from app.model import Mechanism_downtime_1C
#from app.model import Rfid_work, Rfid_ids
#from app import db
from app.functions_for_all import get_start_shift
# from app.usm import usm_periods, time_for_shift_usm # DEL
# from app.kran import kran_periods, time_for_shift_kran # DEL
#from typing import Dict, List

# def get_resons(type_mechanisms: str, date_shift: datetime.date, shift: int) -> dict:
#    shift = int(shift)
#    all_mechs = all_mechanisms_id(type_mechanisms)
#    cursor = db.session.query(MD).filter(MD.data_smen == date_shift, MD.smena ==
#                                           shift, MD.inv_num.in_(all_mechs)).order_by(MD.inv_num).all()
#    return cursor


# def process_resons(resons: list, ids_and_nums:list) -> dict:
#    result:dict = {}
#    for el in resons:
#        number = ids_and_nums[el.inv_num]
#        start = el.data_nach
#        stop = el.data_kon
#        reson = el.id_downtime
#        try:
#            result[number].append(
#                {
#                    'start': start,
#                    'stop': stop,
#                    'reson': reson
#                }
#            )
#        except KeyError:
#            result[number] = []
#            result[number].append(
#                {
#                    'start': start,
#                    'stop': stop,
#                    'reson': reson
#                }
#            )
#    return result


# def handle_reson(start:datetime, stop:datetime, reson:[int, None]):
#    start = start.replace(second=0)
#    stop = stop.replace(second=0)
#    return {
#        "start": start.strftime("%H:%M"),
#        "stop": stop.strftime("%H:%M"),
#        "reson": reson,
#        "step": int((stop - start).total_seconds()/60)
#    }

# #DEL
# def convert_resons_to_720minuts(resons: List[Dict[str, object]], start_shift: datetime) -> dict:
#    if not resons:
#        return {}
#    result: dict = {
#        '0': handle_reson(start_shift,  resons[0]["start"],  None)
#    }
#    count = 0
#    for i in range(len(resons)):
#        count += 1
#        result[str(count)] = handle_reson(
#            resons[i]["start"], resons[i]["stop"],  resons[i]["reson"])
#        count += 1
#        try:
#            result[str(count)] = handle_reson(
#                resons[i]["stop"], resons[i+1]["start"],  None)
#        except IndexError:
#            result[str(count)] = handle_reson(
#                resons[i]["stop"], start_shift + timedelta(minutes=719), None)
#    return result

def _count_step(start: datetime, stop: datetime) -> int:
    return int(round((stop - start).total_seconds()/60))


def _add_empty_spaces(resons, start_shift):
    if not resons:
        return {}
    stop_shift = start_shift + timedelta(hours=12)
    resons = sorted(resons, key=lambda r: r.data_nach)
    result = []
    if start_shift != resons[0].data_nach:
        result.append([start_shift, resons[0].data_nach, None])
    for i in range(len(resons)):
        result.append(
            [resons[i].data_nach, resons[i].data_kon, resons[i].id_downtime])
        try:
            result.append([resons[i].data_kon, resons[i+1].data_nach, None])
        except IndexError:
            if stop_shift != resons[i].data_kon:
                result.append([resons[i].data_kon, stop_shift, None])
    return result


def _del_dublicates(items):
    new_items = []
    tmp_list = []
    for i in items:
        if i.data_nach in tmp_list:
            continue
        tmp_list.append(i.data_nach)
        new_items.append(i)
    return new_items


def _add_steps(resons):
    if not resons:
        return {}
    result = {}
    sum_step = 0
    for en, i in enumerate(resons):
        result[str(en)] = {
            "start": i[0].strftime("%H:%M"),
            "stop": i[1].strftime("%H:%M"),
            "reson": i[2],
            "step": _count_step(i[0], i[1])
        }
        sum_step += _count_step(i[0], i[1])
    # if sum_step > 720:
    #     print(sum_step)
    # if sum_step < 717:
    #     print(sum_step)
    return result


def add_resons_from_1c(data_period, date, shift):
    if not data_period:
        return {}
    ids = [x['id'] for x in data_period.values()]
    cursor = db.session.query(Mechanism_downtime_1C).filter(
        Mechanism_downtime_1C.data_smen == date,
        Mechanism_downtime_1C.smena == shift,
        Mechanism_downtime_1C.inv_num.in_(ids),
    ).all()
    start_shift = get_start_shift(date, shift)
    for key, value in data_period.items():
        mech_id = value['id']
        resons_1c = [x for x in cursor if x.inv_num == mech_id]
        resons_1c = _del_dublicates(resons_1c)
        resons_1c = _add_empty_spaces(resons_1c, start_shift)
        resons_1c = _add_steps(resons_1c)
        data_period[key]['resons'] = resons_1c
    return data_period


if __name__ == "__main__":
    import pickle
    TYPE = 'usm'
    date = datetime.now().date()
    date -= timedelta(days=1)
    shift = 2
    name_file_pickle = 'New' + TYPE+'_'+str(date)+"_"+str(shift)
    # res = kran_periods(time_for_shift_kran(date, shift))
    # res = usm_periods(time_for_shift_usm(date, shift))
    # with open(name_file_pickle, 'wb') as f:
    #     pickle.dump(res, f)

    with open(name_file_pickle, 'rb') as f:
        load = pickle.load(f)

    res = add_resons_from_1c(load, date, shift)
    print(date, shift)
    print(res)
