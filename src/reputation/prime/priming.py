# ================================================== #
#                      PRIMING                       #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 01/21/2017                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #


from collections import OrderedDict as ODict, deque
from ioflo.aid import getConsole
from ioflo.aid import timing
from ioflo.aid.sixing import *
from ..help.helping import setupTmpBaseDir
from ..db import dbing
from __future__ import generator_stop

import datetime
import enum
import lmdb
import os

try:
    import ujson as json
except ImportError:
    import json

# ================================================== #
#                 CONSTANTS & GLOBALS                #
# ================================================== #

console = getConsole()

# ================================================== #
#                     FUNCTIONS                      #
# ================================================== #

def setup(dbDirPath=None):
    dbEnv = dbing.setupDbEnv(baseDirPath=dbDirPath)

# ================================================== #

def setupTest():
    dt = datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)
    stamp = timing.iso8601(dt, aware=True)

    baseDirPath = setupTmpBaseDir()
    dbDirPath = os.path.join(baseDirPath, "reputation/db")
    os.makedirs(dbDirPath)

    setup(dbDirPath=dbDirPath)

# ================================================== #
#                        EOF                         #
# ================================================== #