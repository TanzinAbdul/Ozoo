"""
Detailed debug script to trace exactly where animal creation fails.
"""

from core.game_manager import ZooManager
from core.factory import AnimalFactory
from animals.species.lion import Lion
from zoo.enclosure import Enclosure

def debug_step_by_step():
    """Debug each step of the animal creation process."""
    
    print("🔍 DETAILED DEBUG - STEP BY STEP")
    print("=" * 60)
    
    # Step 1: Create zoo and enclosures
    print("\n1. CREATING ZOO AND ENCLOSURES...")
    manager = ZooManager()
    manager.create_zoo("Debug Zoo", 50000.0)
    
    # Step 2: Test direct Lion creation
    print("\n2. TESTING DIRECT LION CREATION...")
    try:
        lion = Lion("DebugLion", 1, is_male=True)
        print(f"✅ Direct Lion creation: {lion.name} the {lion.species}")
        print(f"   Health: {lion.health}, Habitat: {lion.habitat}")
    except Exception as e:
        print(f"❌ Direct Lion creation failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 3: Test factory creation
    print("\n3. TESTING FACTORY CREATION...")
    try:
        factory_lion = AnimalFactory.create_animal("lion", "FactoryLion", 1, is_male=True)
        print(f"✅ Factory creation: {factory_lion.name} the {factory_lion.species}")
    except Exception as e:
        print(f"❌ Factory creation failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 4: Test adding to enclosure directly
    print("\n4. TESTING DIRECT ENCLOSURE ADDITION...")
    try:
        # Get the Savannah Plains enclosure directly
        savannah = None
        for enclosure in manager.zoo._enclosures:
            if enclosure.name == "Savannah Plains":
                savannah = enclosure
                break
        
        if savannah:
            print(f"🔍 Found enclosure: {savannah.name}")
            print(f"   Capacity: {savannah._capacity}")
            print(f"   Current animals: {len(savannah._animals)}")
            print(f"   Compatible species: {savannah._compatible_species}")
            
            # Try to add the lion directly
            result = savannah.add_animal(lion)
            print(f"✅ Direct enclosure add result: {result}")
            
            if result:
                print(f"🎉 Success! Animals in enclosure: {[a.name for a in savannah._animals]}")
            else:
                print("❌ Direct enclosure add failed silently")
        else:
            print("❌ Could not find Savannah Plains enclosure")
            
    except Exception as e:
        print(f"❌ Direct enclosure add failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Step 5: Test the full manager method
    print("\n5. TESTING FULL MANAGER METHOD...")
    try:
        success = manager.add_animal_to_zoo("lion", "ManagerLion", 1, "Savannah Plains", is_male=True)
        print(f"✅ Manager add_animal_to_zoo result: {success}")
    except Exception as e:
        print(f"❌ Manager add_animal_to_zoo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_step_by_step()