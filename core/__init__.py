"""
Core package containing fundamental game components, interfaces, and utilities.
"""

from .interfaces import ICleanable
from .factory import AnimalFactory
from .exceptions import ZooError, AnimalError, EnclosureError

__all__ = ['ICleanable', 'AnimalFactory', 'ZooError', 'AnimalError', 'EnclosureError']