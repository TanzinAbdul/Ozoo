"""
Penguin species implementation.
"""

from animals.bird import Bird
from animals.animal import DietType

class Penguin(Bird):
    """
    Penguin species class.
    """
    
    def __init__(self, name: str, age: int):
        super().__init__(name, "Penguin", age, DietType.CARNIVORE, "arctic",
                        wingspan=0.3, can_fly=False)
        self._swimming_speed = 8.0  # km/h
    
    def make_sound(self) -> str:
        return "Honk! 🐧"
    
    def eat(self, food: str) -> str:
        if "fish" in food.lower():
            self._modify_hunger(-20.0)
            self._modify_happiness(12.0)
            return f"{self._name} eagerly swallows the {food} whole! 🐧"
        else:
            self._modify_hunger(-10.0)
            return f"{self._name} waddles away from the {food}."
    
    def slide(self) -> str:
        self._modify_happiness(15.0)
        return f"{self._name} slides on its belly! 🐧⛄"