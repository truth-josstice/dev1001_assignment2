import csv as c
import json as j
import os
import sys
from time import sleep
import art as a
import colorama as co
from rich import progress as p
from custom_lib.playingcards import Deck, Card

# Sets up empty list to house stats for player and table classes
player_stats = []
table_stats = []
player_bet_list = []

# Declared variables for outside data files
n_t_stats_json = "newtables_DONOTDELETE.json"
t_stats_json = "tablestats.json"
p_stats_json = "playerstats.json"
dealer = "dealerasciicards.csv"
player = "playerasciicards.csv"


class Table:
    """
    Creates a class for Tables, with a subclass for the nolimit table which is slightly different
    than the rest, including all parameters which are necessary for each. Sets up the table with
    a deck to deal from.
    """

    # Class-level type annotations. Details what attributes the class has, and type of attribute.
    name: str  # Name of each table (e.g. High Stakes), used for display/tracking tables
    bank: int  # How many chips the dealer has
    max: int  # Maximum bet allowed, used to validate players bets
    min: int  # Minimum bet allowed, used to validate players bets
    r17: str  # Rule to decide dealer behavior upon drawing 17 (e.g Hit or Stand)
    deck: Deck  # Card Deck object created from playingcards Deck class
    player1: "Player"  # Player object created from Player class used for defining player data
    player: list[Card]  # Players current hand as a list of Card objects
    dealer: list[Card]  # Dealers current hand as a list of Card objects

    def __init__(
        self, name: str, bank: int, max_bet: int, min_bet: int, r17: int
    ) -> None:
        """
        Sets up the table using Deck class imported from playingcards package to deal from, and
        other params for each loaded from newtables json file. Sets up instance of player by
        calling choose_player function. Returns a Table object.
        """

        self.deck = Deck()
        self.deck.shuffle()
        self.name = name
        self.bank = bank
        self.max = max_bet
        self.min = min_bet
        self.r17 = r17
        self.player1 = choose_player()
        self.player1 = choose_player()

    def new_table(self) -> None:
        """Saves new table data to the player_stats list."""

        table_stats.clear()
        table_stats.append(
            {
                "name": self.name,
                "bank": self.bank,
                "max_bet": self.max,
                "min_bet": self.min,
                "r17": self.r17,
            }
        )

    def new_deal(self) -> None:
        """
        Deals the initial hands to player and dealer by calling draw_n function of Deck class from
        playingcards package, updates playerstats, calls 'first_hand' function to display dealer
        cards, calls 'display_hand' function to display player cards.
        """

        self.player = self.deck.draw_n(2)
        self.player1.update_stats(hands=1)
        self.dealer = self.deck.draw_n(2)
        self.first_hand()
        self.display_hand("player")

    def t_rules(self) -> None:
        """Prints the rules of the table using instance parameters."""

        print(
            f"""
=====  {self.name} Table Rules  =====
        Hands cannot be split.
        Deck size: {len(self.deck)}.
        Chips to win: ${self.bank}.
        Maximum bet: ${self.max}.
        Minimum bet: ${self.min}.
        This dealer will {self.r17} on 17.
======================================
        """
        )

    def first_hand(self) -> None:
        """
        Only used for the initial display of the dealers hand do only display the rank and suit of
        the first card, calls 'asciicards' method from playingcards package used to represent
        cards in ascii art. Prints the rank and suit of dealers first card as string.
        """

        name = "Dealer"
        filename = "dealerasciicards.csv"
        cards = [x for x in self.dealer]
        ascii = [cards[0].img, cards[0].img1]
        print("=" * 20 + f"{name} Cards" + "=" * 20)
        asciicards(filename, *ascii)
        print(f"{name} shows: '{cards[0]}'" + "\n" + "=" * 52 + "\n")

    def display_hand(self, hand: str) -> None:
        """
        ASCII display function for every deal bar the first turn of dealer. Refers to .csv files
        used to correctly format ascii art display of cards. Calls 'asciicards' function from
        playingcards package to represent cards in ascii art. Checks if player has bust or has
        blackjack, prints total value of cards dealt.
        """
        # IF the passed hand parameter is "player", sets all variables needed to show player cards
        if hand == "player":
            cards = self.player
            filename = "playerasciicards.csv"
            name = "Player"

        # IF the passed hand parameter is "dealer", sets all variables needed to show dealer cards1
        if hand == "dealer":
            cards = self.dealer
            filename = "dealerasciicards.csv"
            name = "Dealer"

        individual_cards = [x for x in cards]
        score = self.scores(name.lower())
        ascii = [x.img for x in individual_cards]
        print("=" * 20 + f"{name} Cards" + "=" * 20)
        asciicards(filename, *ascii)
        print(f"{name} score: {score}" + "\n")
        self.eval_hand(name, score, cards)
        print("=" * 52)

    def eval_hand(self, name, score, cards) -> None:
        """
        Evaluates cards passed through cards argument, prints whether hand has blackjack or bust.
        Calls methods from colorama to display text in colour.
        """

        # IF score is over 21, sends formatted Bust message
        if score > 21:
            print(
                co.Fore.RED + co.Style.BRIGHT + f"{name} Bust!\n" + co.Style.RESET_ALL
            )
            return

        # Length and Score validation to check for Blackjack, sends formatted message
        if len(cards) == 2 and score == 21:
            print(
                co.Fore.GREEN
                + co.Style.BRIGHT
                + f"{name} has Blackjack!"
                + co.Style.RESET_ALL
            )
            return

    def scores(self, hand: str) -> int:
        """
        Calculates scores of hand passed through hand argument with conversion functionality
        for scoring aces as wild (either 11 or 1).
        """

        if hand == "player":
            cards = [x for x in self.player]

        if hand == "dealer":
            cards = [x for x in self.dealer]

        score = []

        # Check all cards in hand and score based on value of int cards,
        # customised value of face + ace cards
        for card in cards:
            if card.rank == "Ace":
                score.append(11)

            if card.rank == "King" or card.rank == "Queen" or card.rank == "Jack":
                score.append(10)

            if type(card.rank) is int:
                score.append(card.rank)

        total = sum(score)

        # Checks for the possibility of two Aces dealt, adjusts one ace to be wild by removing
        # 10 from total, returns total value of cards
        if total > 21 and len(cards) == 2:
            total -= 10
            return total

        # Checks for total larger than 21, checks for any aces held in hand, changes value of
        # aces in hand to wild by removing ten for each held ace, returns total value of cards
        elif total > 21 and len(cards) > 2 and score.count(11) > 0:
            total -= 10 * (score.count(11))
            return total

        else:
            return total

    def player_bet(self) -> None:
        """
        User input prompt for entering bet amount. Follows table rules for maximum and minimum bet
        limits, appends playerstats with any relevant stats. Appends bet amount to player_bet_list.
        """
        bet = input("How much would you like to bet?: ")

        # Checks if player has enough chips to cover bet
        try:
            if self.player1.chips >= int(bet):
            
                # IF bet is between min-max table limits, appends to list of bet amounts
                if int(bet) >= self.min and int(bet) <= self.max:
                    return player_bet_list.append(int(bet))

                # IF bet is outside of table limits, prints limits of table and re-prompts player
                elif int(bet) < self.min or int(bet) > self.max:
                    print(f"Please enter a bet between ${self.min} and ${self.max}")
                    self.player_bet()
            
            else:  # IF player does not have enough chips to cover bet, prints total remaining
            # chips and re-prompts player
                print(
                f"You only have ${player_stats[0]['chips']} in chips remaining, please change your bet."
                )
                self.player_bet()

        except ValueError:  # Checks bet amount is interpretable as an int amount
            print("Please enter a valid bet!")
            self.player_bet()


    def double_down(self) -> None:
        """
        Prompts the player to double their initial bet, validates whether the player has enough
        chips to double, returns an appended list value for player bet.
        """

        # IF player has enough chips to double the bet, prompts user input
        if player_stats[0]["chips"] > (player_bet_list[0] * 2):
            while True:
                dd = input("Would you like to double your bet? (Y or N): ")

                # IF y is in user input, copies first bet to bet list
                if dd.lower() == "y":
                    return player_bet_list.append(player_bet_list[0])

                # IF n is in user input, takes no action
                if dd.lower() == "n":
                    return

                else: # IF user has entered an invalid option
                    print("Please select either Y or N")

        else: # IF player does not have enough chips to double the bet, does not prompt user input
            print("You don't have enough chips to double down.")
            return

    def player_move(self) -> None:
        """
        Prompts the player to input their move based on their dealt hand, checks for hand length
        to ensure no more than five cards are dealt.
        """

        while True:
            move = input("Would you like to hit or stand?: ")
            match move:

                # IF user chooses hit
                case "hit":

                    # IF player is less than the five card maximum, adds a card to the hand and displays
                    if len(self.player) < 5:
                        printslow("\n" + "Player hits!" + "\n\n")
                        self.player += self.deck.draw_n(1)
                        self.display_hand("player")

                        # IF card drawn results in total over 21, takes no action
                        if self.scores("player") > 21:
                            return

                    else: # IF player has the maximum of five cards currently held
                        print("You cannot draw more than five cards!")
                        return

                # IF user chooses stand, starts dealer turn
                case "stand":
                    print("\n" + "Player stands." + "\n")
                    self.dealer_ai()
                    break
                
                # IF user makes a choice other than those available
                case _:
                    print("Please choose a valid move (either hit or stand.)")
                    return

    def dealer_ai(self) -> None:
        """
        Displays the dealers full hand and score, checks for blackjack, otherwise calls
        ai_threshold function to decide if dealer hits or stands according to score and
        table rules. Calls methods from colorama to display text in color.
        """

        self.display_hand("dealer")
        score = self.scores("dealer")

        # Checks length and score of hand for Blackjack
        if len(self.dealer) == 2 and score == 21:
            self.display_hand("dealer")
            print(
                co.Fore.GREEN
                + co.Style.BRIGHT
                + "Dealer has Blackjack!\n"
                + co.Style.RESET_ALL
            )
            return

        else: # IF dealer does not have blackjack, initiates dealer decision making
            self.ai_threshold()

    def ai_threshold(self) -> None:
        """
        Calls the scoring function to ascertain the total value of dealer hand. Applies if
        statments based on score, calls draw_n function from Deck class to add cards to hand.
        Returns ascii display of cards, or printed message of dealer's choice.
        """

        # Ensures dealer cannot draw more than five cards
        while len(self.dealer) < 5:
            score = self.scores("dealer")

            # IF score 21 or less simulates dealer decision time
            if score <= 21:
                printslow("Dealer is thinking...\n")
                sleep(2)

                # IF table soft 17 rule is hit, dealer will draw card on 17 or below
                if score <= 17 and self.r17 == "hit":
                    self.dealer += self.deck.draw_n(1)
                    printslow("Dealer hits!\n")
                    self.display_hand("dealer")

                # IF table soft 17 rule is stand, dealer will draw card on 16 or below
                elif score < 17 and self.r17 == "stand":
                    self.dealer += self.deck.draw_n(1)
                    printslow("Dealer hits!\n")
                    self.display_hand("dealer")

                # IF dealer score is between 18 and 21 dealer will stand
                elif score > 17 and score < 21 and self.r17 == "hit":
                    printslow("Dealer stands!\n")
                    return

                # IF dealer score is between 17 and 21 dealer will stand
                elif score >= 17 and score < 21 and self.r17 == "stand":
                    printslow("Dealer stands!\n")
                    return

                else: # IF dealer reaches maximum and no score conditions are met dealer stands
                    printslow("Dealer stands.\n")
                    return

            else: # Once maximum is reached, returns to gameplay loop
                return

    def results(self, bet: int) -> str:
        """
        Evaluates player score and dealer score, and returns results string. Updates playerstats
        json file dependent on blackjack, winning or losing score.
        """

        p_score = self.scores("player")
        d_score = self.scores("dealer")

        # Checks for blackjack by checking length of hand and score
        if len(self.player) == 2 and p_score == 21:
            self.player1.update_stats(
                chips=int(bet * 1.5), chip_won=int(bet * 1.5), wins=1
            )
            self.update_stats(bank=-bet)
            return f"Blackjack earns extra chips! You won ${int(bet*1.5)}!\n"

        # Checks for player score beating dealer score
        elif (d_score > 21) or ((p_score > d_score) and p_score <= 21):
            self.player1.update_stats(chips=int(bet), chip_won=int(bet), wins=1)
            self.update_stats(bank=-bet)
            return f"Player {p_score} beats dealer {d_score}. You won ${bet}!\n"

        # Checks for exact matching score
        elif p_score == d_score:
            return "Hand was a tie, no chips gained or lost!\n"

        # Checks for all losing scenarios, score, dealer blackjack and player bust
        elif (
            (p_score < d_score)
            or (len(self.player) > 2 and d_score == 21)
            or p_score > 21
        ):
            self.player1.update_stats(chips=-int(bet), chip_lost=int(bet), losses=1)
            return f"You lost ${bet}!\n"

    def update_stats(self, **kwargs: dict) -> None:
        """General function updates local table_stats list based on passed keyword arguments."""

        for key, value in kwargs.items():
            for x in table_stats[0]:
                if self.name in x["name"]:
                    x[key] += value


