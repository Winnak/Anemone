""" Dashboard view. """

import random
from os.path import join as path
from flask import render_template, g, request, redirect, url_for, flash, session
from Anemone import app
from Anemone.models import Job, Project
import Anemone.views
import Anemone.buildslave

JOBS_PER_PAGE = 10

@app.route("/<project>")
def dashboard(project):
    """ Index of the homepage. """
    g.selected_tab = "dashboard"

    # Check if project argument is correct
    project_query = Project.select().where(Project.slug == project).first()
    if project_query is None:
        flash("invalid project")
        return redirect(url_for("projects"))
    session["project"] = project_query

    health = dict(total=0, success=0, warning=0, error=0)

    # pylint: disable=R0204
    #disabling warning about redefining settings. I do this on purpose
    project_path = path(project_query.path, "build.abc")
    settings = Anemone.abcfile.parse(project_path)
    if settings is None:
        flash("Could not parse settings file, prehaps the file path ({}) is wrong"
              .format(project_path))
        settings = dict()
    else:
        settings = settings.m_nodes
    # pylint: enable=R0204

    query = (Job
             .select()
             .where(Job.project == project_query)
             .order_by(-Job.started.is_null(), -Job.started))

    entries = []
    count = 0
    for job in query:
        span = job.ended
        status = job.get_status()
        if job.started is not None:
            if job.ended is not None:
                span = job.ended - job.started

        if status is 1:
            health["total"] += 1
            health["success"] += 1
        elif status is 2:
            health["total"] += 1
            health["warning"] += 1
        elif status is 3:
            health["total"] += 1
            health["error"] += 1

        if count < JOBS_PER_PAGE:
            entries.append(dict(id=job.id, status=status, name=job.name,
                                start=job.started, end=job.ended, span=span))

    return render_template('dashboard.html', entries=entries, buildconf=settings, health=health)

@app.route("/test-build/<project>", methods=["POST"])
def build(project):
    """ temp: builds test project """
    project_query = Project.select().where(Project.slug == project).first()
    if project_query is None:
        flash("invalid project")
        return redirect(url_for("projects"))
    session["project"] = project_query

    settings = Anemone.abcfile.parse(path(project_query.path, "build.abc"))
    if settings is None:
        flash("project was missing a build file, please configure")

    # Check if project argument is correct
    if request.method == "POST":
        randomnames = open(path("Anemone", "templates", "namegen.html")).readlines()
        jobname = ("Quick." +
                   random.choice(randomnames)[:-1] + # for some reason choice gives extra space
                   random.choice(randomnames)[:-1]) # for some reason choice gives extra space

        newjob = Job.create(project=project_query, name=jobname,
                            description="was build from the dashboard")
        newjob.name = newjob.name + ".{0:0=3d}".format(newjob.id)
        newjob.save()
        Anemone.buildslave.build(newjob,
                                 project_query,
                                 settings[request.form.get("config", None)])
    return redirect(project)
