# -*- coding: utf-8 -*-
from flask import request, jsonify, abort, make_response
from flask import render_template  # ,redirect
from app import db, app
from app.model import Mechanism, Post
from datetime import datetime, timedelta
from app.functions import   add_fio, state_mech,  get_status_alarm, get_dict_mechanisms_number_by_id, get_dict_mechanisms_id_by_number
from app.usm import time_for_shift_usm, usm_periods
from app.kran import time_for_shift_kran, kran_periods
from app.sennebogen import time_for_shift_sennebogen, sennebogen_periods
from app.functions import image_mechanism 
from app.functions_for_all import all_mechanisms_id, today_shift_date, id_by_number, name_by_id
 # all_mechanisms_type, all_number, name_by_id
from psw import post_pass

import time
from config import HOURS
from app.functions import perpendicular_line_equation, intersection_point_of_lines, line_kran
from app.functions import which_terminal, mech_periods
from config import krans_if_3_then_2, krans_if_1_then_0, usm_no_move
from loguru import logger
from pymongo import MongoClient
from pprint import pprint
import random

client = MongoClient('mongodb://localhost:27017')
mongodb = client['HashShift']
dict_mechanisms_number_by_id = get_dict_mechanisms_number_by_id()
dict_mechanisms_id_by_number = get_dict_mechanisms_id_by_number()

def add_fix_post(post):  # !move
    ''' I use it fix because arduino sometimes accumulates an extra minute '''
    try:
        last = db.session.query(Post).filter(
            Post.mechanism_id == post.mechanism_id).order_by(Post.timestamp.desc()).first()
    except Exception as e:
        logger.debug(e)
    if last:  # if not exist item in db not use function
        dt_seconds = (post.timestamp - last.timestamp).seconds
    else:
        dt_seconds = 201
    if dt_seconds < 200:  # whatever the difference is not big
        last_minute = last.timestamp.minute
        post_minute = post.timestamp.minute
        dt_minutes = post_minute - last_minute
        if dt_minutes == 2 or dt_minutes == -58:
            post.timestamp -= timedelta(seconds=30)
    db.session.add(post)
    try:
        db.session.commit()
    except Exception as e:
        logger.debug(e)
        time.sleep(10)
        db.session.commit()

def corect_position(mech, latitude, longitude):
    if float(latitude) == 0 or float(longitude) == 0: # get last values
        try:
            data_mech = db.session.query(Post).filter(
                Post.mechanism_id == mech.id).order_by(Post.timestamp.desc()).first()
        except Exception as e:
            logger.debug(e)
        latitude = data_mech.latitude
        longitude = data_mech.longitude
    k1, b1 = line_kran(mech.number)
    if not k1:
        return latitude, longitude
    k2, b2 = perpendicular_line_equation(
        k1, float(latitude), float(longitude))
    latitude, longitude = intersection_point_of_lines(k1, b1, k2, b2)
    return latitude, longitude

@app.route("/api/v1.0/get_per_shift/<int:m_id>", methods=["GET"])
def get_per_shift(m_id):
    '''get data for this shift by id mechanism'''
    date_shift, shift = today_shift_date()
    try:
        data_per_shift = db.session.query(Post).filter(
            Post.date_shift == date_shift, Post.shift == shift, Post.mechanism_id == m_id).all()
    except Exception as e:
        logger.debug(e)
    try:
        start = db.session.query(Post.timestamp).filter(
            Post.date_shift == date_shift, Post.shift == shift, Post.mechanism_id == m_id).first()[0]
        stop = db.session.query(Post.timestamp).filter(Post.date_shift == date_shift, Post.shift ==
                                                       shift, Post.mechanism_id == m_id).order_by(Post.timestamp.desc()).first()[0]
    except TypeError:
        abort(405)
    start += timedelta(hours=HOURS)  # it should be better
    stop += timedelta(hours=HOURS)
    total = round(sum(el.value for el in data_per_shift) / 60, 3)
    data = {'total': total, 'start': start, 'stop': stop}
    return jsonify(data)