class NoLimit(Table):
    """Subclass of Table. Inherits arguments for deck, name, min_bet, r17."""

    def __init__(self, *args) -> None:
        """Allows for the removal of max_bet, bank."""

        super().__init__(*args)

    def t_rules(self) -> None:
        """Customized table rules display as multiple limits no longer exist."""

        print(
            f"""=====  {self.name} Rules  =====
        Hands cannot be split.
        Deck size: {len(self.deck)}.
        Minimum bet: ${self.min}.
        This dealer will {self.r17} on 17.
==========================================
        """
        )

    def player_bet(self) -> None:
        """
        Customized version of Table function, added custom string for the no limit table, removing
        the maximum bet limit from function.
        """

        # IF player has more chips than the table minimum
        if self.player1.chips >= self.min:
            bet = input("How much would you like to bet?: ")

            # IF player has enough chips to bet
            if self.player1.chips >= int(bet):
                try:

                    # IF player bet is above the table minimum, adds to bet list
                    if int(bet) >= self.min:
                        return player_bet_list.append(int(bet))

                    # IF player bet is below minimum, prompts rebet with minimum bet message
                    elif int(bet) < self.min:
                        print(f"Please enter a bet between of at least ${self.min}")
                        self.player_bet()

                # IF player enters any data type other than INT
                except ValueError:
                    print(f"Please enter a valid bet!")
                    self.player_bet()

            else: # IF player does not have enough chips to meet table minimum
                print(
                    f"You only have ${player_stats[0]['chips']} remaining in chips. Please choose a lower bet."
                )
                self.player_bet()

        else:  # Custom script for the no limit table's minimum bet not being met
            printslow(
                "You don't have enough chips to play at this table yet. Try the other tables first! \n"
            )
            printslow("Returning to Main Menu.")
            main_menu()

    def results(self, bet: int) -> str:
        """
        Customized from Table.results function. No longer removes any chips from table bank.
        Returns string dependent on result.
        """

        p_score = self.scores("player")
        d_score = self.scores("dealer")

        # Checks for blackjack by checking length of hand and score
        if len(self.player) == 2 and p_score == 21:
            self.player1.update_stats(
                chips=int(bet * 1.5), chip_won=int(bet * 1.5), wins=1
            )
            return f"Blackjack earns extra chips! You won ${int(bet*1.5)}!\n"

        # Checks for dealer bust
        elif d_score > 21:
            self.player1.update_stats(chips=int(bet), chip_won=int(bet), wins=1)
            return f"You won &{bet}\n"

        # Checks for player score beating dealer score
        elif d_score < 21 and ((p_score > d_score) and p_score <= 21):
            self.player1.update_stats(chips=int(bet), chip_won=int(bet), wins=1)
            return f"Player {p_score} beats dealer {d_score}. You won ${bet}!\n"

        # Checks for tie
        elif p_score == d_score:
            return "Hand was a tie, no chips gained or lost!\n"

        # Checks all cases for player loss
        elif (
            (p_score < d_score)
            or (len(self.player) > 2 and d_score == 21)
            or p_score > 21
        ):
            self.player1.update_stats(chips=-int(bet), chip_lost=int(bet), losses=1)
            return f"You lost ${bet}!\n"


