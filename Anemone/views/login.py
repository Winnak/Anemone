""" represnets all the views of the projects """

from flask import request, session, redirect, url_for, render_template, flash
from Anemone import app

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ login page """
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    """ logging out redirect """
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('home'))
