""" The main configuration and import stuff script """
# pylint: disable=C0103, method-hidden
# pylint: disable=C0413, method-hidden

import os
from flask import Flask

app = Flask(__name__)

# important: has to be importet before app is created
import Anemone.views

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='password' #legit password
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# important: has to be importet before app is created and configured
import Anemone.database
