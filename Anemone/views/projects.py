""" view for overview of projects """

from flask import render_template, session
from Anemone import app
from Anemone.models import Project, Job

@app.route("/")
@app.route("/projects")
@app.route("/projects/")
def projects():
    """ view for projects """
    session.pop("project", None)
    entries = []
    for pro in Project.select():
        status = (Job.select()
                  .where(Job.project == pro)
                  .order_by(Job.started.desc())
                  .get())

        latest = (Job.select()
                  .where(Job.project == pro and ((Job.status == 1) | (Job.status == 2)))
                  .order_by(Job.started.desc())
                  .get())

        entries.append(dict(name=pro.name, slug=pro.slug,
                            description=pro.description,
                            status=status, latest=latest))


    return render_template("projects.html", entries=entries)


@app.route("/projects/add", methods=["GET", "POST"])
@app.route("/projects/add/", methods=["GET", "POST"])
def projects_add():
    """ view for projects """
    return render_template("projects.html")
