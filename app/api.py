# -*- coding: utf-8 -*-
from flask import request, json, jsonify, abort, make_response
from flask import render_template, flash, redirect
from app import db, app
from app.model import Mechanism, Post
from app.form import AddMechanism
from datetime import datetime, timedelta
from functions import today_shift_date, all_mechanisms_id, time_for_shift, time_for_shift_list, image_mechanism
from sqlalchemy import func
from pprint import pprint
from psw import post_pass
from datetime import datetime

HOURS = 10

@app.route("/api/v1.0/get_per_shift/<int:m_id>", methods=["GET"])
def get_per_shift(m_id):
    '''get data for this shift by id mechanism'''
    date_shift, shift = today_shift_date()
    data_per_shift = db.session.query(Post).filter(
        Post.date_shift == date_shift, Post.shift == shift, Post.mechanism_id == m_id).all()
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
    data = time_for_shift(type_mechanism, date, shift)

    return jsonify(data)


@app.route("/api/v1.0/all_last_data", methods=["GET"])
def all_last_data():
    '''get all data mechanism'''
    last_data_mech = [db.session.query(Post).filter(Post.mechanism_id == x).order_by(
        Post.timestamp.desc()).first() for x in all_mechanisms_id()]
    # last_data_mech = [db.session.query(Post).filter(Post.mechanism_id == x).first() for x in all_mechanisms_id()]
    data = {el.mech.type + str(el.mech.number): {'id': el.mech.id,
                                                 'name': el.mech.name,
                                                 'value': el.value,
                                                 'latitude': el.latitude,
                                                 'longitude': el.longitude,
                                                 'time': el.timestamp + timedelta(hours=HOURS)} for el in last_data_mech}
    return jsonify(data)

@app.route("/api/v1.0/all_last_data_ico", methods=["GET"])
def all_last_data_ico():
    '''get all data mechanism and mechanism state'''
    last_data_mech = [db.session.query(Post).filter(Post.mechanism_id == x).order_by(
    Post.timestamp.desc()).first() for x in all_mechanisms_id()]
    data = {el.mech.type + str(el.mech.number): {'id': el.mech.id,
                                                 'name': el.mech.name,
                                                 'value': el.value,
                                                 'latitude': el.latitude,
                                                 'longitude': el.longitude,
                                                 'src': image_mechanism(el.value, el.mech.type, el.mech.number, el.timestamp+ timedelta(hours=HOURS)),
                                                 'time': el.timestamp + timedelta(hours=HOURS)} for el in last_data_mech}
    return jsonify(data)


@app.route("/api/v1.0/get_mech/<int:m_id>", methods=["GET"])
def get_mech(m_id):
    '''get name mechanism'''
    mech = Mechanism.query.get(m_id)
    print(mech)
    return f'{mech.name}'

def add_fix_post(post):
    ''' I use it fix because arduino sometimes accumulates an extra minute '''
    last = db.session.query(Post).filter(Post.mechanism_id==post.mechanism_id).order_by(Post.timestamp.desc()).first()
    dt_seconds =  (post.timestamp -last.timestamp).seconds
    if dt_seconds < 200: # whatever the difference is not big
        last_minute =  last.timestamp.minute
        post_minute =  post.timestamp.minute
        dt_minutes = post_minute - last_minute
        if dt_minutes == 2 or dt_minutes == -58:
            post.timestamp -= timedelta(seconds=30)
    db.session.add(post)
    db.session.commit()

@app.route('/api/v1.0/add_get', methods=['GET'])
def add_get():
    '''add post by GET request from arduino'''
    mechanism_id = request.args.get('mechanism_id')
    password = request.args.get('password')
    value = request.args.get('value')
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    if latitude == '':
        latitude = 0
        longitude = 0
        print('fix-->', end=' ')
    items = mechanism_id, password, value, latitude, longitude
    test_items = any([item==None for item in items])
    print(items, datetime.now(), not test_items)
    if test_items:
        return 'Bad request'
    if password != post_pass:
        return 'Bad password'
    if int(mechanism_id) not in all_mechanisms_id():
        return 'Not this id'
    if float(latitude) == 0 or float(longitude) == 0:
        mech = Mechanism.query.get(mechanism_id)
        data_mech = db.session.query(Post).filter(
        Post.mechanism_id == mechanism_id).order_by(Post.timestamp.desc()).first()
        latitude = data_mech.latitude
        longitude = data_mech.longitude
    new_post = Post(value, latitude, longitude, mechanism_id)
    # data = request.data
    # db.session.add(new_post)
    # db.session.commit()
    add_fix_post(new_post)
    return f'Success, {str(items)}, {str(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))}'

@app.route('/api/v1.0/add_post', methods=['GET', 'POST'])
def add_post():
    '''add post by POST request from arduino'''
    print(request.method)
    need_keys = 'password', 'value', 'latitude', 'longitude', 'mechanism_id'
    request_j = request.json
    print(request_j, datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    if request.method == 'POST':
        if not request_j:
            abort(400)
        keys = [p for p in request_j.keys()]
        if not set(keys).issubset(need_keys):
            abort(400)
        if request_j['password'] != post_pass:
            abort(403)  # need use this password in Arduino
        if request_j['mechanism_id'] not in all_mechanisms_id():
            abort(405)
        value = request_j['value']
        latitude = request_j['latitude']
        longitude = request_j['longitude']
        mechanism_id = request_j['mechanism_id']
        if float(latitude) == 0 or float(longitude) == 0:
            mech = Mechanism.query.get(mechanism_id)
            data_mech = db.session.query(Post).filter(Post.mechanism_id == mechanism_id).order_by(Post.timestamp.desc()).first()
            latitude = data_mech.latitude
            longitude = data_mech.longitude
            print('--->', latitude, longitude, )
    elif request.method=='GET':
        print('==', request)
        text = request.args
        return 'Need POST methods'
    else:
        abort(400)

    new_post = Post(value, latitude, longitude, mechanism_id)
    data = request.data
    db.session.add(new_post)
    db.session.commit()
    # import sys
    # print('******', sys.getsizeof(request_j))
    return data, 201


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
    # return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(403)
def not_found(error):
    return make_response(jsonify({'error': 'Wrong password'}), 403)


@app.route('/api/v1.0/add_mechanism', methods=['POST'])
def add_mechanism():
    all_mech_id = [mech.id for mech in Mechanism.query.all()]
    request_f = request.form
    id = request_f['id']
    company = request_f['company']
    type = request_f['type']
    model = request_f['model']
    number = request_f['number']
    name = request_f['name']
    new_mech = Mechanism(id, company, type, model, number, name)
    data = request.data
    db.session.add(new_mech)
    db.session.commit()
    return redirect("http://localhost:5000/show_all_mechanisms", code=301)
    # return data



@app.route('/api/v1.0/add_mech_json', methods=['POST'])
# may be not use
def add_mechanism_json():
    id = request.json['id']
    company = request.json['company']
    type = request.json['type']
    model = request.json['model']
    number = request.json['number']
    name = request.json['name']
    new_mech = Mechanism(id, company, type, model, number, name)
    data = request.data
    db.session.add(new_mech)
    db.session.commit()
    return data
