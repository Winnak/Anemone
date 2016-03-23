""" represnets all the views of the projects """

from datetime import datetime
from flask import request, session, g, redirect, url_for, abort, \
    render_template, flash
from Anemone import app

@app.route("/")
def home():
    """ Index of the homepage """
    query = 'SELECT status, name, started, ended FROM jobs \
             ORDER BY id DESC LIMIT 30'
    cur = g.database.execute(query)
    entries = []
    for row in cur.fetchall():
        end = row[3]
        if row[2] is not None:
            if row[3] is not None:
                buildfrom = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
                buildto = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
                end = str(buildto - buildfrom)

        entries.append(dict(STATUS=row[0], NAME=row[1], START=row[2], END=row[3], SPAN=end))

    return render_template('dashboard.html', entries=entries)


@app.route('/add', methods=['POST'])
def add_entry():
    """ Add entry page """
    if not session.get('logged_in'):
        abort(401)
    g.database.execute('insert into entries (title, text) values (?, ?)',
                       [request.form['title'], request.form['text']])
    g.database.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('home'))


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
