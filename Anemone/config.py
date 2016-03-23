""" Configuration file for Anemone """
# pylint: disable=C0103, method-hidden

import os
from Anemone import app

configuration = dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='password' #legit password
)
