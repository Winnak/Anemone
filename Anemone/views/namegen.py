""" view functions for name generation views """

from flask import render_template
from Anemone import app

@app.route("/namegen")
def namegen_data():
    """ returns a view for a list of random words """
    return render_template("namegen.html")
