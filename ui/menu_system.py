"""
Enhanced CLI menu system with colored interface and better user experience.
Maintains OOP separation - only calls backend methods.
"""

from core.game_manager import ZooManager
from core.factory import AnimalFactory
from core.exceptions import ZooError, FinancialError, CompatibilityError
from ui.display import Display
from colorama import Style, Fore
from typing import Optional, List, Dict
import sys

class MenuSystem:
    """
    Enhanced CLI menu system with colored interface and formatted output.
    """
    
    def __init__(self, zoo_manager: ZooManager):
        """Initialize menu system with zoo manager."""
        self._zoo_manager = zoo_manager
        self._display = Display()
    
    def display_main_menu(self) -> None:
        """Display the enhanced main game menu."""
        Display.clear_screen()
        
        # Print fancy header
        print(f"{Display.COLORS['header']}{'🦁' * 20}")
        print(f"      OZZOO - ZOO SIMULATION GAME")
        print(f"{'🦁' * 20}{Style.RESET_ALL}")
        
        # Quick stats line
        if self._zoo_manager.zoo:
            Display.print_quick_stats(self._zoo_manager)
        
        # Main menu options
        menu_options = [
            {
                'key': '1',
                'label': '📊 View Detailed Zoo Status',
                'description': 'Comprehensive zoo overview with statistics'
            },
            {
                'key': '2', 
                'label': '🐾 Add New Animal',
                'description': 'Purchase and place a new animal'
            },
            {
                'key': '3',
                'label': '🍽️  Feed Animals', 
                'description': 'Feed animals in specific or all enclosures'
            },
            {
                'key': '4',
                'label': '🧹 Clean Enclosures',
                'description': 'Clean dirty habitats'
            },
            {
                'key': '5',
                'label': '📦 Buy Food & Supplies',
                'description': 'Restock food and medicine'
            },
            {
                'key': '6', 
                'label': '🌅 Advance to Next Day',
                'description': 'Progress simulation and see events'
            },
            {
                'key': '7',
                'label': '📜 View Recent Events',
                'description': 'See what happened recently'
            },
            {
                'key': '8',
                'label': '🚨 Health Alerts',
                'description': 'Check animal health status'
            },
            {
                'key': '9',
                'label': '❌ Exit Game',
                'description': 'Save and exit OzZoo'
            }
        ]
        
        Display.print_menu("MAIN MENU", menu_options)
        print(f"{Display.COLORS['menu_item']}Enter your choice (1-9): {Style.RESET_ALL}", end="")
    
    def display_zoo_status(self) -> None:
        """Display enhanced zoo status with colors and formatting."""
        status = self._zoo_manager.get_zoo_status()
        Display.print_zoo_status(status)
        Display.wait_for_enter()
    
    def display_add_animal_menu(self) -> None:
        """Display enhanced menu for adding new animals."""
        if not self._zoo_manager.zoo:
            Display.print_error("Please create a zoo first!")
            Display.wait_for_enter()
            return
        
        Display.clear_screen()
        Display.print_header("🐾 ADD NEW ANIMAL")
        
        # Show available animals
        available_animals = self._zoo_manager.get_available_animals()
        Display.print_section("AVAILABLE SPECIES", 'info')
        print(f"{Fore.CYAN}{', '.join(available_animals)}{Style.RESET_ALL}")
        
        try:
            # Get animal details with validation
            animal_type = input(f"\n{Display.COLORS['menu_item']}Enter animal type: {Style.RESET_ALL}").strip()
            if animal_type not in available_animals:
                Display.print_error(f"Unknown animal type. Available: {', '.join(available_animals)}")
                Display.wait_for_enter()
                return
            
            name = input(f"{Display.COLORS['menu_item']}Enter animal name: {Style.RESET_ALL}").strip()
            if not name:
                Display.print_error("Animal name cannot be empty!")
                Display.wait_for_enter()
                return
            
            age = int(input(f"{Display.COLORS['menu_item']}Enter animal age (years): {Style.RESET_ALL}"))
            if age < 0 or age > 50:
                Display.print_error("Please enter a reasonable age (0-50)!")
                Display.wait_for_enter()
                return
            
            # Show available enclosures
            status = self._zoo_manager.get_zoo_status()
            Display.print_section("AVAILABLE ENCLOSURES", 'enclosure')
            
            enclosure_options = []
            for i, enclosure in enumerate(status['enclosures'], 1):
                occupancy = f"{enclosure['animal_count']}/{enclosure['capacity']}"
                cleanliness = "✨" if enclosure['cleanliness'] > 70 else "✅" if enclosure['cleanliness'] > 40 else "🧹"
                enclosure_options.append({
                    'key': str(i),
                    'label': f"{enclosure['name']} ({occupancy} animals) {cleanliness}",
                    'description': f"Type: {enclosure['type']}, Cleanliness: {enclosure['cleanliness']:.1f}%"
                })
            
            Display.print_menu("SELECT ENCLOSURE", enclosure_options)
            
            enclosure_choice = input(f"{Display.COLORS['menu_item']}Select enclosure (number): {Style.RESET_ALL}").strip()
            
            # Find enclosure
            selected_enclosure = None
            try:
                enclosure_index = int(enclosure_choice) - 1
                if 0 <= enclosure_index < len(status['enclosures']):
                    selected_enclosure = status['enclosures'][enclosure_index]['name']
            except ValueError:
                Display.print_error("Please enter a valid number!")
                Display.wait_for_enter()
                return
            
            if not selected_enclosure:
                Display.print_error("Invalid enclosure selection!")
                Display.wait_for_enter()
                return
            
            # Add the animal
            success = self._zoo_manager.add_animal_to_zoo(
                animal_type, name, age, selected_enclosure
            )
            
            if success:
                Display.print_success(f"{name} the {animal_type} added successfully!")
            else:
                Display.print_error(f"Failed to add {name}.")
        
        except ValueError:
            Display.print_error("Please enter a valid number for age!")
        except Exception as e:
            Display.print_error(f"Error: {e}")
        
        Display.wait_for_enter()
    
    def display_feed_animals_menu(self) -> None:
        """Display enhanced menu for feeding animals."""
        if not self._zoo_manager.zoo:
            Display.print_error("Please create a zoo first!")
            Display.wait_for_enter()
            return
        
        Display.clear_screen()
        Display.print_header("🍽️  FEED ANIMALS")
        
        status = self._zoo_manager.get_zoo_status()
        
        menu_options = [
            {
                'key': '1',
                'label': 'Feed All Animals',
                'description': 'Feed all animals in all enclosures'
            },
            {
                'key': '2', 
                'label': 'Feed Specific Enclosure',
                'description': 'Choose which enclosure to feed'
            },
            {
                'key': '3',
                'label': 'Back to Main Menu',
                'description': 'Return to main menu'
            }
        ]
        
        Display.print_menu("FEEDING OPTIONS", menu_options)
        
        try:
            choice = input(f"{Display.COLORS['menu_item']}Enter your choice (1-3): {Style.RESET_ALL}").strip()
            
            if choice == "1":
                results = self._zoo_manager.feed_animals()
                self._display_feeding_results(results)
            elif choice == "2":
                self._display_enclosure_selection_menu("feed")
            elif choice == "3":
                return
            else:
                Display.print_error("Invalid choice!")
        
        except Exception as e:
            Display.print_error(f"Error: {e}")
        
        Display.wait_for_enter()
    
    def _display_feeding_results(self, results: Dict) -> None:
        """Display formatted feeding results."""
        if not results:
            Display.print_error("No feeding results available!")
            return
        
        total_fed = 0
        Display.print_section("FEEDING RESULTS", 'info')
        
        for enclosure, enclosure_results in results.items():
            fed_count = len(enclosure_results.get('successful', []))
            total_fed += fed_count
            
            if fed_count > 0:
                Display.print_success(f"Fed {fed_count} animals in {enclosure}")
                
                # Show some individual feeding results
                successful_feeds = enclosure_results.get('successful', [])[:2]
                for feed_msg in successful_feeds:
                    print(f"   {Fore.LIGHTGREEN_EX}✓ {feed_msg}{Style.RESET_ALL}")
        
        if total_fed == 0:
            Display.print_error("No animals were fed. Check food supplies!")
        else:
            Display.print_success(f"Successfully fed {total_fed} animals total!")
    
    def _display_enclosure_selection_menu(self, action: str) -> None:
        """Display menu for selecting enclosures for various actions."""
        status = self._zoo_manager.get_zoo_status()
        
        Display.print_section("SELECT ENCLOSURE", 'enclosure')
        
        enclosure_options = []
        for i, enclosure in enumerate(status['enclosures'], 1):
            animal_count = enclosure['animal_count']
            enclosure_options.append({
                'key': str(i),
                'label': f"{enclosure['name']} ({animal_count} animals)",
                'description': f"Type: {enclosure['type']}, Cleanliness: {enclosure['cleanliness']:.1f}%"
            })
        
        Display.print_menu(f"SELECT ENCLOSURE TO {action.upper()}", enclosure_options)
        
        enclosure_choice = input(f"{Display.COLORS['menu_item']}Select enclosure (number): {Style.RESET_ALL}").strip()
        
        try:
            enclosure_index = int(enclosure_choice) - 1
            if 0 <= enclosure_index < len(status['enclosures']):
                selected_enclosure = status['enclosures'][enclosure_index]['name']
                
                if action == "feed":
                    results = self._zoo_manager.feed_animals(selected_enclosure)
                    self._display_feeding_results({selected_enclosure: results})
                elif action == "clean":
                    cleaned = self._zoo_manager.clean_enclosures(selected_enclosure)
                    if cleaned > 0:
                        Display.print_success(f"Cleaned {selected_enclosure}!")
                    else:
                        Display.print_warning(f"{selected_enclosure} is already clean!")
            else:
                Display.print_error("Invalid enclosure selection!")
        except ValueError:
            Display.print_error("Please enter a valid number!")
    
    def display_clean_enclosures_menu(self) -> None:
        """Display enhanced menu for cleaning enclosures."""
        if not self._zoo_manager.zoo:
            Display.print_error("Please create a zoo first!")
            Display.wait_for_enter()
            return
        
        Display.clear_screen()
        Display.print_header("🧹 CLEAN ENCLOSURES")
        
        status = self._zoo_manager.get_zoo_status()
        
        # Find dirty enclosures
        dirty_enclosures = [
            enclosure for enclosure in status['enclosures'] 
            if enclosure['needs_cleaning']
        ]
        
        if not dirty_enclosures:
            Display.print_success("All enclosures are clean! 🎉")
            Display.wait_for_enter()
            return
        
        Display.print_section("DIRTY ENCLOSURES NEEDING CLEANING", 'warning')
        for enclosure in dirty_enclosures:
            cleanliness = enclosure['cleanliness']
            if cleanliness < 20:
                clean_color = Fore.RED
                urgency = "URGENT"
            elif cleanliness < 40:
                clean_color = Fore.YELLOW
                urgency = "Needs cleaning"
            else:
                clean_color = Fore.LIGHTYELLOW_EX
                urgency = "Could use cleaning"
            
            print(f"  {clean_color}🧹 {enclosure['name']} - {cleanliness:.1f}% ({urgency}){Style.RESET_ALL}")
        
        menu_options = [
            {
                'key': '1',
                'label': 'Clean All Dirty Enclosures',
                'description': f'Clean all {len(dirty_enclosures)} dirty enclosures'
            },
            {
                'key': '2',
                'label': 'Clean Specific Enclosure',
                'description': 'Choose which enclosure to clean'
            },
            {
                'key': '3',
                'label': 'Back to Main Menu',
                'description': 'Return to main menu'
            }
        ]
        
        Display.print_menu("CLEANING OPTIONS", menu_options)
        
        try:
            choice = input(f"{Display.COLORS['menu_item']}Enter your choice (1-3): {Style.RESET_ALL}").strip()
            
            if choice == "1":
                cleaned = self._zoo_manager.clean_enclosures()
                Display.print_success(f"Cleaned {cleaned} enclosures!")
            elif choice == "2":
                self._display_enclosure_selection_menu("clean")
            elif choice == "3":
                return
            else:
                Display.print_error("Invalid choice!")
        
        except Exception as e:
            Display.print_error(f"Error: {e}")
        
        Display.wait_for_enter()
    
    def display_health_alerts(self) -> None:
        """Display enhanced health alerts."""
        critical_animals = self._zoo_manager.get_health_alerts()
        Display.clear_screen()
        Display.print_header("🚨 HEALTH MONITOR")
        Display.print_health_alerts(critical_animals)
        Display.wait_for_enter()
    
    def display_recent_events(self) -> None:
        """Display enhanced recent events view."""
        events = self._zoo_manager.get_recent_events()
        Display.clear_screen()
        Display.print_header("📜 RECENT EVENTS")
        
        if not events:
            Display.print_info("No recent events to display.")
        else:
            for event in events[-10:]:  # Show last 10 events
                print(f"• {event}")
        
        Display.wait_for_enter()
    
    def handle_main_menu_choice(self, choice: str) -> bool:
        """
        Process user menu selection with enhanced feedback.
        
        Returns:
            True if should continue, False if should exit
        """
        try:
            if choice == "1":
                self.display_zoo_status()
            elif choice == "2":
                self.display_add_animal_menu()
            elif choice == "3":
                self.display_feed_animals_menu()
            elif choice == "4":
                self.display_clean_enclosures_menu()
            elif choice == "5":
                if self._zoo_manager.buy_food():
                    Display.print_success("Food supplies purchased!")
                else:
                    Display.print_error("Failed to purchase food!")
                Display.wait_for_enter()
            elif choice == "6":
                self._handle_advance_day()
            elif choice == "7":
                self.display_recent_events()
            elif choice == "8":
                self.display_health_alerts()
            elif choice == "9":
                Display.print_success("Thanks for playing OzZoo! 👋")
                return False
            else:
                Display.print_error("Invalid choice! Please enter 1-9.")
                Display.wait_for_enter()
            
            return True
            
        except Exception as e:
            Display.print_error(f"Unexpected error: {e}")
            Display.wait_for_enter()
            return True
    
    def _handle_advance_day(self) -> None:
        """Handle day advancement with enhanced display."""
        try:
            day_results = self._zoo_manager.advance_day()
            
            # Show special events
            if day_results['special_events']:
                Display.print_event_summary(day_results['special_events'])
            
            # Show behavior events
            if day_results['behavior_events']:
                Display.print_section("ANIMAL BEHAVIOR", 'animal')
                for event in day_results['behavior_events'][:5]:  # Show first 5
                    print(f"• {event}")
            
            # Show critical animals
            if day_results['critical_animals']:
                Display.print_health_alerts(day_results['critical_animals'])
            
            # Check for game over
            if self._zoo_manager.is_game_over():
                Display.print_header("💀 GAME OVER", 50)
                Display.print_error("Your zoo has run out of funds!")
                Display.print_info("Better luck next time!")
                Display.wait_for_enter()
                return False
            
        except Exception as e:
            Display.print_error(f"Error advancing day: {e}")
        
        Display.wait_for_enter()
    
    def run(self) -> None:
        """Run the enhanced main game loop."""
        # Initial zoo creation
        if not self._zoo_manager.zoo:
            self._create_initial_zoo()
        
        # Main game loop
        running = True
        while running:
            try:
                self.display_main_menu()
                choice = input().strip()
                running = self.handle_main_menu_choice(choice)
                
            except KeyboardInterrupt:
                Display.print_success("\n\nThanks for playing OzZoo! 👋")
                break
            except Exception as e:
                Display.print_error(f"Unexpected error: {e}")
                Display.wait_for_enter()
    
    def _create_initial_zoo(self) -> None:
        """Create initial zoo setup with enhanced interface."""
        Display.clear_screen()
        Display.print_header("🎮 WELCOME TO OZZOO!")
        Display.print_section("CREATE YOUR DREAM ZOO", 'header')
        
        while True:
            try:
                zoo_name = input(f"\n{Display.COLORS['menu_item']}Enter your zoo name: {Style.RESET_ALL}").strip()
                if not zoo_name:
                    Display.print_error("Zoo name cannot be empty!")
                    continue
                
                initial_funds = 50000.0
                self._zoo_manager.create_zoo(zoo_name, initial_funds)
                break
                
            except Exception as e:
                Display.print_error(f"Error creating zoo: {e}")
        
        Display.print_success(f"Zoo '{zoo_name}' created with ${initial_funds:,.2f}!")
        Display.print_info("💡 Tip: Start by adding some animals and feeding them daily.")
        Display.wait_for_enter("Press Enter to start managing your zoo...")