class Player:
    """Player class which sets up new player with default variables."""

    # Class-level type annotations. Details what attributes the class has, and type of attribute.
    name: str  # The player’s name, used for display/tracking player
    chips: int  # Current players chip total
    hands: int  # Total hands played by player
    wins: int  # Total hands won by player
    losses: int  # Total hands lost by player
    chip_won: int  # Total chips won by player
    chip_lost: int  # Total chips lost by player

    def __init__(
        self,
        name: str,
        chips: int = 100,
        hands: int = 0,
        wins: int = 0,
        losses: int = 0,
        chip_won: int = 0,
        chip_lost: int = 0,
    ) -> None:
        """Set up initial player stats, all default values are parsed here. Returns player object"""

        self.name = name.capitalize()
        self.chips = chips
        self.hands = hands
        self.wins = wins
        self.losses = losses
        self.chip_won = chip_won
        self.chip_lost = chip_lost

    def new_save(self) -> None:
        """Saves new players data to the local player_stats list."""

        player_stats.clear()
        player_stats.append(
            {
                "name": self.name,
                "chips": self.chips,
                "hands": self.hands,
                "wins": self.wins,
                "losses": self.losses,
                "chip_won": self.chip_won,
                "chip_lost": self.chip_lost,
            }
        )

    def update_stats(self, **kwargs: dict) -> None:
        """Function updates player stats in the local player_stats list."""

        for key, value in kwargs.items():
            for x in player_stats:
                x[key] += value

    def read_stats(self) -> None:
        """String function which displays all player stats."""

        try:
            print(
                f"""============= Player Stats =============
            Player: {self.name.title()}
            Current chip total: ${self.chips}
            Total hands played: {self.hands}
            Total hands won: {self.wins}
            Total hands lost: {self.losses}
            Total chips won: ${self.chip_won}
            Total chips lost: ${self.chip_lost}
    ========================================
            """
            )

        except IndexError:  # Error catching
            print("No player data exists, please create or load a player!")


