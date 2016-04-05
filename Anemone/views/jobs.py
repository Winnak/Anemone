""" Jobs and job view """

from flask import g, render_template, flash, redirect
import peewee
from Anemone import app
from Anemone.models import Job

JOBSPERPAGE = 30

@app.route('/jobs')
@app.route('/jobs/')
def jobs_index():
    """ shows the index if no jobs given """
    return jobs(1)

@app.route('/jobs/<page>')
def jobs(page):
    """ for when no job id was given """
    g.selected_tab = "jobs"

    page = int(page) # would have set the app.route to do this, but it expects a uint

    if page <= 0:
        flash("invalid page number")
        return redirect("/jobs/1")

    count = peewee.SelectQuery(Job).count()

    query = (Job
             .select()
             .order_by(-Job.started.is_null(), -Job.started)
             .paginate(page, JOBSPERPAGE))

    entries = []
    for job in query:
        span = job.ended
        if job.started is not None:
            if job.ended is not None:
                span = job.ended - job.started

        entries.append(dict(id=job.id, status=job.status, name=job.name,
                            start=job.started, end=job.ended, span=span))

    more = count > (page) * JOBSPERPAGE
    less = page > 1
    pagedata = dict(id=page, more=more, less=less)

    return render_template("/jobs.html", entries=entries, page=pagedata)

@app.route('/jobs/id/<int:job_id>')
def job_view(job_id):
    """ Shows information about a specific job """
    g.selected_tab = "jobs"

    job = Job.get(Job.id == job_id)
    if job is None:
        flash("Invalid job id", category='error')
        return jobs_index()

    data = dict(id=job.id, status=job.status, name=job.name,
                start=job.started, end=job.ended)

    return render_template('job.html', data=data)

# @app.route('/jobs/new')
# def new_job():
#     """ view for creating a new job """
#
#     g.selected_tab = "jobs"
