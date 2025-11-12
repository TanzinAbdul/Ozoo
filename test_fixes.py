"""
Test script to verify the import fixes.
"""

try:
    from zoo.enclosure import Enclosure
    from core.factory import AnimalFactory
    from core.exceptions import ResourceError
    from typing import Dict
    
    print("✅ All imports successful!")
    print("✅ ResourceError is properly defined")
    print("✅ Dict type is properly imported")
    
    # Test creating an enclosure
    enclosure = Enclosure("Test Enclosure", 3, "savannah")
    print("✅ Enclosure creation works")
    
    # Test factory
    animals = AnimalFactory.get_available_species()
    print(f"✅ Factory works. Available animals: {animals}")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")