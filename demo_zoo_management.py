"""
Demonstration script for Zoo, Enclosure, and ResourceManager functionality.
"""

from zoo.zoo import Zoo
from zoo.enclosure import Enclosure
from animals.species.lion import Lion
from animals.species.eagle import Eagle
from animals.species.snake import Snake
from core.exceptions import CompatibilityError, FinancialError

def demonstrate_zoo_management():
    """Demonstrate zoo management functionality."""
    
    print("=== OZZOO ZOO MANAGEMENT DEMONSTRATION ===\n")
    
    # Create zoo
    ozzoo = Zoo("OzZoo Wildlife Park", initial_funds=50000.0)
    print(f"🦁 Created {ozzoo.name} with ${ozzoo.funds:.2f} initial funds\n")
    
    # Create enclosures
    savannah = Enclosure("Savannah Plains", 3, "savannah", ["Lion"])
    aviary = Enclosure("Eagle's Peak", 2, "aviary", ["Eagle"])
    reptile_house = Enclosure("Reptile House", 4, "forest", ["Snake", "Lizard"])
    
    # Add enclosures to zoo
    ozzoo.add_enclosure(savannah)
    ozzoo.add_enclosure(aviary)
    ozzoo.add_enclosure(reptile_house)
    
    # Create animals
    simba = Lion("Simba", 5, is_male=True, pride_leader=True)
    nala = Lion("Nala", 4, is_male=False, pride_leader=False)
    baldy = Eagle("Baldy", 3, wingspan=2.5)
    slinky = Snake("Slinky", 2, length=1.8, is_venomous=True)
    
    print("\n1. ADDING ANIMALS TO ENCLOSURES:")
    # Add animals to appropriate enclosures
    ozzoo.add_animal(simba, "Savannah Plains")
    ozzoo.add_animal(nala, "Savannah Plains")
    ozzoo.add_animal(baldy, "Eagle's Peak")
    ozzoo.add_animal(slinky, "Reptile House")
    
    print("\n2. DEMONSTRATING COMPATIBILITY CHECKS:")
    # Try to add incompatible animal
    try:
        wrong_animal = Eagle("Wrongo", 2)
        ozzoo.add_animal(wrong_animal, "Savannah Plains")
    except CompatibilityError as e:
        print(f"❌ Compatibility error (expected): {e}")
    
    print("\n3. FEEDING ANIMALS:")
    # Feed animals
    feeding_results = ozzoo.feed_animals()
    for enclosure, results in feeding_results.items():
        print(f"   {enclosure}:")
        for category, messages in results.items():
            if messages:
                print(f"     {category.capitalize()}: {len(messages)} animals")
    
    print("\n4. ZOO STATUS:")
    status = ozzoo.get_zoo_status()
    print(f"   Animals: {status['animal_count']}")
    print(f"   Enclosures: {status['enclosure_count']}")
    print(f"   Funds: ${status['financials']['funds']:.2f}")
    
    print("\n5. DAILY UPDATE SIMULATION:")
    ozzoo.daily_update()
    
    print("\n6. ORDERING SUPPLIES:")
    ozzoo.order_supplies()
    
    print("\n7. FINAL ZOO STATUS:")
    final_status = ozzoo.get_zoo_status()
    print(f"   Days Operational: {final_status['days_operational']}")
    print(f"   Total Visitors: {final_status['total_visitors']}")
    print(f"   Current Funds: ${final_status['financials']['funds']:.2f}")
    
    print("\n8. ENCLOSURE DETAILS:")
    for enclosure in final_status['enclosures']:
        print(f"   {enclosure['name']}: {enclosure['animal_count']} animals, "
              f"Cleanliness: {enclosure['cleanliness']:.1f}%")

if __name__ == "__main__":
    demonstrate_zoo_management()