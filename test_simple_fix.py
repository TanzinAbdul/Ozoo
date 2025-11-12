"""
Test the simplified fix.
"""

from core.game_manager import ZooManager

def test_simple_fix():
    """Test the simplified animal addition."""
    
    print("🧪 TESTING SIMPLIFIED FIX")
    print("=" * 50)
    
    manager = ZooManager()
    manager.create_zoo("Simple Fix Zoo", 50000.0)
    
    # Test the simplified method (if added)
    print("\n1. TESTING SIMPLIFIED METHOD...")
    try:
        # If you added the simplified method, use it:
        # success = manager.add_animal_to_zoo_simple("lion", "SimpleLion", 1, "Savannah Plains", is_male=True)
        
        # Otherwise use the fixed main method:
        success = manager.add_animal_to_zoo("lion", "SimpleLion", 1, "Savannah Plains", is_male=True)
        
        print(f"✅ Result: {success}")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    # Check results
    status = manager.get_zoo_status()
    print(f"\n2. FINAL STATUS:")
    print(f"   Total animals: {status['animal_count']}")
    for enclosure in status['enclosures']:
        animals = [animal['name'] for animal in enclosure['animals']]
        print(f"   {enclosure['name']}: {animals}")

if __name__ == "__main__":
    test_simple_fix()