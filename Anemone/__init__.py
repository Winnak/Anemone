""" The main import stuff script """
# invalid constant name app
# pylint: disable=C0103


import os
from flask import Flask

app = Flask(__name__)

# TODO: find a better place for this
@app.context_processor
def utility_processor():
    """ custom funcions for jinja """
    def get_status_icon(statuscode):
        """ returns the proper icon for the status code """
        def status_switch(x):
            """ switch case for status codes """
            return {
                0 : "fa fa-circle",
                1 : "fa fa-check-circle",
                2 : "fa fa-exclamation-circle",
                3 : "fa fa-times-circle",
                4 : "fa fa-cog fa-spin",
                5 : "fa fa-clock-o"
            }.get(x, 0)

        return status_switch(statuscode)

    return dict(get_status_icon=get_status_icon)

# Import should be placed at the top of the moduleat
# pylint: disable=C0413
# pylint has been disabled here because of how flask recommends maintaining a project
from Anemone.config import configuration
import Anemone.views.projects
import Anemone.views.dashboard
import Anemone.views.jobs
import Anemone.views.login
import Anemone.views.configuration

# Load default config and override config from an environment variable
app.config.update(configuration)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

# important: has to be importet before app is created and configured
import Anemone.database
#pylint: enable=C0413
