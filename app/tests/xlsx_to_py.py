#!/usr/bin/env python
# -*- coding: utf-8 -*-


import openpyxl
from pprint import pprint
import pickle

wb = openpyxl.load_workbook('alarm_test.xlsx')

sheet = wb['main']

tpl = tuple(sheet['A1':'P106'])
data = []
for row_of_cell in tpl:
    values = []
    minutes = []
    for en, cell in enumerate(row_of_cell[:-1]):
        if cell.value is not None:
            values.append(cell.value)
            minutes.append(14-en)
    data.append([values, minutes, row_of_cell[-1].value == 'True'])
pprint(data)

with open('data.pickle', 'wb') as f:
    pickle.dump(data, f)
