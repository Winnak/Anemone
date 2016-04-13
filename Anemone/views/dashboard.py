""" dashboard view """

from flask import render_template, g, request, redirect, url_for, flash, session
from Anemone import app
from Anemone.models import Job, Project
import Anemone.views
import Anemone.buildslave

@app.route("/dashboard")
def home():
    """ Uses dashboard with the currently active project """
    if session.get("project", None) is None:
        return redirect(url_for("projects"))
    return dashboard(session["project"]["slug"])

@app.route("/<project>")
@app.route("/<project>/")
@app.route("/<project>/dashboard")
@app.route("/<project>/dashboard/")
def dashboard(project):
    """ Index of the homepage """
    g.selected_tab = "dashboard"

    # Check if project argument is correct
    project_query = Project.select().where(Project.slug == project).first()
    if project_query is None:
        flash("invalid project")
        return redirect(url_for("projects"))
    session["project"] = project_query

    settings = Anemone.abcfile.parse(project_query.filepath)

    query = (Job
             .select()
             .where(Job.project == project_query)
             .order_by(-Job.started.is_null(), -Job.started)
             .limit(10))

    entries = []
    for job in query:
        span = job.ended
        if job.started is not None:
            if job.ended is not None:
                span = job.ended - job.started

        entries.append(dict(id=job.id, status=job.status, name=job.name,
                            start=job.started, end=job.ended, span=span))

    return render_template('dashboard.html', entries=entries, buildconf=settings.m_nodes)

@app.route("/test-build/<project>", methods=["POST"])
def build(project): #TODO: create better build started stuff
    """ temp: builds test project """
    project_query = Project.select().where(Project.slug == project).first()
    if project_query is None:
        flash("invalid project")
        return redirect(url_for("projects"))
    session["project"] = project_query

    settings = Anemone.abcfile.parse(project_query.filepath)
    if settings is None:
        flash("project was missing a build file, please configure")

    # Check if project argument is correct
    if request.method == "POST":
        Anemone.buildslave.build(project_query, settings[request.form.get("config", None)])
    return redirect(url_for("home"))
