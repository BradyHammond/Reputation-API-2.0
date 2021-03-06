# ================================================== #
#                   REPUTATIONING                    #
# ================================================== #
# Author: Brady Hammond                              #
# Created: 01/21/2017                                #
# Last Edited: N/A                                   #
# Last Edited By: N/A                                #
# ================================================== #
#                      IMPORTS                       #
# ================================================== #

from __future__ import generator_stop

import sys

# ================================================== #
#                  CLASS DEFINITIONS                 #
# ================================================== #

class ReputationError(Exception):
    """
    Base class for reputation exception
    """
# ================================================== #

class ValidationError(ReputationError):
    """
    Class for validation related errors
    """

# ================================================== #
#                        EOF                         #
# ================================================== #
