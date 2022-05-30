#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.model import Mechanism, Post, Rfid_work
from dataclasses import dataclass
from app import db, app, redis_client
from config import usm_no_move
from app.functions import   *
from app.functions_for_all import *
from loguru import logger
import pickle
from rich import print
from datetime import datetime, timedelta
from psw import post_passw
import time

@dataclass
class CurrentUSM:
    type_mech: str 
    mech_id: int
    number: int
    count: int
    lever: float
    roll: float
    rfid_id: str
    flag: bool
    lat: float
    lon: float
    def terminal(self) -> int:
        return which_terminal(self.type_mech, self.number, self.lat, self.lon) # exist 9, 11, 13, 15

def add_fix_post(post):  # !move
    ''' I use it fix because arduino sometimes accumulates an extra minute '''
    try:
        last = db.session.query(Post).filter(
            Post.mechanism_id == post.mechanism_id).order_by(Post.timestamp.desc()).first()
    except Exception as e:
        print('exept', e)
        logger.debug(e)
    if last:  # if not exist item in db not use function
        dt_seconds = (post.timestamp - last.timestamp).seconds
    else:
        dt_seconds = 201
    if dt_seconds < 200:  # whatever the difference is not big
        last_minute = last.timestamp.minute
        post_minute = post.timestamp.minute
        dt_minutes = post_minute - last_minute
        if dt_minutes == 2 or dt_minutes == -58:
            post.timestamp -= timedelta(seconds=30)
    db.session.add(post)
    try:
        db.session.commit()
    except Exception as e:
        logger.debug(e)
        time.sleep(10)
        db.session.commit()

def corect_position(mech, latitude, longitude):
    if float(latitude) == 0 or float(longitude) == 0: # get last values
        try:
            data_mech = db.session.query(Post).filter(
                Post.mechanism_id == mech.id).order_by(Post.timestamp.desc()).first()
        except Exception as e:
            logger.debug(e)
        latitude = data_mech.latitude
        longitude = data_mech.longitude
    k1, b1 = line_kran(mech.number)
    if not k1:
        return latitude, longitude
    k2, b2 = perpendicular_line_equation(
        k1, float(latitude), float(longitude))
    latitude, longitude = intersection_point_of_lines(k1, b1, k2, b2)
    return latitude, longitude

def add_to_db_rfid_work(current):
    if current.rfid_id == '0/00000':
        return 'RFID is empy'
    fio = fio_by_rfid_id(current.rfid_id)
    if fio is None:
        print('fio is', None, 'for', current.rfid_id)
        logger.debug(current.rfid_id)
    new_rfid = Rfid_work(mechanism_id = current.mech_id,
                        count = current.count,
                        rfid_id = current.rfid_id,
                        flag = current.flag,
                        )
    db.session.add(new_rfid)
    db.session.commit()
    return f'Success, {fio} {current},  {str(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))}'


def handler_rfid(current):
    '''if last request rfid_work failed  get previos values and compare with current value'''
    if current.rfid_id == '0/00000':
        return f'rfid is {current.rfid_id}'
    redis_tmp = redis_client.get(str( current.mech_id ))  # load from redis
    if redis_tmp is None:
        return 'redis_tmp is Empty'
    redis_tmp = pickle.loads(redis_tmp)  # convert to dataclass

    if current.rfid_id != redis_tmp.rfid_id or current.flag != redis_tmp.flag:
        two_min_ago= datetime.now() - timedelta(minutes=2)
        last = db.session.query(Rfid_work).filter(
            Rfid_work.rfid_id == current.rfid_id, 
            Rfid_work.mechanism_id == current.mech_id, 
            Rfid_work.flag == current.flag,
            Rfid_work.timestamp > two_min_ago
        ).order_by(Rfid_work.timestamp.desc()).first()
        print(f"[yellow]CHANGED current RFID: {current.rfid_id}, redis_tmp RFID: {redis_tmp.rfid_id}[/yellow]")
        print(f"[yellow]CHANGED current flag: {current.flag}, redis_tmp flag:  {redis_tmp.flag}[/yellow]")
        print(f"[sky_blue1]LAST {last}[/sky_blue1]")
        if last is None:
            print(f"[cian]ADD {current.rfid_id}[/cian]")
            return add_to_db_rfid_work(current)
        if current.rfid_id != last.rfid_id or current.flag != last.flag:
            print(f"[red]ADD {current.rfid_id}[/red]")
            return add_to_db_rfid_work(current)
    return 'ok'


def handler_position(mech):
    '''if position is empty or this mech should not move'''
    if mech.number in usm_no_move \
            or mech.lat == 0 \
            or mech.lon == 0: 
        redis_mech = redis_client.get(str( mech.mech_id ))  # load from redis
        if redis_mech is not None:
            redis_mech = pickle.loads(redis_mech)  # convert to dataclass
            mech.lat = redis_mech.lat
            mech.lon = redis_mech.lon
            return mech
        try:
            data_mech = db.session.query(Post).filter(
                Post.mechanism_id == mech.mech_id).order_by(Post.timestamp.desc()).first()
        except Exception as e:
            print('exept', e)
            logger.debug(e)
        mech.lat = data_mech.latitude
        mech.lon = data_mech.longitude
    return mech
