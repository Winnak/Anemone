""" Jobs and job view. """

import os
from datetime import datetime
from flask import g, render_template, flash, redirect, url_for, session, request
import peewee
from Anemone import app, abcfile, schedule
from Anemone.models import Job, Project
from Anemone.buildslave import build

JOBSPERPAGE = 30

@app.route("/<project>/jobs")
def jobs_index(project):
    """ Shows the index if no jobs given. """
    return jobs(project, 1)

@app.route("/jobs")
def jobs_index_2():
    """ Shows the index if no jobs or project given. """
    return jobs_index(session.get("project"))

@app.route("/<project>/jobs/<page>")
def jobs(project, page):
    """ For when no job id was given. """
    g.selected_tab = "jobs"

    # Check if project argument is correct
    project_query = Project.select().where(Project.slug == project).first()
    if project_query is None:
        flash("Invalid project.")
        return redirect(url_for("projects"))
    session["project"] = project_query

    page = int(page)
    if page <= 0:
        flash("invalid page number")
        return redirect(project + "/jobs/1")

    count = peewee.SelectQuery(Job).count()

    query = (Job
             .select()
             .where(Job.project == project_query)
             .order_by(-Job.started.is_null(), -Job.started)
             .paginate(page, JOBSPERPAGE))

    entries = []
    for job in query:
        span = job.ended
        if job.started is not None:
            if job.ended is not None:
                span = job.ended - job.started

        entries.append(dict(id=job.id, status=job.get_status(), name=job.name,
                            start=job.started, end=job.ended, span=span))

    more = count > (page * JOBSPERPAGE)
    less = page > 1
    pagedata = dict(id=page, more=more, less=less)

    return render_template("/jobs.html", entries=entries, page=pagedata)

@app.route("/jobs/id/<int:job_id>")
def job_view(job_id):
    """ Shows information about a specific job. """
    g.selected_tab = "jobs"

    job = Job.get(Job.id == job_id)
    if job is None:
        flash("Invalid job id", category="error")
        return jobs_index_2()

    log = ""
    try:
        if job.log_path is None:
            log = None
        elif os.path.isfile(job.log_path):
            log = open(job.log_path, "r").readlines()
        else:
            flash("could not find file " + job.log_path)
    except Exception as excep:
        flash("failed to to open log file " + job.log_path)
        if app.config["DEBUG"]:
            flash(excep)

    session["project"] = job.project
    data = dict(id=job.id, status=job.get_status(), name=job.name,
                start=job.started, end=job.ended)

    return render_template("job.html", data=data, log=log)

@app.route("/<project>/jobs/create")
def job_create(project):
    """ view for creating a new job """
    g.selected_tab = "jobs"

    project_query = ensure_project(project)
    if project_query is None:
        redirect(url_for("projects"))

    # pylint: disable=R0204
    #disabling warning about redefining settings. I do this on purpose
    buildfilepath = os.path.join(project_query.path, "build.abc")
    settings = abcfile.parse(buildfilepath)
    if settings is None:
        flash("Could not parse settings file, prehaps the file path ({}) is wrong"
              .format(buildfilepath), category="error")
        settings = dict()
    else:
        settings = settings.m_nodes
    # pylint: enable=R0204

    return render_template("newjob.html", buildconf=settings)

@app.route("/<project>/jobs/create/new", methods=["POST"])
def job_new(project):
    """ Handles the post request for the new job schedule """
    g.selected_tab = "jobs"

    project_query = ensure_project(project)
    if project_query is None:
        redirect(url_for("projects"))

    name = request.form.get("jobname")
    config = request.form.get("buildconfigurations")
    starttimestr = request.form.get("starttime")
    if len(name) < 3:
        flash("Invalid name", category="error")
        return redirect(url_for("job_create", project=project))
    if config is None:
        flash("ERROR: config", category="error")
        return redirect(url_for("job_create", project=project))
    else:
        buildfilepath = os.path.join(project_query.path, "build.abc")
        settings = abcfile.parse(buildfilepath)[config]
        if settings is None:
            flash("ERROR: invalid config", category="error")
            return redirect(url_for("job_create", project=project))
    if starttimestr is None:
        flash("ERROR: start time not set", category="error")
        return redirect(url_for("job_create", project=project))
    else:
        try:
            jobtime = parse_time(starttimestr)
        except ValueError:
            flash("Time format is wrong", category="error")
            return redirect(url_for("job_create", project=project))

    newjob = Job.create(project=project_query, name=name, started=jobtime,
                        description="was build from the dashboard")
    newjob.name = newjob.name + ".{0:0=3d}".format(newjob.id)
    newjob.save()

    arguments = {"job": newjob, "project": project_query, "config": settings}

    schedule.add_job(build, "date", run_date=jobtime, kwargs=arguments, misfire_grace_time=None)

    flash("Sucess", category="Success")
    return redirect(url_for("job_view", job_id=newjob.id))

def parse_time(timestring):
    """ Parses the string and returns a datetime object """
    result = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return result.strptime(timestring, "%Y-%m-%dT%H:%M:%S.%fZ")

def ensure_project(project):
    """ Ensures we are on a project, or else kicks back to the project page """
    # Check if project argument is correct
    project_query = Project.select().where(Project.slug == project).first()
    if project_query is None:
        flash("Invalid project.")
    session["project"] = project_query
    return project_query
