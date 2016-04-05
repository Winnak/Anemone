""" a build slave for the program """

import os.path
import datetime
import subprocess
from flask import flash

LOGS_TEMP_DIR = os.path.join("Anemone", "tmp", "logs")

# Anemone needs its own settings. It needs to know the following:
# Where is the unity executable?
# Where is the unity build log?

# The project needs its own settings. It needs to know the following:
# what platforms are we building to (unittest is now a platform)
# what is out pre build steps
# what is our post build steps
# where do we put the project afterwards
# what do we rename the project to afterwards
# what scenes are we building
# is it a development build
# unity specific settings etc.

# C:\Users\Erik\AppData\Local\Unity\Editor\Editor.log
# yyyy-MM-dd_HH\\hmm\\mss\\s

def build():
    """ builds the project """
    # TODO: combine with project slug and job id (thereby dropping the datetime)
    os.makedirs(LOGS_TEMP_DIR, exist_ok=True)
    logpath = os.path.join(LOGS_TEMP_DIR,
                           "TestProject.%Y-%m-%d_%Hh%Mm%Ss.log")

    # Win "C:\Program Files\Unity\Editor\Unity.exe"
    # Mac /Applications/Unity/Unity.app/Contents/MacOS/Unity
    cmd = [r"C:\Program Files\Unity\Editor\Unity.exe", "-quit", "-batchmode",
           "-executeMethod", "Anemone.Build.Windows",
           "-logFile", str(datetime.datetime.now().strftime(logpath)),
           "-projectPath", r"C:\Projects\Unity\BuildServerTest"]

    process = subprocess.Popen(cmd)

    #pylint: disable=E1101
    # this var does in fact exists
    flash(process.args)
    #pylint: enable=E1101

    flash(process.returncode)
