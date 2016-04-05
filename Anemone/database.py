""" database management """

from flask import g
import peewee
import Anemone

PATH = "Anemone/tmp/"
FILEPATH = PATH + "anemone.db"
DATABASE = peewee.SqliteDatabase(FILEPATH)

@Anemone.app.before_request
def before_request():
    """ called before a request """
    g.database = DATABASE.connect()

@Anemone.app.teardown_request
@Anemone.app.teardown_appcontext
def teardown_request(exception):
    """ called if a request returns wrong object or no object """
    database = getattr(g, 'database', None)
    if database is not None:
        database.close()
    if exception != None:
        print(exception)
