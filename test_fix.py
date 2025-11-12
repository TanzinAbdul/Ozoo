"""
Test script to verify the animal creation fix.
"""

from core.game_manager import ZooManager

def test_fixed_animal_creation():
    """Test if animal creation works after fixes."""
    
    print("🧪 TESTING FIXED ANIMAL CREATION")
    print("=" * 50)
    
    manager = ZooManager()
    manager.create_zoo("Test Zoo", 50000.0)
    
    # Check enclosure setup
    print("\n1. CHECKING ENCLOSURE SETUP...")
    status = manager.get_zoo_status()
    for enclosure in status['enclosures']:
        print(f"   {enclosure['name']}: {enclosure.get('compatible_species', 'Not set')}")
    
    # Try to add animal
    print("\n2. ADDING ANIMAL...")
    success = manager.add_animal_to_zoo("lion", "loly", 1, "Savannah Plains", is_male=True)
    
    print(f"\n3. RESULT: {'✅ SUCCESS' if success else '❌ FAILED'}")
    
    # Check final status
    print("\n4. FINAL STATUS:")
    status = manager.get_zoo_status()
    print(f"   Total animals: {status['animal_count']}")
    for enclosure in status['enclosures']:
        animals = [animal['name'] for animal in enclosure['animals']]
        print(f"   {enclosure['name']}: {animals}")

if __name__ == "__main__":
    test_fixed_animal_creation()