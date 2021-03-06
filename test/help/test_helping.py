# ================================================== #
#                    TEST HELPING                    #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 01/21/2017                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

from __future__ import generator_stop

from pytest import approx
from reputation.db import dbing
from reputation.help.helping import (setupTmpBaseDir, cleanupTmpBaseDir,
                                     getAll, getClarity, getReach, getClout)
from reputation.prime import priming

import os
import pytest

try:
    import ujson as json
except ImportError:
    import json

# ================================================== #
#                     FUNCTIONS                      #
# ================================================== #

def test_getAll():
    entries = []
    result = getAll("Nathan", entries)
    assert result is False

    entries = [{
      "reputer": "Danny",
      "reputee": "Nathan",
      "repute":
      {
        "rid" : "dda6555f-21c8-45ff-9633-f9b5cdc59f44",
        "feature": "reach",
        "value": 4
      }
    },
    {
      "reputer": "Danny",
      "reputee": "Nathan",
      "repute":
      {
        "rid": "dda6555f-21c8-45ff-9633-f9b5cdc59f45",
        "feature": "reach",
        "value": 5
      }
    },
    {
      "reputer": "Danny",
      "reputee": "Nathan",
      "repute":
      {
        "rid": "dda6555f-21c8-45ff-9633-f9b5cdc59f44",
        "feature": "reach",
        "value": 6
      }
    },
    {
      "reputer": "Danny",
      "reputee": "Nathan",
      "repute":
        {
          "rid": "dda6555f-21c8-45ff-9633-f9b5cdc59f44",
          "feature": "clarity",
          "value": 7
        }
    },
    {
    "reputer": "Danny",
    "reputee": "Nathan",
    "repute":
      {
        "rid": "dda6555f-21c8-45ff-9633-f9b5cdc59f45",
        "feature": "clarity",
        "value": 8
      }
    },
    {
    "reputer": "Danny",
    "reputee": "Nathan",
    "repute":
      {
        "rid": "dda6555f-21c8-45ff-9633-f9b5cdc59f44",
        "feature": "clarity",
        "value": 9
      }
    }
    ]

    result = getAll("Nathan", entries)
    assert result[0] == (0.5, 0)
    assert result[1] == (5.0, 0.125)
    assert result[2] == (8.0, 0)

    print("test/help/test_helping: test_getAll() \033[92mPASSED\033[0m")

# ================================================== #

def test_getReach():
    reach_list = []
    reach = getReach(reach_list)
    assert reach == (0, 0)

    reach_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    reach = getReach(reach_list)
    assert reach == (4.5, 1)

    reach_list = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    reach = getReach(reach_list)
    assert reach == (4.0, 1)

    reach_list = [1, 9]
    reach = getReach(reach_list)
    assert reach == (5.0, 0)

    reach_list = [1, 5, 9]
    reach = getReach(reach_list)
    assert reach == (5.0, 0.125)

    reach_list = [1, 3, 4, 5, 6, 7, 9]
    reach = getReach(reach_list)
    assert reach == (5.0, 1)

    print("test/help/test_helping: test_getReach() \033[92mPASSED\033[0m")

# ================================================== #

def test_getClarity():
    clarity_list = []
    clarity = getClarity(clarity_list)
    assert clarity == (0, 0)

    clarity_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    clarity = getClarity(clarity_list)
    assert clarity == (4.5, 1)

    clarity_list = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4]
    clarity = getClarity(clarity_list)
    assert clarity == (4.0, 1)

    clarity_list = [1, 9]
    clarity = getClarity(clarity_list)
    assert clarity == (5.0, 0)

    clarity_list = [1, 5, 9]
    clarity = getClarity(clarity_list)
    assert clarity == (5.0, 0)

    clarity_list = [1, 3, 4, 5, 6, 7, 9]
    clarity = getClarity(clarity_list)
    assert clarity == (5.0, 0.875)

    print("test/help/test_helping: test_getClarity() \033[92mPASSED\033[0m")

# ================================================== #

def test_getClout():
    clout = getClout((0, 0), (0, 0))
    assert clout == (0.0, 0)

    clout = getClout((0, 0), (9, 1))
    assert clout == (0.9, 0)

    clout = getClout((0, 0), (9, 0))
    assert clout == (0.0, 0)

    clout = getClout((1, 0), (1, 1))
    assert clout == (0.1, 0)

    clout = getClout((5, 0.5), (5, 0.5))
    assert clout == (0.5, 0.5)

    clout = getClout((4, 0.875), (5, 0.5))
    assert clout == (0.43636363636363634, 0.5)

    clout = getClout((7, 1), (6, 0.875))
    assert clout == (0.6533333333333333, 0.875)

    print("test/help/test_helping: test_getClout() \033[92mPASSED\033[0m")

# ================================================== #
#                        EOF                         #
# ================================================== #