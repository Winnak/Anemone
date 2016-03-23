""" dashboard view """

from datetime import datetime
from flask import render_template, g
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
    cur.close()
    return render_template('dashboard.html', entries=entries)
