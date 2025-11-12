"""
Test script to verify the colorama imports are working correctly.
"""

try:
    from colorama import Style, Fore
    from ui.display import Display
    
    print("✅ Colorama imports successful!")
    print("✅ Style and Fore are properly imported")
    
    # Test basic color functionality
    print(f"{Fore.GREEN}Green text works!{Style.RESET_ALL}")
    print(f"{Fore.RED}Red text works!{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Yellow text works!{Style.RESET_ALL}")
    
    # Test Display class
    display = Display()
    display.print_success("Success message test")
    display.print_error("Error message test")
    display.print_warning("Warning message test")
    
    print("\n🎉 All color functionality is working correctly!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")