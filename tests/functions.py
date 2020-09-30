#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
# from app import db
from app.functions import is_alarm
from datetime import datetime, timedelta
# from app.model import Post
from tests.kran_data import value_minutes


class Data():

    def __init__(self, timestamp, value):
        self.timestamp = timestamp
        self.value = value

    def __str__(self):
        return f"{self.timestamp}, {self.value}"

    def timestamp(self):
        return self.timestamp

    def value(self):
        return self.value


class GetState(unittest.TestCase):

    def get_data_kran(self, arg, delta=0):
        data = {}
        for e, (v, m) in enumerate(arg):
            time = datetime.now() - timedelta(minutes=m)
            data[e] = Data(time, v)
            # print(e, v, m, time)
        return data

    def get_data(self, arg, delta=0):
        dt = sum([1 for _ in arg])
        data = {}
        for e, (v, m) in enumerate(arg):
            dt -= m
            time = datetime.now() - timedelta(minutes=dt)
            data[e] = Data(time, v)
            # print(e, v, m, time)
        return data

#     def test_11111111111(self):
#         values = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
#         minutes = 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1
#         assert len(values) == len(minutes), 'Not equal lens'
#         data = self.get_data(list(zip(values, minutes)))
#         result = state_mech(data)
#         self.assertEqual(result, 'work')

#     def test_10000000000(self):
#         values = 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
#         minutes = 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1
#         assert len(values) == len(minutes), 'Not equal lens'
#         data = self.get_data(list(zip(values, minutes)))
#         result = state_mech(data)
#         self.assertEqual(result, 'stay')

#     def test_10000000001(self):
#         values = 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1
#         minutes = 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1
#         assert len(values) == len(minutes), 'Not equal lens'
#         data = self.get_data(list(zip(values, minutes)))
#         result = state_mech(data)
#         self.assertEqual(result, 'work')

#     def test_1m1m1m1m1m1(self):
#         values = 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
#         minutes = 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1
#         assert len(values) == len(minutes), 'Not equal lens'
#         data = self.get_data(list(zip(values, minutes)))
#         result = state_mech(data)
#         self.assertEqual(result, 'no_power')

#     def test_1m1m1m_1_1m1m1(self):
#         values = 1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1
#         minutes = 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
#         assert len(values) == len(minutes), 'Not equal lens'
#         data = self.get_data(list(zip(values, minutes)))
#         result = state_mech(data)
#         self.assertEqual(result, 'stay')

    def test_kran(self):
        for en, i in enumerate(value_minutes, 1):
            values = i[0]
            minutes = i[1]
            result_1 = i[2]
            with self.subTest(True):
                data = self.get_data_kran(list(zip(values, minutes)))
                result_2 = is_alarm(data)
                self.assertEqual(result_1, result_2, [en, i])


if __name__ == '__main__':
    # last = db.session.query(Post).filter(Post.mechanism_id == 32711).order_by(
    #     Post.timestamp.desc()).limit(11)
    # for i in last:
    #     print('->', i.timestamp, i.value)
    unittest.main()
