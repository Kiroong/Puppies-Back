"Puppies"

import json
import random
import string

from functools import wraps

from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_cors import CORS

from database_wrapper_redis import DatabaseWrapperRedis
import config

app = Flask(__name__) #pylint:disable=invalid-name
CORS(app)

db = DatabaseWrapperRedis( #pylint:disable=invalid-name
    host=config.DB_HOST, port=config.DB_PORT,
    db=config.DB_NUM, namespace='puppies'
)

def random_string(n):
    return ''.join(random.choice(string.ascii_letters) for _ in range(n))

@app.route('/')
def index():
    # puppy_ids = db.lrange('puppy-ids', 0, -1)
    return jsonify('hello, world!')

@app.route('/auth', methods=['POST'])
def authenticate():
    data = request.get_json()
    arg_id = data['id']
    arg_pw = data['pw']
    matches = arg_id == config.ID and arg_pw == config.PW
    if matches:
        token = random_string(20)
        db.set('session-' + token, 1)
        db.expire('session-' + token, 86400)
        return jsonify(token)
    else:
        return jsonify('')

def login_required(f):
    @wraps(f)
    def login_check(*args, **kwargs):
        try:
            token = request.get_json()['token']
            if db.get('session-' + token):
                return f(*args, **kwargs)
            else:
                return jsonify('')
        except:
            return jsonify('')
    return login_check

@app.route('/puppies/create', methods=['POST'])
@login_required
def create_puppy():
    new_puppy_id = random_string(20)
    db.rpush('puppy-ids', new_puppy_id)
    return jsonify(new_puppy_id)

@app.route('/puppies/list', methods=['POST'])
@login_required
def list_puppies():
    puppy_ids = db.lrange('puppy-ids', 0, -1)
    return jsonify(puppy_ids)

@app.route('/puppies/get', methods=['POST'])
@login_required
def get_puppy():
    data = request.get_json()
    puppy_id = data['puppyId']
    return jsonify(db.get('puppy:{}'.format(puppy_id)) or {})

@app.route('/puppies/update', methods=['POST'])
@login_required
def update_puppy():
    data = request.get_json()
    puppy_id = data['puppyId']
    new_puppy = data['newPuppy']
    db.set('puppy:{}'.format(puppy_id), new_puppy)
    return jsonify(new_puppy)

@app.route('/puppies/delete', methods=['POST'])
@login_required
def delete_puppy():
    data = request.get_json()
    puppy_id = data['puppyId']
    print(puppy_id)
    db.lrem('puppy-ids', 0, puppy_id)
    print(db.lrange('puppy-ids', 0, -1))
    return jsonify(True)

app.run(host=config.HOST, port=config.PORT)