# Global functions not tied to any class but may use class data
def new_tables() -> None:
    """Loads default Table data from json and appends to local list for object creation."""

    with open(n_t_stats_json, "r") as f:
        save = j.load(f)
        table_stats.clear()
        table_stats.append(save)


def save_tables() -> None:
    """Dumps local table_stats list to json document and formats for human readability."""

    with open(t_stats_json, "w") as f:
        j.dump(table_stats[0], f, indent=4)


def load_tables() -> None:
    """Loads saved table data from json and appends to local table_stats list."""

    with open(t_stats_json, "r") as f:
        save = j.load(f)
        table_stats.append(save)


def load_stats() -> None:
    """Loads saved player data from json and appends to local player_stats list."""

    with open(p_stats_json, "r") as f:
        save = j.load(f)
        player_stats.append(save)


def save_stats() -> None:
    """Dumps local player_stats list to json and indents for human readability."""

    with open(p_stats_json, "w") as f:
        j.dump(player_stats[0], f, indent=4)


def new_player() -> Player:
    """Prompts user to overwrite saved data, prompts for username input. Returns a Player object."""

    printslow(
        "Are you sure you would like to start a new game? All previous save data will be deleted.\n",
        delay=0.03,
    )

    while True:
        confirm = input("Confirm new player (Y or N)?: ")

        # Checks for both a y and n in the input
        if "y" and "n" in confirm.lower():
            printslow("Please enter one choice only.\n")

        # For new player, clears local player_stats list and calls new_save function to set default
        # values with passed player name
        elif "y" in confirm.lower():
            name = input("Please enter a name for your player: ")
            player_stats.clear()
            player1 = Player(name)
            player1.new_save()
            return player1

        elif "n" in confirm.lower():  # Returns to the main menu
            printslow("Returning to Main Menu."), os.system("clear")

        else:  # Checks for any input other than y or n
            printslow("Please enter a valid choice: Y or N.\n")


