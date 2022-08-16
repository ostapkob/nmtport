#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.model import Post, Rfid_work
from dataclasses import dataclass
from app import db, app, redis_client
from typing import Dict
from datetime import datetime, timedelta
from app.functions_for_all import id_by_number
from app.functions import which_terminal,  dez10_to_dez35C
from config import usm_no_move
import pickle


@dataclass
class PostUSM:
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
        self._handler_rfid()
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

    def _handler_rfid(self):
        print('pass')
