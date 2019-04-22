"Puppies"

from flask import Flask

from database_wrapper_redis import DatabaseWrapperRedis
import config

app = Flask(__name__) #pylint:disable=invalid-name

db = DatabaseWrapperRedis( #pylint:disable=invalid-name
    host=config.DB_HOST, port=config.DB_PORT,
    db=config.DB_NUM, namespace=__name__
)

@app.route('/')
def index():
    return 'Hello, World!'

app.run(host=config.HOST, port=config.PORT)
