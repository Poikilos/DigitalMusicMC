#!/usr/bin/env python
verbose = False

def getVerbose():
    return verbose

def setVerbose(setVerbose):
    global verbose
    if setVerbose is True:
        verbose = True
    elif setVerbose is False:
        verbose = False
    else:
        raise ValueError("setVerbose must be True or False.")
