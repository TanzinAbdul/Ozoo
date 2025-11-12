"""
Demonstration script for the enhanced CLI interface.
"""

from core.game_manager import ZooManager
from ui.menu_system import MenuSystem

def demonstrate_enhanced_cli():
    """Demonstrate the enhanced CLI interface."""
    
    print("🎨 ENHANCED CLI INTERFACE DEMONSTRATION")
    print("This will show the improved user interface with colors and formatting\n")
    
    manager = ZooManager()
    manager.create_zoo("Demo Zoo", 75000.0)
    
    # Add some animals quickly
    print("🐾 Setting up demo zoo...")
    manager.add_animal_to_zoo("lion", "Simba", 4, "Savannah Plains", is_male=True)
    manager.add_animal_to_zoo("elephant", "Dumbo", 6, "Savannah Plains")
    manager.add_animal_to_zoo("eagle", "Sky", 2, "Eagle's Peak")
    
    # Create menu system
    menu_system = MenuSystem(manager)
    
    print("\n🎯 FEATURES DEMONSTRATED:")
    features = [
        "✅ Colored text output using Colorama",
        "✅ Formatted headers and sections", 
        "✅ Color-coded health and status indicators",
        "✅ Enhanced menu layouts with descriptions",
        "✅ Better error and success messaging",
        "✅ Visitor satisfaction metrics",
        "✅ Quick stats overview",
        "✅ Clear OOP separation (UI vs Business Logic)"
    ]
    
    for feature in features:
        print(f"   {feature}")
    
    print(f"\n🚀 Launching enhanced interface...")
    input("Press Enter to see the main menu...")
    
    # Show main menu (this will clear screen and show formatted interface)
    menu_system.display_main_menu()
    
    print(f"\n✨ Enhanced CLI is ready! The game now features:")
    print(f"   • Professional-looking interface")
    print(f"   • Color-coded feedback")
    print(f"   • Better user experience")
    print(f"   • Maintained OOP architecture")

if __name__ == "__main__":
    demonstrate_enhanced_cli()