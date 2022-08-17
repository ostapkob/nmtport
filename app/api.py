from flask import request, jsonify, abort, make_response
from flask import render_template
from app import db, app, redis_client, mongodb
from app.model import Mechanism, Post, Rfid_work
from datetime import datetime, timedelta
from app.functions import get_dict_mechanisms_number_by_id, get_dict_mechanisms_id_by_number, mech_periods, state_mech, which_terminal, dez10_to_dez35C
from app.functions_for_all import all_mechanisms_id, today_shift_date,  id_by_number, fio_by_rfid_id
from app.handlers import add_fix_post, corect_position,  add_to_db_rfid_work
from app.usm import time_for_shift_usm, usm_periods
from app.usm_post import PostUSM
from app.kran import time_for_shift_kran, kran_periods
from app.sennebogen import time_for_shift_sennebogen, sennebogen_periods
from psw import post_passw
from config import HOURS
from config import krans_if_3_then_2, krans_if_1_then_0, usm_no_move
from loguru import logger
from rich import print
import pickle

from app.add_fio_1c import add_fio_and_grab_from_1c
from app.add_fio_rfid import add_fio_from_rfid
from app.add_resons_1c import add_resons_from_1c

dict_mechanisms_number_by_id = get_dict_mechanisms_number_by_id()
dict_mechanisms_id_by_number = get_dict_mechanisms_id_by_number()


@app.route("/api/v1.0/get_per_shift/<int:m_id>", methods=["GET"])
def get_per_shift(m_id):
    '''get data for this shift by id mechanism'''
    date_shift, shift = today_shift_date()
    try:
        data_per_shift = db.session.query(Post).filter(
            Post.date_shift == date_shift, Post.shift == shift, Post.mechanism_id == m_id).all()
    except Exception as e:
        data_per_shift = []
        # logger.debug(e)
    try:
        start = db.session.query(Post.timestamp).filter(
            Post.date_shift == date_shift, Post.shift == shift, Post.mechanism_id == m_id).first()[0]
        stop = db.session.query(Post.timestamp).filter(Post.date_shift == date_shift, Post.shift ==
                                                       shift, Post.mechanism_id == m_id).order_by(Post.timestamp.desc()).first()[0]
    except TypeError:
        abort(405)
        return
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
        return jsonify(data)
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
        return jsonify(data)
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
        # mongo_data = {str(key): value for key, value in data.items()}
        # for key, value in data.items():
        #     mongo_data[str(key)]['data'] = {
        #         str(k): v for k, v in value['data'].items()}
        mongo_data = convert_keys_int_to_str(data)
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


def convert_keys_int_to_str(data):
    mongo_data = {str(key): value for key, value in data.items()}
    for key, value in data.items():
        mongo_data[str(key)]['data'] = {  # del str
            str(k): v for k, v in value['data'].items()
        }
    return mongo_data


@app.route("/api/v1.0/get_data_period_with_fio/<type_mechanism>/<date_shift>/<int:shift>", methods=['GET', 'POST'])
def get_data_period_with_fio(type_mechanism, date_shift, shift):
    '''get data shift for by type of mechanism'''
    try:
        date = datetime.strptime(date_shift, '%d.%m.%Y').date()
    except ValueError:
        return make_response(jsonify({'error': 'Bad format date'}), 400)
    data = {}
    if type_mechanism == 'usm':
        data = usm_periods(time_for_shift_usm(date, shift))
    if type_mechanism == 'kran':
        data = kran_periods(time_for_shift_kran(date, shift))
    if type_mechanism == 'sennebogen':
        data = sennebogen_periods(time_for_shift_sennebogen(date, shift))
    data_with_fio = add_fio_and_grab_from_1c(data, date, shift)
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
    print(str(data is None))
    data = add_fio_and_grab_from_1c(data, date, shift)
    print(str(data is None))
    data = add_fio_from_rfid(data, date, shift)
    print(str(data is None))
    data = add_resons_from_1c(data, date, shift)
    print(str(data is None))

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
    data = {}
    if type_mechanism == 'usm':
        data = usm_periods(time_for_shift_usm(*today_shift_date()))

    if type_mechanism == 'kran':
        data = kran_periods(time_for_shift_kran(*today_shift_date()))

    if type_mechanism == 'sennebogen':
        data = sennebogen_periods(
            time_for_shift_sennebogen(*today_shift_date()))
    return jsonify(data)


