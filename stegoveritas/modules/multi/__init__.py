
import logging
logger = logging.getLogger('StegoVeritas:Modules:Multi')

import os
import sys
from .. import ModuleBase

class MultiHandler(ModuleBase):

    def __init__(self, veritas):
        super().__init__(veritas)

        # Given it's the mutli format handler, just assume we can handle it and let the plugins figure out the rest.
        self.valid = True
        
        """
        # Should we run all default plugins?
        if all([not veritas.args.imageTransform, not veritas.args.extractLSB, not veritas.args.bruteLSB, veritas.args.colorMap is None, veritas.args.colorMapRange is None, not veritas.args.trailing, not veritas.args.meta]):
            self._default_run = True
        else:
            self._default_run = False
        """

    @property
    def description(self):
        return ""

