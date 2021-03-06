""" Create Database
script to create a new database

Available commands include:
    --force, -f     force creation of database, even if it means deleting old database
    --tmpdata       Create temporary data into the database
"""

import os
import sys
from datetime import datetime, timedelta
from Anemone.models import Project, Job, DATABASE
from Anemone import app

FORCE = False
GENERATE_DATA = False
PATH = app.config["DATABASE_PATH"]
TEMP_PATH = app.config["TEMP_PATH"]

def main():
    """ Main entry point. """
    if FORCE:
        os.makedirs(TEMP_PATH, exist_ok=True)
        if os.path.isfile(PATH):
            print("removing old database. RIP data.")
            os.remove(PATH)

    if os.path.isfile(PATH):
        print(("database already exists, please run this with the argument"
               " --force to remove the database and create a new.\n"
               " Warning: This will remove all Anemone's data."))
        return

    DATABASE.connect()
    DATABASE.create_tables([Project, Job])

    if GENERATE_DATA:
        print("Generating temporary data")
        description = ("This is just a test project, hence the name. It mainly"
                       " here to check if features work, while Anemone is under"
                       " development.")

        project = Project.create(name="TestProject", slug="testproject",
                                 path="", description=description,
                                 output="/output", schedule_interval=2,
                                 created_at=datetime(2016, 1, 6, 8, 23, 19))
        project.save()

        Job.create(project=project, active=False, result=1,
                   name="ClearChimpanzee-001", description="",
                   started=datetime(2016, 1, 8, 8, 23, 19),
                   ended=datetime(2016, 1, 8, 9, 24, 34), log="success").save()
        Job.create(project=project, active=False, result=2,
                   name="MissionHorse-002", description="",
                   started=datetime(2016, 1, 8, 9, 45, 34),
                   ended=datetime(2016, 1, 8, 10, 0, 0), log="warnings").save()
        Job.create(project=project, active=False, result=3,
                   name="MiddlePorcupine-003", description="",
                   started=datetime(2016, 1, 8, 10, 0, 0),
                   ended=datetime(2016, 1, 8, 10, 10, 0), log="error").save()
        Job.create(project=project, active=True, result=0,
                   name="OpeningBadger-004", description="",
                   started=datetime.now(), log="building ...").save()
        Job.create(project=project, active=False, result=0,
                   name="ClassicVixen-005", description="",
                   started=datetime.now() + timedelta(days=2)).save()
        Job.create(project=project, active=False, result=0,
                   name="VariousMoose-006", description="").save()

if __name__ == "__main__":
    BAD_ARGS = False
    # handle args
    for arg in sys.argv[1:]:
        if str(arg) == "--force" or str(arg) == "-f":
            FORCE = True
        elif str(arg) == "--tmpdata":
            GENERATE_DATA = True
        else:
            print("ERROR: did not understand '{}'".format(arg))
            BAD_ARGS = True

    if not BAD_ARGS:
        # run program
        main()
