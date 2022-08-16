#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from datetime import datetime
from tests.test_get_usm import USM
import sys
sys.path.insert(0, '/home/admin/nmtport')
from app import db
from app.model import Post, Rfid_work
from psw import post_passw
from app.functions import which_terminal,  dez10_to_dez35C
class TestUSM(unittest.TestCase):
    mech = USM(number=4, passw=post_passw[1], lever=0,
               roll=0,  lat=42.8118, lon=132.8893, port=5000)

    def test_01_existed_rfid_id(self):
        self.mech.change_rfid('0002419252')
        self.mech.change_flag()
        self.assertTrue(self.mech.send_req_rfid())

    def test_011_existed_rfid_id(self):
        self.mech.change_rfid('0005787018')
        self.mech.change_flag()
        self.assertTrue(self.mech.send_req_rfid())

    def test_02_fail_rfid_id(self):
        self.mech.change_rfid('0002419253')
        self.mech.change_flag()
        self.assertFalse(self.mech.send_req_rfid())

    def test_03_existed_passw(self):
        self.assertTrue(self.mech.send_req_work())

    def test_04_fail_passw(self):
        self.mech.change_passw('qwe')
        self.assertFalse(self.mech.send_req_work())
        self.mech.change_passw(post_passw[1])

    def test_05_existed_num(self):
        self.assertTrue(self.mech.send_req_work())

    def test_06_fail_num(self):
        self.mech.change_number(0)
        self.assertFalse(self.mech.send_req_work())
        self.mech.change_number(4)

    def test_07_find_in_db_post(self):
        cursor = db.session.query(Post).filter(
            Post.mechanism_id == self.mech.mech_id,
        ).order_by(Post.timestamp.desc()).first()
        dt = datetime.now() - cursor.timestamp 
        self.assertTrue(dt.total_seconds()<1)

    def test_08_find_in_db_rfid(self):
        cursor = db.session.query(Post).filter(
            Rfid_work.mechanism_id == self.mech.mech_id,
        ).order_by(Post.timestamp.desc()).first()
        dt = datetime.now() - cursor.timestamp 
        self.assertTrue(dt.total_seconds()<1)

if __name__ == '__main__':
    unittest.main()
