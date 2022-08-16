#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '/home/admin/nmtport')
from app.functions import   dez10_to_dez35C

rfids = ( 
    ('0005787018', '088,19850'),
    ('0015730188', '240,01548')
)

for q, a in rfids:
    res = dez10_to_dez35C(q)
    if res == a:
        print('good', q, res)
    else:
        print('bad', q, res)