@app.route("/api/v1.0/get_data/<type_mechanism>/<date_shift>/<int:shift>", methods=['GET', 'POST'])
def get_data(type_mechanism, date_shift, shift):
    '''get data shift for by type of mechanism'''
    try:
        date = datetime.strptime(date_shift, '%d.%m.%Y').date()
    except ValueError:
        return make_response(jsonify({'error': 'Bad format date'}), 400)
    if type_mechanism == 'usm':
        data = time_for_shift_usm(date, shift)

    if type_mechanism == 'kran':
        data = time_for_shift_kran(date, shift)

    return jsonify(data)


@app.route("/api/v1.0/get_data_period/<type_mechanism>/<date_shift>/<int:shift>", methods=['GET', 'POST'])
def get_data_period(type_mechanism, date_shift, shift):
    '''get data shift for by type of mechanism'''
    try:
        date = datetime.strptime(date_shift, '%d.%m.%Y').date()
    except ValueError:
        return make_response(jsonify({'error': 'Bad format date'}), 400)
    if type_mechanism == 'usm':
        data = usm_periods(time_for_shift_usm(date, shift))
    if type_mechanism == 'kran':
        data = time_for_shift_kran(date, shift)
    return jsonify(data)


@app.route("/api/v2.0/get_data_period/<type_mechanism>/<date_shift>/<int:shift>", methods=['GET', 'POST'])
def get_data_period2(type_mechanism, date_shift, shift):
    '''get data shift for by type of mechanism and id'''
    try:
        date = datetime.strptime(date_shift, '%d.%m.%Y').date()
        # convert 1.1.2020 to 01.01.2020
        date_shift = date.strftime("%d.%m.%Y")
    except ValueError:
        return make_response(jsonify({'error': 'Bad format date'}), 400)

    mongo_request = mongodb[type_mechanism].find_one(  # request
        {"_id": f"{date_shift}|{shift}"})
    if mongo_request is not None:  # if item alredy exist
        del mongo_request["_id"]
        return jsonify(mongo_request)

    data = mech_periods(type_mechanism, date, shift)

    # add_to_mongo(data, date, shift)
    if data is not None:
        today_date, today_shift = today_shift_date()
        # convert int key to str
        mongo_data = {str(key): value for key, value in data.items()}
        for key, value in data.items():
            mongo_data[str(key)]['data'] = {
                str(k): v for k, v in value['data'].items()}
        if today_date == date and today_shift == shift:
            mongo_request = mongodb[type_mechanism].find_one(  # request
                {"_id": "now"})
            if mongo_request is not None:  # if item alredy exist
                del mongo_request["_id"]
                return jsonify(mongo_request)
        else:
            mongo_data['_id'] = f'{date_shift}|{shift}'
            posts = mongodb[type_mechanism]
            posts.insert_one(mongo_data)
    return jsonify(data)


@app.route("/api/v1.0/get_data_period_with_fio/<type_mechanism>/<date_shift>/<int:shift>", methods=['GET', 'POST'])
def get_data_period_with_fio(type_mechanism, date_shift, shift):
    '''get data shift for by type of mechanism'''
    try:
        date = datetime.strptime(date_shift, '%d.%m.%Y').date()
    except ValueError:
        return make_response(jsonify({'error': 'Bad format date'}), 400)
    if type_mechanism == 'usm':
        data = usm_periods(time_for_shift_usm(date, shift))
    if type_mechanism == 'kran':
        data = kran_periods(time_for_shift_kran(date, shift))
    if type_mechanism == 'sennebogen':
        data = sennebogen_periods(time_for_shift_sennebogen(date, shift))
    data_with_fio = add_fio(data, date, shift)
    return jsonify(data_with_fio)


