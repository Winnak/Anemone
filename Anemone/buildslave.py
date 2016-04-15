""" A build slave for the program. """

import os.path
import datetime
import subprocess
from flask import flash
from Anemone import app
from Anemone.models import Job

#TODO: figure out a cloud solution
#TODO: pre build steps
#TODO: post build steps

def build(project, config):
    """ builds the project """
    if config is None:
        flash("ERROR COULD NOT BUILD, INVALID CONFIG")
        return

    newjob = Job.create(project=project, name="quickbuild",
                        description="was build from the dashboard",
                        started=datetime.datetime.now(), status=0)

    os.makedirs(app.config["LOG_PATH"], exist_ok=True)
    logpath = os.path.join(app.config["LOG_PATH"], project.slug + str(newjob.id) +
                           ".%Y-%m-%d_%Hh%Mm%Ss.log")
    newjob.log_path = logpath
    cmd = [app.config["UNITY_PATH"], config.get("arguments"),
           "-executeMethod", config.get("method"),
           "-logFile", str(datetime.datetime.now().strftime(logpath)),
           "-projectPath", config.get("project-path")]

    subprocess.Popen(cmd) #TODO: hook this up to something so that we know when the process is done.
    newjob.status = 5
    newjob.save()
