""" Simple python script to start the website. """

import sys
from Anemone import app

DEBUG = False

if __name__ == '__main__':
    BAD_ARGS = False
    # handle args
    for arg in sys.argv[1:]:
        if str(arg) == "--debug" or str(arg) == "-d":
            DEBUG = True
        else:
            print("ERROR: did not understand '{}'".format(arg))
            BAD_ARGS = True

    if not BAD_ARGS:
        # run program
        app.run(debug=DEBUG)
