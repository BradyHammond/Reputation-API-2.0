# ================================================== #
#                     BEHAVING                       #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 01/21/2017                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

from collections import deque
from ioflo.aid import timing
from ioflo.aid import getConsole
from ioflo.aid.odicting import odict
from ioflo.aid.sixing import *
from ioflo.base import doify
from ..db import dbing
from ..help import helping
from __future__ import generator_stop

import datetime
import sys
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

# ================================================== #
#                        EOF                         #
# ================================================== #