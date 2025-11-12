"""
Debug the ZooManager.add_animal_to_zoo method specifically.
"""

from core.game_manager import ZooManager

def debug_manager_method():
    """Debug the manager's add_animal_to_zoo method."""
    
    print("🔍 DEBUGGING ZOO MANAGER METHOD")
    print("=" * 50)
    
    manager = ZooManager()
    manager.create_zoo("Manager Debug Zoo", 50000.0)
    
    print("\n1. CALLING add_animal_to_zoo WITH DEBUG...")
    
    # Let's add detailed debugging to the manager method temporarily
    success = manager.add_animal_to_zoo("lion", "ManagerLion", 1, "Savannah Plains", is_male=True)
    
    print(f"\n2. FINAL RESULT: {success}")
    
    # Check what actually happened
    status = manager.get_zoo_status()
    print(f"\n3. ACTUAL ZOO STATUS:")
    print(f"   Total animals: {status['animal_count']}")
    for enclosure in status['enclosures']:
        animals = [animal['name'] for animal in enclosure['animals']]
        print(f"   {enclosure['name']}: {animals}")

if __name__ == "__main__":
    debug_manager_method()