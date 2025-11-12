"""
Enhanced Display Manager with colored output and formatted UI.
Uses Colorama for cross-platform colored text.
"""

import os
import sys
from typing import Dict, List, Any
from colorama import init, Fore, Back, Style

# Initialize colorama for cross-platform colored text
init(autoreset=True)

class Display:
    """
    Enhanced display manager for formatted, colored CLI output.
    Maintains OOP separation - only handles presentation logic.
    """
    
    # Color schemes for different message types
    COLORS = {
        'success': Fore.GREEN,
        'error': Fore.RED,
        'warning': Fore.YELLOW,
        'info': Fore.CYAN,
        'money': Fore.GREEN + Style.BRIGHT,
        'health_good': Fore.GREEN,
        'health_warning': Fore.YELLOW,
        'health_critical': Fore.RED + Style.BRIGHT,
        'header': Fore.MAGENTA + Style.BRIGHT,
        'menu_title': Fore.CYAN + Style.BRIGHT,
        'menu_item': Fore.WHITE,
        'animal': Fore.YELLOW,
        'enclosure': Fore.BLUE,
    }
    
    @staticmethod
    def clear_screen() -> None:
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header(title: str, width: int = 60) -> None:
        """
        Print a formatted header with color.
        
        Args:
            title: Header title
            width: Header width
        """
        color = Display.COLORS['header']
        print(f"\n{color}{'═' * width}")
        print(f"{title.center(width)}")
        print(f"{'═' * width}{Style.RESET_ALL}\n")
    
    @staticmethod
    def print_section(title: str, color: str = 'info') -> None:
        """
        Print a section header.
        
        Args:
            title: Section title
            color: Color key from COLORS
        """
        color_code = Display.COLORS.get(color, Fore.WHITE)
        print(f"\n{color_code}{Style.BRIGHT}▶ {title}{Style.RESET_ALL}")
    
    @staticmethod
    def print_success(message: str) -> None:
        """Print a success message."""
        print(f"{Display.COLORS['success']}✅ {message}")
    
    @staticmethod
    def print_error(message: str) -> None:
        """Print an error message."""
        print(f"{Display.COLORS['error']}❌ {message}")
    
    @staticmethod
    def print_warning(message: str) -> None:
        """Print a warning message."""
        print(f"{Display.COLORS['warning']}⚠️  {message}")
    
    @staticmethod
    def print_info(message: str) -> None:
        """Print an info message."""
        print(f"{Display.COLORS['info']}💡 {message}")
    
    @staticmethod
    def print_money(amount: float, context: str = "") -> None:
        """Print money amount with formatting."""
        color = Display.COLORS['money']
        formatted_amount = f"${amount:,.2f}"
        if context:
            print(f"{color}💰 {context}: {formatted_amount}")
        else:
            print(f"{color}💰 {formatted_amount}")
    
    @staticmethod
    def print_animal_status(name: str, species: str, health: float, happiness: float, hunger: float) -> None:
        """
        Print formatted animal status with color-coded health.
        
        Args:
            name: Animal name
            species: Animal species
            health: Health percentage
            happiness: Happiness percentage
            hunger: Hunger percentage
        """
        # Determine health color
        if health >= 70:
            health_color = Display.COLORS['health_good']
            health_emoji = "💚"
        elif health >= 40:
            health_color = Display.COLORS['health_warning']
            health_emoji = "💛"
        else:
            health_color = Display.COLORS['health_critical']
            health_emoji = "❤️"
        
        # Determine happiness emoji
        if happiness >= 80:
            happiness_emoji = "😄"
        elif happiness >= 60:
            happiness_emoji = "😊"
        elif happiness >= 40:
            happiness_emoji = "😐"
        elif happiness >= 20:
            happiness_emoji = "😟"
        else:
            happiness_emoji = "😢"
        
        # Determine hunger emoji
        if hunger <= 20:
            hunger_emoji = "🍖"
        elif hunger <= 50:
            hunger_emoji = "🍽️"
        else:
            hunger_emoji = "🆘"
        
        animal_color = Display.COLORS['animal']
        print(f"  {animal_color}{name} the {species}")
        print(f"    {health_emoji} {health_color}Health: {health:.1f}%{Style.RESET_ALL} | "
              f"{happiness_emoji} Happiness: {happiness:.1f}% | "
              f"{hunger_emoji} Hunger: {hunger:.1f}%")
    
    @staticmethod
    def print_zoo_status(status_data: Dict[str, Any]) -> None:
        """
        Print comprehensive zoo status with formatting.
        
        Args:
            status_data: Zoo status dictionary from ZooManager
        """
        if not status_data:
            Display.print_error("No zoo status available")
            return
        
        Display.clear_screen()
        Display.print_header(f"🏰 {status_data['name']} - ZOO STATUS", 70)
        
        # Financial Summary
        Display.print_section("FINANCIAL SUMMARY", 'money')
        financials = status_data['financials']
        Display.print_money(financials['funds'], "Current Funds")
        Display.print_money(financials['daily_income'], "Today's Income")
        Display.print_money(financials['daily_costs'], "Today's Costs")
        print(f"🎟️  Ticket Price: ${financials['ticket_price']:.2f}")
        
        # Zoo Statistics
        Display.print_section("ZOO STATISTICS", 'info')
        print(f"📅 Days Operational: {status_data['days_operational']}")
        print(f"🎟️  Total Visitors: {status_data['total_visitors']:,}")
        print(f"🐾 Total Animals: {status_data['animal_count']}")
        print(f"🏠 Total Enclosures: {status_data['enclosure_count']}")
        
        # Visitor Satisfaction (calculated)
        total_animals = status_data['animal_count']
        clean_enclosures = sum(1 for e in status_data['enclosures'] if e['cleanliness'] > 70)
        total_enclosures = len(status_data['enclosures'])
        
        if total_enclosures > 0:
            cleanliness_score = (clean_enclosures / total_enclosures) * 100
            animal_density = total_animals / total_enclosures if total_enclosures > 0 else 0
            satisfaction = min(100, (cleanliness_score * 0.6 + min(animal_density * 10, 40)))
            
            if satisfaction >= 80:
                satisfaction_emoji = "😍"
                satisfaction_color = Fore.GREEN
            elif satisfaction >= 60:
                satisfaction_emoji = "😊"
                satisfaction_color = Fore.YELLOW
            elif satisfaction >= 40:
                satisfaction_emoji = "😐"
                satisfaction_color = Fore.YELLOW
            else:
                satisfaction_emoji = "😞"
                satisfaction_color = Fore.RED
            
            print(f"{satisfaction_emoji} {satisfaction_color}Visitor Satisfaction: {satisfaction:.1f}%{Style.RESET_ALL}")
        
        # Enclosure Status
        Display.print_section("ENCLOSURE STATUS", 'enclosure')
        for enclosure in status_data['enclosures']:
            enclosure_color = Display.COLORS['enclosure']
            cleanliness = enclosure['cleanliness']
            
            if cleanliness >= 80:
                clean_emoji = "✨"
                clean_color = Fore.GREEN
            elif cleanliness >= 50:
                clean_emoji = "✅"
                clean_color = Fore.YELLOW
            else:
                clean_emoji = "🧹"
                clean_color = Fore.RED
            
            print(f"  {enclosure_color}{enclosure['name']} "
                  f"({enclosure['animal_count']}/{enclosure['capacity']} animals)")
            print(f"    {clean_emoji} {clean_color}Cleanliness: {cleanliness:.1f}%{Style.RESET_ALL} | "
                  f"🏠 Type: {enclosure['type']}")
            
            # Show animals in this enclosure
            for animal in enclosure['animals'][:3]:  # Show first 3 animals
                Display.print_animal_status(
                    animal['name'], animal['species'],
                    animal['health'], animal['happiness'], animal['hunger']
                )
            
            if len(enclosure['animals']) > 3:
                print(f"    ... and {len(enclosure['animals']) - 3} more animals")
        
        # Food Supplies
        Display.print_section("RESOURCE STATUS", 'warning')
        resources = status_data['resources']
        for food_type, amount in resources['food_supply'].items():
            if amount > 50:
                supply_emoji = "📦"
                supply_color = Fore.GREEN
            elif amount > 20:
                supply_emoji = "📦"
                supply_color = Fore.YELLOW
            else:
                supply_emoji = "🆘"
                supply_color = Fore.RED
            
            print(f"  {supply_emoji} {supply_color}{food_type.title()}: {amount:.1f}kg{Style.RESET_ALL}")
    
    @staticmethod
    def print_menu(title: str, options: List[Dict[str, str]]) -> None:
        """
        Print a formatted menu with colored options.
        
        Args:
            title: Menu title
            options: List of option dictionaries with 'key', 'label', and optional 'description'
        """
        Display.print_header(title, 50)
        
        for option in options:
            key = option['key']
            label = option['label']
            description = option.get('description', '')
            
            print(f"{Display.COLORS['menu_item']}{Style.BRIGHT}{key}.{Style.RESET_ALL} {label}")
            if description:
                print(f"     {Fore.LIGHTBLACK_EX}{description}{Style.RESET_ALL}")
        
        print()
    
    @staticmethod
    def print_event_summary(events: List[Dict]) -> None:
        """
        Print formatted event summary.
        
        Args:
            events: List of event dictionaries
        """
        if not events:
            Display.print_info("No special events today.")
            return
        
        Display.print_section("TODAY'S SPECIAL EVENTS", 'header')
        
        for event_data in events:
            event = event_data['event']
            result = event_data['result']
            
            # Color based on event severity
            if event.severity.value == 'positive':
                event_color = Fore.GREEN + Style.BRIGHT
                emoji = "✨"
            elif event.severity.value == 'negative':
                event_color = Fore.RED + Style.BRIGHT
                emoji = "⚠️"
            elif event.severity.value == 'critical':
                event_color = Fore.RED + Style.BRIGHT
                emoji = "🚨"
            else:
                event_color = Fore.CYAN
                emoji = "ℹ️"
            
            print(f"{emoji} {event_color}{event.name}{Style.RESET_ALL}")
            print(f"   {event.description}")
            
            for message in result.get('messages', []):
                print(f"   • {message}")
            
            # Show impacts
            impacts = []
            if 'financial_impact' in result:
                impact = result['financial_impact']
                if impact > 0:
                    impacts.append(f"💰 +${impact:,}")
                elif impact < 0:
                    impacts.append(f"💰 -${-impact:,}")
            
            if 'visitor_impact' in result:
                impact = result['visitor_impact']
                if impact > 0:
                    impacts.append(f"🎟️  +{impact} visitors")
                elif impact < 0:
                    impacts.append(f"🎟️  -{-impact} visitors")
            
            if impacts:
                print(f"   {Fore.LIGHTBLACK_EX}Impact: {', '.join(impacts)}{Style.RESET_ALL}")
    
    @staticmethod
    def print_health_alerts(critical_animals: List[str]) -> None:
        """
        Print formatted health alerts.
        
        Args:
            critical_animals: List of animal IDs with critical health
        """
        if not critical_animals:
            Display.print_success("No critical health issues!")
            return
        
        Display.print_section("🚨 CRITICAL HEALTH ALERTS", 'error')
        
        for animal_id in critical_animals:
            name, species = animal_id.split('_')
            print(f"{Fore.RED}❌ {name} the {species} needs immediate medical attention!{Style.RESET_ALL}")
        
        Display.print_info("Feed animals and clean enclosures to improve health.")
    
    @staticmethod
    def print_quick_stats(zoo_manager) -> None:
        """
        Print quick statistics line for header.
        
        Args:
            zoo_manager: ZooManager instance
        """
        status = zoo_manager.get_zoo_status()
        if not status:
            return
        
        financials = status['financials']
        funds_color = Display.COLORS['money']
        animal_color = Display.COLORS['animal']
        
        print(f"{funds_color}💰 ${financials['funds']:,.2f}{Style.RESET_ALL} | "
              f"{animal_color}🐾 {status['animal_count']} animals{Style.RESET_ALL} | "
              f"🎟️ {status['total_visitors']:,} visitors | "
              f"📅 Day {zoo_manager.day_count}")
    
    @staticmethod
    def wait_for_enter(prompt: str = "Press Enter to continue...") -> None:
        """Wait for user to press Enter."""
        print(f"\n{Fore.LIGHTBLACK_EX}{prompt}{Style.RESET_ALL}", end="")
        input()