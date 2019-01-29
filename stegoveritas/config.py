import os.path,os

# Get our script dir
SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

# Get the current dir
PWD = os.getcwd()

TEMPFILE = os.path.join(SCRIPTDIR,"stegoveritas.temp")
# TODO: Use python to make this dynamic
RESULTSDIR = os.path.join(PWD,"results")

