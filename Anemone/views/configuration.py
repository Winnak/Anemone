""" view for configuration """

from flask import render_template, g
from Anemone import app

@app.route("/configuration")
@app.route("/configuration/")
def configuration_view():
    """ Displays the view for configuration """
    g.selected_tab = "configuration"
    return render_template("configure.html")
