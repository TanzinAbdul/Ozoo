"""
Demonstration script for Factory and Observer patterns.
"""

from core.game_manager import ZooManager
from core.factory import AnimalFactory
from zoo.enclosure import Enclosure

def demonstrate_factory_pattern():
    """Demonstrate Factory Pattern for animal creation."""
    
    print("=== FACTORY PATTERN DEMONSTRATION ===\n")
    
    print("1. AVAILABLE ANIMAL SPECIES:")
    species = AnimalFactory.get_available_species()
    print(f"   Available: {', '.join(species)}")
    
    print("\n2. CREATING ANIMALS WITH FACTORY:")
    animals = []
    
    # Create different animals using factory
    animal_configs = [
        ('lion', 'Simba', 5, {'is_male': True, 'pride_leader': True}),
        ('eagle', 'Baldy', 3, {'wingspan': 2.5}),
        ('elephant', 'Dumbo', 8, {'tusk_length': 2.0}),
        ('penguin', 'Waddles', 2, {}),
        ('snake', 'Slinky', 4, {'is_venomous': False}),
    ]
    
    for animal_type, name, age, kwargs in animal_configs:
        try:
            animal = AnimalFactory.create_animal(animal_type, name, age, **kwargs)
            animals.append(animal)
            print(f"   ✅ Created {animal_type}: {animal.name} (Sound: {animal.make_sound()})")
        except Exception as e:
            print(f"   ❌ Failed to create {animal_type}: {e}")
    
    print("\n3. DEMONSTRATING EXTENSIBILITY:")
    # Show how easy it is to register new species
    try:
        from animals.species.lion import Lion
        AnimalFactory.register_animal('mountain_lion', Lion)
        print("   ✅ Registered new species: 'mountain_lion'")
        
        # Create with new type
        new_animal = AnimalFactory.create_animal('mountain_lion', 'Rocky', 4)
        print(f"   ✅ Created registered type: {new_animal.name}")
    except Exception as e:
        print(f"   ❌ Registration failed: {e}")
    
    return animals

def demonstrate_observer_pattern():
    """Demonstrate Observer Pattern for health monitoring."""
    
    print("\n=== OBSERVER PATTERN DEMONSTRATION ===\n")
    
    # Create zoo manager with both patterns
    manager = ZooManager()
    manager.create_zoo("Pattern Zoo", 50000.0)
    
    # Create enclosures
    savannah = Enclosure("Main Savannah", 5, "savannah", ["Lion", "Elephant", "Zebra"])
    aviary = Enclosure("Bird Sanctuary", 4, "aviary", ["Eagle", "Penguin"])
    reptile_house = Enclosure("Reptile Zone", 3, "forest", ["Snake"])
    
    manager.zoo.add_enclosure(savannah)
    manager.zoo.add_enclosure(aviary)
    manager.zoo.add_enclosure(reptile_house)
    
    print("1. CREATING OBSERVABLE ANIMALS:")
    # Add animals using the combined factory+observer approach
    animals_to_add = [
        ('lion', 'Leo', 4, 'Main Savannah', {'is_male': True}),
        ('elephant', 'Ellie', 6, 'Main Savannah', {}),
        ('eagle', 'Sky', 2, 'Bird Sanctuary', {}),
        ('penguin', 'Chilly', 1, 'Bird Sanctuary', {}),
        ('snake', 'Viper', 3, 'Reptile Zone', {'is_venomous': True}),
    ]
    
    for animal_type, name, age, enclosure, kwargs in animals_to_add:
        success = manager.add_animal_to_zoo(animal_type, name, age, enclosure, **kwargs)
        if not success:
            print(f"   ❌ Failed to add {name}")
    
    print("\n2. RUNNING SIMULATION WITH HEALTH MONITORING:")
    # Run simulation that will trigger health events
    manager.run_simulation(days=3)
    
    print("\n3. HEALTH MONITORING RESULTS:")
    manager.get_health_alerts()

def demonstrate_pattern_benefits():
    """Explain the benefits of both patterns."""
    
    print("\n=== DESIGN PATTERN BENEFITS ===\n")
    
    print("🏭 FACTORY PATTERN BENEFITS:")
    benefits_factory = [
        "1. 📦 CENTRALIZED CREATION: All animal creation logic in one place",
        "2. 🔗 DECOUPLING: Client code uses interfaces, not concrete classes", 
        "3. 🎯 EXTENSIBILITY: New species added without modifying existing code",
        "4. 🛡️ TYPE SAFETY: Compile-time checking of available species",
        "5. 🔧 CONFIGURABILITY: Easy to change creation logic centrally"
    ]
    
    for benefit in benefits_factory:
        print(f"   {benefit}")
    
    print("\n👀 OBSERVER PATTERN BENEFITS:")
    benefits_observer = [
        "1. 🔄 LOOSE COUPLING: Subjects and observers don't know each other",
        "2. 🎯 DYNAMIC RELATIONSHIPS: Observers can be added/removed at runtime",
        "3. 📡 BROADCAST COMMUNICATION: One event notifies multiple observers",
        "4. 🎨 SEPARATION OF CONCERNS: Monitoring logic separate from business logic",
        "5. 🔍 FLEXIBLE MONITORING: Different observers can watch for different events"
    ]
    
    for benefit in benefits_observer:
        print(f"   {benefit}")

if __name__ == "__main__":
    # Run all demonstrations
    demonstrate_factory_pattern()
    demonstrate_observer_pattern() 
    demonstrate_pattern_benefits()
    
    print("\n🎉 DESIGN PATTERNS SUCCESSFULLY IMPLEMENTED!")
    print("   The zoo simulation now demonstrates:")
    print("   ✅ Factory Pattern for flexible animal creation")
    print("   ✅ Observer Pattern for reactive health monitoring")
    print("   ✅ Improved modularity and extensibility")