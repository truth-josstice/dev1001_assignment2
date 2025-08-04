from functions import (
    main_menu,
    choose_table,
    progbar,
    sleep,
    os,
    printslow,
    player_stats,
    player_bet_list,
    meme_error,
    sys,
)


def mainloop() -> None:
    """
    Loops through the regular gameplay, and calls required functions where needed.
    Checks all required parameters are valid
    """

    while True:
        try:
            main_menu()  # Calls the main menu
            sleep(1)
            os.system("clear")

            # Calls choose_table constructor function based on main menu input, imports table
            # parameters from json file, outputs selected table rules calling t_rules function
            while True:
                activetable = choose_table()
                progbar("Loading your table...", 40)
                progbar("Loading your table...", 40)
                sleep(2)
                os.system("clear")
                os.system("clear")
                activetable.t_rules()

                # IF the number of chips available at the selection table is not 0,
                # prints the number of chips the player has available to bet
                if activetable.bank is None or activetable.bank > 0:
                    print(f"You have ${player_stats[0]['chips']} remaining in chips.")

                    if player_stats[0]["chips"] > 0:
                        activetable.player_bet()
                        activetable.new_deal()
                        activetable.double_down()
                        activetable.player_move()
                        printslow(activetable.results(sum(player_bet_list)))
                        sleep(2)

                        if player_stats[0]["chips"] > 0:
                            printslow("Play again? ")
                            player_bet_list.clear()
                            playagain = input("Y/N: ")

                            if "y" in playagain.lower():
                                os.system("clear")

                                if activetable.bank is None or activetable.bank > 0:
                                    continue

                                else:  # ELSE user input is Y, but table has no chips left, prints
                                    # message and continues loop by returning to table select screen
                                    printslow(
                                        "This table is out of chips. Please choose another table."
                                    )
                                    printslow(
                                        "This table is out of chips. Please choose another table."
                                    )
                                    sleep(2)
                                    os.system("clear")
                                    os.system("clear")
                                    continue

                            if "n" in playagain.lower():
                                printslow("Returning to Main Menu")
                                sleep(2)
                                break

                        else:
                            printslow(
                                "You are out of chips. Please start a new game.\n"
                            )
                            player_bet_list.clear()
                            printslow("Returning to Main Menu")
                            printslow("Returning to Main Menu")
                            sleep(2)
                            break

                else:  # ELSE the selected table has 0 chips available, prompts user to select
                    # different table, and continues loop by returning to the table selection screen
                    printslow(
                        "This table is out of chips. Please choose another table."
                    )
                    printslow(
                        "This table is out of chips. Please choose another table."
                    )
                    sleep(2)
                    os.system("clear")
                    os.system("clear")
                    continue

        except IndexError:  # Checks the playerstats.json file for data, if none exists
            # or data is incorrect or insufficient (IndexError), plays an automated custom
            # error message with some video game references and memes, returns to main menu
            meme_error()
            sleep(1)

        except FileNotFoundError:  # Checks all relevant files needed in base folder, if
            # file does not exist, requests the creation of a new player to create playerstats.json
            printslow(
                "Error: File not Found. No player data exists. Please create a new player!"
            )
            printslow(
                "Error: File not Found. No player data exists. Please create a new player!"
            )
            sleep(1)

        except KeyboardInterrupt:  # Checks for user input KeyboardInterrupt error and
            # instead of exiting, prints input for user to save or exit without saving
            os.system("clear")
            print("Exit without saving?")
            ex = input("Y/N: ")

            if "y" in ex.lower():
                printslow("\nExiting Blackjack. Thanks for playing!"), sleep(
                    1
                ), os.system("clear"), sys.exit()

            if "n" in ex.lower():
                printslow("\nReturning to Main Menu"), sleep(2), main_menu()

        except SystemExit:  # Allows for clean system exit
            quit()

        except:  # Catch all general error, should not occur but when it
            # does will return the user to the main menu
            printslow(
                "That's a little embarassing! An unexpected error has occured. Returning to main menu."
            )
            sleep(1)


mainloop()
