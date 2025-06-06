import csv as c
import json as j
import os
import sys
import art as a
import colorama as co
from rich import progress as p
from time import sleep
from playingcards import *



# sets up initial stats
player_stats = []
table_stats = []
player_bet_list = []


# variables for outside data files
n_t_stats_json ='newtables.json'
t_stats_json = 'tablestats.json'
p_stats_json = 'playerstats.json'
dealer = 'dealerasciicards.csv'
player = 'playerasciicards.csv'

#trying to set up tables with a subclass for the nolimit table which is slightly different than the rest
class Table():
    def __init__(self, name, bank, max_bet, min_bet, r17):
        """Sets up the table with deck to deal from, and other params for each."""
        self.deck = Deck()
        self.deck.shuffle()
        self.name = name
        self.bank = bank
        self.max = max_bet
        self.min = min_bet
        self.r17 = r17
        self.player1=choose_player()

    def new_table(self):
        "saves new table data to the save file"
        table_stats.clear()
        table_stats.append({'name': self.name, 'bank': self.bank, 'max_bet': self.max, 'min_bet': self.min, 'r17': self.r17})

    def new_deal(self):
        """for ever new hand this will occur"""
        self.player = self.deck.draw_n(2)
        self.player1.update_stats(hands=1)
        self.dealer = self.deck.draw_n(2)
        self.first_hand()
        self.display_hand('player')
        
    def t_rules(self):
        print(f"""
=====  {self.name} Table Rules  =====
        Hands cannot be split.
        Deck size: {len(self.deck)}.
        Chips to win: ${self.bank}.
        Maximum bet: ${self.max}.
        Minimum bet: ${self.min}.
        This dealer will {self.r17} on 17.
======================================
        """)
    
    def first_hand(self):
        name = 'Dealer'
        filename = 'dealerasciicards.csv'
        cards = [x for x in self.dealer]
        ascii = [cards[0].img, cards[0].img1]
        print("=" * 20 + f"{name} Cards" + "=" * 20)
        asciicards(filename, *ascii)
        print(f"{name} shows: '{cards[0]}'" + '\n' + '=' * 52 + '\n')

    def display_hand(self, hand):
        """ASCII display function for player's hand in each game"""
        if hand == 'player':
            cards = self.player
            filename = 'playerasciicards.csv'
            name = 'Player'
        if hand == 'dealer':
            cards = self.dealer
            filename = 'dealerasciicards.csv'
            name = 'Dealer'
        individual_cards = [x for x in cards]
        score = self.scores(name.lower())
        ascii = [x.img for x in individual_cards]     
        print("=" * 20 + f"{name} Cards" + "=" * 20)
        asciicards(filename, *ascii)
        print(f'{name} score: {score}' + '\n') 
        self.eval_hand(name, score, cards)
        print('=' * 52)
        
    def eval_hand(self, name, score, cards):    
        if score >21:
            print(co.Fore.RED + co.Style.BRIGHT + f'{name} Bust!\n' + co.Style.RESET_ALL)
            return
        if len(cards) == 2 and score == 21:
            print(co.Fore.GREEN + co.Style.BRIGHT + f'{name} has Blackjack!' + co.Style.RESET_ALL)
            return
          
    def scores(self, hand):
        """Calculates scores with conversion functionality for aces"""
        if hand == 'player':
            cards = [x for x in self.player]
        if hand == 'dealer':
            cards = [x for x in self.dealer]

        score = []
        for card in cards:
            if card.rank == 'Ace': score.append(11) 
            if card.rank == 'King' or card.rank == 'Queen' or card.rank == 'Jack': score.append(10)
            if type(card.rank) is int: score.append(card.rank)
        total = sum(score)
        if total >21 and len(cards) == 2:
            total -= 10
            return total
        elif total > 21 and len(cards) >2 and score.count(11) > 0: 
            total -= (10*(score.count(11)))
            return total
        else:
            return total
        
    def player_bet(self):
        bet = input("How much would you like to bet?: ")
        if self.player1.chips >= int(bet):
            try:
                if int(bet) >= self.min and int(bet) <= self.max:
                    return player_bet_list.append(int(bet))
                elif int(bet)<self.min or int(bet) >self.max:
                    print(f'Please enter a bet between ${self.min} and ${self.max}')
                    self.player_bet()
            except ValueError:
                print(f'Please enter a valid bet!')
                self.player_bet()
        else:
            print(f'You only have ${player_stats[0]['chips']} in chips remaining, please change your bet.')
            self.player_bet()
    
    def double_down(self):
        if player_stats[0]['chips'] > (player_bet_list[0]*2):
            while True:
                    dd = input('Would you like to double your bet? (Y or N): ')
                    if dd.lower() == 'y': return player_bet_list.append(player_bet_list[0])
                    if dd.lower() == 'n': return
                    else:
                        print(f'Please select either Y or N')
        else:
            print("You don't have enough chips to double down.")
            return

    def player_move(self):
        while True:
            move = input('Would you like to hit or stand?: ')
            match move:
                case 'hit':
                    if len(self.player)<5:
                        printslow('\n' + 'Player hits!' + '\n\n')
                        self.player += self.deck.draw_n(1)
                        self.display_hand('player')
                        if self.scores('player') >21:
                            return
                    else:
                        print('You cannot draw more than five cards!')
                        return
                case 'stand':
                    print('\n' + 'Player stands.' + '\n')
                    self.dealer_ai()
                    break
                case _:
                    print('Please choose a valid move (either hit or stand.)')
                    return
            
    def dealer_ai(self):
        self.display_hand('dealer')
        score = self.scores('dealer')
        if len(self.dealer) ==2 and score == 21:
            self.display_hand('dealer')
            print(co.Fore.GREEN + co.Style.BRIGHT + 'Dealer has Blackjack!\n' + co.Style.RESET_ALL)
            return
        else:
            self.ai_threshold()
        
    def ai_threshold(self):
        while len(self.dealer) < 5:
            score = self.scores('dealer')
            if score<=21:
                printslow('Dealer is thinking...\n')
                sleep(2)
                if score <= 17 and self.r17 == 'hit':
                    self.dealer += self.deck.draw_n(1)
                    printslow('Dealer hits!\n')
                    self.display_hand('dealer')
                elif score < 17 and self.r17 == 'stand':
                    self.dealer += self.deck.draw_n(1)
                    printslow('Dealer hits!\n')
                    self.display_hand('dealer')
                elif score >17 and score <21 and self.r17 =='hit': 
                    printslow('Dealer stands!\n') 
                    return
                elif score>=17 and score <21 and self.r17 == 'stand':
                    printslow('Dealer stands!\n')
                    return
                else:
                    printslow('Dealer stands.\n')
                    return
            else:
                return

    def results(self, bet):
        p_score = self.scores('player')
        d_score = self.scores('dealer')
        if len(self.player) ==2 and p_score == 21:
            self.player1.update_stats(chips=int(bet*1.5),chip_won=int(bet*1.5),wins=1)
            self.update_stats(bank=-bet)
            return f'Blackjack earns extra chips! You won ${int(bet*1.5)}!\n'
        elif (d_score >21) or ((p_score > d_score) and p_score <=21):
            self.player1.update_stats(chips=int(bet),chip_won=int(bet),wins=1)
            self.update_stats(bank=-bet)
            return f'Player {p_score} beats dealer {d_score}. You won ${bet}!\n'
        elif p_score == d_score:
            return f'Hand was a tie, no chips gained or lost!\n'
        elif (p_score < d_score) or (len(self.player) >2 and d_score == 21) or p_score>21:
            self.player1.update_stats(chips=-int(bet),chip_lost=int(bet),losses=1)
            return f'You lost ${bet}!\n'
    
    def update_stats(self, **kwargs):
        for key, value in kwargs.items():
            for x in table_stats[0]:
                if self.name in x['name']:
                    x[key] += value         

