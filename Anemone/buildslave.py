""" a build slave for the program """

import subprocess
from flask import flash

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

def build():
    """ builds the project """
    # Win "C:\Program Files\Unity\Editor\Unity.exe"
    # Mac /Applications/Unity/Unity.app/Contents/MacOS/Unity
    cmd = [r"C:\Program Files\Unity\Editor\Unity.exe", "-quit", "-batchmode",
           "-executeMethod", "Anemone.Build.Windows",
           "-projectPath", r"C:\Projects\Unity\BuildServerTest"]

    process = subprocess.Popen(cmd)

    #pylint: disable=E1101
    # this var does in fact exists
    flash(process.args)
    #pylint: enable=E1101

    flash(process.returncode)
