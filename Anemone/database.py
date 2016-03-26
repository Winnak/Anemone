""" database management """

import sqlite3
from contextlib import closing
from flask import g
from Anemone import app

def connect_db():
    """ Connects to the SQLite database """
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    """ Initializes the database """
    with closing(connect_db()) as database:
        with app.open_resource('schema.sql', mode='r') as schemafile:
            database.cursor().executescript(schemafile.read())
        database.commit()


@app.before_request
def before_request():
    """ called before a request """
    g.database = connect_db()

@app.teardown_request
@app.teardown_appcontext
def teardown_request(exception):
    """ called if a request returns wrong object or no object """
    database = getattr(g, 'database', None)
    if database is not None:
        database.close()
    if exception != None:
        print(exception)
