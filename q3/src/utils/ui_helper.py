import os

def clear_display():
    """
    Clear the terminal screen for better UI experience.
    
    Cross-platform implementation that works on both Windows and Unix-based systems.
    """
    os.system("cls" if os.name == "nt" else "clear")

def show_logo():
    """
    Display application logo in ASCII art.
    
    Provides a visual identity for the application and enhances
    user experience with a branded interface.
    """
    print(
        r"""
$$$$$$$\   $$$$$$\  $$\       $$\       $$\      $$\   $$$$$$\  $$$$$$$\  $$$$$$$$\ 
$$  __$$\ $$  __$$\ $$ |      $$ |      $$$\    $$$ | $$  __$$\ $$  __$$\ \__$$  __|
$$ |  $$ |$$ /  $$ |$$ |      $$ |      $$$$\  $$$$ | $$ /  $$ |$$ |  $$ |   $$ |   
$$ |  $$ |$$ |  $$ |$$ |      $$ |      $$\$$\$$ $$ | $$$$$$$$ |$$$$$$$  |   $$ |   
$$ |  $$ |$$ |  $$ |$$ |      $$ |      $$ \$$$  $$ | $$  __$$ |$$  __$$<    $$ |   
$$ |  $$ |$$ |  $$ |$$ |      $$ |      $$ |\$  /$$ | $$ |  $$ |$$ |  $$ |   $$ |   
$$$$$$$  | $$$$$$  |$$$$$$$$\ $$$$$$$$\ $$ | \_/ $$ | $$ |  $$ |$$ |  $$ |   $$ |   
\_______/  \______/ \________|\________|\__|     \__| \__|  \__|\__|  \__|   \__|   
"""
    )

def display_menu(title, options):
    """
    Display a menu with numbered options.
    
    Args:
        title: The title of the menu
        options: List of option strings
        
    Returns:
        The selected option index
    """
    print(f"\n=== {title} ===\n")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    while True:
        try:
            choice = int(input("\nEnter your choice: "))
            if 1 <= choice <= len(options):
                return choice
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a number.")
