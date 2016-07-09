""" View for configuration. """

from os.path import join as path
from flask import render_template, g, redirect, session, flash, url_for, request
from Anemone import app, schedule
from Anemone.models import Project
import Anemone.abcfile

@app.route("/<project>/configuration", methods=["GET", "POST"])
def configuration_view(project):
    """ Displays the view for configuration. """
    project_query = Project.select().where(Project.slug == project).first()
    if project_query is None:
        flash("invalid project")
        return redirect(url_for("projects"))
    session["project"] = project_query

    g.selected_tab = "configuration"

    settings = None
    if request.method == "GET":
        settings = Anemone.abcfile.parse(path(project_query.path, "build.abc"))
    elif request.method == "POST":
        configuration_post(project_query, request)

    return render_template("configure.html", ssh=open(app.config["SSH_PUBLIC"]).readline(),
                           build=settings, unity=app.config["UNITY_PATH"])

#pylint: disable=R0912
# disabling "too many branches", which is true, but this looks nice currently.
def configuration_post(project, req):
    """ The post part of the configuration view. """
    error = ""
    if req.form.get("name", None) is None:
        flash("Project name must be something", category="error")
        error += "name "
    else:
        project.name = req.form["name"]

    if req.form.get("slug", None) is None: #TODO: Check if unique
        flash("Project slug must be something (should be automaticly generated)", category="error")
        error += "slug "
    else:
        project.slug = req.form["slug"]

    if req.form.get("path", None) is None:
        flash("Folder path must be something with a  in order to be able to build the project.")
        error += "output "
    else:
        project.path = req.form["path"]

    if req.form.get("output", None) is None:
        flash("Project Output folder must be something", category="error")
        error += "path "
    else:
        project.output = req.form["output"]

    if req.form.get("description", None) is not None:
        if len(req.form["description"]) > 1:
            project.description = req.form["description"]

    if req.form.get("scheduleinterval", None) is None:
        schedule.pause_job("building_" + str(project.id))
    elif isinstance(req.form["scheduleinterval"]):
        schedule.modify_job("building_" + str(project.id), hours=req.form["scheduleinterval"])
        schedule.resume_job("building_" + str(project.id))

    if error is not "":
        print(error)

    project.save()
#pylint: enable=R0912
