""" represnets all the views of the projects """

from flask import request, session, g, redirect, url_for, abort, \
    render_template, flash
from Anemone import app

@app.route("/")
def home():
    """ Index of the homepage """
    # cur = g.database.execute('select title, text from entries order by id desc')
    # entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    # return render_template('show_entries.html', entries=entries)
    return render_template('dashboard.html')


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
