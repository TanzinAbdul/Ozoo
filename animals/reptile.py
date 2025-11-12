"""
Reptile class representing reptilian animals.
Demonstrates inheritance and method overriding.
"""
import random
from animals.animal import Animal, DietType

class Reptile(Animal):
    """
    Base class for reptilian animals.
    
    Additional Attributes:
        _scale_type (str): Type of scales
        _is_venomous (bool): Whether the reptile is venomous
    """
    
    def __init__(self, name: str, species: str, age: int, diet: DietType,
                 habitat: str, scale_type: str = "smooth", is_venomous: bool = False):
        """
        Initialize reptile with specific attributes.
        
        Args:
            name: Animal's name
            species: Animal species
            age: Age in years
            diet: Diet type
            habitat: Preferred habitat
            scale_type: Type of scales
            is_venomous: Whether reptile is venomous
        """
        super().__init__(name, species, age, diet, habitat)
        self._scale_type = scale_type
        self._is_venomous = is_venomous
    
    def make_sound(self) -> str:
        """
        Generic reptile sound.
        
        Returns:
            String representing reptile sound
        """
        return "Hiss!"
    
    def eat(self, food: str) -> str:
        """
        Reptile-specific eating behavior.
        
        Args:
            food: Type of food being offered
            
        Returns:
            String describing eating behavior
        """
        # Reptiles eat less frequently but larger meals
        if "insect" in food.lower() or "rodent" in food.lower():
            self._modify_hunger(-40.0)
            self._modify_happiness(3.0)
            venom_note = " using venom!" if self._is_venomous else "."
            return f"{self._name} slowly consumes the {food}{venom_note}"
        else:
            self._modify_hunger(-20.0)
            return f"{self._name} cautiously tastes the {food} before eating."
    
    def shed_skin(self) -> str:
        """
        Reptile-specific skin shedding behavior.
        
        Returns:
            String describing skin shedding
        """
        self._modify_health(5.0)  # Health improves after shedding
        return f"{self._name} sheds its {self._scale_type} skin!"
    
    def bask(self) -> str:
        """
        Reptile-specific sun basking behavior.
        
        Returns:
            String describing basking
        """
        self._modify_happiness(15.0)
        return f"{self._name} basks in the sun to regulate body temperature."
    
    def update_daily_status(self) -> None:
        """
        Override daily status update with reptile-specific behavior.
        """
        super().update_daily_status()
        
        # Reptiles have slower metabolism
        self._modify_hunger(-5.0)  # They get hungry slower
        
        # Chance to bask and improve happiness
        if random.random() < 0.4:
            self._modify_happiness(3.0)
    
    def get_reptile_info(self) -> dict:
        """
        Get reptile-specific information.
        
        Returns:
            Dictionary with reptile attributes
        """
        base_info = self.get_info()
        base_info.update({
            'scale_type': self._scale_type,
            'is_venomous': self._is_venomous,
            'type': 'reptile'
        })
        return base_info