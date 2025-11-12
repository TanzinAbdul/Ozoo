"""
Main Zoo class managing enclosures, resources, and operations.
"""

from core.exceptions import ZooError, EnclosureError, FinancialError
from zoo.enclosure import Enclosure
from zoo.resource_manager import ResourceManager
from animals.animal import Animal
from typing import List, Optional, Dict
import random

class Zoo:
    """
    Main zoo class managing all enclosures, staff, and operations.
    
    Attributes:
        _name (str): Zoo name
        _enclosures (List[Enclosure]): All enclosures in zoo
        _resource_manager (ResourceManager): Manages funds and supplies
        _visitors_today (int): Number of visitors today
        _total_visitors (int): Total visitors since opening
        _days_operational (int): Days zoo has been open
    """
    
    def __init__(self, name: str, initial_funds: float = 100000.0):
        """
        Initialize zoo with name and resources.
        
        Args:
            name: Zoo name
            initial_funds: Starting budget
        """
        self._name = name
        self._enclosures = []
        self._resource_manager = ResourceManager(initial_funds)
        self._visitors_today = 0
        self._total_visitors = 0
        self._days_operational = 0
        self._ticket_price = 25.0
    
    @property
    def name(self) -> str:
        """Get zoo name."""
        return self._name
    
    @property
    def funds(self) -> float:
        """Get current funds."""
        return self._resource_manager.funds
    
    def add_enclosure(self, enclosure: Enclosure) -> bool:
        """
        Add new enclosure to zoo.
        
        Args:
            enclosure: Enclosure to add
            
        Returns:
            True if successful
        """
        # Check if enclosure with same name exists
        if any(e.name == enclosure.name for e in self._enclosures):
            raise EnclosureError(f"Enclosure with name '{enclosure.name}' already exists")
        
        self._enclosures.append(enclosure)
        print(f"🏠 Added enclosure '{enclosure.name}' to {self._name}")
        return True
    
    def remove_enclosure(self, enclosure_name: str) -> bool:
        """
        Remove enclosure from zoo by name.
        
        Args:
            enclosure_name: Name of enclosure to remove
            
        Returns:
            True if successful, False if not found
        """
        for i, enclosure in enumerate(self._enclosures):
            if enclosure.name == enclosure_name:
                if enclosure.animal_count > 0:
                    raise EnclosureError(
                        f"Cannot remove enclosure '{enclosure_name}' with {enclosure.animal_count} animals"
                    )
                
                removed_enclosure = self._enclosures.pop(i)
                print(f"🗑️  Removed enclosure '{removed_enclosure.name}' from {self._name}")
                return True
        
        return False
    
    def add_animal(self, animal: Animal, enclosure_name: str) -> bool:
        """
        Add animal to specific enclosure with detailed error reporting.
        
        Args:
            animal: Animal to add
            enclosure_name: Name of target enclosure
            
        Returns:
            True if successful
        """
        print(f"🐾 Attempting to add {animal.name} the {animal.species} to {enclosure_name}")
        
        enclosure = self._find_enclosure(enclosure_name)
        if enclosure:
            try:
                result = enclosure.add_animal(animal)
                print(f"✅ Successfully added {animal.name} to {enclosure_name}")
                return result
            except Exception as e:
                print(f"❌ Failed to add {animal.name} to {enclosure_name}: {e}")
                return False
        else:
            print(f"❌ Enclosure '{enclosure_name}' not found")
            return False
    
    def feed_animals(self, enclosure_name: Optional[str] = None) -> Dict:
        """
        Feed animals in specific enclosure or all enclosures.
        
        Args:
            enclosure_name: Specific enclosure name, or None for all
            
        Returns:
            Dictionary with feeding results
        """
        results = {}
        
        if enclosure_name:
            enclosure = self._find_enclosure(enclosure_name)
            if enclosure:
                # Determine appropriate food type based on animals
                food_type = self._determine_food_type(enclosure.animals)
                results[enclosure_name] = enclosure.feed_animals(food_type, self._resource_manager)
            else:
                raise EnclosureError(f"Enclosure '{enclosure_name}' not found")
        else:
            # Feed all enclosures
            for enclosure in self._enclosures:
                food_type = self._determine_food_type(enclosure.animals)
                results[enclosure.name] = enclosure.feed_animals(food_type, self._resource_manager)
        
        return results
    
    def _determine_food_type(self, animals: List[Animal]) -> str:
        """
        Determine appropriate food type for a group of animals.
        
        Args:
            animals: List of animals
            
        Returns:
            Appropriate food type
        """
        if not animals:
            return "seeds"  # Default
        
        # Count diet types
        diet_counts = {}
        for animal in animals:
            diet = animal.diet.value
            diet_counts[diet] = diet_counts.get(diet, 0) + 1
        
        # Return most common diet type's preferred food
        if diet_counts.get('carnivore', 0) > 0:
            return "meat"
        elif diet_counts.get('herbivore', 0) > 0:
            return "vegetables"
        else:
            return "seeds"  # Default for omnivores or unknown
    
    def daily_update(self) -> None:
        """
        Perform daily zoo operations and updates.
        """
        print(f"\n=== DAY {self._days_operational + 1} UPDATE FOR {self._name.upper()} ===")
        
        # Simulate visitors
        self._simulate_visitors()
        
        # Update all enclosures
        for enclosure in self._enclosures:
            enclosure.update_daily_status()
        
        # Pay daily operating costs
        self._pay_operating_costs()
        
        # Reset daily stats in resource manager
        self._resource_manager.reset_daily_stats()
        
        self._days_operational += 1
        self._visitors_today = 0  # Reset for next day
        
        print(f"✅ Day {self._days_operational} completed!")
    
    def _simulate_visitors(self) -> None:
        """Simulate daily visitor attendance and income."""
        # Base visitors with some randomness
        base_visitors = 100
        random_factor = random.randint(-20, 50)
        animal_attraction = self.get_animal_count() * 2
        
        self._visitors_today = max(10, base_visitors + random_factor + animal_attraction)
        self._total_visitors += self._visitors_today
        
        # Calculate income
        daily_income = self._visitors_today * self._ticket_price
        self._resource_manager.add_funds(daily_income, "ticket sales")
        
        print(f"🎟️  {self._visitors_today} visitors today (${daily_income:.2f} income)")
    
    def _pay_operating_costs(self) -> None:
        """Pay daily operating costs."""
        base_cost = 500.0  # Fixed daily costs
        animal_cost = self.get_animal_count() * 10.0  # Per animal cost
        enclosure_cost = len(self._enclosures) * 50.0  # Per enclosure cost
        
        total_cost = base_cost + animal_cost + enclosure_cost
        
        try:
            self._resource_manager.spend_funds(total_cost, "daily operations")
        except FinancialError as e:
            print(f"⚠️  Warning: Could not pay full operating costs: {e}")
    
    def calculate_costs(self) -> Dict[str, float]:
        """
        Calculate various zoo costs.
        
        Returns:
            Dictionary with cost breakdown
        """
        return {
            'daily_operations': 500.0,
            'per_animal': self.get_animal_count() * 10.0,
            'per_enclosure': len(self._enclosures) * 50.0,
            'total_daily': 500.0 + (self.get_animal_count() * 10.0) + (len(self._enclosures) * 50.0)
        }
    
    def get_animal_count(self) -> int:
        """
        Get total number of animals in zoo.
        
        Returns:
            Total animal count
        """
        return sum(enclosure.animal_count for enclosure in self._enclosures)
    
    def _find_enclosure(self, enclosure_name: str) -> Optional[Enclosure]:
        """
        Find enclosure by name.
        
        Args:
            enclosure_name: Name to search for
            
        Returns:
            Enclosure or None if not found
        """
        for enclosure in self._enclosures:
            if enclosure.name.lower() == enclosure_name.lower():
                return enclosure
        return None
    
    def get_zoo_status(self) -> Dict:
        """
        Get comprehensive zoo status information.
        
        Returns:
            Dictionary with zoo status
        """
        resource_status = self._resource_manager.get_resource_status()
        
        return {
            'name': self._name,
            'days_operational': self._days_operational,
            'total_visitors': self._total_visitors,
            'visitors_today': self._visitors_today,
            'enclosure_count': len(self._enclosures),
            'animal_count': self.get_animal_count(),
            'enclosures': [enclosure.get_enclosure_info() for enclosure in self._enclosures],
            'resources': resource_status,
            'financials': {
                'funds': resource_status['funds'],
                'ticket_price': self._ticket_price,
                'daily_costs': resource_status['daily_costs'],
                'daily_income': resource_status['daily_income']
            }
        }
    
    def order_supplies(self) -> None:
        """
        Order basic supplies to replenish stocks.
        """
        print("\n📦 Ordering basic supplies...")
        
        # Order food
        self._resource_manager.order_food("meat", 50.0, 8.0)      # $8/kg
        self._resource_manager.order_food("seeds", 100.0, 2.0)    # $2/kg
        self._resource_manager.order_food("vegetables", 80.0, 3.0) # $3/kg
        
        # Order medicine
        self._resource_manager.order_medicine("vaccine", 5, 15.0)      # $15/unit
        self._resource_manager.order_medicine("antibiotics", 10, 8.0)  # $8/unit