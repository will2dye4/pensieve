import json
import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI='sqlite:///%s' % os.path.join(app.root_path, 'pensieve.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS=True,
    SECRET_KEY='development_key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('PENSIEVE_SETTINGS', silent=True)

db = SQLAlchemy(app)


@app.route('/')
def index():
    return json.dumps({'message': 'Hello, Harry'})


if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run()