@app.route("/api/v1.0/get_data_period_with_fio_now/<type_mechanism>", methods=['GET', 'POST'])
def get_data_period_with_fio_now(type_mechanism):
    '''get data shift for by type of mechanism with work NOW'''
    data = {}
    if type_mechanism == 'usm':
        data = usm_periods(time_for_shift_usm(*today_shift_date()))
    if type_mechanism == 'kran':
        data = kran_periods(time_for_shift_kran(*today_shift_date()))
    if type_mechanism == 'sennebogen':
        data = sennebogen_periods(
            time_for_shift_sennebogen(*today_shift_date()))
    data_with_fio = add_fio_and_grab_from_1c(data, *today_shift_date())
    return jsonify(data_with_fio)


@app.route("/api/v2.0/get_data_period_with_fio_now/<type_mechanism>", methods=['GET', 'POST'])
def get_data_period_with_fio_now2(type_mechanism):
    '''get data shift for by type of mechanism with work NOW'''
    data = mech_periods(type_mechanism, *today_shift_date())
    data_with_fio = add_fio_and_grab_from_1c(data, *today_shift_date())
    return jsonify(data_with_fio)


@app.route("/api/v1.0/get_all_last_data", methods=["GET"])
def get_all_last_data():
    '''get all data mechanism'''
    try:
        last_data_mech = [db.session.query(Post).filter(Post.mechanism_id == x).order_by(
            Post.timestamp.desc()).first() for x in all_mechanisms_id()]
    except Exception as e:
        last_data_mech = []
        # logger.debug(e)
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


@app.route("/api/v1.0/get_all_last_data_state", methods=["GET"])
def get_all_last_data_state():
    '''get all data mechanism and mechanism state'''
    # start = datetime.now()
    try:
        last_data_mech = [db.session.query(Post).filter(Post.mechanism_id == x).order_by(
            Post.timestamp.desc()).first() for x in all_mechanisms_id()]
    except Exception as e:
        last_data_mech = []
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


@app.route("/api/v1.0/get_mech/<int:m_id>", methods=["GET"])
def get_mech(m_id):
    '''get name mechanism'''
    try:
        mech = Mechanism.query.get(m_id)
        return f'{mech.name}'
    except Exception as e:
        # logger.debug(e)
        return


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
        pass
        logger.debug(e)
    if number==11 and float(value) >0: # FIX
        value3 = 25
    # if (number==13 or number==11) and float(value) == 1: # FIX
    # if number==13 and float(value) <0.7: # FIX
    #     value = 0.8
    # if number==7: # FIX
    #     value = 0.8
    # if number==6: # FIX
    #     value3 = 15

    items = mechanism_id, password, latitude, longitude
    test_items = any([item is None for item in items])
    if int(value3) < 5:  # if roller not circle
        value = 0
    if test_items:
        return 'Bad request'
    if password not in post_passw:
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
            latitude = data_mech.latitude
            longitude = data_mech.longitude
        except Exception as e:
            latitude = 132.9
            longitude = 42.9
            logger.debug(e)
    terminal = which_terminal('usm', number, latitude,
                              longitude)  # exist 9, 11, 13, 15
    new_post = Post(value=value, value2=value2, value3=value3, count=count,
                    latitude=latitude, longitude=longitude, mechanism_id=mechanism_id,
                    terminal=terminal)
    add_fix_post(new_post)
    return f'Success, {str(items)}, {str(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))}'