class NoLimit(Table):
    def __init__(self, *args):
        """sets up specific nolimit params"""
        super().__init__(*args)

    def t_rules(self):
        print(f"""=====  {self.name} Rules  =====
        Hands cannot be split.
        Deck size: {len(self.deck)}.
        Minimum bet: ${self.min}.
        This dealer will {self.r17} on 17.
==========================================
        """)

    def player_bet(self):
        if self.player1.chips >= self.min:
            bet = input("How much would you like to bet?: ")
            if self.player1.chips >= int(bet):
                try:
                    if int(bet) >= self.min:
                        return player_bet_list.append(int(bet))
                    elif int(bet)<self.min:
                        print(f'Please enter a bet between of at least ${self.min}')
                        self.player_bet()
                except ValueError:
                    print(f'Please enter a valid bet!')
                    self.player_bet()
            else: 
                print(f'You only have ${player_stats[0]['chips']} remaining in chips. Please choose a lower bet.')
                self.player_bet()
        else:
            printslow("You don't have enough chips to play at this table yet. Try the other tables first! \n")
            printslow('Returning to Main Menu.')
            sleep(2)
            main_menu()

    def results(self, bet):
        p_score = self.scores('player')
        d_score = self.scores('dealer')
        if len(self.player) ==2 and p_score == 21:
            self.player1.update_stats(chips=int(bet*1.5),chip_won=int(bet*1.5),wins=1)
            return f'Blackjack earns extra chips! You won ${int(bet*1.5)}!\n'
        elif d_score > 21:
            self.player1.update_stats(chips=int(bet),chip_won=int(bet),wins=1)
            return f'You won &{bet}\n'
        elif d_score<21 and ((p_score > d_score) and p_score <=21):
            self.player1.update_stats(chips=int(bet),chip_won=int(bet),wins=1)
            return f'Player {p_score} beats dealer {d_score}. You won ${bet}!\n'
        elif p_score == d_score:
            return f'Hand was a tie, no chips gained or lost!\n'
        elif (p_score < d_score) or (len(self.player) >2 and d_score == 21) or p_score>21:
            self.player1.update_stats(chips=-int(bet),chip_lost=int(bet),losses=1)
            return f'You lost ${bet}!\n'

