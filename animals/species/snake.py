"""
Snake species implementation.
"""

from animals.reptile import Reptile

class Snake(Reptile):
    """
    Snake species class.
    
    Relationships:
        - Inherits from Reptile
        - Concrete implementation of Animal
    """
    
    def __init__(self, name: str, age: int, is_venomous: bool = False):
        """Initialize snake with venom information."""
        super().__init__(name, "Snake", age)
        self._is_venomous = is_venomous
        self._diet = "carnivore"
        self._habitat = "forest"
    
    def make_sound(self) -> str:
        """Return snake's hiss."""
        pass
    
    def slither(self) -> None:
        """Handle snake slithering behavior."""
        pass