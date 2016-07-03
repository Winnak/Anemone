""" The main import stuff script """
# pylint: disable=C0103
# disabling C0103: Invalid constant name "app", to be consistent with flask apps.

import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config.from_pyfile("../application.cfg", False)
schedule = BackgroundScheduler()
schedule.start() #TODO: restart unfinshed jobs

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

# pylint: disable=C0413
# Import should be placed at the top of the module
# pylint has been disabled here because of how flask recommends maintaining a project
import Anemone.views.projects
import Anemone.views.dashboard
import Anemone.views.jobs
import Anemone.views.login
import Anemone.views.configuration
import Anemone.views.namegen
import Anemone.views.health

from Anemone.models import ProjectJSONEncoder
app.json_encoder = ProjectJSONEncoder
