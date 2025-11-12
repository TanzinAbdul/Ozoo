"""
Mammal class representing mammalian animals.
Demonstrates inheritance and method overriding.
"""
import random
from animals.animal import Animal, DietType

class Mammal(Animal):
    """
    Base class for mammalian animals.
    
    Additional Attributes:
        _fur_color (str): Color of the mammal's fur
        _is_nocturnal (bool): Whether the mammal is nocturnal
    """
    
    def __init__(self, name: str, species: str, age: int, diet: DietType, 
                 habitat: str, fur_color: str = "brown", is_nocturnal: bool = False):
        """
        Initialize mammal with specific attributes.
        
        Args:
            name: Animal's name
            species: Animal species
            age: Age in years
            diet: Diet type
            habitat: Preferred habitat
            fur_color: Color of fur
            is_nocturnal: Whether animal is nocturnal
        """
        super().__init__(name, species, age, diet, habitat)
        self._fur_color = fur_color
        self._is_nocturnal = is_nocturnal
    
    def make_sound(self) -> str:
        """
        Generic mammal sound.
        
        Returns:
            String representing mammal sound
        """
        return "Generic mammal sound!"
    
    def eat(self, food: str) -> str:
        """
        Mammal-specific eating behavior.
        
        Args:
            food: Type of food being offered
            
        Returns:
            String describing eating behavior
        """
        if self._diet == DietType.CARNIVORE and "meat" not in food.lower():
            return f"{self._name} sniffs the {food} but refuses to eat it - needs meat!"
        elif self._diet == DietType.HERBIVORE and "meat" in food.lower():
            return f"{self._name} looks disgusted by the {food} - prefers plants!"
        else:
            self._modify_hunger(-30.0)  # Reduce hunger
            self._modify_happiness(5.0)  # Increase happiness
            return f"{self._name} happily eats the {food} with mammalian appetite!"
    
    def give_birth(self) -> str:
        """
        Mammal-specific behavior for giving birth.
        
        Returns:
            String describing birth process
        """
        return f"{self._name} gives birth to live young!"
    
    def update_daily_status(self) -> None:
        """
        Override daily status update with mammal-specific behavior.
        """
        super().update_daily_status()
        
        # Mammals get extra happiness from social interaction
        if random.random() < 0.3:
            self._modify_happiness(2.0)
    
    def get_mammal_info(self) -> dict:
        """
        Get mammal-specific information.
        
        Returns:
            Dictionary with mammal attributes
        """
        base_info = self.get_info()
        base_info.update({
            'fur_color': self._fur_color,
            'is_nocturnal': self._is_nocturnal,
            'type': 'mammal'
        })
        return base_info