# ================================================== #
#                      RESTING                       #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 01/21/2017                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

from __future__ import generator_stop

from collections import deque
from ioflo.aid import getConsole
from ioflo.aid import odict
from ioflo.aid.sixing import *
from ioflo.aio import WireLog
from ioflo.aio.http import Valet
from ioflo.base import doify
from .. import reputationing
from ..db import dbing
from ..end import ending
from ..help import helping
from ..prime import priming

import falcon
import os
import sys

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

@doify('ReputationServerOpen', ioinits=odict(valet="",
                                             port=odict(ival=8080),
                                             dbDirPath="",
                                             test="",
                                             preload=""))
def reputationServerOpen(self, buffer=False, **kwa):
    if buffer:
        wlog = WireLog(buffify=True, same=True)
        result = wlog.reopen()
    else:
        wlog = None

    port = int(self.port.value)
    test = True if self.test.value else False
    preload = True if self.preload.value else False

    if test:
        priming.setupTest()
        if preload:
            dbing.preloadTestDbs()

    else:
        dbDirPath = self.dbDirPath.value if self.dbDirPath.value else None
        dbDirPath = os.path.abspath(os.path.expanduser(dbDirPath)) if dbDirPath else None
        priming.setup(dbDirPath)

        self.dbDirPath.value = dbing.gDbDirPath

        app = falcon.API()
        ending.loadEnds(app, store=self.store)

        self.valet.value = Valet(port=port,
                                 bufsize=131072,
                                 wlog=wlog,
                                 store=self.store,
                                 app=app,
                                 timeout=0.5)

        result = self.valet.value.servant.reopen()
        if not result:
            console.terse("Error opening server '{0}' at '{1}'\n".format(
                self.valet.name,
                self.valet.value.servant.ha))

            return

        console.concise("Opened server '{0} at '{1}'\n".format(
            self.valet.name,
            self.valet.value.servant.ha))

# ================================================== #

@doify('ReputationServerService', ioinits=odict(valet=""))
def reputationServerService(self, **kwa):
    if self.valet.value:
        self.valet.value.serviceAll()

# ================================================== #

@doify('ReputationServerClose', ioinits=odict(valet=""))
def reputationServerClose(self, **kwa):
    if self.valet.value:
        self.valet.value.servant.closeAll()

        console.concise("Closed server '{0}' at '{1}'\n".format(
            self.valet.name,
            self.valet.value.servant.eha))

# ================================================== #
#                        EOF                         #
# ================================================== #