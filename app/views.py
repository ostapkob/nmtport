# -*- coding: utf-8 -*-
from flask import request, json, jsonify, abort, make_response
from flask import render_template, flash, redirect
from app import db, app
from app.model import Mechanism, Post
from app.form import AddMechanism
db.create_all()

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html",
                           val = 'fox')

#Dont work
@app.route("/form_mech", methods=['GET', 'POST'])
def form_mech():
    form_m = AddMechanism()
    if form_m.validate_on_submit():
        flash('Ostap')
        return redirect('/test')
    return render_template("form_mech.html",
                           title = 'Добавить механизм',
                           form=form_m)


@app.route("/show_all_mechanisms")
def show_all_mechanisms():
    all_mech = Mechanism.query.all()
    return render_template("mechanisms.html",
                           title = 'Механизмы',
                           mechs = all_mech)



#================API=========================
@app.route("/get_mech/<int:m_id>", methods=["GET"])
def get_mech(m_id):
    mech= Mechanism.query.get(m_id)
    return f'{mech.name}'

@app.route("/get_post/<int:p_id>", methods=["GET"])
def get_post(p_id):
    mech= Post.query.get(p_id)
    if mech == None:
        return abort(404)
    return f'{mech.value}'

@app.route('/add_post', methods=['POST'])
def add_post():
    all_mech_id = [m.id for m in Mechanism.query.all()]
    need_keys= 'password', 'value', 'latitude', 'longitude', 'mechanism_id'
    request_j =request.json
    if not request_j: abort(400)
    keys = [p for p in request_j.keys()]
    if not set(keys).issubset(need_keys): abort(400)
    if request_j['password'] != 'super': abort(403) # need use this password in Arduino
    if request_j['mechanism_id'] not in all_mech_id: abort(405)

    value=request_j['value']
    latitude = request_j['latitude']
    longitude = request_j['longitude']
    mechanism_id =  request_j['mechanism_id']
    new_post = Post(value, latitude, longitude, mechanism_id)
    data = request.data
    db.session.add(new_post)
    db.session.commit()
    return data, 201

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(403)
def not_found(error):
    return make_response(jsonify({'error': 'Wrong password'}), 403)

@app.route('/add_mechanism', methods=['POST'])
def add_mechanism():
    all_mech_id = [mech.id for mech in Mechanism.query.all()]
    request_f = request.form
    # need_keys = 'id', 'company', 'type', 'model', 'number', 'name'
    # keys = [p for p in request_f.keys()]
    # return render_template(keys)
    # if not set(keys).issubset(need_keys): abort(402)
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
    return data

#maybe not use
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

