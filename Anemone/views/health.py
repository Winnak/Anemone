""" View for generating the csv file """

from Anemone import app
from Anemone.models import Job, Project

@app.route("/<project>/health", defaults={"limit": 30})
@app.route("/<project>/health/<int:limit>")
def project_health(project, limit):
    """ Gets the project health in csv format """
    proj = Project.get(Project.slug == project)
    query = (Job.select()
             .where(Job.project == proj)
             .order_by(-Job.started)
             .limit(limit))

    health = dict(success=0, warning=0, error=0)
    for job in query:
        status = job.get_status()
        if status is 1:
            health["success"] += 1
        elif status is 2:
            health["warning"] += 1
        elif status is 3:
            health["error"] += 1
    return ("category,count,color" +
            "\nSuccess,{},#5CB85C\nWarning,{},#F0AD4E\nError,{},#D9534F"
            .format(health["success"], health["warning"], health["error"]))
