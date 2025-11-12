"""
Eagle species implementation.
Demonstrates concrete class implementation and polymorphism.
"""

from animals.bird import Bird
from animals.animal import DietType

class Eagle(Bird):
    """
    Eagle species class.
    
    Additional Attributes:
        _vision_range (float): Eagle's vision range in kilometers
    """
    
    def __init__(self, name: str, age: int, wingspan: float = 2.2):
        """
        Initialize eagle with specific attributes.
        
        Args:
            name: Eagle's name
            age: Age in years
            wingspan: Wingspan in meters
        """
        super().__init__(name, "Eagle", age, DietType.CARNIVORE, "mountains",
                        wingspan=wingspan, can_fly=True)
        self._vision_range = 3.0  # kilometers
    
    def make_sound(self) -> str:
        """
        Eagle's characteristic screech.
        
        Returns:
            String representing eagle's sound
        """
        return "Screeeech! 🦅"
    
    def eat(self, food: str) -> str:
        """
        Eagle-specific eating behavior.
        
        Args:
            food: Type of food being offered
            
        Returns:
            String describing eating behavior
        """
        if "fish" in food.lower() or "rodent" in food.lower():
            self._modify_hunger(-30.0)
            self._modify_happiness(12.0)
            return f"{self._name} tears into the {food} with sharp talons! 🦅"
        else:
            self._modify_hunger(-15.0)
            return f"{self._name} picks at the {food} reluctantly."
    
    def soar(self) -> str:
        """
        Eagle-specific soaring behavior.
        
        Returns:
            String describing soaring
        """
        self._modify_happiness(20.0)
        return f"{self._name} soars high above, scanning {self._vision_range}km ahead! 🦅"