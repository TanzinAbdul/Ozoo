"""
Lion species implementation.
Demonstrates concrete class implementation and polymorphism.
"""

from animals.mammal import Mammal
from animals.animal import DietType

class Lion(Mammal):
    """
    Lion species class.
    
    Additional Attributes:
        _mane_size (str): Size of the lion's mane (if male)
        _pride_leader (bool): Whether this lion leads the pride
    """
    
    def __init__(self, name: str, age: int, is_male: bool = True, 
                 pride_leader: bool = False):
        """
        Initialize lion with specific attributes.
        
        Args:
            name: Lion's name
            age: Age in years
            is_male: Whether the lion is male
            pride_leader: Whether this lion leads the pride
        """
        super().__init__(name, "Lion", age, DietType.CARNIVORE, "savannah",
                        fur_color="golden", is_nocturnal=False)
        self._is_male = is_male
        self._mane_size = "large" if is_male else "none"
        self._pride_leader = pride_leader
    
    def make_sound(self) -> str:
        """
        Lion's characteristic roar.
        
        Returns:
            String representing lion's roar
        """
        if self._pride_leader:
            return "ROAR! 🦁 (The ground trembles with authority!)"
        else:
            return "Rooaar! 🦁"
    
    def eat(self, food: str) -> str:
        """
        Lion-specific eating behavior.
        
        Args:
            food: Type of food being offered
            
        Returns:
            String describing eating behavior
        """
        if "meat" not in food.lower():
            return f"{self._name} stares at the {food} with disdain - this is not meat!"
        
        self._modify_hunger(-35.0)
        self._modify_happiness(10.0)
        
        if self._pride_leader:
            return f"{self._name} eats the {food} first as pride leader! 🦁"
        else:
            return f"{self._name} devours the {food} hungrily! 🦁"
    
    def hunt(self) -> str:
        """
        Lion-specific hunting behavior.
        
        Returns:
            String describing hunting
        """
        self._modify_hunger(-20.0)
        self._modify_happiness(15.0)
        leader_note = " leading the pride" if self._pride_leader else ""
        return f"{self._name} goes hunting{leader_note}!"