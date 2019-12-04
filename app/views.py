# -*- coding: utf-8 -*-
from flask import request, json, jsonify, abort, make_response
from flask import render_template, flash, redirect, url_for
from app import db, app
from app.model import Mechanism, Post
from app.form import AddMechanism, SelectDataShift
from datetime import datetime, timedelta
from functions import today_shift_date, all_mechanisms_id, time_for_shift, time_for_shift_list
import app.api as API
from sqlalchemy import func
from pprint import pprint
db.create_all()

@app.route("/")
@app.route("/index")
def index():
    date_shift, shift = today_shift_date()
    data = time_for_shift('usm', date_shift, shift)
    # data = time_for_shift('sennebogen', date_shift, shift)
    return render_template("index.html",
                           data=data,
                           shift=shift,
                           date_shift = date_shift
                           )

@app.route("/form_mech", methods=['GET', 'POST'])
def form_mech():
    form_m = AddMechanism()
    if form_m.validate_on_submit():
        flash('Ostap')
        return redirect('/test')
    return render_template("form_mech.html",
                           title='Добавить механизм',
                           form=form_m)

@app.route("/vue")
def vue():

    return render_template("vue.html",
                           title='Vue')

@app.route("/show_all_mechanisms")
def show_all_mechanisms():
    all_mech = Mechanism.query.all()
    return render_template("mechanisms.html",
                           title='Механизмы',
                           mechs=all_mech)

@app.route("/history", methods=['GET', 'POST'])
def history():
    form = SelectDataShift()
    if form.validate_on_submit():
        date_shift= form.date_shift.data
        shift=form.shift.data
        type_mechanism=form.type.data
        try:
            date = datetime.strptime(date_shift, '%Y-%m-%d').date()
        except ValueError:
            flash('Enter correct shift')
            return redirect(url_for('index'))
        data = time_for_shift(type_mechanism, date, shift)
        return render_template("history.html",
                            data=data,
                            shift=shift,
                            date_shift = date,
                            form=form,
                            )

    date, shift = today_shift_date()
    data={}
    return render_template("history.html",
                            data=data,
                            shift=shift,
                            date_shift = date,
                            form=form,
                            )

@app.route("/list_api")
def list_api():
    ls_api=dir(API)
    return render_template("list_api.html",
                           title='Posible_api',
                           ls_api=ls_api)
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

