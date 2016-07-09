""" A layer on top of GitPython, handles pulling and scheduling. """

import os.path
import platform
import random
import git
from Anemone import app, schedule
from Anemone.models import Job, Project
from Anemone.abcfile import parse as abcparse
from Anemone.buildslave import build

def setup_schedule():
    """ Setups up the schedule for building the project periodically. """
    for project in Project.select():
        if (project.schedule_interval is not None) and (project.schedule_interval > 0):
            schedule.add_job(pull_build_project, "interval", id="building_" + str(project.id),
                             hours=project.schedule_interval,
                             args=[project, "master"])

def pull_build_project(project, branch="master"):
    """ pulls and build a project """
    repo_result, pull_log = pull(project.path, app.config["SSH_PRIVATE"], branch)
    if repo_result:
        newjob = create_job(project, pull_log)
        settings = abcparse(os.path.join(project.path, "build.abc"))
        build(newjob, project, settings["windows"]) #TODO: Handle configs

def pull(repo_path, ssh, branch="master"):
    """ Pulls the project and returns wether or not there were changes """
    ssh_key = os.path.abspath(ssh)
    if platform.system() == "Windows":
        ssh_key = "/" + ssh_key.replace("\\", "/").replace(":", "")
    ssh_cmd = "ssh -i %s" % ssh_key

    my_repo = git.Repo(repo_path)

    pull_output = ""
    contributer_emails = list()
    files = list()
    new_commit = False

    with my_repo.git.custom_environment(GIT_SSH_COMMAND=ssh_cmd):
        for result in my_repo.remotes.origin.pull(branch):
            if result.commit == my_repo.head.commit:
                continue
            new_commit = True
            contributer_emails.append(result.commit.author.email)
            pull_output += str(result.commit) + "\n"
            pull_output += str(result.commit.author) + "<" + str(result.commit.author.email) + ">\n"
            pull_output += str(result.commit.committed_datetime) + "\n"
            pull_output += str(result.commit.summary) + "\n"
            pull_output += str(result.commit.stats.total) + "\n\n"

            for stat in result.commit.stats.files: #We write all files at the end of the description
                files.append(stat)

    if not new_commit:
        # There were no new changes, we do not need to rebuild.
        return False, "No new changes"

    pull_output += "Files changed:\n"
    for changes in files:
        pull_output += changes

    return True, pull_output

def create_job(project, description):
    """ Creates and returns a new job with a random name """
    randomnames = open(os.path.join("Anemone", "templates", "namegen.html")).readlines()
    jobname = ("Quick." +
               random.choice(randomnames)[:-1] + # for some reason choice gives extra space
               random.choice(randomnames)[:-1]) # for some reason choice gives extra space

    newjob = Job.create(project=project, name=jobname, description=description)
    newjob.name = newjob.name + ".{0:0=3d}".format(newjob.id)
    newjob.save()
    return newjob
