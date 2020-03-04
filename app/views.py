#int -*- coding: utf-8 -*-
from flask import request, json, jsonify, abort, make_response
from flask import render_template, flash, redirect, url_for, send_from_directory
from app import db, app
from app.model import Mechanism, Post
from app.form import AddMechanism, SelectDataShift
from datetime import datetime, timedelta
from functions import today_shift_date, all_mechanisms_id, time_for_shift_usm, time_for_shift_kran, handle_date
import app.api as API
from sqlalchemy import func
from pprint import pprint
import os


db.create_all()


@app.route("/")
@app.route("/index")
def index():
    date_shift, shift = today_shift_date()
    # data = time_for_shift_usm(date_shift, shift)
    # data = time_for_shift('sennebogen', date_shift, shift)
    # date_shift = datetime.strptime(date_shift, '%d.%m.%Y').date()
    return render_template("index.html",
                           title='Мониторинг',
                           # data=data,
                           shift=shift,
                           date_shift=date_shift
                           )

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico')

@app.route("/form_mech", methods=['GET', 'POST'])
def form_mech():
    form_m = AddMechanism()
    if form_m.validate_on_submit():
        flash('Ostap')
        return redirect('/test')
    return render_template("form_mech.html",
                           title='Добавить механизм',
                           form=form_m)


@app.route("/last")
def last():
    return render_template("last.html",
                           title='Last')

@app.route("/kran")
def kran():
    return render_template("kran.html",
                           title='Краны')

@app.route("/usm")
def usm():
    return render_template("usm.html",
                           title='УСМ')
@app.route("/map")
def maps():
    return render_template("map.html",
                           title='Maps')


# @app.route("/vue")
# def vue():
#     date_shift, shift = today_shift_date()
#     date_shift = date_shift.strftime('%d.%m.%Y')
#     type_mech = 'usm'
#     http = 'http://127.0.0.1:5000/api/v1.0/get_data/'
#     http += type_mech + '/' + date_shift + '/' + str(shift)
#     print(http)
#     return render_template("vue.html",
#                            http=http,
#                            date_shift=date_shift,
#                            shift=shift,
#                            title='Vue')


@app.route("/show_all_mechanisms")
def show_all_mechanisms():
    all_mech = Mechanism.query.all()
    return render_template("mechanisms.html",
                           title='Механизмы',
                           mechs=all_mech)



@app.route("/archive", methods=['GET', 'POST'])
def archive():
    form = SelectDataShift()
    if form.validate_on_submit():
        date = handle_date(form.date_shift.data)
        shift = form.shift.data
        type_mechanism = form.type.data
        if type_mechanism == 'usm':
            data = time_for_shift_usm(date, shift)
        if type_mechanism =='kran':
            data = time_for_shift_kran(date, shift)

        return render_template("archive.html",
                               data=data,
                               type_mechanism = type_mechanism,
                               shift=shift,
                               date_shift=date.strftime("%d.%m.%Y"),
                               form=form,
                               )

    date, shift = today_shift_date()
    data = {}
    return render_template("archive.html",
                           data=data,
                           shift=shift,
                           date_shift=date.strftime("%d.%m.%Y"),
                           form=form,
                           )


@app.route("/list_api")
def list_api():
    ls_api = dir(API)
    return render_template("list_api.html",
                           title='Posible_api',
                           ls_api=ls_api)


# @app.route("/per_shift")
# def per_shift():
#     date_shift, shift = today_shift_date()

#     cursor = db.session.query(Post).filter(
#         Post.date_shift == date_shift, Post.shift == shift).order_by(Post.mechanism_id).all()
#     data_per_shift = {}
#     for el in cursor:
#         if data_per_shift.get(el.mech.id):
#             data_per_shift[el.mech.id].append(el)
#         else:
#             data_per_shift[el.mech.id] = [el]
#     return render_template("per_shift.html",
#                            title='За смену',
#                            date_shift=date_shift,
#                            shift=shift,
#                            data_per_shift=data_per_shift,
#                            )
