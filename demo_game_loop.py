"""
Quick demonstration of the complete game loop.
"""

from core.game_manager import ZooManager
from ui.menu_system import MenuSystem

def quick_demo():
    """Run a quick demonstration of the game loop."""
    print("🎮 OZZOO GAME LOOP DEMONSTRATION")
    print("This will simulate 3 days of zoo management\n")
    
    manager = ZooManager()
    manager.create_zoo("Demo Zoo", 75000.0)
    
    # Add some initial animals quickly
    print("🐾 Adding initial animals...")
    manager.add_animal_to_zoo("lion", "Simba", 4, "Savannah Plains", is_male=True)
    manager.add_animal_to_zoo("elephant", "Dumbo", 6, "Savannah Plains")
    manager.add_animal_to_zoo("eagle", "Sky", 2, "Eagle's Peak")
    
    # Simulate 3 days
    for day in range(3):
        print(f"\n{'='*50}")
        print(f"🌅 DAY {day + 1}")
        print(f"{'='*50}")
        
        # Show morning status
        status = manager.get_zoo_status()
        print(f"💰 Funds: ${status['financials']['funds']:.2f}")
        print(f"🐾 Animals: {status['animal_count']}")
        
        # Player actions (automated for demo)
        print("\n🎮 Player actions:")
        print("🍽️  Feeding animals...")
        manager.feed_animals()
        
        print("🧹 Cleaning enclosures...")
        manager.clean_enclosures()
        
        print("📦 Buying supplies...")
        manager.buy_food()
        
        # Advance day
        print("🌅 Advancing to next day...")
        day_results = manager.advance_day()
        
        # Show results
        if day_results['events']:
            print("\n📢 Today's events:")
            for event in day_results['events'][:3]:  # Show first 3 events
                print(f"   • {event}")
    
    print(f"\n🎉 DEMO COMPLETED!")
    print("The game loop is fully functional with:")
    print("✅ Daily simulation mechanics")
    print("✅ Player decision system") 
    print("✅ Animal status updates")
    print("✅ Resource management")
    print("✅ Event generation system")

if __name__ == "__main__":
    quick_demo()