#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rich import print
from datetime import datetime, timedelta, date
from app.model import Work_1C_1
from app import db
from app.functions_for_all import all_mechanisms_id
from app.kran import time_for_shift_kran, kran_periods


def _fio_to_fi(fio):
    if not fio:
        return None
    fio = fio.split()
    return f'{fio[0].capitalize()} {fio[1][0]}.'


def _handler_grab(grab: float | None, mech_id: int) -> float | None:
    '''if grab not write then find last item'''
    if (grab is None or grab < 3.0) and mech_id in all_mechanisms_id('kran'):  # TODO redis
        try:
            last_find_item = db.session.query(Work_1C_1).filter(
                Work_1C_1.inv_num == mech_id,
                Work_1C_1.greifer_vol > 0.0
            ).order_by(Work_1C_1.data_nach.desc()).first()
            return float(last_find_item.greifer_vol)
        except AttributeError:
            return None
    if mech_id in all_mechanisms_id('usm'):
        return None
    return grab


def _get_cursor(data_period: dict, date_shift: date, shift: int):
    """get all ids for shift and find items in 1c"""
    ids = [x['id'] for x in data_period.values()]
    try:
        cursor = db.session.query(Work_1C_1).filter(
            Work_1C_1.data_smen == date_shift,
            Work_1C_1.smena == shift,
            Work_1C_1.inv_num.in_(ids)
        ).all()
    except Exception as e:
        print(e)
        return []

    return cursor


def add_fio_and_grab_from_1c(data_period: dict, date_shift: date, shift: int) -> dict | None:
    ''' add fio and grab if it exec '''
    if not data_period:
        return None
    cursor = _get_cursor(data_period, date_shift, shift)
    for key, value in data_period.items():
        mech_id = value['id']
        work_1c = [
            {
                'fio':  _fio_to_fi(x.fio),
                'grab': float(x.greifer_vol),
                'contract': x.port,
                'start': x.data_nach,
                'stop': x.data_kon,
            }
            for x in cursor if x.inv_num == mech_id]
        fio = None
        grab = None
        contract = 1  # 1-Nmtp, 0-DVV
        if len(work_1c) == 1:
            fio = work_1c[0]['fio']
            grab = work_1c[0]['grab']
            contract = work_1c[0]['contract']
        elif len(work_1c) > 1:
            fio = 'Два оператора'
            grab = work_1c[0]['grab']

        data_period[key]['fio'] = fio
        # not bool because may stay more then 2
        data_period[key]['contract'] = contract
        data_period[key]['grab'] = _handler_grab(grab, mech_id)
        data_period[key]['work_1c'] = work_1c
        # print(f'{fio=}, {grab=}, {contract=}')
    return data_period


if __name__ == "__main__":
    import pickle
    TYPE = 'Kran'
    date = datetime.now().date()
    date -= timedelta(days=1)
    shift = 1
    name_file_pickle = 'tmp' + TYPE+'_'+str(date)+"_"+str(shift)
    # res = kran_periods(time_for_shift_kran(date, shift))
    # res = usm_periods(time_for_shift_usm(date, shift))
    # with open(name_file_pickle, 'wb') as f:
    #     pickle.dump(res, f)
    print(name_file_pickle)
    with open(name_file_pickle, 'rb') as f:
        load = pickle.load(f)

    res = add_fio_and_grab_from_1c(load, date, shift)
    print(res)

    # for k in res.keys():
    #     print(k, res[k]['id'], res[k]['grab'])

    # with open('tmp', 'wb') as f:
    #     pickle.dump(res, f)

    # with open('tmp', 'rb') as f:
    #     load = pickle.load(f)
    # print(load==res)
