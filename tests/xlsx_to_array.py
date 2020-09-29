#!/usr/bin/env python
# -*- coding: utf-8 -*-

import openpyxl

book = openpyxl.load_workbook('data_test.xlsx')
sheet = book.active
