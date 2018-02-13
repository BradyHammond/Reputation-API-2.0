# ================================================== #
#                       ENDING                       #
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

import falcon

try:
    import ujson as json
except ImportError:
    import json

# ================================================== #
#                 CONSTANTS & GLOBALS                #
# ================================================== #

BASE_PATH = "/reputation"

console = getConsole()

# ================================================== #
#                  CLASS DEFINITIONS                 #
# ================================================== #

class ReputationResource:
    def __init__(self, store=None, **kwa):
        super(**kwa)
        self.store = store

    # ============================================== #

    def on_get(self, req, resp, reputee=None):
        if reputee is None:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'A valid query is required.')

        result = dbing.getEntry(reputee, dbn='reputation')
        if result == False:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'Reputee could not be found.')
        else:
            resp.status = falcon.HTTP_200
            resp.body = json.dumps(result)

    # ============================================== #

    def on_post(self, req, resp, parameter=None):
        if not parameter is None:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'Malformed URI.')
        try:
            raw_json = req.stream.read()
            if not raw_json:
                raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'A valid JSON document is required.')
        except Exception:
                raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'A valid JSON document is required.')

        try:
            json_object = json.loads(raw_json)
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_422, 'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')

        try:
            reputer = json_object['reputer']
            reputee = json_object['reputee']
            rid = str(json_object['repute']['rid'])
            feature = json_object['repute']['feature']
            value = json_object['repute']['value']

            key = reputee + '-' + rid
            ser = json.dumps({"reputer": reputer,
                              "reputee": reputee,
                              "repute": {"rid": rid, "feature": feature, "value": value}})

            dbing.putEntry(key, ser)
            dbing.putEntry(reputee, ser, dbn="unprocessed")
            resp.status = falcon.HTTP_201
            resp.body = json.dumps({'Message': 'entry successfully created.'})

        except KeyError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was formatted incorrectly.')

# ================================================== #
#                     FUNCTIONS                      #
# ================================================== #

def loadEnds(app, store):
    reputation = ReputationResource()
    app.add_route('{}/'.format(BASE_PATH), reputation)
    app.add_route('{}/{{reputee}}'.format(BASE_PATH), reputation)

# ================================================== #
#                        EOF                         #
# ================================================== #