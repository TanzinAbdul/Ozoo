"""
Factory Pattern implementation for creating animals and other entities.
Demonstrates creational pattern for flexible object creation.
"""

from animals.animal import Animal, DietType
from animals.mammal import Mammal
from animals.bird import Bird
from animals.reptile import Reptile
from animals.species.lion import Lion
from animals.species.eagle import Eagle
from animals.species.snake import Snake
from animals.species.elephant import Elephant
from animals.species.penguin import Penguin
from core.exceptions import AnimalError
from typing import Dict, Any

class AnimalFactory:
    """
    Factory class for creating animal instances using Factory Pattern.
    
    Why Factory Pattern improves modularity:
    1. Centralized Creation: All animal creation logic in one place
    2. Decoupling: Client code doesn't need to know concrete classes
    3. Extensibility: Easy to add new species without modifying existing code
    4. Maintainability: Changes to creation logic affect only the factory
    """
    
    # Registry of available animal types and their classes
    _animal_registry: Dict[str, type] = {
        # Big Cats
        'lion': Lion,
        'tiger': lambda name, age, **kwargs: Mammal(name, "Tiger", age, DietType.CARNIVORE, "jungle", **kwargs),
        
        # Birds
        'eagle': Eagle,
        'penguin': Penguin,
        
        # Reptiles
        'snake': Snake,
        
        # Mammals
        'elephant': Elephant,
        'giraffe': lambda name, age, **kwargs: Mammal(name, "Giraffe", age, DietType.HERBIVORE, "savannah", **kwargs),
        'zebra': lambda name, age, **kwargs: Mammal(name, "Zebra", age, DietType.HERBIVORE, "savannah", **kwargs),
        
        # Generic types (fallbacks)
        'mammal': Mammal,
        'bird': Bird,
        'reptile': Reptile,
    }
    
    @classmethod
    def register_animal(cls, animal_type: str, animal_class: type) -> None:
        """
        Register a new animal type in the factory.
        
        Args:
            animal_type: Type identifier string
            animal_class: Animal class to instantiate
        """
        if not issubclass(animal_class, Animal):
            raise AnimalError(f"Registered class must be a subclass of Animal")
        
        cls._animal_registry[animal_type.lower()] = animal_class
        print(f"✅ Registered new animal type: {animal_type} -> {animal_class.__name__}")
    
    @classmethod
    def create_animal(cls, animal_type: str, name: str, age: int, **kwargs) -> Animal:
        """
        Create an animal instance based on type.
        
        Args:
            animal_type: Type of animal to create
            name: Animal's name
            age: Animal's age
            **kwargs: Additional species-specific parameters
            
        Returns:
            Animal instance
            
        Raises:
            AnimalError: If animal type is unknown
        """
        animal_type = animal_type.lower()
        
        if animal_type not in cls._animal_registry:
            raise AnimalError(f"Unknown animal type: {animal_type}. Available: {list(cls._animal_registry.keys())}")
        
        animal_class = cls._animal_registry[animal_type]
        
        try:
            # Handle lambda functions for generic types
            if callable(animal_class) and not isinstance(animal_class, type):
                return animal_class(name, age, **kwargs)
            else:
                # Instantiate the concrete animal class
                return animal_class(name, age, **kwargs)
                
        except TypeError as e:
            raise AnimalError(f"Error creating {animal_type}: {e}. Check required parameters.")
    
    @classmethod
    def get_available_species(cls) -> list:
        """
        Get list of available animal species.
        
        Returns:
            List of available species names
        """
        return list(cls._animal_registry.keys())
    
    @classmethod
    def create_from_config(cls, config: Dict[str, Any]) -> Animal:
        """
        Create animal from configuration dictionary.
        
        Args:
            config: Dictionary with animal configuration
            
        Returns:
            Animal instance
        """
        required_keys = ['type', 'name', 'age']
        missing_keys = [key for key in required_keys if key not in config]
        
        if missing_keys:
            raise AnimalError(f"Missing required configuration keys: {missing_keys}")
        
        animal_type = config.pop('type')
        name = config.pop('name')
        age = config.pop('age')
        
        return cls.create_animal(animal_type, name, age, **config)