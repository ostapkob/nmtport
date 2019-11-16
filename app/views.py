# -*- coding: utf-8 -*-
from flask import request, json, jsonify, abort, make_response
from flask import render_template, flash, redirect
from app import db, app
from app.model import Mechanism, Post
from app.form import AddMechanism
from datetime import datetime, timedelta
from functions import today_shift_date, all_mechanisms_id, time_for_shift, time_for_shift_list
from sqlalchemy import func
db.create_all()
@app.route("/")
@app.route("/index")
def index():
    date_shift, shift = today_shift_date()
    data = time_for_shift_list(date_shift, shift)
    # data ={'firstname': "Mr.", 'lastname': "My Father's Son"}
    return render_template("index.html",
                           data=data,
                           val=type(data),
                           )

# Dont work
@app.route("/form_mech", methods=['GET', 'POST'])
def form_mech():
    form_m = AddMechanism()
    if form_m.validate_on_submit():
        flash('Ostap')
        return redirect('/test')
    return render_template("form_mech.html",
                           title='Добавить механизм',
                           form=form_m)


@app.route("/show_all_mechanisms")
def show_all_mechanisms():
    all_mech = Mechanism.query.all()
    return render_template("mechanisms.html",
                           title='Механизмы',
                           mechs=all_mech)

@app.route("/last")
def last():
    # all_mech_id = [m.id for m in Mechanism.query.all()]
    posts = [Post.query.filter_by(mechanism_id=p).order_by(
        Post.id.desc()).limit(10) for p in all_mechanisms_id()]
    return render_template("last.html",
                           title='Последние данные',
                           tim=datetime.now() + timedelta(days=2),
                           posts=posts)

@app.route("/per_shift")
def per_shift():
    date_shift, shift = today_shift_date()

    cursor = db.session.query(Post).filter(Post.date_shift==date_shift, Post.shift==shift).order_by(Post.mechanism_id).all()
    data_per_shift={}
    for el in cursor:
        if data_per_shift.get(el.mech.id):
            data_per_shift[el.mech.id].append(el)
        else:
            data_per_shift[el.mech.id]=[el]
    return render_template("per_shift.html",
                           title='За смену',
                           date_shift=date_shift,
                           shift=shift,
                           data_per_shift=data_per_shift,
                           )

# ================API=========================

@app.route("/get_per_shift/<int:m_id>", methods=["GET"])
def get_per_shift(m_id):
    date_shift, shift = today_shift_date()
    data_per_shift = db.session.query(Post).filter( Post.date_shift == date_shift, Post.shift == shift, Post.mechanism_id == m_id).all()
    try:
        start = db.session.query(Post.timestamp).filter( Post.date_shift == date_shift, Post.shift == shift, Post.mechanism_id == m_id).first()[0]
        stop = db.session.query(Post.timestamp).filter(Post.date_shift == date_shift, Post.shift == shift, Post.mechanism_id == m_id).order_by(Post.timestamp.desc()).first()[0]
    except TypeError:
        abort(405)
    start += timedelta(hours=10)
    stop += timedelta(hours=10)
    total = round(sum(el.value for el in data_per_shift)/60, 3)
    data = {'total': total, 'start': start, 'stop': stop}
    return jsonify(data)


@app.route("/get_mech/<int:m_id>", methods=["GET"])
def get_mech(m_id):
    mech = Mechanism.query.get(m_id)
    return f'{mech.name}'


@app.route("/get_post/<int:m_id>", methods=["GET"])
def get_post(m_id):
    mech = Post.query.get(m_id)
    if mech == None:
        return abort(404)
    post = Post.query.filter_by(mechanism_id=m_id).first()
    return f'{post.value}'


@app.route('/add_post', methods=['POST'])
def add_post():
    # import sys
    need_keys = 'password', 'value', 'latitude', 'longitude', 'mechanism_id'
    request_j = request.json
    print(request_j)
    if not request_j:
        abort(400)
    keys = [p for p in request_j.keys()]
    if not set(keys).issubset(need_keys):
        abort(400)
    if request_j['password'] != 'super':
        abort(403)  # need use this password in Arduino
    if request_j['mechanism_id'] not in all_mechanisms_id():
        abort(405)
    value = request_j['value']
    latitude = request_j['latitude']
    longitude = request_j['longitude']
    mechanism_id = request_j['mechanism_id']
    new_post = Post(value, latitude, longitude, mechanism_id)
    data = request.data
    db.session.add(new_post)
    db.session.commit()
    # print('******', sys.getsizeof(request_j))
    return data, 201


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
    # return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(403)
def not_found(error):
    return make_response(jsonify({'error': 'Wrong password'}), 403)


@app.route('/add_mechanism', methods=['POST'])
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

# maybe not use
@app.route('/add_mech_json', methods=['POST'])
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
