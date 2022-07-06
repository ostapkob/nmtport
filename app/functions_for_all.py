#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import db
from app.model import Mechanism, Rfid_ids
from datetime import datetime, timedelta
from app import logger


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


def all_number():
    '''Need to do then'''
    return [m.id for m in Mechanism.query.all()]


def name_by_id(id):
    '''Need to do then'''
    return Mechanism.query.filter(Mechanism.id == id).first().name


def id_by_number(type, number):  # TODO new project not started when exist it
    '''Find mechanism_id by type and number'''
    mech = Mechanism.query.filter(
        Mechanism.type == type,  Mechanism.number == number).first()
    if mech:
        return mech.id
    return None


def number_by_id(id):
    mech = Mechanism.query.filter(Mechanism.id == id).first()
    if mech:
        return mech.number
    return None


def id_and_number(type):
    '''id and number by type'''
    mechanisms = Mechanism.query.filter(Mechanism.type == type).all()
    if mechanisms:
        return {mech.id: mech.number for mech in mechanisms}
    return None


def get_start_shift(date_shift, shift):
    start_shift = datetime.combine(date_shift, datetime.min.time())
    if shift == 1:
        return start_shift.replace(hour=8, minute=0, second=0, microsecond=0)
    else:
        return start_shift.replace(hour=20, minute=0, second=0, microsecond=0)


def fio_by_rfid_id(rfid_id):  # DEL
    val = Rfid_ids.query.filter(Rfid_ids.rfid_id == rfid_id).first()
    if val:
        return val.fio
    return None


def is_kran(mech_id):
    return mech_id in all_mechanisms_id('kran')
