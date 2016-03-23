""" The main import stuff script """
# pylint: disable=C0103, method-hidden
# pylint: disable=C0413, method-hidden

import os
from flask import Flask

app = Flask(__name__)

@app.context_processor
def utility_processor():
    """ custom funcions for jinja """
    def get_status_icon(statuscode):
        """ returns the proper icon for the status code """
        def status_switch(x):
            """ switch case for status codes """
            return {
                0 : "fa fa-circle fa-2x",
                1 : "fa fa-check-circle fa-2x",
                2 : "fa fa-exclamation-circle fa-2x",
                3 : "fa fa-times-circle fa-2x",
                4 : "fa fa-cog fa-spin fa-2x",
                5 : "fa fa-clock-o fa-2x"
            }.get(x, 0)

        return status_switch(statuscode)

    return dict(get_status_icon=get_status_icon)

# important: has to be importet before app is created
from Anemone.config import configuration
import Anemone.views

# Load default config and override config from an environment variable
app.config.update(configuration)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# important: has to be importet before app is created and configured
import Anemone.database
