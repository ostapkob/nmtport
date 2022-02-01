#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app import db
from app.model import  Mechanism
from datetime import datetime, timedelta

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

