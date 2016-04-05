""" view for overview of projects """

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


# pylint: disable=W0703
#"Catching too general exception", because so much can go wrong here
@app.route("/projects/add", methods=["GET", "POST"])
@app.route("/projects/add/", methods=["GET", "POST"])
def projects_add(): #TODO: Validate filepath
    """ view for projects """
    error = None
    if request.method == "POST":
        if not session['logged_in']:
            return redirect(url_for("projects"))

        name = request.form["name"]
        slug = request.form["slug"]

        if ((name is None) or (slug is None)) or ((name is "") or (slug is "")):
            error = "Project Name and Slug required."
        else:
            try:
                Project.create(name=name, slug=slug,
                               description=request.form["description"],
                               filepath=request.form["filepath"]).save()
                flash("Succesfully created {}".format(name))
                return redirect(url_for("projects"))
            except Exception as exception:
                error = str(exception)

    return render_template("projects-new.html", error=error)
# pylint: enable=W0703
