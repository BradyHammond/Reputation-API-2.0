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

from collections import OrderedDict as OrderedDict, deque
from ioflo.aid import classing
from ioflo.aid import getConsole
from ioflo.aid import lodict
from ioflo.aid import timing
from ioflo.aio.http import httping
from ioflo.aid.sixing import *
from .. import reputationing
from ..db import dbing
from ..help import helping

import arrow
import datetime
import enum
import falcon
import libnacl
import mimetypes
import os
import sys

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

        result = helping.getAll(reputee)
        if result == False:
            raise falcon.HTTPError(falcon.HTTP_400, 'Error', 'Reputee could not be found.')

        else:
            resp.status = falcon.HTTP_200
            resp.body = json.dumps({"reputee": reputee, "clout": {
                "score": result[0][0],
                "confidence": result[0][1]}, "reach": {
                "score": result[1][0],
                "confidence": result[1][1]}, "clarity": {
                "score": result[2][0],
                "confidence": result[2][1]}})

    # ============================================== #

    def on_post(self, req, resp):
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
        except KeyError:
            raise falcon.HTTPError(falcon.HTTP_400, 'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was formatted incorrectly.')

        key = rid+"-"+reputer+"-"+reputee
        ser = json.dumps({"reputer": reputer,
                          "reputee": reputee,
                          "repute": {"rid": rid, "feature": feature, "value": value}})

        dbing.putEntry(key, ser)
        resp.status = falcon.HTTP_201
        resp.body = json.dumps({'message': 'rid-' + key + ' successfully created.'})

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