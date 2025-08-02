from functions import *


def mainloop():
    """Loops through the high level gameplay and calls required functions from functions.py where needed. Handles global exceptions and errors."""
    while True:
        try:
            # Calls the main menu
            main_menu()
            sleep(1)
            os.system('clear')
            
            while True:
                # Calls the choose_table constructor function based on main menu input, imports table parameters from json file, outputs selected table rules calling t_rules function
                activetable = choose_table()
                progbar('Loading your table...',40)
                sleep(2)
                os.system('clear')
                activetable.t_rules()

                # IF the number of chips available at the selection table is not 0, prints the number of chips the player has available to bet 
                if activetable.bank is None or activetable.bank > 0:
                    print(f'You have ${player_stats[0]['chips']} remaining in chips.')
                    
                    # IF the number of chips the player has available is not 0, calls functions to initiate blackjack gameplay, prints the amount of chips won or lost
                    if player_stats[0]['chips'] > 0:
                        activetable.player_bet()
                        activetable.new_deal()
                        activetable.double_down()
                        activetable.player_move()
                        printslow(activetable.results(sum(player_bet_list)))
                        sleep(2)

                        # IF the number of chips the player has available after the hand is not 0, calls for input to play again or return to menu
                        if player_stats[0]['chips'] > 0:
                            printslow('Play again? ')
                            player_bet_list.clear()
                            playagain = input('Y/N: ')

                            # Checks user input for choice (Y/N)
                            if 'y' in playagain.lower():
                                os.system('clear')
                                
                                # IF user input is Y, validates the number of chips the table has remaining is not 0, continues the loop by returning to table select screen
                                if activetable.bank is None or activetable.bank > 0:
                                    continue
                                # IF user input is Y, but table has no chips remaining, prints message and continues the loop by returning to table select screen
                                else:
                                    printslow('This table is out of chips. Please choose another table.')
                                    sleep(2)
                                    os.system('clear')
                                    continue
                            
                            # IF user input is N, prints message and returns to the main menu
                            if 'n' in playagain.lower():
                                printslow('Returning to Main Menu')
                                sleep(2)
                                break
                        
                        # IF number of chips the player has available is 0, prints a prompt to start a new game, returns to the main menu by breaking the while loop
                        else: 
                            printslow('You are out of chips. Please start a new game.\n')
                            player_bet_list.clear()
                            printslow('Returning to Main Menu')
                            sleep(2)
                            break
                
                #IF the selected table has 0 chips available, prompts user to select a different table, and continues the loop by returning to the table selection screen
                else:
                    printslow('This table is out of chips. Please choose another table.')
                    sleep(2)
                    os.system('clear')
                    continue
        
        # Checks the playerstats.json file for data, if none exists or data is incorrect or insufficient (IndexError), plays an automated custom error message with some video game references and memes, returns to main menu
        except IndexError:
            meme_error()
            sleep(1)
        # Checks for all relevent files needed in the base folder, if the file does not exist, requests the creation of a new player to create playerstats.json            
        except FileNotFoundError:
            printslow('Error: File not Found. No player data exists. Please create a new player!')
            sleep(1)
        # Checks for user input KeyboardInterrupt error and instead of exiting, prints input for user to save or exit without saving
        except KeyboardInterrupt:
            os.system('clear')
            print('Exit without saving?')
            ex=input('Y/N: ')
            if 'y' in ex.lower(): printslow('\nExiting Blackjack. Thanks for playing!'), sleep(1), os.system('clear'), quit()
            if 'n' in ex.lower(): printslow('\nReturning to Main Menu'), sleep(2), main_menu()
        # Catch all general error, should not occur but when it does will return the user to the main menu
        except: 
            printslow("That's a little embarassing! An unexpected error has occured. Returning to main menu.")
            sleep(1)

# Explicitly calls the main menu function, if app was refactored, would include "if __name__ = __main__" loop instead
mainloop()

