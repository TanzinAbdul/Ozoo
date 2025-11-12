"""
Event System for OzZoo - Random daily events with polymorphic outcomes.
Demonstrates polymorphism and event-driven game mechanics.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from enum import Enum
import random

class EventType(Enum):
    """Types of events that can occur in the zoo."""
    WEATHER = "weather"
    ANIMAL = "animal"
    FINANCIAL = "financial"
    VISITOR = "visitor"
    SPECIAL = "special"

class EventSeverity(Enum):
    """Severity levels for events."""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    CRITICAL = "critical"

class ZooEvent(ABC):
    """
    Abstract base class for all zoo events.
    Demonstrates polymorphism through different event implementations.
    """
    
    def __init__(self, name: str, description: str, event_type: EventType, 
                 severity: EventSeverity, probability: float):
        """
        Initialize a zoo event.
        
        Args:
            name: Event name
            description: Event description
            event_type: Type of event
            severity: Severity level
            probability: Chance of occurring (0.0 to 1.0)
        """
        self.name = name
        self.description = description
        self.event_type = event_type
        self.severity = severity
        self.probability = probability
        self._occurred_today = False
    
    @abstractmethod
    def trigger(self, zoo_manager) -> Dict:
        """
        Trigger the event and apply its effects.
        
        Args:
            zoo_manager: The zoo manager to apply effects to
            
        Returns:
            Dictionary with event results and messages
        """
        pass
    
    def should_occur(self) -> bool:
        """
        Check if this event should occur based on probability.
        
        Returns:
            True if event should occur
        """
        return random.random() < self.probability and not self._occurred_today
    
    def reset(self) -> None:
        """Reset event for new day."""
        self._occurred_today = False
    
    def get_emoji(self) -> str:
        """Get emoji representation based on severity."""
        emoji_map = {
            EventSeverity.POSITIVE: "✨",
            EventSeverity.NEUTRAL: "ℹ️",
            EventSeverity.NEGATIVE: "⚠️",
            EventSeverity.CRITICAL: "🚨"
        }
        return emoji_map.get(self.severity, "📢")
    
    def __str__(self) -> str:
        return f"{self.get_emoji()} {self.name}: {self.description}"

# =============================================================================
# WEATHER EVENTS
# =============================================================================

class WeatherEvent(ZooEvent):
    """Base class for weather-related events."""
    
    def __init__(self, name: str, description: str, severity: EventSeverity, probability: float):
        super().__init__(name, description, EventType.WEATHER, severity, probability)

class HeatwaveEvent(WeatherEvent):
    """Heatwave event - affects animal happiness and health."""
    
    def __init__(self):
        super().__init__(
            name="Heatwave",
            description="A severe heatwave hits the zoo!",
            severity=EventSeverity.NEGATIVE,
            probability=0.15
        )
    
    def trigger(self, zoo_manager) -> Dict:
        """Trigger heatwave effects."""
        zoo = zoo_manager.zoo
        if not zoo:
            return {'success': False, 'message': 'No zoo to affect'}
        
        messages = []
        health_impact = 0
        happiness_impact = 0
        
        # Affect all animals
        for enclosure in zoo._enclosures:
            for animal in enclosure.animals:
                # Animals lose health and happiness in heatwave
                health_loss = random.uniform(5.0, 15.0)
                happiness_loss = random.uniform(10.0, 25.0)
                
                animal._modify_health(-health_loss)
                animal._modify_happiness(-happiness_loss)
                
                health_impact += health_loss
                happiness_impact += happiness_loss
        
        messages.append("🌡️ Animals are suffering from the heat! Health and happiness decreased.")
        
        # Visitors decrease in bad weather
        visitor_loss = random.randint(20, 50)
        messages.append(f"☀️ Visitor numbers dropped by {visitor_loss} due to extreme heat.")
        
        self._occurred_today = True
        return {
            'success': True,
            'messages': messages,
            'health_impact': -health_impact,
            'happiness_impact': -happiness_impact,
            'visitor_impact': -visitor_loss
        }

class PerfectWeatherEvent(WeatherEvent):
    """Perfect weather event - boosts visitor numbers and animal happiness."""
    
    def __init__(self):
        super().__init__(
            name="Perfect Weather",
            description="The weather is absolutely perfect today!",
            severity=EventSeverity.POSITIVE,
            probability=0.20
        )
    
    def trigger(self, zoo_manager) -> Dict:
        """Trigger perfect weather effects."""
        zoo = zoo_manager.zoo
        if not zoo:
            return {'success': False, 'message': 'No zoo to affect'}
        
        messages = []
        happiness_impact = 0
        
        # Boost animal happiness
        for enclosure in zoo._enclosures:
            for animal in enclosure.animals:
                happiness_gain = random.uniform(10.0, 20.0)
                animal._modify_happiness(happiness_gain)
                happiness_impact += happiness_gain
        
        messages.append("☀️ Animals are enjoying the beautiful weather! Happiness increased.")
        
        # Increase visitors
        visitor_boost = random.randint(30, 80)
        messages.append(f"🌤️ Visitor numbers increased by {visitor_boost} due to perfect weather!")
        
        self._occurred_today = True
        return {
            'success': True,
            'messages': messages,
            'happiness_impact': happiness_impact,
            'visitor_impact': visitor_boost
        }

class RainyDayEvent(WeatherEvent):
    """Rainy day event - mixed effects."""
    
    def __init__(self):
        super().__init__(
            name="Rainy Day",
            description="It's raining heavily at the zoo.",
            severity=EventSeverity.NEUTRAL,
            probability=0.25
        )
    
    def trigger(self, zoo_manager) -> Dict:
        """Trigger rainy day effects."""
        zoo = zoo_manager.zoo
        if not zoo:
            return {'success': False, 'message': 'No zoo to affect'}
        
        messages = []
        
        # Some animals love rain, some don't
        for enclosure in zoo._enclosures:
            for animal in enclosure.animals:
                if animal.species in ["Elephant", "Penguin"]:
                    # These animals enjoy rain
                    animal._modify_happiness(15.0)
                    messages.append(f"💧 {animal.name} the {animal.species} is enjoying the rain!")
                else:
                    # Most animals don't like rain
                    animal._modify_happiness(-8.0)
        
        # Visitors decrease
        visitor_loss = random.randint(10, 30)
        messages.append(f"🌧️ Visitor numbers decreased by {visitor_loss} due to rain.")
        
        # Enclosures get cleaner from rain
        for enclosure in zoo._enclosures:
            cleanliness_boost = random.uniform(5.0, 15.0)
            enclosure._cleanliness = min(100.0, enclosure._cleanliness + cleanliness_boost)
        
        messages.append("💦 Rain naturally cleaned the enclosures!")
        
        self._occurred_today = True
        return {
            'success': True,
            'messages': messages,
            'visitor_impact': -visitor_loss
        }

# =============================================================================
# ANIMAL EVENTS
# =============================================================================

class AnimalEvent(ZooEvent):
    """Base class for animal-related events."""
    
    def __init__(self, name: str, description: str, severity: EventSeverity, probability: float):
        super().__init__(name, description, EventType.ANIMAL, severity, probability)

class AnimalBirthEvent(AnimalEvent):
    """Animal birth event - new animal is born."""
    
    def __init__(self):
        super().__init__(
            name="Animal Birth",
            description="A new animal is born in the zoo!",
            severity=EventSeverity.POSITIVE,
            probability=0.10
        )
    
    def trigger(self, zoo_manager) -> Dict:
        """Trigger animal birth."""
        zoo = zoo_manager.zoo
        if not zoo:
            return {'success': False, 'message': 'No zoo to affect'}
        
        # Find enclosures with animals that could have babies
        potential_parents = []
        for enclosure in zoo._enclosures:
            for animal in enclosure.animals:
                if animal.age >= 2:  # Adults can have babies
                    potential_parents.append((enclosure, animal))
        
        if not potential_parents:
            return {'success': False, 'message': 'No adult animals for birth event'}
        
        # Select random parent
        enclosure, parent = random.choice(potential_parents)
        
        # Create baby animal
        baby_name = self._generate_baby_name(parent.name)
        baby_species = parent.species
        
        try:
            # Use factory to create baby
            baby = zoo_manager.create_animal_with_factory(
                baby_species.lower(), baby_name, 0  # Age 0 for baby
            )
            
            # Add to parent's enclosure
            success = enclosure.add_animal(baby)
            
            if success:
                message = f"🎉 {parent.name} gave birth to {baby_name} the baby {baby_species}!"
                self._occurred_today = True
                
                # Boost happiness for all animals in enclosure
                for animal in enclosure.animals:
                    animal._modify_happiness(10.0)
                
                return {
                    'success': True,
                    'messages': [message, f"🎊 Animals in {enclosure.name} are celebrating!"],
                    'new_animal': baby_name,
                    'species': baby_species
                }
            else:
                return {'success': False, 'message': 'Could not add baby to enclosure'}
                
        except Exception as e:
            return {'success': False, 'message': f'Birth failed: {e}'}
    
    def _generate_baby_name(self, parent_name: str) -> str:
        """Generate a cute baby name based on parent name."""
        suffixes = ["Junior", "II", "Little", "Baby"]
        prefixes = ["Little ", "Tiny ", "Baby "]
        
        if random.random() > 0.5:
            return f"{parent_name} {random.choice(suffixes)}"
        else:
            return f"{random.choice(prefixes)}{parent_name}"

class AnimalEscapeEvent(AnimalEvent):
    """Animal escape event - negative event with financial impact."""
    
    def __init__(self):
        super().__init__(
            name="Animal Escape",
            description="An animal has escaped from its enclosure!",
            severity=EventSeverity.CRITICAL,
            probability=0.08
        )
    
    def trigger(self, zoo_manager) -> Dict:
        """Trigger animal escape."""
        zoo = zoo_manager.zoo
        if not zoo:
            return {'success': False, 'message': 'No zoo to affect'}
        
        # Find animals that could escape
        potential_escapers = []
        for enclosure in zoo._enclosures:
            for animal in enclosure.animals:
                if animal.happiness < 40.0:  # Unhappy animals more likely to escape
                    potential_escapers.append((enclosure, animal))
        
        if not potential_escapers:
            return {'success': False, 'message': 'No unhappy animals to escape'}
        
        # Select random animal to escape
        enclosure, escapee = random.choice(potential_escapers)
        
        # Remove animal from enclosure
        enclosure.remove_animal(escapee.name)
        
        # Financial penalty
        penalty = random.randint(500, 2000)
        zoo._resource_manager.spend_funds(penalty, "escape recovery")
        
        # Visitor impact
        visitor_loss = random.randint(50, 100)
        
        messages = [
            f"🚨 {escapee.name} the {escapee.species} escaped from {enclosure.name}!",
            f"💰 ${penalty} spent on recovery efforts.",
            f"🎟️ Visitor numbers decreased by {visitor_loss} due to safety concerns."
        ]
        
        self._occurred_today = True
        return {
            'success': True,
            'messages': messages,
            'financial_impact': -penalty,
            'visitor_impact': -visitor_loss,
            'lost_animal': escapee.name
        }

# =============================================================================
# FINANCIAL EVENTS
# =============================================================================

class FinancialEvent(ZooEvent):
    """Base class for financial events."""
    
    def __init__(self, name: str, description: str, severity: EventSeverity, probability: float):
        super().__init__(name, description, EventType.FINANCIAL, severity, probability)

class GenerousDonorEvent(FinancialEvent):
    """Generous donor event - large financial donation."""
    
    def __init__(self):
        super().__init__(
            name="Generous Donor",
            description="A wealthy donor makes a generous contribution!",
            severity=EventSeverity.POSITIVE,
            probability=0.12
        )
    
    def trigger(self, zoo_manager) -> Dict:
        """Trigger donor event."""
        zoo = zoo_manager.zoo
        if not zoo:
            return {'success': False, 'message': 'No zoo to affect'}
        
        # Larger donation for more established zoos
        base_donation = random.randint(1000, 5000)
        zoo_bonus = zoo_manager.day_count * 10  # $10 per day of operation
        total_donation = base_donation + zoo_bonus
        
        zoo._resource_manager.add_funds(total_donation, "generous donation")
        
        message = f"💰 Generous donor contributed ${total_donation:,} to the zoo!"
        
        self._occurred_today = True
        return {
            'success': True,
            'messages': [message],
            'financial_impact': total_donation
        }

class UnexpectedExpenseEvent(FinancialEvent):
    """Unexpected expense event - negative financial impact."""
    
    def __init__(self):
        super().__init__(
            name="Unexpected Expense",
            description="An unexpected maintenance cost arises.",
            severity=EventSeverity.NEGATIVE,
            probability=0.18
        )
    
    def trigger(self, zoo_manager) -> Dict:
        """Trigger unexpected expense."""
        zoo = zoo_manager.zoo
        if not zoo:
            return {'success': False, 'message': 'No zoo to affect'}
        
        expense = random.randint(300, 1200)
        
        try:
            zoo._resource_manager.spend_funds(expense, "unexpected maintenance")
            message = f"🔧 Unexpected maintenance cost: ${expense}"
            
            self._occurred_today = True
            return {
                'success': True,
                'messages': [message],
                'financial_impact': -expense
            }
        except FinancialError:
            message = f"❌ Could not pay ${expense} expense - insufficient funds!"
            return {
                'success': False,
                'messages': [message],
                'financial_impact': 0
            }

# =============================================================================
# VISITOR EVENTS
# =============================================================================

class VisitorEvent(ZooEvent):
    """Base class for visitor-related events."""
    
    def __init__(self, name: str, description: str, severity: EventSeverity, probability: float):
        super().__init__(name, description, EventType.VISITOR, severity, probability)

class SchoolTripEvent(VisitorEvent):
    """School trip event - large visitor boost."""
    
    def __init__(self):
        super().__init__(
            name="School Trip",
            description="A large school group visits the zoo!",
            severity=EventSeverity.POSITIVE,
            probability=0.15
        )
    
    def trigger(self, zoo_manager) -> Dict:
        """Trigger school trip event."""
        zoo = zoo_manager.zoo
        if not zoo:
            return {'success': False, 'message': 'No zoo to affect'}
        
        visitor_boost = random.randint(80, 150)
        message = f"🎒 School trip brought {visitor_boost} extra visitors!"
        
        self._occurred_today = True
        return {
            'success': True,
            'messages': [message],
            'visitor_impact': visitor_boost
        }

class ProtestEvent(VisitorEvent):
    """Animal rights protest event - negative visitor impact."""
    
    def __init__(self):
        super().__init__(
            name="Animal Rights Protest",
            description="Protesters are demonstrating outside the zoo.",
            severity=EventSeverity.NEGATIVE,
            probability=0.07
        )
    
    def trigger(self, zoo_manager) -> Dict:
        """Trigger protest event."""
        zoo = zoo_manager.zoo
        if not zoo:
            return {'success': False, 'message': 'No zoo to affect'}
        
        # Check if zoo has poor conditions (dirty enclosures, unhappy animals)
        poor_conditions = False
        for enclosure in zoo._enclosures:
            if enclosure.needs_cleaning():
                poor_conditions = True
                break
            for animal in enclosure.animals:
                if animal.happiness < 30.0:
                    poor_conditions = True
                    break
        
        if poor_conditions:
            visitor_loss = random.randint(60, 120)
            message = f"🚫 Animal rights protest reduced visitors by {visitor_loss}!"
            
            self._occurred_today = True
            return {
                'success': True,
                'messages': [message],
                'visitor_impact': -visitor_loss
            }
        else:
            # Zoo has good conditions, protest has little effect
            message = "🚫 Protest occurred but had little impact due to good animal care."
            return {
                'success': True,
                'messages': [message],
                'visitor_impact': -10  # Minimal impact
            }

# =============================================================================
# EVENT MANAGER
# =============================================================================

class EventManager:
    """
    Manages all zoo events and their triggering.
    """
    
    def __init__(self):
        """Initialize event manager with all possible events."""
        self._events: List[ZooEvent] = [
            # Weather events
            HeatwaveEvent(),
            PerfectWeatherEvent(),
            RainyDayEvent(),
            
            # Animal events
            AnimalBirthEvent(),
            AnimalEscapeEvent(),
            
            # Financial events
            GenerousDonorEvent(),
            UnexpectedExpenseEvent(),
            
            # Visitor events
            SchoolTripEvent(),
            ProtestEvent(),
        ]
        
        self._today_events: List[Dict] = []
    
    def trigger_daily_events(self, zoo_manager) -> List[Dict]:
        """
        Trigger random events for the day.
        
        Args:
            zoo_manager: The zoo manager
            
        Returns:
            List of event results
        """
        self._today_events.clear()
        
        # Reset all events
        for event in self._events:
            event.reset()
        
        # Trigger 1-3 random events per day
        num_events = random.randint(1, 3)
        triggered_events = 0
        
        # Shuffle events for random selection
        random.shuffle(self._events)
        
        for event in self._events:
            if triggered_events >= num_events:
                break
                
            if event.should_occur():
                result = event.trigger(zoo_manager)
                if result.get('success', False):
                    self._today_events.append({
                        'event': event,
                        'result': result
                    })
                    triggered_events += 1
        
        return self._today_events
    
    def get_today_events(self) -> List[Dict]:
        """Get events that occurred today."""
        return self._today_events.copy()
    
    def add_custom_event(self, event: ZooEvent) -> None:
        """Add a custom event to the manager."""
        self._events.append(event)
    
    def get_available_events(self) -> List[ZooEvent]:
        """Get list of all available events."""
        return self._events.copy()