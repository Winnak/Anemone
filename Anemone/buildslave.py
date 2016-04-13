""" a build slave for the program """

import os.path
import datetime
import subprocess
from flask import flash
from Anemone import app
from Anemone.models import Job

# Anemone needs its own settings. It needs to know the following:
# Where is the unity executable?
# Where is the unity build log? (job log)
# what do we rename the project to afterwards (job name)
# where do we put the project afterwards

# The project needs its own settings. It needs to know the following:
# what platforms are we building to (unittest is now a platform)
# what is out pre build steps
# what is our post build steps
# what scenes are we building
# is it a development build
# unity specific settings etc.

def build(project, config):
    """ builds the project """
    # TODO: combine with project slug and job id (thereby dropping the datetime)
    if config is None:
        flash("ERROR COULD NOT BUILD, INVALID CONFIG")
        return

    newjob = Job.create(project=project, name="quickbuild",
                        description="was build from the dashboard",
                        started=datetime.datetime.now(), status=0)

    os.makedirs(app.config["LOG_PATH"], exist_ok=True)
    logpath = os.path.join(app.config["LOG_PATH"], project.slug +
                           ".%Y-%m-%d_%Hh%Mm%Ss.log")
    newjob.log_path = logpath
    cmd = [app.config["UNITY_PATH"], config.get("arguments"),
           "-executeMethod", config.get("method"),
           "-logFile", str(datetime.datetime.now().strftime(logpath)),
           "-projectPath", config.get("project-path")]

    process = subprocess.Popen(cmd)
    newjob.status = 5
    newjob.save()

    #pylint: disable=E1101
    # this var does in fact exists
    flash(process.args)
    #pylint: enable=E1101
