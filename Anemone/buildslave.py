""" A build slave for the program. """

import os.path
import shutil
import subprocess
import threading
import re
import datetime
from distutils.dir_util import remove_tree
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

def build(job, project, config):
    """ builds a job """
    if config is None:
        flash("ERROR COULD NOT BUILD, INVALID CONFIG")
        return

    if project.path is None:
        flash("ERROR no project-path specified")
        return

    os.makedirs(app.config["LOG_PATH"], exist_ok=True)
    logpath = os.path.join(app.config["LOG_PATH"], job.project.slug + str(job.id) +
                           str(datetime.datetime.now().strftime(".%Y-%m-%d_%Hh%Mm%Ss.log")))
    job.log_path = logpath
    cmd = (app.config["UNITY_PATH"] + " " + config.get("arguments") +
           " -executeMethod " + config.get("method") +
           " -logFile " + logpath +
           " -projectPath " + project.path)

    def run_in_thread(job, args):
        """ waits for the job to finish and updates the job """
        pre = config.get("pre-build")
        if pre is not None: #TODO: embed into unity log
            subprocess.call(pre, shell=True, cwd=project.path)
        proc = subprocess.Popen(args)
        job.started = datetime.datetime.now()
        job.active = True
        job.save()
        proc.wait()

        # build finsihed.
        result = parse_joblog(job.log_path)
        post = config.get("post-build")
        if result is not 3: # as long as we don't have any errors.
            if post is not None: #TODO: embed into unity log
                subprocess.call(post, shell=True, cwd=project.path)
            job.path = move_to_out_folder(project, job, config)
        job.active = False
        job.ended = datetime.datetime.now()
        job.result = result
        job.save()
    thread = threading.Thread(target=run_in_thread, args=(job, cmd))
    thread.start()
    return thread

def move_to_out_folder(project, job, config):
    """ Moves the final project into the tmp folder """
    build_file = config.get("out")
    if os.path.isfile(build_file):
        flash("Could not find output file", category="error")
        return

    build_folder = os.path.join(project.path, os.path.dirname(build_file))
    output_folder = os.path.join(project.output, job.name)

    shutil.make_archive(output_folder, "zip", build_folder)
    remove_tree(build_folder)

    return output_folder + ".zip"

def parse_joblog(filepath):
    """ regexes through the log and looks for errors or warnings returns status code """
    log = open(filepath).read()
    if PROG_ERROR.search(log) or not PROG_SUCCESS.search(log):
        return 3
    elif PROG_WARNING.search(log):
        return 2
    else:
        return 1
