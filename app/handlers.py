#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.model import  Post, Rfid_work
from dataclasses import dataclass
from app import db, app, redis_client
from config import usm_no_move
from app.functions import which_terminal, line_kran, perpendicular_line_equation, intersection_point_of_lines,  dez10_to_dez35C
from app.functions_for_all import id_by_number, fio_by_rfid_id
from loguru import logger
import pickle
from rich import print
from datetime import datetime, timedelta
from config import HOURS
from typing import Dict
import time


@dataclass
class CurrentUSM:
    number: int
    passw: str
    count: int
    lever: float
    roll: int
    rfid_id: str
    flag: bool
    lat: float
    lon: float
    mech_id: int | None
    terminal: int
    timestamp: datetime

    def __init__(self, number, passw, count, rfid_id, flag, lever=0, roll=0,  lat=0, lon=0):
        self.type_mech = 'usm'
        self.number = int(number)
        self.passw = str(passw)
        self.count = int(count)
        self.lever = float(lever)
        self.roll = int(roll)
        self.rfid_id = str(rfid_id)
        self.flag = bool(int(flag))
        self.lat = float(lat)
        self.lon = float(lon)
        self.rfid_id = dez10_to_dez35C(int(self.rfid_id))
        self.mech_id = id_by_number(self.type_mech, self.number)
        self._handler_roll()
        self._handler_position()
        self.terminal = which_terminal(
            self.type_mech, self.number, self.lat, self.lon)
        self.timestamp = datetime.now()
        self._fix_timestamp()
        redis_client.set(str(self.mech_id), pickle.dumps(self))

    def _handler_roll(self):
        # if self.number==13 and self.lever>0: # FIX
        #     self.roll = 25
        if self.roll < 5:
            self.lever = 0

    def _handler_position(self):
        '''if position is empty or this mech should not move'''
        if self.number in usm_no_move \
                or self.lat == 0 \
                or self.lon == 0:
            last_post = self._get_last_post()
            self.lat = float(last_post["lat"])
            self.lon = float(last_post["lon"])

    def _get_last_post(self) -> Dict:
        '''try return last redis or db else None'''
        redis_mech = redis_client.get(str(self.mech_id))  # load from redis
        if redis_mech:
            redis_mech = pickle.loads(redis_mech)  # convert to dataclass
            return {
                "number": redis_mech.number,
                "count": redis_mech.count,
                "lever": redis_mech.lever,
                "roll": redis_mech.roll,
                "lat": redis_mech.lat,
                "lon": redis_mech.lon,
                "mech_id": redis_mech.mech_id,
                "terminal": redis_mech.terminal,
                "timestamp": redis_mech.timestamp
            }

        try:
            sql_mech = db.session.query(Post).filter(
                Post.mechanism_id == self.mech_id).order_by(Post.timestamp.desc()).first()
        except:
            sql_mech = None

        if sql_mech:
            return {
                "number": sql_mech.mech.number,
                "count": sql_mech.count,
                "lever": sql_mech.value,
                "roll": sql_mech.value3,
                "lat": sql_mech.latitude,
                "lon": sql_mech.longitude,
                "mech_id": sql_mech.mech.id,
                "terminal": sql_mech.terminal,
                "timestamp": sql_mech.timestamp
            }

        return {
            "number": None,
            "count": None,
            "lever": None,
            "roll": None,
            "lat": 132.5,
            "lon": 42.5,
            "mech_id": None,
            "terminal": 78,
            "timestamp": datetime.now()
        }

    def _fix_timestamp(self):
        last_post = self._get_last_post()
        dt_seconds = (self.timestamp - last_post['timestamp']).seconds
        dt_minutes = self.timestamp.minute - last_post['timestamp'].minute
        if dt_seconds < 200 and (dt_minutes == 2 or dt_minutes == -58):
            self.timestamp -= timedelta(seconds=30)
            print(f'{self.timestamp}')


def add_fix_post(post):  # delete after change all api to version2
    ''' I use it fix because arduino sometimes accumulates an extra minute '''
    try:
        last = db.session.query(Post).filter(
            Post.mechanism_id == post.mechanism_id).order_by(Post.timestamp.desc()).first()
    except Exception as e:
        print('exept', e)
        last = None
        logger.debug(e)
    if last:  # if not exist item in db not use function
        dt_seconds = (post.timestamp - last.timestamp).seconds
    else:
        dt_seconds = 201
    if dt_seconds < 200 and last:  # whatever the difference is not big
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


def corect_position(mech, latitude, longitude):  # TODO dataclasses
    if float(latitude) == 0 or float(longitude) == 0:  # get last values
        try:
            data_mech = db.session.query(Post).filter(
                Post.mechanism_id == mech.id).order_by(Post.timestamp.desc()).first()
            latitude = data_mech.latitude
            longitude = data_mech.longitude
        except Exception as e:
            logger.debug(e)
            latitude = 132.6
            longitude = 42.6
    k1, b1 = line_kran(mech.number)
    if not k1:
        return latitude, longitude
    k2, b2 = perpendicular_line_equation(
        k1, float(latitude), float(longitude))
    latitude, longitude = intersection_point_of_lines(k1, b1, k2, b2)
    return latitude, longitude


def add_to_db_rfid_work(current: CurrentUSM):
    if current.rfid_id == '0/00000':
        return 'RFID is empy'
    fio = fio_by_rfid_id(current.rfid_id)
    if fio is None:
        print('fio is', None, 'for', current.rfid_id)
        logger.debug(current.rfid_id)
    new_rfid = Rfid_work(mechanism_id=current.mech_id,
                         count=current.count,
                         rfid_id=current.rfid_id,
                         flag=current.flag,
                         )
    db.session.add(new_rfid)
    db.session.commit()
    return f'Success, {fio} {current},  {str(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))}'


def handler_rfid(current):
    '''if last request rfid_work failed get previos values and compare with current value'''
    if current.rfid_id == '0/00000':
        return f'rfid is {current.rfid_id}'
    redis_tmp = redis_client.get(str(current.mech_id))  # load from redis
    if redis_tmp is None:
        return 'redis_tmp is Empty'
    redis_tmp = pickle.loads(redis_tmp)  # convert to dataclass

    if current.rfid_id != redis_tmp.rfid_id or current.flag != redis_tmp.flag:
        two_min_ago = datetime.now() - timedelta(minutes=2)
        last = db.session.query(Rfid_work).filter(
            Rfid_work.rfid_id == current.rfid_id,
            Rfid_work.mechanism_id == current.mech_id,
            Rfid_work.flag == current.flag,
            Rfid_work.timestamp > two_min_ago
        ).order_by(Rfid_work.timestamp.desc()).first()
        print(
            f"[yellow]CHANGED current RFID: {current.rfid_id}, redis_tmp RFID: {redis_tmp.rfid_id}[/yellow]")
        print(
            f"[yellow]CHANGED current flag: {current.flag}, redis_tmp flag:  {redis_tmp.flag}[/yellow]")
        print(f"[sky_blue1]LAST {last}[/sky_blue1]")
        if last is None:
            print(f"[cian]ADD {current.rfid_id}[/cian]")
            return add_to_db_rfid_work(current)
        if current.rfid_id != last.rfid_id or current.flag != last.flag:
            print(f"[red]ADD {current.rfid_id}[/red]")
            return add_to_db_rfid_work(current)
    return 'ok'
