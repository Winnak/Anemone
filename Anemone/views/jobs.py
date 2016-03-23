""" jobs view """

from flask import g, redirect, render_template, flash
from Anemone import app

@app.route('/jobs')
def invalid_job():
    """ for when no job id was given """
    flash("Invalid job ID")
    return redirect("/")

@app.route('/jobs/<int:job_id>')
def jobs(job_id=None):
    """ Shows information about a specific job """
    if job_id is None:
        return invalid_job()

    query = 'SELECT id,status,name,started,ended FROM jobs \
             WHERE id=' + str(job_id)
    entries = g.database.execute(query).fetchall()

    if len(entries) != 1:
        return invalid_job()

    row = entries[0]

    if row is None:
        return invalid_job()
    data = dict(ID=[0], STATUS=row[1], NAME=row[2], START=row[3], END=row[4])

    return render_template('jobs.html', data=data)
