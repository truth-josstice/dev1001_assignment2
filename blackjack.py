from functions import *



def mainloop():
    try:
        while True:
            main_menu()
            sleep(1)
            os.system('clear')
            while True:
                activetable = choose_table()
                printslow('Loading your table...')
                sleep(2)
                os.system('clear')
                activetable.t_rules()
                if activetable.bank is None or activetable.bank > 0:
                    print(f'You have ${player_stats[0]['chips']} remaining in chips.')
                    if player_stats[0]['chips'] > 0:
                        activetable.player_bet()
                        activetable.new_deal()
                        activetable.double_down()
                        activetable.player_move()
                        printslow(activetable.results(sum(player_bet_list)))
                        sleep(2)
                        if player_stats[0]['chips'] > 0:
                            printslow('Play again? ')
                            player_bet_list.clear()
                            playagain = input('Y/N: ')
                            if 'y' in playagain.lower():
                                os.system('clear')
                                if activetable.bank is None or activetable.bank > 0:
                                    continue
                                else:
                                    printslow('This table is out of chips. Please choose another table.')
                                    sleep(2)
                                    os.system('clear')
                                    continue
                            if 'n' in playagain.lower():
                                printslow('Returning to Main Menu')
                                sleep(2)
                                break
                        else: 
                            printslow('You are out of chips. Please start a new game.\n')
                            player_bet_list.clear()
                            printslow('Returning to Main Menu')
                            sleep(2)
                            break
                else:
                    printslow('This table is out of chips. Please choose another table.')
                    sleep(2)
                    os.system('clear')
                    continue
    except KeyboardInterrupt:
        os.system('clear')
        print('Exit without saving?')
        ex=input('Y/N: ')
        if 'y' in ex.lower(): printslow('Exiting Blackjack. Thanks for playing!'), sleep(1), os.system('clear'), quit()
        if 'n' in ex.lower(): printslow('Returning to Main Menu'), sleep(2), main_menu()

mainloop()