def printslow(text, delay=0.05) -> None:
    """Prints passed argument string character by character."""

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(delay)


def main_menu() -> None:
    """
    Displays main menu, prompts user for choices and handles all input choices by calling the
    associated functions. Calls progbar function imported from rich package to show
    saving/loading progress.
    """

    os.system("clear")
    printslow(
        """    ============ Welcome to Blackjack! ============
                1. New Game
                2. Play Some Blackjack!
                3. Rules for Playing
                4. See Your Stats
                5. See Table Chips Remaining
                6. Quit
    -----------------------------------------------
            Press Ctrl+C to quit at any time.      
    ===============================================            
                """,
        delay=0.02,
    )

    while True:
        choice = input("Please select an option: ")

        # Checks for both str and int inputs, calls required functions to create a new player,
        # returns main menu function to re-display the main menu
        if choice == "1" or "new" in choice.lower():
            os.system("clear")
            new_player()
            new_tables()
            save_tables()
            progbar("Creating player and table data...")
            player1 = choose_player()
            printslow("New player created! Returning to Main Menu")
            sleep(1)
            return main_menu()

        # Checks for both str and int inputs, calls required functions to load player stats
        elif choice == "2" or "continue" in choice.lower():
            os.system("clear")
            load_stats()
            player1 = choose_player()
            printslow(f"Continue your game as {player1.name.title()}? ")
            pch = input("(Y/N): ")
            while True:
                if "y" in pch.lower():
                    progbar("Initialising player and table data...")
                    return load_tables()
                elif "n" in pch.lower():
                    printslow("Please select new game.\n")
                    sleep(0.5)
                    input("Press any key to return to Main Menu.")
                    return main_menu()
                else:
                    print("Invalid selection, please try again.")

        # Checks for both str and int inputs, calls house rules function, returns to main menu
        elif choice == "3" or "rules" in choice.lower():
            os.system("clear")
            house_rules()
            return main_menu()

        # Checks for both str and int inputs, calls required functions to show player functions
        elif choice == "4" or "see pla" in choice.lower():
            progbar("Loading player stats...")
            sleep(2)
            os.system("clear")
            load_stats()
            player1 = choose_player()
            player1.read_stats()
            input("Press any key to return to Main Menu")
            return main_menu()

        # Checks for both str and int inputs, calls required functions to display table data,
        # returns to main menu
        elif choice == "5" or "see tab" in choice.lower():
            progbar("Loading chip data...")
            sleep(0.5)
            os.system("clear")
            load_tables()

            for x in table_stats[0][:-1]:
                printslow(f"{x['name']} chips remaining: ${x['bank']}\n", delay=0.03)

            printslow(
                f"{table_stats[0][3]['name']} has no limit! You can win as many chips as you like!\n"
            )
            sleep(0.3)
            input("Press any key to return to Main Menu")
            return main_menu()

        # Checks for both str and int inputs, calls custom quit menu function
        elif choice == "6" or "quit" in choice.lower():
            os.system("clear")
            return custom_quit()

        else: # IF user input is not a valid choice
            printslow("Invalid selection, please try again.\n")


