"""
Demonstration script for the Event System.
"""

from core.game_manager import ZooManager
from core.events import EventManager, ZooEvent, EventType, EventSeverity

class CustomSpecialEvent(ZooEvent):
    """Custom event example to demonstrate extensibility."""
    
    def __init__(self):
        super().__init__(
            name="VIP Visit",
            description="A celebrity visits your zoo!",
            severity=EventSeverity.POSITIVE,
            probability=0.10,
            event_type=EventType.SPECIAL
        )
    
    def trigger(self, zoo_manager):
        zoo = zoo_manager.zoo
        if not zoo:
            return {'success': False}
        
        # VIP visit brings lots of visitors and money
        visitor_boost = 200
        donation = 5000
        
        zoo._resource_manager.add_funds(donation, "VIP donation")
        
        return {
            'success': True,
            'messages': [
                f"🌟 Celebrity visit brought {visitor_boost} extra visitors!",
                f"💰 VIP donated ${donation:,} to your zoo!"
            ],
            'visitor_impact': visitor_boost,
            'financial_impact': donation
        }

def demonstrate_event_system():
    """Demonstrate the event system in action."""
    
    print("🎭 OZZOO EVENT SYSTEM DEMONSTRATION")
    print("Simulating 5 days with random events...\n")
    
    manager = ZooManager()
    manager.create_zoo("Event Test Zoo", 100000.0)
    
    # Add some animals
    print("🐾 Setting up zoo with animals...")
    manager.add_animal_to_zoo("lion", "Simba", 4, "Savannah Plains", is_male=True)
    manager.add_animal_to_zoo("elephant", "Dumbo", 6, "Savannah Plains")
    manager.add_animal_to_zoo("eagle", "Sky", 2, "Eagle's Peak")
    
    # Add custom event
    custom_event = CustomSpecialEvent()
    manager._event_manager.add_custom_event(custom_event)
    print("✅ Added custom VIP Visit event")
    
    print(f"\n{'='*60}")
    print("STARTING 5-DAY SIMULATION WITH EVENTS")
    print(f"{'='*60}")
    
    for day in range(1, 6):
        print(f"\n--- DAY {day} ---")
        
        # Advance day (this triggers events)
        day_results = manager.advance_day()
        
        # Show event statistics
        event_stats = manager.get_event_statistics()
        print(f"📊 Events today: {event_stats['events_today']}")
        
        # Show zoo status
        status = manager.get_zoo_status()
        print(f"💰 Funds: ${status['financials']['funds']:.2f}")
        print(f"🐾 Animals: {status['animal_count']}")
        print(f"🎟️  Total Visitors: {status['total_visitors']}")
    
    print(f"\n{'='*60}")
    print("SIMULATION COMPLETE!")
    print(f"{'='*60}")
    
    final_status = manager.get_zoo_status()
    print(f"📈 Final Statistics:")
    print(f"   Days Operated: {manager.day_count}")
    print(f"   Total Visitors: {final_status['total_visitors']}")
    print(f"   Final Funds: ${final_status['financials']['funds']:.2f}")
    print(f"   Animals: {final_status['animal_count']}")
    
    print(f"\n🎭 EVENT SYSTEM FEATURES DEMONSTRATED:")
    features = [
        "✅ Polymorphic Event System - Different event types with unique behaviors",
        "✅ Probability-based Triggering - Events occur based on configured probabilities", 
        "✅ Impact System - Events affect funds, visitors, animal stats",
        "✅ Extensibility - Easy to add new custom events",
        "✅ Daily Variety - 1-3 random events per day",
        "✅ Severity Levels - Positive, Negative, Neutral, Critical events",
        "✅ Event Categories - Weather, Animal, Financial, Visitor events"
    ]
    
    for feature in features:
        print(f"   {feature}")

if __name__ == "__main__":
    demonstrate_event_system()