""" Jobs and job view """

from datetime import datetime
from flask import g, render_template, flash, redirect
from Anemone import app

JOBSPERPAGE = 30

@app.route('/jobs')
@app.route('/jobs/')
def jobs_index():
    """ shows the index if no jobs given """
    return jobs(0)

@app.route('/jobs/<page>')
def jobs(page):
    """ for when no job id was given """
    g.selected_tab = "jobs"

    page = int(page) # would have set the app.route to do this, but it expects a uint

    if page < 0:
        flash("invalid page number")
        redirect("/jobs/0")

    count = g.database.execute("SELECT Count(*) FROM jobs").fetchone()[0]
    projects = g.database.execute("SELECT id, name FROM projects").fetchall()

    def whereis(item):
        """ find item in collection that matches an item """
        for row in projects:
            if row[0] == item:
                return row

    query = 'SELECT id, project, status, name, started, ended FROM jobs \
             ORDER BY (CASE WHEN started IS NULL THEN 1 ELSE 0 END) DESC, \
             started DESC LIMIT {0}, {1}'.format(page * JOBSPERPAGE, JOBSPERPAGE)

    cur = g.database.execute(query)
    entries = []
    for row in cur.fetchall():
        end = row[5]
        if row[4] is not None:
            if row[5] is not None:
                buildfrom = datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')
                buildto = datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S')
                end = str(buildto - buildfrom)

        project = whereis(row[1])[1]
        entries.append(dict(ID=row[0], PROJECT=project, STATUS=row[2],
                            NAME=row[3], START=row[4], END=row[5], SPAN=end))

    more = count > (page + 1) * JOBSPERPAGE
    less = page > 0
    pagedata = dict(ID=page, MORE=more, LESS=less)

    cur.close()
    return render_template("/jobs.html", entries=entries, page=pagedata)

@app.route('/jobs/id/<int:job_id>')
def job(job_id):
    """ Shows information about a specific job """

    g.selected_tab = "jobs"

    query = 'SELECT id,status,name,started,ended FROM jobs \
             WHERE id=' + str(job_id)
    entries = g.database.execute(query).fetchall()

    if len(entries) != 1:
        flash("Invalid job id", category='error')
        return jobs_index()

    row = entries[0]

    if row is None:
        flash("Invalid job id", category='error')
        return jobs_index()

    data = dict(ID=row[0], STATUS=row[1], NAME=row[2], START=row[3], END=row[4])

    return render_template('job.html', data=data)

@app.route('/jobs/new')
def new_job():
    """ view for creating a new job """

    g.selected_tab = "jobs"
