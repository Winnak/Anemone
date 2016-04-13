""" View for configuration """

from flask import render_template, g, redirect, session, flash, url_for, request
from Anemone import app
from Anemone.models import Project
import Anemone.abcfile

@app.route("/<project>/configuration", methods=['GET', 'POST'])
@app.route("/<project>/configuration/", methods=['GET', 'POST'])
def configuration_view(project):
    """ Displays the view for configuration """
    # Check if project argument is correct
    print("agdagdgds")
    project_query = Project.select().where(Project.slug == project).first()
    if project_query is None:
        flash("invalid project")
        return redirect(url_for("projects"))
    session["project"] = project_query

    g.selected_tab = "configuration"

    settings = None
    if request.method == "GET":
        settings = Anemone.abcfile.parse(project_query.filepath)
    elif request.method == "POST":
        configuration_post(project_query, request)

    return render_template("configure.html", ssh=app.config["SSH_PUBLIC"],
                           build=settings, unity=app.config["UNITY_PATH"])

def configuration_post(project, req):
    """ The post part of the configuration view """
    error = ""
    print(error)
    if req.form.get("name", None) is None:
        flash("Project name must be something")
        error += "name "
    if req.form.get("slug", None) is None: #TODO: Check if unique
        flash("Project slug must be something (should be automaticly generated)")
        error += "slug "
    if req.form.get("filepath", None) is None:
        flash("File path must be something in order to be able to build the project.")
    if req.form.get("output", None) is None:
        flash("Project Output folder must be something")
        error += "output "
    if error is not "":
        print(error)
        return
    try:
        project.name = req.form["name"]
        project.slug = req.form["slug"]
        project.description = req.form["description"]
        project.filepath = req.form["filepath"]
        project.output = req.form["output"]
        project.save()
    except Exception as excep:
        flash(str(excep))
        raise excep
