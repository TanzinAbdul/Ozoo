"""
Observer Pattern implementation for health monitoring and notifications.
Demonstrates behavioral pattern for event-driven communication.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from animals.animal import Animal, DietType  # ADD DietType IMPORT
from core.exceptions import ZooError

class Subject(ABC):
    """
    Subject interface for Observer Pattern.
    Objects that can be observed should implement this.
    """
    
    @abstractmethod
    def attach(self, observer: 'Observer') -> None:
        """Attach an observer to the subject."""
        pass
    
    @abstractmethod
    def detach(self, observer: 'Observer') -> None:
        """Detach an observer from the subject."""
        pass
    
    @abstractmethod
    def notify(self, event: str, data: Dict[str, Any] = None) -> None:
        """Notify all observers about an event."""
        pass

class Observer(ABC):
    """
    Observer interface for Observer Pattern.
    Objects that want to receive notifications should implement this.
    """
    
    @abstractmethod
    def update(self, subject: Subject, event: str, data: Dict[str, Any] = None) -> None:
        """
        Receive update from subject.
        
        Args:
            subject: The subject that triggered the update
            event: Type of event that occurred
            data: Additional event data
        """
        pass

class HealthMonitor(Observer):
    """
    Health monitor that watches animal health and triggers alerts.
    Now uses dependency injection instead of direct ZooManager reference.
    """
    
    def __init__(self):
        # Remove direct ZooManager dependency - use dependency injection instead
        self._critical_animals = set()
        self._alert_history = []
    
    def update(self, subject: Subject, event: str, data: Dict[str, Any] = None) -> None:
        """
        Handle updates from observed animals.
        """
        data = data or {}
        
        if event == "health_critical":
            self._handle_health_critical(subject, data)
        elif event == "health_improved":
            self._handle_health_improved(subject, data)
        elif event == "animal_died":
            self._handle_animal_died(subject, data)
    
    def _handle_health_critical(self, animal: 'ObservableAnimal', data: Dict[str, Any]) -> None:
        """Handle critical health alerts."""
        animal_id = f"{animal.name}_{animal.species}"
        self._critical_animals.add(animal_id)
        
        alert_message = (
            f"🚨 CRITICAL HEALTH: {animal.name} the {animal.species} "
            f"health dropped to {data['new_health']:.1f}%!"
        )
        
        self._alert_history.append({
            'type': 'critical_health',
            'animal': animal.name,
            'species': animal.species,
            'health': data['new_health'],
            'timestamp': 'now'  # In real implementation, use datetime
        })
        
        print(f"🔔 {alert_message} Immediate medical attention required!")
        
        # In a full implementation, this would trigger UI alerts, emails, etc.
    
    def _handle_health_improved(self, animal: 'ObservableAnimal', data: Dict[str, Any]) -> None:
        """Handle health improvement notifications."""
        animal_id = f"{animal.name}_{animal.species}"
        if animal_id in self._critical_animals:
            self._critical_animals.remove(animal_id)
        
        alert_message = (
            f"✅ HEALTH IMPROVED: {animal.name} the {animal.species} "
            f"health improved to {data['new_health']:.1f}%"
        )
        
        self._alert_history.append({
            'type': 'health_improved',
            'animal': animal.name,
            'species': animal.species,
            'health': data['new_health'],
            'timestamp': 'now'
        })
        
        print(f"🔔 {alert_message}")
    
    def _handle_animal_died(self, animal: 'ObservableAnimal', data: Dict[str, Any]) -> None:
        """Handle animal death notifications."""
        animal_id = f"{animal.name}_{animal.species}"
        if animal_id in self._critical_animals:
            self._critical_animals.remove(animal_id)
        
        alert_message = (
            f"💀 ANIMAL DIED: {animal.name} the {animal.species} "
            f"has died. Cause: {data.get('cause', 'unknown')}"
        )
        
        self._alert_history.append({
            'type': 'animal_died',
            'animal': animal.name,
            'species': animal.species,
            'cause': data.get('cause', 'unknown'),
            'timestamp': 'now'
        })
        
        print(f"🔔 {alert_message}")
    
    def get_critical_animals(self) -> List[str]:
        """Get list of animals with critical health."""
        return list(self._critical_animals)
    
    def get_alert_history(self) -> List[Dict]:
        """Get history of health alerts."""
        return self._alert_history.copy()

class ObservableAnimal(Animal, Subject):
    """
    Observable animal that notifies observers about important events.
    Extends Animal with Subject capabilities.
    
    Why Observer Pattern improves modularity:
    1. Loose Coupling: Subjects don't know concrete observers
    2. Dynamic Relationships: Observers can be added/removed at runtime
    3. Broadcast Communication: One event can notify multiple observers
    4. Separation of Concerns: Monitoring logic separated from animal logic
    """
    
    def __init__(self, name: str, species: str, age: int, diet: DietType, habitat: str):
        """Initialize observable animal with observer list."""
        super().__init__(name, species, age, diet, habitat)
        self._observers: List[Observer] = []
        self._health_threshold = 30.0  # Notify when health drops below this
    
    def attach(self, observer: Observer) -> None:
        """Attach an observer to this animal."""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"🔍 Attached health monitor to {self.name}")
    
    def detach(self, observer: Observer) -> None:
        """Detach an observer from this animal."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, event: str, data: Dict[str, Any] = None) -> None:
        """Notify all observers about an event."""
        data = data or {}
        for observer in self._observers:
            observer.update(self, event, data)
    
    def _modify_health(self, amount: float) -> None:
        """
        Override health modification to include notifications.
        """
        old_health = self.health
        super()._modify_health(amount)
        new_health = self.health
        
        # Notify on significant health changes
        if new_health <= self._health_threshold and old_health > self._health_threshold:
            self.notify("health_critical", {
                'old_health': old_health,
                'new_health': new_health,
                'threshold': self._health_threshold
            })
        
        # Notify on health improvement from critical state
        elif new_health > self._health_threshold and old_health <= self._health_threshold:
            self.notify("health_improved", {
                'old_health': old_health,
                'new_health': new_health,
                'threshold': self._health_threshold
            })
        
        # Notify on death
        elif new_health <= 0 and old_health > 0:
            self.notify("animal_died", {
                'cause': 'health_depleted',
                'final_health': new_health
            })