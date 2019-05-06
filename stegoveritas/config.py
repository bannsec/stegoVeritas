import os.path,os

# Get our script dir
SCRIPTDIR = os.path.dirname(os.path.realpath(__file__))

# Get the current dir
PWD = os.getcwd()

TEMPFILE = os.path.join(SCRIPTDIR,"stegoveritas.temp")

RESULTSDIR = os.path.join(PWD,"results")

# TODO: Use python to make this dynamic                                                                                                        ✔  7513  08:12:12

a = input("ENTER ABSOLUTE OR RELATIVE PATH: ")
try:
    a = str(a)
except:
    print("DEBUG")
    quit()
try:
    PWD = os.chdir(a)
except:
    print("DEBUG")
    quit()

