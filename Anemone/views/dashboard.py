""" dashboard view """

from datetime import datetime
from flask import render_template, g
from Anemone import app

@app.route("/")
def home():
    """ Index of the homepage """
    g.selected_tab = "dashboard"

    query = 'SELECT id, status, name, started, ended FROM jobs \
             ORDER BY (CASE WHEN started IS NULL THEN 1 ELSE 0 END) DESC, \
             started DESC LIMIT 10'

    cur = g.database.execute(query)
    entries = []
    for row in cur.fetchall():
        end = row[4]
        if row[3] is not None:
            if row[4] is not None:
                buildfrom = datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')
                buildto = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')
                end = str(buildto - buildfrom)

        entries.append(dict(ID=row[0], STATUS=row[1], NAME=row[2], START=row[3],
                            END=row[4], SPAN=end))
    cur.close()
    return render_template('dashboard.html', entries=entries)
