"""
Enhanced Zoo Manager with complete game loop and simulation engine.
"""

from zoo.zoo import Zoo
from zoo.enclosure import Enclosure
from core.observer import HealthMonitor, ObservableAnimal
from core.events import EventManager  # ADD THIS IMPORT
from core.factory import AnimalFactory
from core.exceptions import ZooError, FinancialError, EnclosureError, CompatibilityError
from typing import Optional, List, Dict
import random
import time

class ZooManager:
    """
    Central manager for the zoo simulation game with complete game loop.
    """
    
    def __init__(self):
        """Initialize zoo manager with game state."""
        self._zoo: Optional[Zoo] = None
        self._running = False
        self._day_count = 0
        self._health_monitor = HealthMonitor()  # REMOVED self parameter
        self._event_manager = EventManager()  # ADD EVENT MANAGER
        self._events_log: List[str] = []
    
    def create_zoo(self, name: str, initial_funds: float = 50000.0) -> None:
        """Create a new zoo with given name."""
        self._zoo = Zoo(name, initial_funds)
        self._day_count = 0
        self._log_event(f"Created new zoo: {name} with ${initial_funds:.2f}")
        print(f"🏰 Created zoo: {name} with ${initial_funds:.2f}")
        
        # Create initial enclosures
        self._create_initial_enclosures()
    
    def _create_initial_enclosures(self) -> None:
        """Create starter enclosures for new zoo with proper compatible species."""
        if not self._zoo:
            return
            
        enclosures = [
            ("Savannah Plains", 3, "savannah", ["Lion", "Elephant", "Zebra", "Giraffe"]),
            ("Eagle's Peak", 2, "aviary", ["Eagle", "Bird"]),
            ("Reptile House", 4, "forest", ["Snake", "Lizard", "Reptile"]),
            ("Penguin Pool", 3, "arctic", ["Penguin"]),
        ]
        
        for name, capacity, env_type, compatible_species in enclosures:
            enclosure = Enclosure(name, capacity, env_type, compatible_species)
            self._zoo.add_enclosure(enclosure)
            print(f"🏠 Added {name} with compatible species: {compatible_species}")
    
    def create_animal_with_factory(self, animal_type: str, name: str, age: int, **kwargs) -> ObservableAnimal:
        """Create animal using Factory Pattern and make it observable."""
        print(f"🔧 Factory creating: {animal_type} named {name}")
        
        try:
            base_animal = AnimalFactory.create_animal(animal_type, name, age, **kwargs)
            print(f"✅ Base animal created: {base_animal.name} the {base_animal.species}")
            
            # Convert to observable animal - FIXED APPROACH
            observable_animal = ObservableAnimal(
                name=base_animal.name,
                species=base_animal.species,
                age=base_animal.age,
                diet=base_animal.diet,
                habitat=base_animal.habitat
            )
            
            # Copy internal state more carefully
            health_diff = base_animal.health - 100.0
            observable_animal._modify_health(health_diff)
            observable_animal._modify_hunger(base_animal.hunger - 0.0)  # Start from current hunger
            observable_animal._modify_happiness(base_animal.happiness - 100.0)  # Start from current happiness
            
            # Attach health monitor
            observable_animal.attach(self._health_monitor)
            
            self._log_event(f"Created {animal_type}: {name}")
            print(f"✅ Observable animal created: {observable_animal.name}")
            return observable_animal
            
        except Exception as e:
            print(f"❌ Error in create_animal_with_factory: {e}")
            import traceback
            traceback.print_exc()
            raise

    def add_animal_to_zoo(self, animal_type: str, name: str, age: int, 
                         enclosure_name: str, **kwargs) -> bool:
        """
        Quick fix - bypass ObservableAnimal conversion.
        """
        if not self._zoo:
            raise ZooError("No zoo created yet")
        
        print(f"🐾 QUICK FIX: Adding {animal_type} '{name}' to {enclosure_name}")
        
        try:
            # Use factory directly (skip ObservableAnimal for now)
            animal = AnimalFactory.create_animal(animal_type, name, age, **kwargs)
            print(f"✅ Animal created: {animal.name}")
            
            # Add to zoo enclosure
            success = self._zoo.add_animal(animal, enclosure_name)
            print(f"✅ Add result: {success}")
            
            if success:
                self._log_event(f"Added {name} the {animal_type} to {enclosure_name}")
                print(f"🎉 Successfully added {name}!")
                return True
            else:
                print(f"❌ Failed to add {name}")
                return False
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    def feed_animals(self, enclosure_name: str = None) -> Dict:
        """Feed animals with user feedback."""
        if not self._zoo:
            raise ZooError("No zoo created yet")
        
        try:
            results = self._zoo.feed_animals(enclosure_name)
            self._log_event(f"Fed animals in {enclosure_name or 'all enclosures'}")
            
            # Provide user feedback
            total_fed = 0
            for enclosure, enclosure_results in results.items():
                fed_count = len(enclosure_results.get('successful', []))
                total_fed += fed_count
                
                if fed_count > 0:
                    print(f"🍽️  Fed {fed_count} animals in {enclosure}")
                    
                    # Show some individual feeding results
                    successful_feeds = enclosure_results.get('successful', [])[:2]
                    for feed_msg in successful_feeds:
                        print(f"   {feed_msg}")
            
            if total_fed == 0:
                print("❌ No animals were fed. Check food supplies!")
            else:
                print(f"✅ Successfully fed {total_fed} animals total")
            
            return results
            
        except Exception as e:
            print(f"❌ Feeding failed: {e}")
            return {}
    
    def clean_enclosures(self, enclosure_name: str = None) -> int:
        """
        Clean specific enclosure or all enclosures.
        
        Returns:
            Number of enclosures cleaned
        """
        if not self._zoo:
            raise ZooError("No zoo created yet")
        
        cleaned_count = 0
        
        if enclosure_name:
            # Clean specific enclosure
            for enclosure in self._zoo._enclosures:
                if enclosure.name == enclosure_name:
                    if enclosure.needs_cleaning():
                        enclosure.clean()
                        cleaned_count += 1
                        self._log_event(f"Cleaned enclosure: {enclosure_name}")
                        print(f"🧹 Cleaned {enclosure_name}")
                    else:
                        print(f"✅ {enclosure_name} is already clean enough")
                    break
        else:
            # Clean all dirty enclosures
            for enclosure in self._zoo._enclosures:
                if enclosure.needs_cleaning():
                    enclosure.clean()
                    cleaned_count += 1
                    self._log_event(f"Cleaned enclosure: {enclosure.name}")
                    print(f"🧹 Cleaned {enclosure.name}")
        
        if cleaned_count == 0:
            print("✅ All enclosures are already clean!")
        
        return cleaned_count
    
    def buy_food(self) -> bool:
        """Purchase food supplies."""
        if not self._zoo:
            raise ZooError("No zoo created yet")
        
        try:
            self._zoo.order_supplies()
            self._log_event("Purchased food supplies")
            return True
        except FinancialError as e:
            print(f"❌ Cannot buy food: {e}")
            return False
    
    def get_available_animals(self) -> List[str]:
        """Get list of animals that can be purchased."""
        return AnimalFactory.get_available_species()
    
    def get_zoo_status(self) -> Dict:
        """Get comprehensive zoo status."""
        if not self._zoo:
            return {}
        return self._zoo.get_zoo_status()
    
    def get_health_alerts(self) -> List[str]:
        """Get current health alerts."""
        return self._health_monitor.get_critical_animals()
    
    def advance_day(self) -> Dict:
        """
        Advance simulation by one day with event system integration.
        
        Returns:
            Dictionary with day results
        """
        if not self._zoo:
            raise ZooError("No zoo created yet")
        
        self._day_count += 1
        self._log_event(f"Advanced to day {self._day_count}")
        
        print(f"\n{'='*50}")
        print(f"🌅 DAY {self._day_count} MORNING REPORT")
        print(f"{'='*50}")
        
        # TRIGGER DAILY EVENTS BEFORE ZOO UPDATE
        daily_events = self._event_manager.trigger_daily_events(self)
        event_messages = []
        
        if daily_events:
            print(f"\n📢 TODAY'S SPECIAL EVENTS:")
            for event_data in daily_events:
                event = event_data['event']
                result = event_data['result']
                
                print(f"   {event}")
                for message in result.get('messages', []):
                    print(f"     • {message}")
                    event_messages.append(message)
                
                # Log event impacts
                if 'financial_impact' in result:
                    impact = result['financial_impact']
                    if impact > 0:
                        self._log_event(f"Event: Gained ${impact} from {event.name}")
                    elif impact < 0:
                        self._log_event(f"Event: Lost ${-impact} from {event.name}")
        
        else:
            print("   🌤️  It's a quiet day at the zoo...")

        # Run daily zoo update (this handles visitors, costs, etc.)
        self._zoo.daily_update()
        
        # Generate daily animal behavior events
        behavior_events = self._generate_daily_events()
        
        # Check for critical issues
        critical_animals = self.get_health_alerts()

        return {
            'day': self._day_count,
            'special_events': daily_events,
            'event_messages': event_messages,
            'behavior_events': behavior_events,
            'critical_animals': critical_animals,
            'zoo_status': self.get_zoo_status()
        }
    
    def _generate_daily_events(self) -> List[str]:
        """Generate random daily events."""
        if not self._zoo:
            return []
        
        events = []
        status = self.get_zoo_status()
        
        # Animal behavior events
        for enclosure in status['enclosures']:
            for animal_info in enclosure['animals']:
                animal_name = animal_info['name']
                
                # Happiness events
                if animal_info['happiness'] > 80:
                    happy_events = [
                        f"{animal_name} is playing happily!",
                        f"{animal_name} seems very content today.",
                        f"{animal_name} is entertaining the visitors!"
                    ]
                    events.append(random.choice(happy_events))
                
                # Hunger events
                elif animal_info['hunger'] > 70:
                    hungry_events = [
                        f"{animal_name} looks very hungry.",
                        f"{animal_name} is searching for food.",
                        f"{animal_name} seems restless and hungry."
                    ]
                    events.append(random.choice(hungry_events))
                
                # Health events
                elif animal_info['health'] < 50:
                    health_events = [
                        f"{animal_name} doesn't look well.",
                        f"{animal_name} seems weaker than usual.",
                        f"{animal_name} needs medical attention."
                    ]
                    events.append(random.choice(health_events))
        
        # Zoo-wide events
        if status['financials']['daily_income'] > 1000:
            events.append("🎉 Great visitor turnout today!")
        
        if any(enclosure['needs_cleaning'] for enclosure in status['enclosures']):
            events.append("⚠️  Some enclosures need cleaning.")
        
        # Limit events to avoid overwhelming the player
        return events[:5]  # Max 5 events per day
    
    def _log_event(self, event: str) -> None:
        """Add event to game log."""
        self._events_log.append(f"Day {self._day_count}: {event}")
    
    def get_recent_events(self, count: int = 5) -> List[str]:
        """Get recent game events."""
        return self._events_log[-count:] if self._events_log else []
    
    @property
    def zoo(self) -> Optional[Zoo]:
        """Get current zoo instance."""
        return self._zoo
    
    @property
    def day_count(self) -> int:
        """Get current day count."""
        return self._day_count
    
    def is_game_over(self) -> bool:
        """Check if game should end."""
        if not self._zoo:
            return True
        
        status = self.get_zoo_status()
        return status['financials']['funds'] <= 0
    
    def get_event_statistics(self) -> Dict:
        """Get statistics about events that have occurred."""
        today_events = self._event_manager.get_today_events()
        return {
            'events_today': len(today_events),
            'today_events': [
                {
                    'name': event_data['event'].name,
                    'type': event_data['event'].event_type.value,
                    'severity': event_data['event'].severity.value
                }
                for event_data in today_events
            ]
        }