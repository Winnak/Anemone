""" A build slave for the program. """

import os.path
import subprocess
import threading
import re
import datetime
from flask import flash
from Anemone import app

PROG_ERROR = re.compile("[Ee]rror")
PROG_SUCCESS = re.compile("Exiting batchmode successfully now!")
PROG_WARNING = re.compile("[Ww]arning")

# FILE = open("test.log")
# while PROC.poll() is None:
#     LINE = FILE.readline()
#     if LINE:
#         print(LINE, end="")

#TODO: figure out a cloud solution
#TODO: Check if it is currently building the project an refuse to build if so.
#TODO: Rename build to job name and copy to out directory.

def build(job, config):
    """ builds a job """
    if config is None:
        flash("ERROR COULD NOT BUILD, INVALID CONFIG")
        return

    path = config.get("project-path")
    if path is None:
        flash("ERROR no project-path specified")
        return

    os.makedirs(app.config["LOG_PATH"], exist_ok=True)
    logpath = os.path.join(app.config["LOG_PATH"], job.project.slug + str(job.id) +
                           str(datetime.datetime.now().strftime(".%Y-%m-%d_%Hh%Mm%Ss.log")))
    job.log_path = logpath
    cmd = (app.config["UNITY_PATH"] + " " + config.get("arguments") +
           " -executeMethod " + config.get("method") +
           " -logFile " + logpath +
           " -projectPath " + path)

    def run_in_thread(job, args):
        """ waits for the job to finish and updates the job """
        pre = config.get("pre-build")
        if pre is not None: #TODO: embed into unity log
            subprocess.call(pre, shell=True, cwd=path)
        proc = subprocess.Popen(args)
        job.started = datetime.datetime.now()
        job.active = True
        job.save()
        proc.wait()
        post = config.get("post-build")
        if post is not None: #TODO: embed into unity log
            subprocess.call(post, shell=True, cwd=path)
        job.active = False
        job.ended = datetime.datetime.now()
        job.result = parse_joblog(job.log_path)
        job.save()
    thread = threading.Thread(target=run_in_thread, args=(job, cmd))
    thread.start()
    return thread

def parse_joblog(filepath):
    """ regexes through the log and looks for errors or warnings returns status code """
    log = open(filepath).read()
    if PROG_ERROR.search(log) or not PROG_SUCCESS.search(log):
        return 3
    elif PROG_WARNING.search(log):
        return 2
    else:
        return 1
