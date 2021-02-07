#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
# from app import db
from app.functions import is_alarm
from app.functions import perpendicular_line_equation,  straight_line_equation, intersection_point_of_lines, which_terminal
from datetime import datetime, timedelta
# from app.model import Post
# from tests.alarm_data import value_minutes



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

    # def test_kran(self):   # its work without timestamp
    #     for en, i in enumerate(value_minutes, 1):
    #         values = i[0]
    #         minutes = i[1]
    #         result_1 = i[2]
    #         with self.subTest(True):
    #             data = self.get_data_kran(list(zip(values, minutes)))
    #             result_2 = is_alarm(data)
    #             self.assertEqual(result_1, result_2, [en, i])


class TestWhithTerminal(unittest.TestCase):

    data_test_terminal = [
        [9, [132.89149, 42.81673]], [9, [132.88998, 42.81537]], [9, [132.88946, 42.81541]], [9, [132.89044, 42.81464]], [9, [132.88984, 42.81457]], [9, [132.89061, 42.81413]], [11,[132.89048, 42.81387]], [11,[132.89023, 42.81380]], [11,[132.88974, 42.81375]], [11,[132.88923, 42.81364]], [11,[132.88862, 42.81316]], [11,[132.88889, 42.81259]], [11,[132.88927, 42.81216]], [11,[132.88912, 42.81196]], [11,[132.88824, 42.81201]], [11,[132.88816, 42.81178]],
        [9, [132.89194679066017, 42.81736550995399]], [9, [132.89257462348414, 42.81589379423502]], [9, [132.88986696392485, 42.81595748772176]], [9, [132.89161522194811, 42.81419894232471]], [9, [132.88916770035377, 42.81475478530103]], [9, [132.88917668763676, 42.81476989016062]], [9, [132.89137483936300, 42.81404213350927]], [9, [132.88990317783382, 42.81615568248341]], [9, [132.89020564075590, 42.81567523049253]], [9, [132.89042573840710, 42.81522114523636]], [9, [132.89058743687528, 42.81483370688806]], [9, [132.89074913534347, 42.81444626611244]], [9, [132.89103938675726, 42.81413754727080]], [9, [132.88905238171193, 42.81472577146314]], [9, [132.88948020966708, 42.81484054704739]], [9, [132.89005630963496, 42.81503972041025]], [9, [132.89073024692019, 42.81518359284351]], [9, [132.89136573255382, 42.81520790672962]], [9, [132.89210231604280, 42.81531973361439]], [11, [132.8891646231937, 42.81419314664282]], [11, [132.8888248696648, 42.81370081717350]], [11, [132.88991758824514, 42.81333378283207]], [11, [132.8895013421617, 42.813106384954210]], [
            11, [132.88857236403388, 42.81319772391066]], [11, [132.88782603382631, 42.81261228981140]], [11, [132.88907575397195, 42.81246977997844]], [11, [132.88835626010132, 42.81204749736881]], [11, [132.88918006475876, 42.81154327759049]], [13, [132.88840048662553, 42.81101999945392]], [13, [132.88784625048788, 42.81111158159720]], [13, [132.8872512688971, 42.811370787187370]], [13, [132.88699984920487, 42.81098755490390]], [13, [132.88792165710373, 42.81072675441268]], [13, [132.88861605517303, 42.81055594248610]], [13, [132.88789764724106, 42.81025352816530]], [13, [132.88712132692385, 42.81008988483347]], [13, [132.88638900987576, 42.81011825912287]], [13, [132.88747955657874, 42.80951143862879]], [15, [132.88535149641822, 42.80849242190669]], [15, [132.88586498710285, 42.80856846706237]], [15, [132.88661262650422, 42.80805425483484]], [15, [132.88658177371104, 42.80713661372471]], [15, [132.88585086990005, 42.80700994885330]], [15, [132.8864242215921, 42.808406576413830]], [15, [132.88706787750513, 42.80854399911098]]
    ]
    def test_terminal(self):
        for question, coord  in self.data_test_terminal: #attention first lon
            ans = which_terminal(coord[1], coord[0])
            self.assertEqual(question, ans)

if __name__ == '__main__':
    # last = db.session.query(Post).filter(Post.mechanism_id == 32711).order_by(
    #     Post.timestamp.desc()).limit(11)
    # for i in last:
    #     print('->', i.timestamp, i.value)
    # for question, [y, x] in test:
    #     ans = which_terminal(x, y, False)
    #     print(question, ans)

    unittest.main()
