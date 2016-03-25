""" Jobs and job view """

from datetime import datetime
from flask import g, render_template, flash
from Anemone import app

@app.route('/jobs')
@app.route('/jobs/')
def jobs_index():
    """ shows the index if no jobs given """
    return jobs(0)

@app.route('/jobs/<int:page>')
def jobs(page):
    """ for when no job id was given """
    if page < 0:
        flash("invalid page number")
        page = 0

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
    return render_template("/jobs.html", entries=entries)

@app.route('/jobs/id/<int:job_id>')
def job(job_id):
    """ Shows information about a specific job """
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
    pass
