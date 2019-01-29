
import logging
logger = logging.getLogger('StegoVeritas:Modules')

"""
import handler
handlers = [handler]
"""

class ModuleBase(object):
    """Define things that need to be in the module class."""

    def __init__(self, veritas):
        """
        Args:
            veritas (stegoveritas.StegoVeritas): Base StegoVeritas instantiated class.
        """
        self.veritas = veritas
        self.valid = False

    def run(self):
        """Must implement this. This will be called to perform the analysis."""
        raise NotImplementedError('This call is not implemented!')

    @property
    def veritas(self):
        return self.__veritas

    @veritas.setter
    def veritas(self, veritas):
        if not isinstance(veritas, StegoVeritas):
            logger.error('Invalid veritas class! Got: {}'.format(type(veritas)))

        self.__veritas = veritas

    @property
    def valid(self):
        """Bool: Is this class valid for the given file provided?"""
        return self.__valid

    @valid.setter
    def valid(self, valid):
        assert type(valid) is bool, 'Unexpected type for valid of {}'.format(type(valid))
        self.__valid = valid

def iter_modules(file_path):
    """Iterate through handlers until one of them loads correctly or we run out of handlers.

    Returns:
        Valid handler instantiation or None.
    """
    pass

from .. import StegoVeritas
