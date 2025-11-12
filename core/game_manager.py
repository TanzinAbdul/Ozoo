"""
Enhanced Zoo Manager with complete game loop and simulation engine.
Refactored for both CLI and Streamlit compatibility.
"""

from zoo.zoo import Zoo
from zoo.enclosure import Enclosure
from core.observer import HealthMonitor, ObservableAnimal
from core.events import EventManager
from core.factory import AnimalFactory
from core.exceptions import ZooError, FinancialError, EnclosureError, CompatibilityError
from typing import Optional, List, Dict
import random

class ZooManager:
    """
    Central manager for the zoo simulation game with complete game loop.
    Works with both CLI and Streamlit interfaces.
    """
    
    def __init__(self):
        """Initialize zoo manager with game state."""
        self._zoo: Optional[Zoo] = None
        self._running = False
        self._day_count = 0
        self._health_monitor = HealthMonitor()
        self._event_manager = EventManager()
        self._events_log: List[str] = []
    
    def create_zoo(self, name: str, initial_funds: float = 50000.0) -> str:
        """
        Create a new zoo with given name.
        
        Returns:
            Summary message string
        """
        self._zoo = Zoo(name, initial_funds)
        self._day_count = 0
        self._log_event(f"Created new zoo: {name} with ${initial_funds:.2f}")
        
        summary = f"🏰 Created zoo: {name} with ${initial_funds:.2f}"
        print(summary)
        
        # Create initial enclosures
        self._create_initial_enclosures()
        
        return summary
    
    def _create_initial_enclosures(self) -> List[str]:
        """
        Create starter enclosures for new zoo with proper compatible species.
        
        Returns:
            List of messages about created enclosures
        """
        if not self._zoo:
            return []
        
        messages = []
        enclosures = [
            ("Savannah Plains", 3, "savannah", ["Lion", "Elephant", "Zebra", "Giraffe"]),
            ("Eagle's Peak", 2, "aviary", ["Eagle", "Bird"]),
            ("Reptile House", 4, "forest", ["Snake", "Lizard", "Reptile"]),
            ("Penguin Pool", 3, "arctic", ["Penguin"]),
        ]
        
        for name, capacity, env_type, compatible_species in enclosures:
            enclosure = Enclosure(name, capacity, env_type, compatible_species)
            self._zoo.add_enclosure(enclosure)
            
            msg = f"🏠 Added {name} with compatible species: {compatible_species}"
            print(msg)
            messages.append(msg)
        
        return messages
    
    def create_animal_with_factory(self, animal_type: str, name: str, age: int, **kwargs) -> ObservableAnimal:
        """Create animal using Factory Pattern and make it observable."""
        print(f"🔧 Factory creating: {animal_type} named {name}")
        
        try:
            base_animal = AnimalFactory.create_animal(animal_type, name, age, **kwargs)
            print(f"✅ Base animal created: {base_animal.name} the {base_animal.species}")
            
            # Convert to observable animal
            observable_animal = ObservableAnimal(
                name=base_animal.name,
                species=base_animal.species,
                age=base_animal.age,
                diet=base_animal.diet,
                habitat=base_animal.habitat
            )
            
            # Copy internal state
            health_diff = base_animal.health - 100.0
            observable_animal._modify_health(health_diff)
            observable_animal._modify_hunger(base_animal.hunger - 0.0)
            observable_animal._modify_happiness(base_animal.happiness - 100.0)
            
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
                         enclosure_name: str, **kwargs) -> Dict:
        """
        Add an animal to the zoo.
        
        Returns:
            Dict with 'success' (bool) and 'message' (str)
        """
        if not self._zoo:
            raise ZooError("No zoo created yet")
        
        print(f"🐾 Adding {animal_type} '{name}' to {enclosure_name}")
        
        try:
            # Use factory directly
            animal = AnimalFactory.create_animal(animal_type, name, age, **kwargs)
            print(f"✅ Animal created: {animal.name}")
            
            # Add to zoo enclosure
            success = self._zoo.add_animal(animal, enclosure_name)
            print(f"✅ Add result: {success}")
            
            if success:
                self._log_event(f"Added {name} the {animal_type} to {enclosure_name}")
                msg = f"🎉 Successfully added {name} the {animal_type} to {enclosure_name}!"
                print(msg)
                return {"success": True, "message": msg}
            else:
                msg = f"❌ Failed to add {name}. Check compatibility or enclosure space."
                print(msg)
                return {"success": False, "message": msg}
            
        except Exception as e:
            msg = f"❌ Error: {e}"
            print(msg)
            import traceback
            traceback.print_exc()
            return {"success": False, "message": msg}
            
    def feed_animals(self, enclosure_name: str = None) -> Dict:
        """
        Feed animals and return structured feedback (CLI + UI friendly).
        
        Returns:
            Dict with 'total_fed' (int) and 'messages' (list of strings)
        """
        if not self._zoo:
            raise ZooError("No zoo created yet")
        
        messages = []
        total_fed = 0
        
        try:
            results = self._zoo.feed_animals(enclosure_name)
            self._log_event(f"Fed animals in {enclosure_name or 'all enclosures'}")
            
            # Provide user feedback
            for enclosure, enclosure_results in results.items():
                fed_count = len(enclosure_results.get('successful', []))
                total_fed += fed_count
                
                if fed_count > 0:
                    msg = f"🍽️  Fed {fed_count} animals in {enclosure}"
                    print(msg)
                    messages.append(msg)
                    
                    # Show some individual feeding results
                    successful_feeds = enclosure_results.get('successful', [])[:2]
                    for feed_msg in successful_feeds:
                        print(f"   {feed_msg}")
                        messages.append(f"   {feed_msg}")
            
            if total_fed == 0:
                msg = "❌ No animals were fed. Check food supplies!"
                print(msg)
                messages.append(msg)
            else:
                msg = f"✅ Successfully fed {total_fed} animals total"
                print(msg)
                messages.append(msg)
            
            return {"total_fed": total_fed, "messages": messages}
            
        except Exception as e:
            msg = f"❌ Feeding failed: {e}"
            print(msg)
            messages.append(msg)
            return {"total_fed": 0, "messages": messages}
    
    def clean_enclosures(self, enclosure_name: str = None) -> Dict:
        """
        Clean specific enclosure or all enclosures.
        
        Returns:
            Dict with 'cleaned_count' (int) and 'messages' (list of strings)
        """
        if not self._zoo:
            raise ZooError("No zoo created yet")
        
        cleaned_count = 0
        messages = []
        
        if enclosure_name:
            # Clean specific enclosure
            for enclosure in self._zoo._enclosures:
                if enclosure.name == enclosure_name:
                    if enclosure.needs_cleaning():
                        enclosure.clean()
                        cleaned_count += 1
                        self._log_event(f"Cleaned enclosure: {enclosure_name}")
                        msg = f"🧹 Cleaned {enclosure_name}"
                        print(msg)
                        messages.append(msg)
                    else:
                        msg = f"✅ {enclosure_name} is already clean enough"
                        print(msg)
                        messages.append(msg)
                    break
        else:
            # Clean all dirty enclosures
            for enclosure in self._zoo._enclosures:
                if enclosure.needs_cleaning():
                    enclosure.clean()
                    cleaned_count += 1
                    self._log_event(f"Cleaned enclosure: {enclosure.name}")
                    msg = f"🧹 Cleaned {enclosure.name}"
                    print(msg)
                    messages.append(msg)
        
        if cleaned_count == 0 and not enclosure_name:
            msg = "✅ All enclosures are already clean!"
            print(msg)
            messages.append(msg)
        
        return {"cleaned_count": cleaned_count, "messages": messages}
    
    def buy_food(self) -> Dict:
        """
        Purchase food supplies.
        
        Returns:
            Dict with 'success' (bool) and 'message' (str)
        """
        if not self._zoo:
            raise ZooError("No zoo created yet")
        
        try:
            self._zoo.order_supplies()
            self._log_event("Purchased food supplies")
            msg = "🛒 Food supplies purchased successfully!"
            print(msg)
            return {"success": True, "message": msg}
        except FinancialError as e:
            msg = f"❌ Cannot buy food: {e}"
            print(msg)
            return {"success": False, "message": msg}
    
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
            Dictionary with day results including all messages for UI display
        """
        if not self._zoo:
            raise ZooError("No zoo created yet")
        
        self._day_count += 1
        self._log_event(f"Advanced to day {self._day_count}")
        
        messages = []
        
        # Day header
        header = f"\n{'='*50}\n🌅 DAY {self._day_count} MORNING REPORT\n{'='*50}"
        print(header)
        messages.append(f"🌅 DAY {self._day_count} MORNING REPORT")
        
        # TRIGGER DAILY EVENTS BEFORE ZOO UPDATE
        daily_events = self._event_manager.trigger_daily_events(self)
        event_messages = []
        
        if daily_events:
            event_header = "\n📢 TODAY'S SPECIAL EVENTS:"
            print(event_header)
            messages.append("📢 TODAY'S SPECIAL EVENTS:")
            
            for event_data in daily_events:
                event = event_data['event']
                result = event_data['result']
                
                event_msg = f"   {event}"
                print(event_msg)
                messages.append(event.name)
                
                for message in result.get('messages', []):
                    detail_msg = f"     • {message}"
                    print(detail_msg)
                    messages.append(f"  • {message}")
                    event_messages.append(message)
                
                # Log event impacts
                if 'financial_impact' in result:
                    impact = result['financial_impact']
                    if impact > 0:
                        self._log_event(f"Event: Gained ${impact} from {event.name}")
                    elif impact < 0:
                        self._log_event(f"Event: Lost ${-impact} from {event.name}")
        else:
            quiet_msg = "   🌤️  It's a quiet day at the zoo..."
            print(quiet_msg)
            messages.append("🌤️  It's a quiet day at the zoo...")

        # Run daily zoo update (this handles visitors, costs, etc.)
        self._zoo.daily_update()
        
        # Generate daily animal behavior events
        behavior_events = self._generate_daily_events()
        
        if behavior_events:
            messages.append("\n📋 Daily Events:")
            for event in behavior_events:
                print(f"   {event}")
                messages.append(event)
        
        # Check for critical issues
        critical_animals = self.get_health_alerts()
        
        if critical_animals:
            messages.append("\n⚠️  Health Alerts:")
            for alert in critical_animals:
                print(f"   ⚠️  {alert}")
                messages.append(f"⚠️  {alert}")

        return {
            'day': self._day_count,
            'messages': messages,
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
    
    # ============ NEW HELPER METHODS FOR STREAMLIT UI ============
    
    def get_summary_text(self) -> str:
        """
        Get plain-text summary for UI display.
        
        Returns:
            Human-readable summary string
        """
        if not self._zoo:
            return "No zoo created yet."
        
        status = self._zoo.get_zoo_status()
        funds = status["financials"]["funds"]
        enclosures = len(status["enclosures"])
        animals = sum(len(e["animals"]) for e in status["enclosures"])
        
        return f"Zoo has {animals} animals in {enclosures} enclosures. Funds: ${funds:.2f}"
    
    def get_enclosure_names(self) -> List[str]:
        """
        List enclosure names for UI dropdowns.
        
        Returns:
            List of enclosure names
        """
        if not self._zoo:
            return []
        return [e.name for e in self._zoo._enclosures]
    
    def serialize_status(self) -> Dict:
        """
        Return a JSON-ready summary for UI or API.
        
        Returns:
            Dict with key metrics
        """
        if not self._zoo:
            return {
                "day": self._day_count,
                "funds": 0,
                "num_enclosures": 0,
                "num_animals": 0,
            }
        
        return {
            "day": self._day_count,
            "funds": self._zoo._funds,
            "num_enclosures": len(self._zoo._enclosures),
            "num_animals": sum(len(e.animals) for e in self._zoo._enclosures),
        }