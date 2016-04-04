""" dashboard view """

from datetime import datetime
from flask import render_template, g
from Anemone import app

@app.route("/dashboard-temp")
def dashboard():
    """ Index of the homepage """
    g.selected_tab = "dashboard"

    queryprojects = 'SELECT id, name FROM projects'
    projects = g.database.execute(queryprojects).fetchall()

    def whereis(item):
        """ find item in collection that matches an item """
        for row in projects:
            if row[0] == item:
                return row

    query = 'SELECT id, project, status, name, started, ended FROM jobs \
             ORDER BY (CASE WHEN started IS NULL THEN 1 ELSE 0 END) DESC, \
             started DESC LIMIT 10'

    cur = g.database.execute(query)
    entries = []
    for row in cur.fetchall():
        end = row[5]
        if row[4] is not None:
            if row[5] is not None:
                buildfrom = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')
                buildto = datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S')
                end = str(buildto - buildfrom)

        project = whereis(row[1])[1] # get project name from project ID
        entries.append(dict(ID=row[0], PROJECT=project, STATUS=row[2], NAME=row[3], START=row[4],
                            END=row[5], SPAN=end))
    cur.close()
    return render_template('dashboard.html', entries=entries)
