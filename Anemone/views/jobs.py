""" Jobs and job view. """

from flask import g, render_template, flash, redirect, url_for, session
import peewee
from Anemone import app
from Anemone.models import Job, Project

JOBSPERPAGE = 30

@app.route("/jobs")
@app.route("/jobs/")
def jobs_index_2():
    """ Shows the index if no jobs or project given. """
    return jobs_index(session["project"])

@app.route("/<project>/jobs")
@app.route("/<project>/jobs/")
def jobs_index(project):
    """ Shows the index if no jobs given. """
    return jobs(project, 1)

@app.route("/<project>/jobs/<page>")
def jobs(project, page):
    """ For when no job id was given. """
    g.selected_tab = "jobs"

    # Check if project argument is correct
    project_query = Project.select().where(Project.slug == project).first()
    if project_query is None:
        flash("Invalid project.")
        return redirect(url_for("projects"))
    session['project'] = project_query

    page = int(page)
    if page <= 0:
        flash("invalid page number")
        return redirect(project + "/jobs/1")

    count = peewee.SelectQuery(Job).count()

    query = (Job
             .select()
             .where(Job.project == project_query)
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
    """ Shows information about a specific job. """
    g.selected_tab = "jobs"

    job = Job.get(Job.id == job_id)
    if job is None:
        flash("Invalid job id", category='error')
        return jobs_index_2()

    session["project"] = job.project
    data = dict(id=job.id, status=job.status, name=job.name,
                start=job.started, end=job.ended)

    return render_template('job.html', data=data)