@app.route("/api/v2.0/get_data_period_with_fio/<type_mechanism>/<date_shift>/<int:shift>", methods=['GET', 'POST'])
def get_data_period_with_fio2(type_mechanism, date_shift, shift):
    '''get data shift for by type of mechanism'''
    today_date, today_shift = today_shift_date()
    try:
        date = datetime.strptime(date_shift, '%d.%m.%Y').date()
        # convert 1.1.2020 to 01.01.2020
        date_shift = date.strftime("%d.%m.%Y")
    except ValueError:
        return make_response(jsonify({'error': 'Bad format date'}), 400)

    if today_date == date and today_shift == shift:
        mongo_request = mongodb[type_mechanism].find_one(  
            {"_id": "now"})
    else:
        mongo_request = mongodb[type_mechanism].find_one( 
            {"_id": f"{date_shift}|{shift}"})
    if mongo_request is not None:  # if item alredy exist
        del mongo_request["_id"]
        return jsonify(mongo_request)

    data = mech_periods(type_mechanism, date, shift)
    data = add_fio(data, date, shift)

    # add_to_mongo(data, date, shift)
    if data is not None: 
        # convert int key to str
        mongo_data = {str(key): value for key, value in data.items()}
        for key, value in data.items():
            mongo_data[str(key)]['data'] = {
                str(k): v for k, v in value['data'].items()}
        if today_date == date and today_shift == shift:
            mongo_request = mongodb[type_mechanism].find_one(  # request
                {"_id": "now"})
            if mongo_request is not None:  # if item alredy exist
                del mongo_request["_id"]
                return jsonify(mongo_request)
        else:
            mongo_data['_id'] = f'{date_shift}|{shift}'
            posts = mongodb[type_mechanism]
            posts.insert_one(mongo_data)
    return jsonify(data)


@app.route("/api/v1.0/get_data_now/<type_mechanism>", methods=['GET', 'POST'])
def get_data_now(type_mechanism):
    '''get data shift for by type of mechanism with work NOW'''
    if type_mechanism == 'usm':
        data = usm_periods(time_for_shift_usm(*today_shift_date()))

    if type_mechanism == 'kran':
        data = kran_periods(time_for_shift_kran(*today_shift_date()))

    if type_mechanism == 'sennebogen':
        data = sennebogen_periods(time_for_shift_sennebogen(*today_shift_date()))
    return jsonify(data)


@app.route("/api/v1.0/get_data_period_with_fio_now/<type_mechanism>", methods=['GET', 'POST'])
def get_data_period_with_fio_now(type_mechanism):
    '''get data shift for by type of mechanism with work NOW'''
    if type_mechanism == 'usm':
        data = usm_periods(time_for_shift_usm(*today_shift_date()))
    if type_mechanism == 'kran':
        data = kran_periods(time_for_shift_kran(*today_shift_date()))
    if type_mechanism == 'sennebogen':
        data = sennebogen_periods(time_for_shift_sennebogen(*today_shift_date()))
    data_with_fio = add_fio(data, *today_shift_date())
    return jsonify(data_with_fio)


@app.route("/api/v2.0/get_data_period_with_fio_now/<type_mechanism>", methods=['GET', 'POST'])
def get_data_period_with_fio_now2(type_mechanism):
    '''get data shift for by type of mechanism with work NOW'''
    data = mech_periods(type_mechanism, *today_shift_date())
    data_with_fio = add_fio(data, *today_shift_date())
    return jsonify(data_with_fio)


@app.route("/api/v1.0/get_all_last_data", methods=["GET"])
def get_all_last_data():
    '''get all data mechanism'''
    try:
        last_data_mech = [db.session.query(Post).filter(Post.mechanism_id == x).order_by(
            Post.timestamp.desc()).first() for x in all_mechanisms_id()]
    except Exception as e:
        logger.debug(e)
    # last_data_mech = [db.session.query(Post).filter(Post.mechanism_id == x).first() for x in all_mechanisms_id()]
    last_data_mech = filter(lambda x: x is not None, last_data_mech)
    data = {el.mech.type + str(el.mech.number): {'id': el.mech.id,
                                                 'name': el.mech.name,
                                                 'value': el.value,
                                                 'value2': el.value2,
                                                 'value3': el.value3,
                                                 'latitude': el.latitude,
                                                 'longitude': el.longitude,
                                                 'time': el.timestamp + timedelta(hours=HOURS)} for el in last_data_mech}
    return jsonify(data)


