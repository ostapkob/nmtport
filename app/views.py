#int -*- coding: utf-8 -*-
from flask import request, json, jsonify, abort, make_response
from flask import render_template, flash, redirect, url_for, send_from_directory
from app import db, app
from app.model import Mechanism, Post, User
from app.form import AddMechanism, SelectDataShift, LoginForm
from datetime import datetime, timedelta
from app.functions import today_shift_date, all_mechanisms_id, handle_date
from app.usm import time_for_shift_usm, usm_periods
from app.kran import time_for_shift_kran
import app.api as API
from sqlalchemy import func
from pprint import pprint
import os
from flask_login import current_user, login_user, logout_user

# db.create_all()


@app.route("/")
@app.route("/index")
def index():
    if not current_user.is_authenticated:
        return redirect("login")
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
    if not current_user.is_authenticated:
        return redirect("login")
    form_m = AddMechanism()
    if form_m.validate_on_submit():
        flash('Ostap')
        return redirect('/test')
    return render_template("form_mech.html",
                           title='Добавить механизм',
                           form=form_m)


@app.route("/last")
def last():
    if not current_user.is_authenticated:
        return redirect("login")
    return render_template("last.html",
                           title='Last')

@app.route("/kran")
def kran():
    if not current_user.is_authenticated:
        return redirect("login")
    return render_template("kran.html",
                           title='Краны')

@app.route("/usm")
def usm():
    if not current_user.is_authenticated:
        return redirect("login")

    return render_template("usm.html", title='УСМ')

@app.route("/map")
def maps():
    if not current_user.is_authenticated:
        return redirect("login")
    return render_template("map.html",
                           title='Maps')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect('login')
        login_user(user, remember=form.remember_me.data)
        flash(f'Login for user {form.username.data} : {form.remember_me.data}')
        return redirect("/")
    return render_template("login.html",
                           title='Log In',
                           form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')


@app.route("/archive", methods=['GET', 'POST'])
def archive():
    if not current_user.is_authenticated:
        return redirect("login")
    form = SelectDataShift()
    if form.validate_on_submit():
        date = handle_date(form.date_shift.data)
        shift = form.shift.data
        type_mechanism = form.type.data
        if type_mechanism == 'usm':
            # data = time_for_shift_usm(date, shift)
            data = usm_periods(time_for_shift_usm(date, shift))
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

@app.route("/show_all_mechanisms")
def show_all_mechanisms():
    if not current_user.is_authenticated:
        return redirect("login")
    all_mech = Mechanism.query.all()
    return render_template("mechanisms.html",
                           title='Механизмы',
                           mechs=all_mech)

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

# @app.route("/list_api")
# def list_api():
#     ls_api = dir(API)
#     return render_template("list_api.html",
#                            title='Posible_api',
#                            ls_api=ls_api)



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
