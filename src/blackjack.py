# CUSTOM MODULES IMPORT

from .functions import (
    main_menu, # Main Menu display and input loop
    choose_table, # Initiates Table object during gameplay loop
    progbar, # Simulates task progression
    sleep, # Pause execution for automatic display
    os, # Operating system function for clearing display
    printslow, # Character by character terminal output
    player_stats, # List containing player stats
    player_bet_list, # List containing player bets
    meme_error, # Custom error message for corrupt or missing player data
    sys, # System-specific function for clean exit
)


def mainloop() -> None:
    """
    Main gameplay loop for Blackjack CLI app.
    The loop will continue running until the user exits the game or encounters
    a fatal error that triggers a system exit.

    This function manages the full flow of the game including:
    - Displaying and handling the Main Menu navigation.
    - Handling table selection and loading table rules.
    - Running the betting and gameplay rounds.
    - Managing play again prompts and chip tracking.
    - Checks all required parameters are valid and error handling.
    """

    while True:
        try:
            # Added a warning in regard to intended audience of the project as per ACM 1.2 Avoid Harm
            os.system('clear')
            printslow("This app contains simulated gambling and is intended for users over the age of 18. Please use responsibly.\n") 
            sleep(5)
            printslow("Thank you for your consideration. Press Enter to proceed to Main Menu.")
            input()

            main_menu()  # Display the Main Menu
            sleep(1)  # Delays execution for 1 second to allow player a moment before continuing.
            os.system("clear")

            # Inner loop: Handles the core gameplay loop after Main Menu selection.
            # Allows continuous table selection and gameplay until user chooses to return to Main Menu.
            while True:
                # Prompt player to select a table and load its parameters from JSON file.
                # Creates a table object using choose_table constructor
                # based on user input by parsing table_stats list.
                activetable = choose_table()
                progbar("Loading your table...", 40)
                sleep(2)
                os.system("clear")
                activetable.t_rules()  # t_rules method displays the selected table rules and bet limits.

                # Checks IF the selected table has chips available for betting (and not 0).
                # Prints the number of chips the player has available to bet.
                if activetable.bank is None or activetable.bank > 0:
                    print(f"You have ${player_stats[0]['chips']} remaining in chips.")

                    if player_stats[0]["chips"] > 0:
                        # Begin the betting round gameplay.
                        activetable.player_bet()   # User input prompt for entering bet amount.
                        activetable.new_deal()     # Deals the initial hands to player and dealer.
                        activetable.double_down()  # Prompts player to double their initial bet.
                        activetable.player_move()  # Prompts player to input their move based on dealt hand.

                        # Slowly prints and display results of the round and pause for 2 seconds.
                        printslow(activetable.results(sum(player_bet_list)))
                        sleep(2)

                        if player_stats[0]["chips"] > 0:
                            # IF player still has chips remaining
                            # Prompt player if they wish to play another round.
                            # This keeps the gameplay flowing without forcing return to Main Menu after round.
                            printslow("Play again? ")  # Prompt the player with a slow-printed message for pacing effect.

                            player_bet_list.clear()  # Reset the bet history for next round.
                            # Important: This prevents cummulative stacking of bets between rounds.

                            playagain = input("Y/N: ")
                            # Capture player input with expected responses:
                            # 'Y' => continue gameplay loop
                            # 'N' => return to Main Menu

                            if "y" in playagain.lower():
                                os.system("clear")

                                # Checks IF the table still has sufficient chips to continue gameplay.
                                if activetable.bank is None or activetable.bank > 0:
                                    continue  # Loops back for another round at the same table.

                                else:
                                    # ELSE player chose to continue ('Y'), but table is now out of chips.
                                    # Prints message to display notification to player.
                                    printslow("This table is out of chips. Please choose another table.")
                                    sleep(2)
                                    os.system("clear")
                                    continue  # Continues loop by returning player to table selection.

                            if "n" in playagain.lower():
                                # Player chose not to play another round ('N').
                                # Returns player back to Main Menu.
                                printslow("Returning to Main Menu")
                                sleep(2)
                                break  # Exit the inner loop to return to Main Menu.

                        else:
                            # Player has run out of chips after the round ends.
                            # Forces return to Main Menu as no further betting is possible.
                            printslow("You are out of chips. Please start a new game.\n")
                            player_bet_list.clear()
                            printslow("Returning to Main Menu")
                            sleep(2)
                            break  # Exit table loop and return to Main Menu.

                else:
                    # ELSE the selected table has no chips available.
                    # Prompt player to select different table.
                    printslow("This table is out of chips. Please choose another table.")
                    sleep(2)
                    os.system("clear")
                    continue  # Return to table selection loop.

        # ERROR HANDLING SECTION

        except IndexError:
            # Triggered if the playerstats.json file data does not exist or incorrect/corrupted.
            # Calls a custom meme-based error (IndexError) screen with some video game references
            # for a more entertaining error handling and then returns to main menu.
            meme_error()
            sleep(1)

        except FileNotFoundError:
            # Triggered if essential game files (eg playerstats.json) data does not exist/missing.
            # Requests user to create a new player profile to proceed with gameplay.
            printslow(
                "Error: File not Found. No player data exists. Please create a new player!"
            )
            sleep(1)

        except KeyboardInterrupt:
            # Handles user input KeyboardInterrupt error 'Ctrl+C' gracefully.
            # Prompts player with an option to exit without saving or return to Main Menu.
            os.system("clear")
            print("Exit without saving?")
            ex = input("Y/N: ")

            if "y" in ex.lower():
                # Player chose ('y') to exit.
                printslow("\nExiting Blackjack. Thanks for playing!")
                sleep(1)
                os.system("clear")
                sys.exit()  # Safely exit of the app.

            if "n" in ex.lower():
                # Player cancels exit ('n') and wishes to return to Main Menu.
                printslow("\nReturning to Main Menu")
                sleep(2)
                main_menu()

        except SystemExit:
            # Clean exit if sys.exit() is called.
            quit()

        except:
            # Generic catch-all for any unexpected errors.
            # Prevents app from crashing by redirecting user back to Main Menu.
            printslow(
                "That's a little embarassing! An unexpected error has occured. Returning to main menu."
            )
            sleep(1)

# Entry point: Starts the main gameplay loop when the script is run.
def main() -> None:
    """Acts as the launcher for the game logic by calling mainloop when this function is called"""

    mainloop()


# Prevents the code being run accidentally when being imported to run_blackjack.py
if __name__ == "__main__":
    main()
