""" database management """

from flask import g
import peewee
from Anemone import app

DATABASE = peewee.SqliteDatabase(app.config["DATABASE_PATH"])

@app.before_request
def before_request():
    """ called before a request """
    g.database = DATABASE.connect()

@app.teardown_request
@app.teardown_appcontext
def teardown_request(exception):
    """ called if a request returns wrong object or no object """
    database = getattr(g, 'database', None)
    if database is not None:
        database.close()
    if exception != None:
        print(exception)
