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

from __future__ import generator_stop

from ioflo.aid import timing
from ioflo.aid import getConsole
from ioflo.aid.odicting import odict
from ioflo.base import doify
from ..db import dbing
from ..help import helping

import datetime

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

@doify('ReputationProcessReputation', ioinits=odict(test=""))
def reputationProcessReputation(self, **kwa):
    if dbing.gDbEnv:
        dt = datetime.datetime.now(tz=datetime.timezone.utc)
        stamp = int(dt.timestamp() * 1000000)
        date = timing.iso8601(dt, aware=True)

        console.verbose("Updating reputation at '{}'\n".format(date))

        try:
            entries = dbing.getEntries(dbn='unprocessed')
        except dbing.DatabaseError as exception:
            console.terse("Error processing reputation. {}".format(exception))

        if len(entries) > 0:
            for entry in entries:
                result = helping.getAll(entry['reputee'], dbing.getEntries())
                ser = json.dumps({"reputee": entry['reputee'], "clout": {
                    "score": result[0][0],
                    "confidence": result[0][1]}, "reach": {
                    "score": result[1][0],
                    "confidence": result[1][1]}, "clarity": {
                    "score": result[2][0],
                    "confidence": result[2][1]}})
                try:
                    success = dbing.putEntry(entry['reputee'], ser, dbn='reputation')
                except dbing.DatabaseError as exception:
                    console.terse("Error processing reputation. {}".format(exception))
                if not success:
                    console.terse("Error processing reputation.")

            success = dbing.deleteEntries()
            console.terse("Unprocessed database cleared: {}".format(str(success)))
            console.verbose("Updated reputation at '{}'\n".format(date))

        else:
            console.verbose("Updated reputation at '{}'\n".format(date))

# ================================================== #
#                        EOF                         #
# ================================================== #