#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import db
from app.model import Rfid_ids  
import openpyxl
db.create_all()

filepath = 'ww.xlsx'
wb = openpyxl.load_workbook(filepath, data_only=True)
ws = wb.active
total_rows = 7

for i in range(2, total_rows):
    rfid_id = ws.cell(row=i, column=2).value
    fio = ws.cell(row=i, column=1).value
    db.session.add(Rfid_ids(rfid_id, fio))
    print(rfid_id, fio)


db.session.commit()
