#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import db
from app.model import  Mechanism, Rfid_ids
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict
from app.model import Post, Mechanism_downtime_1C as MD

def all_mechanisms_id(type=None):
    '''Find all mechanisms id'''
    if type is None:
        try:
            return [m.id for m in db.session.query(Mechanism).all()]
        except:
            return []
    try:
        return [m.id for m in db.session.query(Mechanism).filter(
            Mechanism.type == type).all()]
    except:
        return []


def today_shift_date():
    '''get date and shift'''
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


def all_mechanisms_type():
    '''Find all mechanisms type'''
    ls = []
    try:
        ls = [m.type for m in db.session.query(Mechanism).all()]
    except Exception as e:
        logger.debug(e)
    return set(ls)


def all_number(type, number):
    '''Need to do then'''
    return [m.id for m in Mechanism.query.all()]


def name_by_id(id):
    '''Need to do then'''
    return Mechanism.query.filter(Mechanism.id == id).first().name


def id_by_number(type, number):
    '''Find mechanism_id by type and number'''
    mech = Mechanism.query.filter(Mechanism.type==type,  Mechanism.number==number).first()
    if mech:
        return mech.id
    return None


def id_and_number(type):
    '''id and number by type'''
    mechanisms = Mechanism.query.filter(Mechanism.type==type).all()
    if mechanisms:
        return {mech.id: mech.number for mech in mechanisms}
    return None

def get_resons(type_mechanisms: str, date_shift: datetime.date, shift: int) -> dict:
    shift = int(shift)
    all_mechs = all_mechanisms_id(type_mechanisms)
    cursor = db.session.query(MD).filter(MD.data_smen == date_shift, MD.smena ==
                                           shift, MD.inv_num.in_(all_mechs)).order_by(MD.inv_num).all()
    return cursor


def process_resons(resons: list, ids_and_nums:list) -> dict:
    result:dict = {}
    for el in resons:
        number = ids_and_nums[el.inv_num]
        start = el.data_nach
        stop = el.data_kon
        reson = el.id_downtime
        try:
            result[number].append(
                {
                    'start': start,
                    'stop': stop,
                    'reson': reson
                }
            )
        except KeyError:
            result[number] = []
            result[number].append(
                {
                    'start': start,
                    'stop': stop,
                    'reson': reson
                }
            )
    return result


def handle_reson(start:datetime, stop:datetime, reson:[int, None]):
    start = start.replace(second=0)
    stop = stop.replace(second=0)
    return {
        "start": start.strftime("%H:%M"),
        "stop": stop.strftime("%H:%M"),
        "reson": reson,
        "step": int((stop - start).total_seconds()/60)
    }


def convert_resons_to_720minuts(resons: List[Dict[str, object]], start_shift: datetime) -> dict:
    if not resons:
        return {}
    result: dict = {
        '0': handle_reson(start_shift,  resons[0]["start"],  None)
    }
    count = 0
    for i in range(len(resons)):
        count += 1
        result[str(count)] = handle_reson(
            resons[i]["start"], resons[i]["stop"],  resons[i]["reson"])
        count += 1
        try:
            result[str(count)] = handle_reson(
                resons[i]["stop"], resons[i+1]["start"],  None)
        except IndexError:
            result[str(count)] = handle_reson(
                resons[i]["stop"], start_shift + timedelta(minutes=719), None)
    return result

def get_start_shift(date_shift, shift):
    start_shift = datetime.combine(date_shift, datetime.min.time())
    if shift == 1:
        return start_shift.replace(hour=8, minute=0, second=0, microsecond=0)
    else:
        return start_shift.replace(hour=20, minute=0, second=0, microsecond=0)

def fio_by_rfid_id(rfid_id):
    val = Rfid_ids.query.filter(Rfid_ids.rfid_id==rfid_id).first()
    if val:
        return val.fio
    return None