def house_rules() -> None:
    """
    Prints the rules of blackjack according to this app. Returns main menu function to return
    to main menu.
    """

    printslow(
        """
================ The Casino of Truth and Josstice! ================
                        House Rules
-------------------------------------------------------------------
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
-------------------------------------------------------------------
    - Three tables have a finite number of chips to win, once
      the table has none left, you have beaten that table! You can 
      check these chip totals from the main menu.
    - The no limit table is a high risk high reward table, players
      can aim to increase their chip total exponentially here.
    - If players lose all of their chips, they must return to the
      Main Menu and start a new game!
===================================================================
              """,
        delay=0.02,
    )
    sleep(1)
    input("Press any key to return to Main Menu")
    return main_menu()


def choose_table() -> Table | NoLimit:
    """Creates a table object based on user input by parsing table_stats local list."""

    low = Table(*[x for x in table_stats[0][0].values()])
    mid = Table(*[x for x in table_stats[0][1].values()])
    high = Table(*[x for x in table_stats[0][2].values()])
    nolimit = NoLimit(*[x for x in table_stats[0][3].values()])
    
    printslow(
        """======== Table Menu ========
    1. Low Roller's Table
    2. Mid Roller's Table
    3. High Roller's Table
    4. No Limit Table
    5. Exit to Main Menu
============================""",
        delay=0.02,
    )

    while True:
        tablec = input("\nPlease select an option from the list above: ")

        # IF user chooses Low Rollers table
        if tablec == "1" or "low" in tablec.lower():
            activetable = low
            return activetable

        # IF user chooses Mid Rollers table
        elif tablec == "2" or "mid" in tablec.lower():
            activetable = mid
            return activetable

        # IF user chooses High Rollers table
        elif tablec == "3" or "high" in tablec.lower():
            activetable = high
            return activetable

        # IF user chooses No Limit table
        elif tablec == "4" or "no" in tablec.lower():
            activetable = nolimit
            return activetable

        # IF user chooses to Exit
        elif tablec == "5" or "exit" in tablec.lower():
            printslow("Returning to Main Menu")
            sleep(2)
            os.system("clear")
            main_menu()

        else: # IF user input is not a valid choice
            print("Invalid selection, please select a table from the above.")


