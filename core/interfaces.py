"""
Interface definitions using ABC for contract enforcement.
"""

from abc import ABC, abstractmethod

class ICleanable(ABC):
    """Interface for cleanable entities in the zoo."""
    
    @abstractmethod
    def clean(self) -> None:
        """Perform cleaning action."""
        pass
    
    @abstractmethod
    def get_cleanliness(self) -> float:
        """Return cleanliness level (0-100)."""
        pass
    
    @abstractmethod
    def needs_cleaning(self) -> bool:
        """Check if entity needs cleaning."""
        pass

class IFeedable(ABC):
    """Interface for feedable entities."""
    
    @abstractmethod
    def feed(self, food_type: str) -> bool:
        """Feed the entity with specified food type."""
        pass