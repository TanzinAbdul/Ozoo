"""
Elephant species implementation.
"""

from animals.mammal import Mammal
from animals.animal import DietType

class Elephant(Mammal):
    """
    Elephant species class.
    """
    
    def __init__(self, name: str, age: int, tusk_length: float = 1.5):
        super().__init__(name, "Elephant", age, DietType.HERBIVORE, "savannah",
                        fur_color="gray", is_nocturnal=False)
        self._tusk_length = tusk_length
        self._trunk_skill = "basic"
    
    def make_sound(self) -> str:
        return "Trumpet! 🐘"
    
    def eat(self, food: str) -> str:
        if "fruit" in food.lower() or "vegetable" in food.lower():
            self._modify_hunger(-25.0)
            self._modify_happiness(8.0)
            return f"{self._name} uses its trunk to eat the {food} happily! 🐘"
        else:
            self._modify_hunger(-15.0)
            return f"{self._name} cautiously samples the {food}."
    
    def spray_water(self) -> str:
        self._modify_happiness(10.0)
        return f"{self._name} sprays water with its trunk! 💦🐘"