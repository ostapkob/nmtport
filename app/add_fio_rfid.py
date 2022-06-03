#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rich import print
from datetime import datetime, timedelta
from app.model import Rfid_work, Rfid_ids
from app import db
# from app.usm import usm_periods, time_for_shift_usm


def add_fio_from_rfid(data_period, date_shift, shift):
    if not data_period:
        return None
    cursor = db.session.query(Rfid_work).filter(
        Rfid_work.date_shift == date_shift,
        Rfid_work.shift == shift,
        ).all()
    for key, value in data_period.items():
        mech_id = value['id']
        rfid_work = [
            {
                'fio':  fio_by_rfid_id(x.rfid_id), 
                'time': x.timestamp, 
                'flag': x.flag,
            }
              for x in cursor if x.mechanism_id==mech_id]
        data_period[key]['rfid']  = rfid_work
    return data_period


def fio_by_rfid_id(rfid_id):
    val = Rfid_ids.query.filter(Rfid_ids.rfid_id==rfid_id).first()
    if val:
        return val.fio
    return None


def data_from_work_1c_by_id(date_shift, shift, id_mech):
    try:
        cursor = db.session.query(Work_1C_1).filter(
            Work_1C_1.data_smen == date_shift,
            Work_1C_1.smena == shift,
            Work_1C_1.inv_num == id_mech
            ).all()
    except Exception as e:
        logger.debug(e)
    data_1C = [x.get() for x in cursor]
    return data_1C


if __name__ == "__main__":
    import pickle
    TYPE = 'usm'
    date = datetime.now().date()
    date -= timedelta(days=2)
    shift = 1
    name_file_pickle = 'New' + TYPE+'_'+str(date)+"_"+str(shift)

    # res = kran_periods(time_for_shift_kran(date, shift))
    # res = usm_periods(time_for_shift_usm(date, shift))

    # with open(name_file_pickle, 'wb') as f:
    #     pickle.dump(res, f)

    with open(name_file_pickle, 'rb') as f:
        load = pickle.load(f)

    res = add_fio_from_rfid(load, date, shift)
    print(res)