# player class to hold player data
class Player():
    def __init__(self, name, chips=100, hands=0, wins=0, losses=0, chip_won=0, chip_lost=0):
        "sets up initial player stats, all default values are parsed in here"
        self.name = name.capitalize()
        self.chips = chips
        self.hands = hands
        self.wins = wins
        self.losses = losses
        self.chip_won = chip_won
        self.chip_lost = chip_lost

    def new_save(self):
        "saves new players data to the save file"
        player_stats.clear()
        player_stats.append({'name': self.name, 'chips': self.chips, 'hands': self.hands, 'wins': self.wins, 'losses': self.losses, 'chip_won': self.chip_won, 'chip_lost': self.chip_lost})
    
    def update_stats(self, **kwargs):
        for key, value in kwargs.items():
            for x in player_stats:
                    x[key] += value
      
    def read_stats(self):
        try:
            print(f"""============= Player Stats =============
            Player: {self.name}
            Current chip total: ${self.chips}
            Total hands played: {self.hands}
            Total hands won: {self.wins}
            Total hands lost: {self.losses}
            Total chips won: ${self.chip_won}
            Total chips lost: ${self.chip_lost}
    ========================================
            """)
        except IndexError:
            print("No player data exists, please create or load a player!")

def new_tables():
    try:
        with open(n_t_stats_json, 'r') as f:
            save = j.load(f)
            table_stats.clear()
            table_stats.append(save)
    except j.decoder.JSONDecodeError:
        pass

def save_tables():
    with open(t_stats_json, 'w') as f:
        try:
            j.dump(table_stats[0], f, indent=4)
        except IndexError:
            printslow('No table data exists, please create a new player to initialise tables!')
            sleep(1)
            return main_menu()

