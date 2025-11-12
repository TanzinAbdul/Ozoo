"""
Debug script to identify why animal creation is failing.
"""

from core.game_manager import ZooManager
from core.factory import AnimalFactory
from core.exceptions import ZooError, CompatibilityError

def debug_animal_creation():
    """Debug the animal creation process."""
    
    print("🔍 DEBUGGING ANIMAL CREATION PROCESS")
    print("=" * 50)
    
    # Create zoo manager
    manager = ZooManager()
    manager.create_zoo("Debug Zoo", 50000.0)
    
    # Test 1: Check if factory works
    print("\n1. TESTING ANIMAL FACTORY...")
    try:
        lion = AnimalFactory.create_animal("lion", "TestLion", 1, is_male=True)
        print(f"✅ Factory created: {lion.name} the {lion.species}")
        print(f"   Health: {lion.health}, Hunger: {lion.hunger}, Happiness: {lion.happiness}")
    except Exception as e:
        print(f"❌ Factory failed: {e}")
        return
    
    # Test 2: Check enclosure status
    print("\n2. CHECKING ENCLOSURE STATUS...")
    status = manager.get_zoo_status()
    for enclosure in status['enclosures']:
        print(f"   {enclosure['name']}: {enclosure['animal_count']}/{enclosure['capacity']} animals")
        print(f"   Compatible species: {enclosure.get('_compatible_species', 'Not set')}")
    
    # Test 3: Try to add animal with detailed error handling
    print("\n3. ATTEMPTING TO ADD ANIMAL...")
    try:
        success = manager.add_animal_to_zoo("lion", "loly", 1, "Savannah Plains", is_male=True)
        print(f"✅ Add animal result: {success}")
        
        if not success:
            print("❌ Animal addition failed silently")
            
    except CompatibilityError as e:
        print(f"❌ Compatibility error: {e}")
        print(f"   Animal species: {e.animal1_species}")
        print(f"   Existing species: {e.animal2_species}")
    except ZooError as e:
        print(f"❌ Zoo error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 4: Check final status
    print("\n4. FINAL ZOO STATUS...")
    status = manager.get_zoo_status()
    print(f"   Total animals: {status['animal_count']}")
    for enclosure in status['enclosures']:
        print(f"   {enclosure['name']}: {enclosure['animal_count']} animals")

if __name__ == "__main__":
    debug_animal_creation()