@app.route("/api/v1.0/get_all_last_data_by_type_ico/<mech_type>", methods=["GET"])
def get_all_last_data_by_type(mech_type):
    '''get all data mechanism'''
    try:
        last_data_mech = [db.session.query(Post).filter(Post.mechanism_id == x).order_by(
            Post.timestamp.desc()).first() for x in all_mechanisms_id(mech_type)]
    except Exception as e:
        logger.debug(e)
    data = {el.mech.type + str(el.mech.number): {'id': el.mech.id,
                                                 'name': el.mech.name,
                                                 'value': el.value,
                                                 'latitude': el.latitude,
                                                 'longitude': el.longitude,
                                                 'src': image_mechanism(el.value, el.mech.type, el.mech.number, el.timestamp + timedelta(hours=HOURS)),
                                                 'time': el.timestamp + timedelta(hours=HOURS)} for el in last_data_mech}
    return jsonify(data)


@app.route("/api/v1.0/get_all_last_data_state", methods=["GET"])
def get_all_last_data_state():
    '''get all data mechanism and mechanism state'''
    start = datetime.now()
    try:
        last_data_mech = [db.session.query(Post).filter(Post.mechanism_id == x).order_by(
            Post.timestamp.desc()).first() for x in all_mechanisms_id()]
    except Exception as e:
        logger.debug(e)
    last_data_mech = filter(lambda x: x is not None, last_data_mech)
    data = {el.mech.type + str(el.mech.number): {'id': el.mech.id,
                                                 'name': el.mech.name,
                                                 'type': el.mech.type,
                                                 'number': el.mech.number,
                                                 # if roller not work
                                                 'value': round(el.value, 2) if not el.value3 else 0,
                                                 'value2': el.value2,
                                                 'value3': el.value3,
                                                 'latitude': el.latitude,
                                                 'longitude': el.longitude,
                                                 'state': state_mech(el),
                                                 # 'alarm': get_status_alarm(el.mech.id, el.mech.type),
                                                 # 'alarm': True,
                                                 'alarm': False,
                                                 'terminal': el.terminal,
                                                 'time': el.timestamp + timedelta(hours=HOURS)} for el in last_data_mech}
    print('time last:', datetime.now() - start)
    return jsonify(data)


@app.route("/api/v2.0/get_all_last_data_state", methods=["GET"])
def get_all_last_data_state2():
    '''get all data mechanism and mechanism state'''
    mongo_request = mongodb['hash'].find_one(
        {"_id": "last_data"})
    if mongo_request is not None:  # if item alredy exist
        del mongo_request["_id"]
        return jsonify(mongo_request)
    return jsonify({})


@app.route("/api/v1.0/get_all_last_data_ico", methods=["GET"])
def get_all_last_data_ico():
    '''get all data mechanism and mechanism state'''
    try:
        last_data_mech = [db.session.query(Post).filter(Post.mechanism_id == x).order_by(
            Post.timestamp.desc()).first() for x in all_mechanisms_id()]
    except Exception as e:
        logger.debug(e)
    last_data_mech = filter(lambda x: x is not None, last_data_mech)
    data = {el.mech.type + str(el.mech.number): {'id': el.mech.id,
                                                 'name': el.mech.name,
                                                 'value': el.value,
                                                 'latitude': el.latitude,
                                                 'longitude': el.longitude,
                                                 'src': image_mechanism(el.value, el.mech.type, el.mech.number, el.timestamp + timedelta(hours=HOURS)),
                                                 'time': el.timestamp + timedelta(hours=HOURS)} for el in last_data_mech}
    return jsonify(data)


@app.route("/api/v1.0/get_mech/<int:m_id>", methods=["GET"])
def get_mech(m_id):
    '''get name mechanism'''
    try:
        mech = Mechanism.query.get(m_id)
    except Exception as e:
        logger.debug(e)
    return f'{mech.name}'