def load_tables():
    try:
        with open(t_stats_json, 'r') as f:
            save = j.load(f)
            table_stats.append(save)
    except j.decoder.JSONDecodeError:
        pass
    except IndexError:
        print('No tables exist, please start a new game to initialise tables!')
        sleep(1)
        return main_menu()

def load_stats():
    """without this function, saves will not be carried over between multiple playthroughs, this loads all data in at the start of each session"""
    try:
        with open(p_stats_json, 'r') as f:
            save = j.load(f)
            player_stats.append(save)
    except j.decoder.JSONDecodeError:
        pass
    except IndexError:
        printslow('No player data found, please start a new game.')
        sleep(1)
        return main_menu()
    except FileNotFoundError:
        printslow('Error: File not Found. No player data exists. Please create a new player!')
        sleep(1)
        return main_menu()

def save_stats():
    """saves all stats of all currently saved players"""
    with open(p_stats_json, 'w') as f:
        try:
            j.dump(player_stats[0], f, indent=4)
        except IndexError:
            printslow('No player data exists, please create or load a player!')
            sleep(1)
            return main_menu()

def new_player():
        "saves new players data to the save file"
        printslow('Are you sure you would like to start a new game? All previous save data will be deleted.\n',delay=0.03)
        confirm=input('Confirm new player (Y or N)?: ')
        if 'y' in confirm.lower():
            name=input('Please enter a name for your player: ')
            player_stats.clear()
            player1 = Player(name)
            player1.new_save()
            return player1
        if 'n' in confirm.lower():
            return printslow('Returning to Main Menu.'), os.system('clear')

def printslow(text, delay=0.05):
  for char in text:
    sys.stdout.write(char)
    sys.stdout.flush()
    sleep(delay)

def main_menu():
    while True:
        os.system('clear')
        printslow("""    ============ Welcome to Blackjack! ============
                1. New Game
                2. Play Some Blackjack!
                3. Rules for Playing
                4. See Your Stats
                5. See Table Chips Remaining
                6. Quit
    ===============================================
                """, delay=0.02
            )
        choice = input('Please select an option: ')
        if choice == '1' or 'new' in choice.lower():
            os.system('clear')
            new_player()
            new_tables()
            progbar('Creating player and table data...')
            player1=choose_player()
            os.system('clear')
        elif choice == '2' or 'continue' in choice.lower():
            os.system('clear')
            load_stats()
            player1=choose_player()
            printslow(f'Continue your game as {player1.name.title()}? ')
            pch=input('(Y/N): ')
            while True:
                if 'y' in pch.lower(): 
                    progbar('Initialising player and table data...') 
                    return load_tables()
                elif 'n' in pch.lower(): 
                    printslow('Please select new game.\n')
                    sleep(0.5)
                    input('Press any key to return to Main Menu.')
                    return main_menu()
                else: print('Invalid selection, please try again.')
        elif choice == '3' or 'rules' in choice.lower():
            os.system('clear')
            house_rules()
            return
        elif choice == '4' or 'see pla' in choice.lower():
            progbar('Loading player stats...')
            sleep(2)
            os.system('clear')
            load_stats()
            player1 = choose_player()
            player1.read_stats()
            input('Press any key to return to Main Menu')
            return main_menu()
        elif choice == '5' or 'see tab' in choice.lower():
            progbar("Loading chip data...")
            sleep(0.5)
            os.system('clear')
            load_tables()
            for x in table_stats[0]:
                printslow(f'{x['name']} chips remaining: ${x['bank']}\n',delay=0.03)
                sleep(0.3)
            input('Press any key to return to Main Menu')
            return main_menu()
        elif choice == '6' or 'quit' in choice.lower():
            os.system('clear')
            return custom_quit()
        else:
            printslow('Invalid selection, restarting from Main Menu')
            sleep(1)
            return main_menu()

