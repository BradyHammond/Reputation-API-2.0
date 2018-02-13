# ================================================== #
#                      HELPING                       #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 01/21/2017                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

from __future__ import generator_stop

from ioflo.aid import getConsole
from ..db import dbing

import os
import shutil
import tempfile

try:
    import ujson as json
except ImportError:
    import json

try:
    import msgpack
except ImportError:
    pass

# ================================================== #
#                 CONSTANTS & GLOBALS                #
# ================================================== #

console = getConsole()

# ================================================== #
#                     FUNCTIONS                      #
# ================================================== #

def setupTmpBaseDir(baseDirPath=""):
    if not baseDirPath:
        baseDirPath = tempfile.mkdtemp(prefix="reputation", suffix="test", dir="/tmp")

    baseDirPath = os.path.abspath(os.path.expanduser(baseDirPath))
    return baseDirPath

# ================================================== #

def cleanupTmpBaseDir(baseDirPath):
    if os.path.exists(baseDirPath):
        while baseDirPath.startswith("/tmp/reputation"):
            if baseDirPath.endswith("test"):
                shutil.rmtree(baseDirPath)
                break
            baseDirPath = os.path.dirname(baseDirPath)

# ================================================== #

def cleanupBaseDir(baseDirPath):
    if os.path.exists(baseDirPath):
        shutil.rmtree(baseDirPath)

# ================================================== #

def getAll(reputee, entries):
    reach_list = []
    clarity_list = []

    for entry in entries:
        if entry['reputee'] == reputee:
            if entry['repute']['feature'] == "reach":
                reach_list.append(entry['repute']['value'])
            elif entry['repute']['feature'] == "clarity":
                clarity_list.append(entry['repute']['value'])

    if len(reach_list) == 0 and len(clarity_list) == 0:
        return False

    reach = getReach(reach_list)
    clarity = getClarity(clarity_list)
    clout = getClout(clarity, reach)

    return [clout, reach, clarity]

# ================================================== #

def getReach(reach_list):
    if len(reach_list) == 0:
        score = 0
    else:
        score = sum(reach_list)/len(reach_list)
    confidence = sFunction(2, 6, len(reach_list))

    return (score, confidence)

# ============================================= #

def getClarity(clarity_list):
    if len(clarity_list) == 0:
        score = 0
    else:
        score = sum(clarity_list) / len(clarity_list)
    confidence = sFunction(4, 8, len(clarity_list))

    return (score, confidence)

# ============================================= #

def getClout(reach, clarity):
    if clarity[1] + reach[1] != 0:
        reach_weight = reach[1]/(clarity[1] + reach[1])
        clarity_weight = clarity[1] / (clarity[1] + reach[1])
    else:
        reach_weight = 0
        clarity_weight = 0

    normalized_weight = (clarity_weight*clarity[0]) + (reach_weight*reach[0])
    score = normalized_weight/10
    confidence = min([clarity[1], reach[1]])

    return(score, confidence)

# ============================================= #

def sFunction(a, b, x):
    if x <= a:
        return 0
    elif a <= x <= ((a+b)/2):
        return 2*((x-a)/(b-a))**2
    elif ((a+b)/2) <= x <= b:
        return 1-2*((x-b)/(b-a))**2
    else:
        return 1

# ================================================== #
#                        EOF                         #
# ================================================== #
