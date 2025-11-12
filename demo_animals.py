"""
Demonstration script showing the animal hierarchy in action.
"""

from animals.species.lion import Lion
from animals.species.eagle import Eagle
from animals.species.snake import Snake

def demonstrate_animal_hierarchy():
    """Demonstrate polymorphism and inheritance in animal hierarchy."""
    
    # Create different animals
    simba = Lion("Simba", 5, is_male=True, pride_leader=True)
    baldy = Eagle("Baldy", 3, wingspan=2.5)
    slinky = Snake("Slinky", 2, length=1.8, is_venomous=True)
    
    animals = [simba, baldy, slinky]
    
    print("=== OZZOO ANIMAL HIERARCHY DEMONSTRATION ===\n")
    
    # Demonstrate polymorphism - same method, different behaviors
    print("1. POLYMORPHISM - make_sound():")
    for animal in animals:
        print(f"   {animal.name}: {animal.make_sound()}")
    
    print("\n2. POLYMORPHISM - eat('meat'):")
    for animal in animals:
        result = animal.eat("meat")
        print(f"   {animal.name}: {result}")
    
    print("\n3. ENCAPSULATION - Accessing private attributes via properties:")
    for animal in animals:
        info = animal.get_info()
        print(f"   {animal.name} - Health: {animal.health:.1f}%, "
              f"Hunger: {animal.hunger:.1f}%, Happiness: {animal.happiness:.1f}%")
    
    print("\n4. DAILY STATUS UPDATE - Simulating one day:")
    for animal in animals:
        print(f"\n   Before update - {animal.name}:")
        print(f"     Health: {animal.health:.1f}%, Hunger: {animal.hunger:.1f}%")
        animal.update_daily_status()
        print(f"   After update - {animal.name}:")
        print(f"     Health: {animal.health:.1f}%, Hunger: {animal.hunger:.1f}%")
    
    print("\n5. SPECIFIC BEHAVIORS:")
    print(f"   {simba.name}: {simba.hunt()}")
    print(f"   {baldy.name}: {baldy.soar()}")
    print(f"   {slinky.name}: {slinky.slither()}")

if __name__ == "__main__":
    demonstrate_animal_hierarchy()