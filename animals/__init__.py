"""
Animals package containing all animal-related classes and species.
"""

from .animal import Animal
from .mammal import Mammal
from .bird import Bird
from .reptile import Reptile

__all__ = ['Animal', 'Mammal', 'Bird', 'Reptile']