""" dashboard view """

from flask import render_template, g
from Anemone import app
from Anemone.models import Job

@app.route("/dashboard-temp") #todo filter by project
def dashboard():
    """ Index of the homepage """
    g.selected_tab = "dashboard"

    # query = 'SELECT id, project, status, name, started, ended FROM jobs \
    #          ORDER BY (CASE WHEN started IS NULL THEN 1 ELSE 0 END) DESC, \
    #          started DESC LIMIT 10'
    entries = []
    for job in Job.select().order_by(-Job.started.is_null(), -Job.started).limit(10):
        span = job.ended
        if job.started is not None:
            if job.ended is not None:
                span = job.ended - job.started

        entries.append(dict(id=job.id, status=job.status, name=job.name,
                            start=job.started, end=job.ended, span=span))

    return render_template('dashboard.html', entries=entries)
