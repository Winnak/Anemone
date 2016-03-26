""" View for configuration """

from flask import render_template, g, redirect, session
from Anemone import app

@app.route("/configuration")
@app.route("/configuration/")
def configuration_view():
    """ Displays the view for configuration """

    # querykeys = 'SELECT publicssh FROM configuration'
    # publicssh = g.database.execute(querykeys).fetchone()[0]

    if session.get('logged_in', False) is False:
        return redirect("/")

    g.selected_tab = "configuration"
    return render_template("configure.html", key="todo")
