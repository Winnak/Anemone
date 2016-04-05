""" View for configuration """

from flask import render_template, g, redirect, session, flash, url_for
from Anemone import app
from Anemone.models import Project

@app.route("/<project>/configuration")
@app.route("/<project>/configuration/")
def configuration_view(project):
    """ Displays the view for configuration """
    # if session.get('logged_in', False) is False: #bad idea, they need to see
    #     return redirect("/")

    # Check if project argument is correct
    project_query = Project.select().where(Project.slug == project).first()
    if project_query is None:
        flash("invalid project")
        return redirect(url_for("projects"))
    session["project"] = project_query

    # querykeys = 'SELECT publicssh FROM configuration'
    # publicssh = g.database.execute(querykeys).fetchone()[0]

    g.selected_tab = "configuration"
    return render_template("configure.html", key="todo")
