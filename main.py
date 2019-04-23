"Puppies"

import json
import random
import string

from flask import Flask, render_template, redirect, url_for, jsonify
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

@app.route('/auth')
def authenticate():
    return 1;

@app.route('/add')
def add_puppy():
    db.rpush('puppy-ids', random_string(10))
    return redirect(url_for('index'))

app.run(host=config.HOST, port=config.PORT)