def choose_player() -> Player:
    """
    Allows player object to be created within any table specific functions.
    Returns the player object.
    """

    player1 = Player(*[x for x in player_stats[0].values()])
    return player1


def progbar(desc, rng: int = 30) -> None:
    """Modified progress bar from rich package."""

    for i in p.track(range(rng), description=desc):
        sleep(0.1)  # Simulate work being done


def asciicards(filename: str, *lists: tuple) -> str:
    """
    Creates a side by side ASCII of two or more cards by parsing characters and adding them
    to a single row in CSV file.
    """

    with open(filename, "w", newline="") as f:
        writer = c.writer(f)
        for row in zip(*lists):
            writer.writerow(row)

    with open(filename) as f:
        reader = c.reader(f)
        for row in reader:
            print("   ".join(row))


def custom_quit() -> None:
    """
    Calls all required save functions to write data to external json files. Quits program by
    returning sys.exit function.
    """

    printslow("Thanks for playing!\n")

    while True:
        printslow("Would you like to save your data?\n")
        save = input("Y/N: ")

        # IF user chooses to save loads local lists and saves to external json files
        if save.lower() == "y":
            try:
                load_stats()
                load_tables()
                save_stats()
                save_tables()
                progbar("Saving player data...\n", 40)
                sleep(2)
                printslow("See you next time!")
                sleep(2)
                os.system("clear")
                sys.exit()

            # If external files are altered while app is running the below will occur
            except IndexError:
                printslow(
                    "Save data is corrupt or missing. Unable to save player data.\n"
                )

                while True:
                    err_ex = input(
                        """What would you like to do:
1. Return to Main Menu
2. Exit without saving
Enter your choice: """
                    )

                    # IF user chooses to return to main menu
                    if err_ex == "1" or "main" in err_ex.lower():
                        printslow("Returning to Main Menu.")
                        sleep(2)
                        return main_menu()

                    # IF user chooses to exit without saving
                    elif err_ex == "2" or "exit" in err_ex.lower():
                        printslow(
                            "\nThanks for playing, please start a new game next time you play!"
                        )
                        sleep(2)
                        os.system("clear")
                        sys.exit()

                    else: # IF user input is an invalid choice
                        printslow("Invalid input, please try again.\n")

        # IF user chooses not to save sends confirmation message
        elif save.lower() == "n": 
            printslow("Are you sure? ")
            check = input("Y/N: ")

            # IF user confirms to not save data
            if check.lower() == "y":
                return printslow("See you next time!\n"), os.system("clear"), sys.exit()

            # IF user wishes to save data, prints initial input prompt
            elif check.lower() == "n":
                continue

            else: # IF user input is not a valid choice
                printslow("Please enter either Y or N")

        else: # IF user input is not a valid choice
            printslow("Please enter either Y or N")


def meme(text: str, delay: int = 0.05) -> None:
    """
    For text in the meme error, simulates actual keyboard inputs to return cursor to the beginning
    of the terminal line.
    """

    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(delay)
    sleep(2)

    for char in text:
        sys.stdout.write("\b")
        sys.stdout.flush()
        sleep(delay * 1)
    sleep(1)


def meme_error() -> None:
    """
    A pretty fun little custom error message using a print method from the art package to return
    ascii art, methods from colorama to display text in color. Ultimately returns main_menu
    function to return to the main menu.
    """

    a.aprint("confused3")
    sleep(0.5)
    a.aprint("table flip")
    sleep(0.5)
    a.aprint("cry")
    sleep(0.5)
    print(co.Fore.RED + co.Style.BRIGHT + "ERROR! ERROR! " + co.Style.RESET_ALL)
    sleep(0.5)
    meme("ALL YOUR BASE ARE BELONG TO US!")  # Zero Wing Reference
    printslow(
        "Ahem... Sorry about that. Anyway, turns out your save data is corrupted or missing, would you kindly start a new game?"
    )
    sleep(1)

    for i in range(3):
        printslow("\nWould you kindly...", delay=0.06)  # Bioshock reference
        sleep(0.5)
    printslow(
        "\nOkay, enough video game references, let's go back to the Main Menu already\n"
    )
    a.aprint("happy4")
    sleep(0.5)