@app.route('/api/v2.0/add_kran', methods=['GET'])
def add_kran2():
    '''add post by GET request from arduino'''
    number = int(request.args.get('number'))
    password = request.args.get('passw')
    value = int(request.args.get('value'))
    count = request.args.get('count')
    latitude = request.args.get('lat')
    longitude = request.args.get('lon')
    x = abs(int(request.args.get('x')))  # accelerometr x-axis
    y = abs(int(request.args.get('y')))  # accelerometr y-axis
    try:
        mechanism_id = dict_mechanisms_id_by_number['kran'][number]
    except KeyError:
        return 'Not this id or not kran'
    try:
        mech = Mechanism.query.get(mechanism_id)
    except Exception as e:
        print('Bed request mech', number)
        # logger.debug(e)
        return f"bed request mech, {number}"
    # if (number in (17, 31) ) and value == 1:  # FIX
    #     value = 2
    if number in (6,)  and value == 1:  # FIX
        value = 3
    items = mechanism_id, password, latitude, longitude, value, count

    # if this id is exist
    test_exist_items = any([item is None for item in items])
    if test_exist_items:
        return 'Bad request'
    if password not in post_passw:
        return 'Bad password'
    if number in krans_if_3_then_2 and value == 3:
        value = 2
    if number in krans_if_1_then_0 and value == 1:
        value = 4  # 4 work how 0
    if value == 0 and ((x > 300 and y > 300) or x > 700 or y > 700):  # acselerometer
        value = 5  # kran move
    # if latitude == '':
    #     latitude = 0
    #     longitude = 0
    latitude, longitude = corect_position(mech, latitude, longitude)
    terminal = which_terminal('kran', number, latitude,
                              longitude)  # exist 9, 11, 13, 15
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
        # logger.debug(e)
        pass
    items = mechanism_id, password, latitude, longitude, x, y
    test_items = any([item is None for item in items])

    if test_items:
        return 'Bad request'
    if password not in post_passw:
        return 'Bad password'
    if int(mechanism_id) not in all_mechanisms_id(type_mechanism):
        return 'Not this id'
    if latitude == '':
        latitude = 0
        longitude = 0
    if float(latitude) == 0 or float(longitude) == 0:  # get last find value
        try:
            data_mech = db.session.query(Post).filter(
                Post.mechanism_id == mechanism_id).order_by(Post.timestamp.desc()).first()
            latitude = data_mech.latitude
            longitude = data_mech.longitude
        except Exception as e:
            # logger.debug(e)
            pass
        latitude = 132.8
        longitude = 40.8
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
        keys = [p for p in request_j]
        if not set(keys).issubset(need_keys):
            abort(400)
        if request_j['password'] not in post_passw:
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
                latitude = data_mech.latitude
                longitude = data_mech.longitude
            except Exception as e:
                # logger.debug(e)
                latitude = 132.7
                longitude = 40.7
    elif request.method == 'GET':
        return 'Need POST methods'
    else:
        abort(400)
        return

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


@app.route('/api/v2.0/add_usm_work', methods=['GET'])
def add_usm2():
    '''add post by GET request from arduino'''
    necessary_args = [
        'number',
        'passw',
        'count',
        'rfid',
        'flag',
        'lever',
        'roll',
        'lat',
        'lon'
    ]
    items = [request.args.get(arg, None) for arg in necessary_args]
    if any([item is None for item in items]):
        print(f'400{items=}')
        abort(400, 'Bad request')
    current = PostUSM(*items)
    if current.passw not in post_passw:
        abort(401, 'Bad password')
    if current.mech_id is None:
        abort(406, 'No this number')
    new_post = Post(count=current.count,
                    value=current.lever,
                    value3=current.roll,
                    latitude=current.lat,
                    longitude=current.lon,
                    mechanism_id=current.mech_id,
                    terminal=current.terminal,
                    timestamp=current.timestamp
                    )
    db.session.add(new_post)
    db.session.commit()
    redis_client.set(str(current.mech_id), pickle.dumps(
        current))  # convert and save to redis
    return f'Success, {str(current)}, {str(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))}'


@app.route('/api/v2.0/add_usm_rfid', methods=['GET'])
def add_usm_rfid_2():
    '''add post by GET request from arduino'''
    necessary_args = [
        'number',
        'passw',
        'count',
        'rfid',
        'flag',
    ]
    items = [request.args.get(arg, None) for arg in necessary_args]
    print(f'{items=}')
    if any([item is None for item in items]):
        abort(400, 'Bad request')
    current = PostUSM(*items)

    if current.passw not in post_passw:
        abort(401, 'Bad password')
    if current.mech_id is None:
        abort(406, 'No this number')
    fio = fio_by_rfid_id(current.rfid_id)
    if fio is None:
        abort(406, 'No this rfid id')
    
    last_flag = current.get_last_rfid_flag()

    if last_flag:
        current.set_rfid_flag(0)
    else:
        current.set_rfid_flag(1)
    current.add_to_db_rfid_work()

    if last_flag:
        return "start", 200
    else:
        return "finish", 200

#firs word must be 'add' becouse nginx use it how toggle to 80 port
@app.route('/api/v2.0/add_get_rfid_flag', methods=['GET'])
def get_usm_rfid_flag():
    necessary_args = [
        'number',
        'type',
        'passw',
    ]
    items = [request.args.get(arg, None) for arg in necessary_args]
    if any([item is None for item in items]):
        abort(400, 'Bad request')
    mech_id = id_by_number(items[1], items[0]) # type number
    if items[2] not in post_passw:
        abort(401, 'Bad password')
    try:
        sql_rfid = db.session.query(Rfid_work).filter(
            Rfid_work.mechanism_id == mech_id).order_by(Rfid_work.timestamp.desc()).first()
    except:
        abort(400, 'Bad request')
    last_flag = bool(sql_rfid.flag)
    print('last_flag: ', f"[yellow] {last_flag}[/yellow]")
    if last_flag:
        return "start", 200
    else:
        return "finish", 200

# if __name__ == "__main__":
#     pass
