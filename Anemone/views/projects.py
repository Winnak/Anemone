""" view for overview of projects """

import datetime
from flask import render_template, session, request, url_for, redirect, flash
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
    """ soft delete a project from Anemone """
    if session["logged_in"]:
        proj = Project.get(Project.slug == project)
        if proj is None:
            flash("no such project {}".format(project))
        else:
            removed = proj.delete_instance()
            flash("Succesfully removed {} project ({})".format(removed, proj.name))
    else:
        flash("This acition requires you to be logged in")
    return redirect(url_for("projects"))

# pylint: disable=W0703
#"Catching too general exception", because so much can go wrong here
@app.route("/projects/add", methods=["GET", "POST"])
@app.route("/projects/add/", methods=["GET", "POST"])
def projects_add(): #TODO: Validate filepath
    """ view for projects """
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
                               filepath=request.form["filepath"],
                               created_at=datetime.datetime.now()).save()
                flash("Succesfully created {}".format(name))
                return redirect(url_for("projects"))
            except Exception as exception:
                error = str(exception)

    return render_template("projects-new.html", error=error)
# pylint: enable=W0703
