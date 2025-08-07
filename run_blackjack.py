"""
Launcher for Blackjack CLI Application. Enables game logic to remain in src folder while still
being able to execute the game from the root directory
"""

from src.blackjack import main  # Imports main application function to run the game

# Checks run_blackjack.py is being run directly before executing
if __name__ == "__main__":
    main()