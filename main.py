"""
Main entry point for OzZoo Zoo Simulation Game.
Features complete game loop with daily simulation mechanics.
"""

from core.game_manager import ZooManager
from ui.menu_system import MenuSystem
import sys

def main():
    """Initialize and run the zoo simulation."""
    try:
        print("🦁" * 20)
        print("      OZZOO - ZOO SIMULATION GAME")
        print("🦁" * 20)
        print("Loading game...")
        
        # Initialize game components
        zoo_manager = ZooManager()
        menu_system = MenuSystem(zoo_manager)
        
        # Start the game
        menu_system.run()
        
    except KeyboardInterrupt:
        print("\n\n👋 Thanks for playing OzZoo!")
    except Exception as e:
        print(f"❌ Critical error: {e}")
        print("Please restart the game.")
        sys.exit(1)

if __name__ == "__main__":
    main()