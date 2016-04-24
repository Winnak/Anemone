""" A build slave for the program. """

import os.path
import subprocess
import threading
import datetime
from flask import flash
from Anemone import app

# FILE = open("test.log")
# while PROC.poll() is None:
#     LINE = FILE.readline()
#     if LINE:
#         print(LINE, end="")

#TODO: figure out a cloud solution
#TODO: pre build steps
#TODO: post build steps

def build(job, config):
    """ builds a job """
    if config is None:
        flash("ERROR COULD NOT BUILD, INVALID CONFIG")
        return

    os.makedirs(app.config["LOG_PATH"], exist_ok=True)
    logpath = os.path.join(app.config["LOG_PATH"], job.project.slug + str(job.id) +
                           str(datetime.datetime.now().strftime(".%Y-%m-%d_%Hh%Mm%Ss.log")))
    job.log_path = logpath
    cmd = (app.config["UNITY_PATH"] + " " + config.get("arguments") +
           " -executeMethod " + config.get("method") +
           " -logFile " + logpath +
           " -projectPath " + config.get("project-path"))

    def run_in_thread(job, args):
        """ waits for the job to finish and updates the job """
        proc = subprocess.Popen(args)
        job.started = datetime.datetime.now()
        job.active = True
        job.save()
        proc.wait()
        job.active = False
        job.result = 1 #TODO: look for errors
        job.ended = datetime.datetime.now()
        job.save()
    thread = threading.Thread(target=run_in_thread, args=(job, cmd))
    thread.start()
    return thread
