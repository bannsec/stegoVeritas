
import logging
logger = logging.getLogger('StegoVeritas:Modules')

import importlib
import inspect
import os

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
        """By default, this will dynamically load any python files under the 'analysis' subfolder and call the 'run' method with itself as the only argument."""

        # List out the analysis modules
        module_base = str(self.__class__.__module__)
        analysis_dir = os.path.join(os.path.dirname(inspect.getfile(self.__class__)), 'analysis')
        _,_,files = next(os.walk(analysis_dir))

        for f in files:
            if f.endswith('.py') and f != '__init__.py':
                module = importlib.import_module('.analysis.' + f[:-3], module_base)
                module.run(self)

    @property
    def veritas(self):
        return self.__veritas

    @veritas.setter
    def veritas(self, veritas):
        self.__veritas = veritas

    @property
    def valid(self):
        """Bool: Is this class valid for the given file provided?"""
        return self.__valid

    @valid.setter
    def valid(self, valid):
        assert type(valid) is bool, 'Unexpected type for valid of {}'.format(type(valid))
        self.__valid = valid

    @property
    def description(self) -> str:
        """str: Description of things we know about this file."""
        return 'This hasn\'t been implemented yet.'

def iter_modules(veritas):
    """Iterate through handlers until one of them loads correctly or we run out of handlers.

    Returns:
        Valid handler instantiation or None.
    """

    for module in modules:
        instance = module(veritas)
        
        if instance.valid:
            yield instance

from .image import SVImage
from .multi import MultiHandler

# List of classes of modules to try
modules =  [ SVImage, MultiHandler ]
