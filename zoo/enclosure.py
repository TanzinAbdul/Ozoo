"""
Enclosure class managing animal habitats with ICleanable interface.
"""

from core.interfaces import ICleanable
from core.exceptions import EnclosureError, CompatibilityError, ResourceError
from animals.animal import Animal
from typing import List, Optional, Dict
import random

class Enclosure(ICleanable):
    """
    Enclosure class representing animal habitats.
    
    Attributes:
        _name (str): Enclosure name
        _capacity (int): Maximum number of animals
        _enclosure_type (str): Type of enclosure (savannah, aviary, etc.)
        _animals (List[Animal]): Animals in this enclosure
        _cleanliness (float): Cleanliness level 0-100
        _compatible_species (List[str]): Species that can coexist
    """
    
    def __init__(self, name: str, capacity: int, enclosure_type: str, compatible_species: List[str] = None):
        """
        Initialize enclosure with basic properties.
        
        Args:
            name: Enclosure name
            capacity: Maximum animal capacity
            enclosure_type: Type of enclosure
            compatible_species: List of compatible species
        """
        self._name = name
        self._capacity = capacity
        self._enclosure_type = enclosure_type
        self._animals = []
        self._cleanliness = 100.0
        self._compatible_species = compatible_species or []
    
    @property
    def name(self) -> str:
        """Get enclosure name."""
        return self._name
    
    @property
    def animal_count(self) -> int:
        """Get number of animals in enclosure."""
        return len(self._animals)
    
    @property
    def animals(self) -> List[Animal]:
        """Get copy of animals list (encapsulation protection)."""
        return self._animals.copy()
    
    # ICleanable interface implementation
    def clean(self) -> None:
        """Clean the enclosure to maximum cleanliness."""
        old_cleanliness = self._cleanliness
        self._cleanliness = 100.0
        print(f"🧹 Cleaned {self._name}. Cleanliness: {old_cleanliness:.1f}% → 100.0%")
    
    def get_cleanliness(self) -> float:
        """Get current cleanliness level."""
        return self._cleanliness
    
    def needs_cleaning(self) -> bool:
        """Check if enclosure needs cleaning."""
        return self._cleanliness < 30.0
    
    def add_animal(self, animal: Animal) -> bool:
        """
        Add animal to enclosure with compatibility checks.
        
        Args:
            animal: Animal to add
            
        Returns:
            True if successful
            
        Raises:
            EnclosureError: If enclosure is full
            CompatibilityError: If animal is incompatible with current inhabitants
        """
        # Check capacity
        if len(self._animals) >= self._capacity:
            raise EnclosureError(
                f"Enclosure '{self._name}' is at capacity ({self._capacity} animals)"
            )
        
        # Check species compatibility
        if not self._is_animal_compatible(animal):
            existing_species = [a.species for a in self._animals]
            raise CompatibilityError(
                f"Cannot add {animal.species} to enclosure with {existing_species}",
                animal.species,
                existing_species[0] if existing_species else "none"
            )
        
        # Check habitat suitability
        if animal.habitat != self._enclosure_type:
            print(f"⚠️  Warning: {animal.species} prefers {animal.habitat} but is in {self._enclosure_type}")
        
        self._animals.append(animal)
        print(f"✅ Added {animal.name} the {animal.species} to {self._name}")
        return True
    
    def remove_animal(self, animal_name: str) -> Optional[Animal]:
        """
        Remove animal from enclosure by name.
        
        Args:
            animal_name: Name of animal to remove
            
        Returns:
            Removed animal or None if not found
        """
        for i, animal in enumerate(self._animals):
            if animal.name.lower() == animal_name.lower():
                removed_animal = self._animals.pop(i)
                print(f"❌ Removed {removed_animal.name} from {self._name}")
                return removed_animal
        return None
    
    def _is_animal_compatible(self, new_animal: Animal) -> bool:
        """
        Check if new animal is compatible with current inhabitants.
        
        Args:
            new_animal: Animal to check
            
        Returns:
            True if compatible
        """
        if not self._animals:
            return True  # Empty enclosure, any animal is compatible
        
        print(f"🔍 Compatibility check for {new_animal.name} the {new_animal.species}")
        print(f"   Enclosure: {self._name}, Type: {self._enclosure_type}")
        print(f"   Compatible species: {self._compatible_species}")
        print(f"   Current animals: {[a.species for a in self._animals]}")
        
        # Check against compatible species list (if specified)
        if self._compatible_species:
            if new_animal.species not in self._compatible_species:
                print(f"❌ {new_animal.species} not in compatible species list: {self._compatible_species}")
                return False
            else:
                print(f"✅ {new_animal.species} is in compatible species list")
        
        # Basic compatibility rules
        for existing_animal in self._animals:
            # Carnivores shouldn't be with potential prey (except same species)
            if (existing_animal.diet.value == "carnivore" and 
                new_animal.diet.value != "carnivore" and
                existing_animal.species != new_animal.species):
                print(f"❌ Carnivore conflict: {existing_animal.species} (carnivore) vs {new_animal.species} (not carnivore)")
                return False
            
            if (new_animal.diet.value == "carnivore" and 
                existing_animal.diet.value != "carnivore" and
                existing_animal.species != new_animal.species):
                print(f"❌ Carnivore conflict: {new_animal.species} (carnivore) vs {existing_animal.species} (not carnivore)")
                return False
        
        print(f"✅ {new_animal.species} is compatible with enclosure {self._name}")
        return True
    
    def feed_animals(self, food_type: str, resource_manager) -> Dict[str, List[str]]:
        """
        Feed all animals in enclosure.
        
        Args:
            food_type: Type of food to feed
            resource_manager: Resource manager for food supply
            
        Returns:
            Dictionary with feeding results
        """
        results = {
            'successful': [],
            'failed': [],
            'refused': []
        }
        
        total_food_needed = len(self._animals) * 2.0  # 2kg per animal
        
        try:
            # Use food from resource manager
            if resource_manager.use_food(food_type, total_food_needed):
                for animal in self._animals:
                    try:
                        feeding_result = animal.eat(food_type)
                        results['successful'].append(f"{animal.name}: {feeding_result}")
                    except Exception as e:
                        results['failed'].append(f"{animal.name}: Error - {e}")
            
        except ResourceError as e:
            results['failed'].append(f"Food supply error: {e}")
        
        return results
    
    def update_daily_status(self) -> None:
        """
        Update enclosure and animal status for a new day.
        """
        # Animals make enclosure dirtier
        dirt_per_animal = random.uniform(2.0, 8.0)
        self._cleanliness = max(0.0, self._cleanliness - (len(self._animals) * dirt_per_animal))
        
        # Update all animals
        for animal in self._animals:
            animal.update_daily_status()
        
        # Cleanliness affects animal happiness
        if self._cleanliness < 50.0:
            for animal in self._animals:
                animal._modify_happiness(-5.0)
    
    def get_occupancy(self) -> float:
        """
        Calculate current occupancy percentage.
        
        Returns:
            Occupancy percentage (0-100)
        """
        return (len(self._animals) / self._capacity) * 100.0
    
    def get_enclosure_info(self) -> Dict:
        """
        Get comprehensive enclosure information.
        
        Returns:
            Dictionary with enclosure details
        """
        return {
            'name': self._name,
            'type': self._enclosure_type,
            'capacity': self._capacity,
            'animal_count': len(self._animals),
            'occupancy_percent': self.get_occupancy(),
            'cleanliness': self._cleanliness,
            'needs_cleaning': self.needs_cleaning(),
            'compatible_species': self._compatible_species,  # ADD THIS LINE
            'animals': [animal.get_info() for animal in self._animals]
        }