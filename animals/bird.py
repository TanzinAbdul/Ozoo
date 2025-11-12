"""
Bird class representing avian animals.
Demonstrates inheritance and method overriding.
"""

from animals.animal import Animal, DietType

class Bird(Animal):
    """
    Base class for avian animals.
    
    Additional Attributes:
        _wingspan (float): Wingspan in meters
        _can_fly (bool): Whether the bird can fly
    """
    
    def __init__(self, name: str, species: str, age: int, diet: DietType,
                 habitat: str, wingspan: float = 1.0, can_fly: bool = True):
        """
        Initialize bird with specific attributes.
        
        Args:
            name: Animal's name
            species: Animal species
            age: Age in years
            diet: Diet type
            habitat: Preferred habitat
            wingspan: Wingspan in meters
            can_fly: Whether bird can fly
        """
        super().__init__(name, species, age, diet, habitat)
        self._wingspan = wingspan
        self._can_fly = can_fly
    
    def make_sound(self) -> str:
        """
        Generic bird sound.
        
        Returns:
            String representing bird sound
        """
        return "Chirp chirp!"
    
    def eat(self, food: str) -> str:
        """
        Bird-specific eating behavior.
        
        Args:
            food: Type of food being offered
            
        Returns:
            String describing eating behavior
        """
        eating_style = "pecks at" if self._can_fly else "waddles to"
        
        if "seed" in food.lower() or "worm" in food.lower():
            self._modify_hunger(-25.0)
            self._modify_happiness(8.0)
            return f"{self._name} {eating_style} the {food} enthusiastically!"
        else:
            self._modify_hunger(-15.0)
            return f"{self._name} cautiously {eating_style} the {food}."
    
    def fly(self) -> str:
        """
        Bird-specific flying behavior.
        
        Returns:
            String describing flight attempt
        """
        if self._can_fly:
            self._modify_happiness(10.0)
            return f"{self._name} soars through the air with {self._wingspan}m wingspan!"
        else:
            return f"{self._name} attempts to fly but can't get airborne."
    
    def update_daily_status(self) -> None:
        """
        Override daily status update with bird-specific behavior.
        """
        super().update_daily_status()
        
        # Birds get extra hungry if they can fly
        if self._can_fly:
            self._modify_hunger(5.0)
    
    def get_bird_info(self) -> dict:
        """
        Get bird-specific information.
        
        Returns:
            Dictionary with bird attributes
        """
        base_info = self.get_info()
        base_info.update({
            'wingspan': self._wingspan,
            'can_fly': self._can_fly,
            'type': 'bird'
        })
        return base_info