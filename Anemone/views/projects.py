""" view for overview of projects """

from flask import render_template
from Anemone import app

@app.route("/")
def home():
    return render_template('projects.html')