""" Represnets all the views of the projects """

from flask import request, session, redirect, url_for, render_template, flash, g
from Anemone import app


#TODO: make semi-seperate login screen for non-active project

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Login page. """
    g.selected_tab = "login"

    error = None
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"]:
            error = "Invalid login information"
        elif request.form["password"] != app.config["PASSWORD"]:
            error = "Invalid login information"
        else:
            session["logged_in"] = True
            flash("You were logged in")
            if session.get("project"):
                return redirect(url_for("home"))
            return redirect(url_for("projects"))

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    """ Logging out redirect. """
    session.pop("logged_in", None)
    flash("You were logged out")
    return redirect(url_for("projects"))
