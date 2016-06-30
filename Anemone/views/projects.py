""" View for overview of projects """

import datetime
from flask import render_template, session, request, url_for, redirect, flash
from Anemone import app
from Anemone.models import Project, Job

@app.route("/")
@app.route("/projects")
@app.route("/projects/")
def projects():
    """ View for projects """
    session.pop("project", None)
    entries = []
    for pro in Project.select():
        status = (Job.select()
                  .where((Job.project == pro) & (Job.result > 0))
                  .order_by(Job.started.desc())
                  .first())

        latest = (Job.select()
                  .where(Job.project == pro)
                  .order_by(Job.started.desc())
                  .first())

        entries.append(dict(name=pro.name, slug=pro.slug,
                            description=pro.description,
                            status=status, latest=latest))


    return render_template("projects.html", entries=entries)

@app.route("/projects/remove/<project>", methods=["POST"])
def projects_remove(project):
    """ Delete a project from Anemone """
    if session["logged_in"]:
        proj = Project.get(Project.slug == project)
        if proj is None:
            flash("no such project {}".format(project))
        else:
            name = proj.name
            removed = proj.delete_instance()
            flash("Succesfully removed {} project ({})".format(removed, name))
    else:
        flash("This acition requires you to be logged in")
    return redirect(url_for("projects"))


@app.route("/projects/add", methods=["GET", "POST"])
@app.route("/projects/add/", methods=["GET", "POST"])
def projects_add():
    """ View for projects. """
    error = None
    if request.method == "POST":
        if not session["logged_in"]:
            return redirect(url_for("projects"))

        name = request.form["name"]
        slug = request.form["slug"]

        if ((name is None) or (slug is None)) or ((name is "") or (slug is "")):
            error = "Project Name and Slug required."
        else:
            try:
                Project.create(name=name, slug=slug,
                               description=request.form["description"],
                               path=request.form["projectpath"],
                               output=request.form["output"],
                               created_at=datetime.datetime.now()).save()
                flash("Succesfully created {}".format(name))
                return redirect(url_for("projects"))
            except Exception as excep:
                error = str(excep)

    return render_template("projects-new.html", error=error)

@app.route("/<project>/health.csv", defaults={"limit": 30})
@app.route("/<project>/health/<int:limit>.csv")
def project_health(project, limit):
    """ Gets the project health in csv format """
    proj = Project.get(Project.slug == project)
    jobs = (Job
            .select()
            .where(Job.project == proj)
            .order_by(-Job.started)
            .limit(limit))

    health = {
        "success":{"count":0, "color":"#5CB85C"},
        "warning":{"count":0, "color":"#F0AD4E"},
        "error":{"count":0, "color":"#D9534F"}
    }

    for job in jobs:
        status = 0
        if job.started is not None:
            if job.ended is not None:
                status = 1 #TODO: repport if errors
        if status is 1:
            health["success"]["count"] += 1
        elif status is 2:
            health["warning"]["count"] += 1
        elif status is 3:
            health["error"]["count"] += 1
    return render_template("project-health-data.csv", health=health)