@app.route('/api/v1.0/add_usm', methods=['GET'])
def add_usm():
    '''add post by GET request from arduino'''
    mechanism_id = request.args.get('mechanism_id')
    password = request.args.get('password')
    value = request.args.get('value')
    value2 = request.args.get('value2')
    value3 = request.args.get('value3')
    count = request.args.get('count')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    try:
        number = dict_mechanisms_number_by_id['usm'][int(mechanism_id)]
    except KeyError:
        return 'Not this id or not usm'
    try:
        mech = Mechanism.query.get(mechanism_id)
    except Exception as e:
        logger.debug(e)
    # if (number==13 or number==11) and float(value) == 1: # FIX
    if number==7  and float(value) == 1: # FIX
        value = random.randrange(50, 100, 1)/100

    items = mechanism_id, password, latitude, longitude
    test_items = any([item is None for item in items])
    if int(value3) < 5:  # if roller not circle
        value = 0
    if test_items:
        return 'Bad request'
    if password not in post_pass:
        return 'Bad password'
    if int(mechanism_id) not in all_mechanisms_id('usm'):
        return 'Not this id'
    if number in usm_no_move:
        latitude = 0
        longitude = 0
    if latitude == '': 
        latitude = 0
        longitude = 0
    if float(latitude) == 0 or float(longitude) == 0:
        try:
            data_mech = db.session.query(Post).filter(
                Post.mechanism_id == mechanism_id).order_by(Post.timestamp.desc()).first()
        except Exception as e:
            logger.debug(e)
        latitude = data_mech.latitude
        longitude = data_mech.longitude
    terminal = which_terminal('usm', number, latitude, longitude) # exist 9, 11, 13, 15
    new_post = Post(value=value, value2=value2, value3=value3, count=count,
                    latitude=latitude, longitude=longitude, mechanism_id=mechanism_id,
                    terminal=terminal)
    add_fix_post(new_post)
    return f'Success, {str(items)}, {str(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))}'


@app.route('/api/v1.0/add_kran', methods=['GET'])
def add_kran():
    '''add post by GET request from arduino'''
    mechanism_id = request.args.get('mechanism_id')
    password = request.args.get('password')
    value = request.args.get('value')
    value3 = request.args.get('value3')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    try:
        mech = Mechanism.query.get(mechanism_id)
    except Exception as e:
        logger.debug(e)


    # if mechanism_id == '15510' and value == '1':
    #     value = '2'

    items = mechanism_id, password, latitude, longitude, value, value3
    test_items = any([item is None for item in items]) # if this id is exist
    if test_items:
        return 'Bad request'
    if password not in post_pass:
        return 'Bad password'
    if int(mechanism_id) not in all_mechanisms_id('kran'):
        return 'Not this id or not kran'
    if latitude == '':
        latitude = 0
        longitude = 0
    if float(latitude) == 0 or float(longitude) == 0:
        try:
            data_mech = db.session.query(Post).filter(
                Post.mechanism_id == mechanism_id).order_by(Post.timestamp.desc()).first()
        except Exception as e:
            logger.debug(e)
        latitude = data_mech.latitude
        longitude = data_mech.longitude
    if mech.number in krans_if_3_then_2 and value == '3':
        value = 2
    if mech.number in krans_if_1_then_0 and value == '1':
        value = 4
    k1, b1 = line_kran(mech.number)
    k2, b2 = perpendicular_line_equation(
        k1, float(latitude), float(longitude))
    latitude, longitude = intersection_point_of_lines(k1, b1, k2, b2)
    terminal = which_terminal('kran', number, latitude, longitude) # exist 9, 11, 13, 15
    new_post = Post(value=value, value3=value3, latitude=latitude,
                    longitude=longitude, mechanism_id=mechanism_id, terminal=terminal)
    db.session.add(new_post)
    db.session.commit()
    return f'Success, {str(mech.number)},  {str(items)}, {str(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))}'

