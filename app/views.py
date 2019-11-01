from flask import request, json, jsonify, abort, make_response
from app import db, app
from app.model import Mechanism, Post

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

db.create_all()


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


@app.route("/test", methods=['GET'])
def get_test():
    all_mech_id = Mechanism.query.all()
    a = [mech.id for mech in Mechanism.query.all()]
    return jsonify({'tasks':data})
    abort(404)


@app.route('/add_post', methods=['POST'])
def add_post():
    all_mech_id = [mech.id for mech in Mechanism.query.all()]
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

@app.route('/add_mech', methods=['POST'])
def add_mechanism():
    id = request.form['id']
    company = request.form['company']
    type = request.form['type']
    model = request.form['model']
    number = request.form['number']
    name = request.form['name']
    new_mech = Mechanism(id, company, type, model, number, name)
    data = request.data
    db.session.add(new_mech)
    db.session.commit()
    return data