def house_rules():
    printslow("""
================ The Casino of Truth and Josstice! ================
                    House Rules
            -------------------------
- Dealer will stand on 18 or over regardless of the table
- Depending on the table the dealer may hit or stand on 17
- Hands cannot be split, this functionality is not 
implemented in the current version of this app (v.0.1)
- Player bets before deal, and can double down when hand 
is dealt
- If player hand beats dealer hand by 1 the player's hand wins
- Player Blackjack pays 1.5x the value of the player's bet
- Player cannot beat a dealer Blackjack! 
- 5 Card Stud (5 cards under 21) is scored as a regular 
hand with no advantage to the player

                   Gameplay Rules    
            -------------------------
- Three tables have a finite number of chips to win, once
the table has none left, you have beaten that table! You can check
these chip totals from the main menu.
- The no limit table is a high risk high reward table, players
can aim to increase their chip total exponentially here.
- If players lose all of their chips, they must return to the
Main Menu and start a new game!
===================================================================
              """, delay=0.02)
    sleep(1)
    input('Press any key to return to Main Menu')
    return main_menu()

def choose_table():
    low = Table(*[x for x in table_stats[0][0].values()])
    mid = Table(*[x for x in table_stats[0][1].values()])
    high = Table(*[x for x in table_stats[0][2].values()])
    nolimit = NoLimit(*[x for x in table_stats[0][3].values()])
    printslow("""======== Table Menu ========
    1. Low Roller's Table
    2. Mid Roller's Table
    3. High Roller's Table
    4. No Limit Table
    5. Exit to Main Menu
============================""",delay=0.02)
    while True:
        tablec = input('\nPlease select an option from the list above: ')               
        if tablec == '1' or 'low' in tablec.lower(): 
            activetable = low 
            return activetable
        elif tablec == '2' or 'mid' in tablec.lower():
            activetable = mid
            return activetable
        elif tablec == '3' or 'high' in tablec.lower(): 
            activetable = high
            return activetable
        elif tablec == '4' or 'no' in tablec.lower(): 
            activetable = nolimit
            return activetable
        elif tablec =='5' or 'exit' in tablec.lower():
            printslow('Returning to Main Menu')
            sleep(2)
            os.system('clear')
            main_menu()
        else: print('Invalid selection, please select a table from the above.')

def choose_player():
    player1=Player(*[x for x in player_stats[0].values()])
    return player1

def progbar(desc,rng=30):
    for i in p.track(range(rng), description=desc):
        sleep(0.1)  # Simulate work being done

def asciicards(filename, *lists) -> str:
    """ 
    Creates a side by side ASCII of two or more cards
    """
    with open(filename, 'w', newline='') as f:
        writer = c.writer(f)
        for row in zip(*lists):
            writer.writerow(row)
    
    with open(filename) as f:
        reader = c.reader(f)
        for row in reader:
            print("   ".join(row))

def custom_quit():
    printslow('Thanks for playing!\n') 
    while True:
        printslow('Would you like to save your data?\n')
        save=input('Y/N: ')
        
        if 'y' in save.lower(): 
            try:
                load_stats()
                load_tables()
                save_stats()
                save_tables()
                progbar('Saving player data...\n',40)
                sleep(2)
                printslow('See you next time!')
                sleep(2)
                os.system('clear')
                quit()
            except IndexError:
                printslow('Player data is corrupt or does not exist, please start a new game.')
                sleep(1)
                return main_menu()
        elif 'n' in save.lower():
            printslow('Are you sure? ')
            check=input('Y/N: ')
            if 'y' in check.lower(): return printslow('See you next time!\n'), os.system('clear'), quit()
            if 'n' in check.lower(): continue

def meme(text,delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(delay)
    sleep(2)
    for char in text:        
        sys.stdout.write('\b')
        sys.stdout.flush()
        sleep(delay*1)
    sleep(1)

def meme_error():
    a.aprint('confused3')
    a.aprint('table flip')
    a.aprint('cry')
    print(co.Fore.RED + co.Style.BRIGHT + 'ERROR! ERROR! ' + co.Style.RESET_ALL)
    meme('ALL YOUR BASE ARE BELONG TO US!')
    printslow('Ahem... Sorry about that. Anyway, turns out your save data is corrupted or missing, would you kindly start a new game?')