@app.route('/api/v2.0/add_kran', methods=['GET'])
def add_kran2():
    '''add post by GET request from arduino'''
    number = int(request.args.get('number'))
    password = request.args.get('passw')
    value = int(request.args.get('value'))
    count = request.args.get('count')
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    x = abs(int(request.args.get('x'))) # accelerometr x-axis
    y = abs(int(request.args.get('y'))) # accelerometr y-axis
    try:
        mechanism_id = dict_mechanisms_id_by_number['kran'][number]
    except KeyError:
        return 'Not this id or not kran'
    try:
        mech = Mechanism.query.get(mechanism_id)
    except Exception as e:
        logger.debug(e)
    if (number == 31 or number == 17 or number==28) and value == 1: # FIX
        value = 2 
    items = mechanism_id, password, latitude, longitude, value, count
    test_items = any([item is None for item in items]) # if this id is exist
    if test_items:
        return 'Bad request'
    if password not in post_pass:
        return 'Bad password'
    if number in krans_if_3_then_2 and value == 3:
        value = 2
    if number in krans_if_1_then_0 and value == 1:
        value = 4 # 4 work how 0
    if value==0 and ((x>300 and y > 300) or x>700 or y>700) :  #acselerometer
        value = 5 # kran move
    if latitude == '':
        latitude = 0
        longitude = 0
    latitude, longitude = corect_position(mech, latitude, longitude)
    terminal = which_terminal('kran', number, latitude, longitude) # exist 9, 11, 13, 15
    new_post = Post(value=value, count=count, latitude=latitude,
                    longitude=longitude, mechanism_id=mechanism_id, terminal=terminal)
    db.session.add(new_post)
    db.session.commit()
    return f'Success, {str(mech.number)},  {str(items)}, {str(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))}'

@app.route('/api/v1.0/add_sennebogen', methods=['GET'])
def add_sennebogen():
    '''add post by GET request from arduino'''
    type_mechanism = 'sennebogen'
    number = request.args.get('number')
    password = request.args.get('password')
    x = request.args.get('x')
    y = request.args.get('y')
    count = request.args.get('count')
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    mechanism_id = id_by_number(type_mechanism, number)  
    try:
        mech = Mechanism.query.get(mechanism_id)
    except Exception as e:
        logger.debug(e)
    items = mechanism_id, password, latitude, longitude, x, y
    test_items = any([item is None for item in items])

    if test_items:
        return 'Bad request'
    if password not in post_pass:
        return 'Bad password'
    if int(mechanism_id) not in all_mechanisms_id(type_mechanism):
        return 'Not this id'
    if latitude == '': 
        latitude = 0
        longitude = 0
    if float(latitude) == 0 or float(longitude) == 0: # get last find value
        try:
            data_mech = db.session.query(Post).filter(
                Post.mechanism_id == mechanism_id).order_by(Post.timestamp.desc()).first()
        except Exception as e:
            logger.debug(e)
        latitude = data_mech.latitude
        longitude = data_mech.longitude
    terminal = which_terminal('sennebogen', number, latitude, longitude)
    new_post = Post(value=x, value2=y, count=count,
                    latitude=latitude, longitude=longitude, mechanism_id=mechanism_id,
                    terminal=terminal)
    add_fix_post(new_post)
    return f'Success, {str(items)}, {str(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))}'

@app.route('/api/v1.0/add_post', methods=['GET', 'POST'])
def add_post():
    '''add post by POST request from arduino'''
    need_keys = 'password', 'value', 'latitude', 'longitude', 'mechanism_id'
    request_j = request.json
    if request.method == 'POST':
        if not request_j:
            abort(400)
        keys = [p for p in request_j.keys()]
        if not set(keys).issubset(need_keys):
            abort(400)
        if request_j['password'] not in post_pass:
            abort(403)  # need use this password in Arduino
        if request_j['mechanism_id'] not in all_mechanisms_id():
            abort(405)
        value = request_j['value']
        latitude = request_j['latitude']
        longitude = request_j['longitude']
        mechanism_id = request_j['mechanism_id']
        if float(latitude) == 0 or float(longitude) == 0:
            try:
                data_mech = db.session.query(Post).filter(
                    Post.mechanism_id == mechanism_id).order_by(Post.timestamp.desc()).first()
            except Exception as e:
                logger.debug(e)
            latitude = data_mech.latitude
            longitude = data_mech.longitude
    elif request.method == 'GET':
        return 'Need POST methods'
    else:
        abort(400)

    new_post = Post(value, latitude, longitude, mechanism_id)
    data = request.data
    db.session.add(new_post)
    db.session.commit()
    return data, 201


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
    # return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(403)
def wrong_password(error):
    return make_response(jsonify({'error': 'Wrong password'}), 403)


