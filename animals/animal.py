"""
Abstract Base Class for all animals in OzZoo.
Demonstrates abstraction, encapsulation, and polymorphism.
"""

from abc import ABC, abstractmethod
from enum import Enum
import random

class DietType(Enum):
    """Enumeration for animal diet types."""
    CARNIVORE = "carnivore"
    HERBIVORE = "herbivore"
    OMNIVORE = "omnivore"

class Animal(ABC):
    """
    Abstract base class representing all animals.
    
    Attributes:
        _name (str): Animal's name (protected)
        _species (str): Animal species (protected)
        _age (int): Animal's age in years (protected)
        _health (float): Health percentage 0-100 (private)
        _hunger (float): Hunger level 0-100 (private)
        _happiness (float): Happiness percentage 0-100 (private)
        _diet (DietType): Animal's diet type (protected)
        _habitat (str): Preferred habitat (protected)
    """
    
    def __init__(self, name: str, species: str, age: int, diet: DietType, habitat: str):
        """
        Initialize animal with basic attributes.
        
        Args:
            name: Animal's name
            species: Animal species
            age: Age in years
            diet: Diet type from DietType enum
            habitat: Preferred habitat
        """
        self._name = name
        self._species = species
        self._age = age
        self.__health = 100.0  # Private attribute
        self.__hunger = 0.0    # Private attribute
        self.__happiness = 100.0  # Private attribute
        self._diet = diet
        self._habitat = habitat
    
    @abstractmethod
    def make_sound(self) -> str:
        """
        Abstract method for animal sound.
        
        Returns:
            String representing the animal's sound
        """
        pass
    
    @abstractmethod
    def eat(self, food: str) -> str:
        """
        Abstract method for eating behavior.
        
        Args:
            food: Type of food being offered
            
        Returns:
            String describing eating behavior
        """
        pass
    
    def update_daily_status(self) -> None:
        """
        Simulate daily changes to animal's status.
        Demonstrates encapsulation by modifying private attributes.
        """
        # Increase hunger daily
        self.__hunger = min(100.0, self.__hunger + random.uniform(5.0, 15.0))
        
        # Health decreases if very hungry or unhappy
        if self.__hunger > 70.0:
            self.__health = max(0.0, self.__health - random.uniform(2.0, 5.0))
        
        # Happiness decreases with hunger and age
        happiness_decrease = (self.__hunger * 0.1) + (self._age * 0.5)
        self.__happiness = max(0.0, self.__happiness - happiness_decrease)
        
        # Small chance of random health issue
        if random.random() < 0.1:
            self.__health = max(0.0, self.__health - random.uniform(1.0, 3.0))
    
    # Property getters for encapsulated attributes
    @property
    def name(self) -> str:
        """Get animal's name."""
        return self._name
    
    @property
    def species(self) -> str:
        """Get animal species."""
        return self._species
    
    @property
    def age(self) -> int:
        """Get animal's age."""
        return self._age
    
    @property
    def health(self) -> float:
        """Get health percentage."""
        return self.__health
    
    @property
    def hunger(self) -> float:
        """Get hunger level."""
        return self.__hunger
    
    @property
    def happiness(self) -> float:
        """Get happiness percentage."""
        return self.__happiness
    
    @property
    def diet(self) -> DietType:
        """Get diet type."""
        return self._diet
    
    @property
    def habitat(self) -> str:
        """Get preferred habitat."""
        return self._habitat
    
    # Protected method for subclasses to modify internal state
    def _modify_health(self, amount: float) -> None:
        """
        Protected method to modify health safely.
        
        Args:
            amount: Amount to change health by (positive or negative)
        """
        self.__health = max(0.0, min(100.0, self.__health + amount))
    
    def _modify_hunger(self, amount: float) -> None:
        """
        Protected method to modify hunger safely.
        
        Args:
            amount: Amount to change hunger by (positive or negative)
        """
        self.__hunger = max(0.0, min(100.0, self.__hunger + amount))
    
    def _modify_happiness(self, amount: float) -> None:
        """
        Protected method to modify happiness safely.
        
        Args:
            amount: Amount to change happiness by (positive or negative)
        """
        self.__happiness = max(0.0, min(100.0, self.__happiness + amount))
    
    def get_info(self) -> dict:
        """
        Get comprehensive animal information.
        
        Returns:
            Dictionary with all animal attributes
        """
        return {
            'name': self._name,
            'species': self._species,
            'age': self._age,
            'health': self.__health,
            'hunger': self.__hunger,
            'happiness': self.__happiness,
            'diet': self._diet.value,
            'habitat': self._habitat
        }
    
    def __str__(self) -> str:
        """String representation of animal."""
        return f"{self._name} the {self._species} (Health: {self.__health:.1f}%)"
    
    def __repr__(self) -> str:
        """Technical representation of animal."""
        return f"Animal(name='{self._name}', species='{self._species}', age={self._age})"