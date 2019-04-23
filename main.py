"Puppies"

import json
import random
import string

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

@app.route('/add')
def add_puppy():
    db.rpush('puppy-ids', random_string(10))
    return redirect(url_for('index'))

app.run(host=config.HOST, port=config.PORT)
