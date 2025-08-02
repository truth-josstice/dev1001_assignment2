import csv as c
import json as j
import os
import sys
from time import sleep
import art as a
import colorama as co
from rich import progress as p
from playingcards import Deck, Card

# sets up initial stats
player_stats = []
table_stats = []
player_bet_list = []

# variables for outside data files
n_t_stats_json = "newtables_DONOTDELETE.json"
t_stats_json = "tablestats.json"
p_stats_json = "playerstats.json"
dealer = "dealerasciicards.csv"
player = "playerasciicards.csv"


# trying to set up tables with a subclass for the nolimit table which is slightly different than the rest
class Table:
    """Creates a class for Tables, including all parameters which are necessary for each"""

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
        """Sets up the table with deck to deal from, and other params for each."""
        self.deck = Deck()
        self.deck.shuffle()
        self.name = name
        self.bank = bank
        self.max = max_bet
        self.min = min_bet
        self.r17 = r17
        self.player1 = choose_player()

    def new_table(self) -> None:
        "saves new table data to the save file"
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
        """for ever new hand this will occur"""
        self.player = self.deck.draw_n(2)
        self.player1.update_stats(hands=1)
        self.dealer = self.deck.draw_n(2)
        self.first_hand()
        self.display_hand("player")

    def t_rules(self) -> None:
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
        name = "Dealer"
        filename = "dealerasciicards.csv"
        cards = [x for x in self.dealer]
        ascii = [cards[0].img, cards[0].img1]
        print("=" * 20 + f"{name} Cards" + "=" * 20)
        asciicards(filename, *ascii)
        print(f"{name} shows: '{cards[0]}'" + "\n" + "=" * 52 + "\n")

    def display_hand(self, hand: str) -> None:
        """ASCII display function for player's hand in each game"""
        if hand == "player":
            cards = self.player
            filename = "playerasciicards.csv"
            name = "Player"
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

    def eval_hand(self, name: str, score: int, cards: list[Card]) -> None:
        if score > 21:
            print(
                co.Fore.RED + co.Style.BRIGHT + f"{name} Bust!\n" + co.Style.RESET_ALL
            )
            return
        if len(cards) == 2 and score == 21:
            print(
                co.Fore.GREEN
                + co.Style.BRIGHT
                + f"{name} has Blackjack!"
                + co.Style.RESET_ALL
            )
            return

    def scores(self, hand: str) -> int:
        """Calculates scores with conversion functionality for aces"""
        if hand == "player":
            cards = [x for x in self.player]
        if hand == "dealer":
            cards = [x for x in self.dealer]

        score = []
        for card in cards:
            if card.rank == "Ace":
                score.append(11)
            if card.rank == "King" or card.rank == "Queen" or card.rank == "Jack":
                score.append(10)
            if type(card.rank) is int:
                score.append(card.rank)
        total = sum(score)
        if total > 21 and len(cards) == 2:
            total -= 10
            return total
        elif total > 21 and len(cards) > 2 and score.count(11) > 0:
            total -= 10 * (score.count(11))
            return total
        else:
            return total

    def player_bet(self) -> None:
        bet = input("How much would you like to bet?: ")
        if self.player1.chips >= int(bet):
            try:
                if int(bet) >= self.min and int(bet) <= self.max:
                    return player_bet_list.append(int(bet))
                elif int(bet) < self.min or int(bet) > self.max:
                    print(f"Please enter a bet between ${self.min} and ${self.max}")
                    self.player_bet()
            except ValueError:
                print(f"Please enter a valid bet!")
                self.player_bet()
        else:
            print(
                f"You only have ${player_stats[0]['chips']} in chips remaining, please change your bet."
            )
            self.player_bet()

    def double_down(self) -> None:
        if player_stats[0]["chips"] > (player_bet_list[0] * 2):
            while True:
                dd = input("Would you like to double your bet? (Y or N): ")
                if dd.lower() == "y":
                    return player_bet_list.append(player_bet_list[0])
                if dd.lower() == "n":
                    return
                else:
                    print(f"Please select either Y or N")
        else:
            print("You don't have enough chips to double down.")
            return

    def player_move(self) -> None:
        while True:
            move = input("Would you like to hit or stand?: ")
            match move:
                case "hit":
                    if len(self.player) < 5:
                        printslow("\n" + "Player hits!" + "\n\n")
                        self.player += self.deck.draw_n(1)
                        self.display_hand("player")
                        if self.scores("player") > 21:
                            return
                    else:
                        print("You cannot draw more than five cards!")
                        return
                case "stand":
                    print("\n" + "Player stands." + "\n")
                    self.dealer_ai()
                    break
                case _:
                    print("Please choose a valid move (either hit or stand.)")
                    return

    def dealer_ai(self) -> None:
        self.display_hand("dealer")
        score = self.scores("dealer")
        if len(self.dealer) == 2 and score == 21:
            self.display_hand("dealer")
            print(
                co.Fore.GREEN
                + co.Style.BRIGHT
                + "Dealer has Blackjack!\n"
                + co.Style.RESET_ALL
            )
            return
        else:
            self.ai_threshold()

    def ai_threshold(self) -> None:
        while len(self.dealer) < 5:
            score = self.scores("dealer")
            if score <= 21:
                printslow("Dealer is thinking...\n")
                sleep(2)
                if score <= 17 and self.r17 == "hit":
                    self.dealer += self.deck.draw_n(1)
                    printslow("Dealer hits!\n")
                    self.display_hand("dealer")
                elif score < 17 and self.r17 == "stand":
                    self.dealer += self.deck.draw_n(1)
                    printslow("Dealer hits!\n")
                    self.display_hand("dealer")
                elif score > 17 and score < 21 and self.r17 == "hit":
                    printslow("Dealer stands!\n")
                    return
                elif score >= 17 and score < 21 and self.r17 == "stand":
                    printslow("Dealer stands!\n")
                    return
                else:
                    printslow("Dealer stands.\n")
                    return
            else:
                return

    def results(self, bet: int) -> str:
        p_score = self.scores("player")
        d_score = self.scores("dealer")
        if len(self.player) == 2 and p_score == 21:
            self.player1.update_stats(
                chips=int(bet * 1.5), chip_won=int(bet * 1.5), wins=1
            )
            self.update_stats(bank=-bet)
            return f"Blackjack earns extra chips! You won ${int(bet*1.5)}!\n"
        elif (d_score > 21) or ((p_score > d_score) and p_score <= 21):
            self.player1.update_stats(chips=int(bet), chip_won=int(bet), wins=1)
            self.update_stats(bank=-bet)
            return f"Player {p_score} beats dealer {d_score}. You won ${bet}!\n"
        elif p_score == d_score:
            return f"Hand was a tie, no chips gained or lost!\n"
        elif (
            (p_score < d_score)
            or (len(self.player) > 2 and d_score == 21)
            or p_score > 21
        ):
            self.player1.update_stats(chips=-int(bet), chip_lost=int(bet), losses=1)
            return f"You lost ${bet}!\n"

    def update_stats(self, **kwargs: dict) -> None:
        for key, value in kwargs.items():
            for x in table_stats[0]:
                if self.name in x["name"]:
                    x[key] += value


class NoLimit(Table):
    def __init__(self, *args) -> None:
        """sets up specific nolimit params"""
        super().__init__(*args)

    def t_rules(self) -> None:
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
        if self.player1.chips >= self.min:
            bet = input("How much would you like to bet?: ")
            if self.player1.chips >= int(bet):
                try:
                    if int(bet) >= self.min:
                        return player_bet_list.append(int(bet))
                    elif int(bet) < self.min:
                        print(f"Please enter a bet between of at least ${self.min}")
                        self.player_bet()
                except ValueError:
                    print(f"Please enter a valid bet!")
                    self.player_bet()
            else:
                print(
                    f"You only have ${player_stats[0]['chips']} remaining in chips. Please choose a lower bet."
                )
                self.player_bet()
        else:
            printslow(
                "You don't have enough chips to play at this table yet. Try the other tables first! \n"
            )
            printslow("Returning to Main Menu.")
            sleep(2)
            main_menu()

    def results(self, bet: int) -> str:
        p_score = self.scores("player")
        d_score = self.scores("dealer")
        if len(self.player) == 2 and p_score == 21:
            self.player1.update_stats(
                chips=int(bet * 1.5), chip_won=int(bet * 1.5), wins=1
            )
            return f"Blackjack earns extra chips! You won ${int(bet*1.5)}!\n"
        elif d_score > 21:
            self.player1.update_stats(chips=int(bet), chip_won=int(bet), wins=1)
            return f"You won &{bet}\n"
        elif d_score < 21 and ((p_score > d_score) and p_score <= 21):
            self.player1.update_stats(chips=int(bet), chip_won=int(bet), wins=1)
            return f"Player {p_score} beats dealer {d_score}. You won ${bet}!\n"
        elif p_score == d_score:
            return f"Hand was a tie, no chips gained or lost!\n"
        elif (
            (p_score < d_score)
            or (len(self.player) > 2 and d_score == 21)
            or p_score > 21
        ):
            self.player1.update_stats(chips=-int(bet), chip_lost=int(bet), losses=1)
            return f"You lost ${bet}!\n"


# player class to hold player data
class Player:

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
        "sets up initial player stats, all default values are parsed in here"
        self.name = name.capitalize()
        self.chips = chips
        self.hands = hands
        self.wins = wins
        self.losses = losses
        self.chip_won = chip_won
        self.chip_lost = chip_lost

    def new_save(self) -> None:
        "saves new players data to the save file"
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
        for key, value in kwargs.items():
            for x in player_stats:
                x[key] += value

    def read_stats(self) -> None:
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
        except IndexError:
            print("No player data exists, please create or load a player!")


# global functions not tied to any class but may use class data
def new_tables() -> None:
    try:
        with open(n_t_stats_json, "r") as f:
            save = j.load(f)
            table_stats.clear()
            table_stats.append(save)
    except j.decoder.JSONDecodeError:
        pass


def save_tables() -> None:
    with open(t_stats_json, "w") as f:
        j.dump(table_stats[0], f, indent=4)


def load_tables() -> None:
    try:
        with open(t_stats_json, "r") as f:
            save = j.load(f)
            table_stats.append(save)
    except j.decoder.JSONDecodeError:
        pass


def load_stats() -> None:
    """without this function, saves will not be carried over between multiple playthroughs, this loads all data in at the start of each session"""
    try:
        with open(p_stats_json, "r") as f:
            save = j.load(f)
            player_stats.append(save)
    except j.decoder.JSONDecodeError:
        pass


def save_stats() -> None:
    """saves all stats of all currently saved players"""
    with open(p_stats_json, "w") as f:
        j.dump(player_stats[0], f, indent=4)


def new_player() -> Player:
    """saves new players data to the save file"""
    printslow(
        "Are you sure you would like to start a new game? All previous save data will be deleted.\n",
        delay=0.03,
    )
    while True:
        confirm = input("Confirm new player (Y or N)?: ")
        if "y" and "n" in confirm.lower():
            printslow("Please enter one choice only.\n")
        elif "y" in confirm.lower():
            name = input("Please enter a name for your player: ")
            player_stats.clear()
            player1 = Player(name)
            player1.new_save()
            return player1
        elif "n" in confirm.lower():
            printslow("Returning to Main Menu."), os.system("clear")
        else:
            printslow("Please enter a valid choice: Y or N.\n")


def printslow(text, delay=0.05) -> None:
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        sleep(delay)


def main_menu() -> None:
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
        elif choice == "3" or "rules" in choice.lower():
            os.system("clear")
            house_rules()
            return main_menu()
        elif choice == "4" or "see pla" in choice.lower():
            progbar("Loading player stats...")
            sleep(2)
            os.system("clear")
            load_stats()
            player1 = choose_player()
            player1.read_stats()
            input("Press any key to return to Main Menu")
            return main_menu()
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
        elif choice == "6" or "quit" in choice.lower():
            os.system("clear")
            return custom_quit()
        else:
            printslow("Invalid selection, please try again.\n")


def house_rules() -> None:
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
        if tablec == "1" or "low" in tablec.lower():
            activetable = low
            return activetable
        elif tablec == "2" or "mid" in tablec.lower():
            activetable = mid
            return activetable
        elif tablec == "3" or "high" in tablec.lower():
            activetable = high
            return activetable
        elif tablec == "4" or "no" in tablec.lower():
            activetable = nolimit
            return activetable
        elif tablec == "5" or "exit" in tablec.lower():
            printslow("Returning to Main Menu")
            sleep(2)
            os.system("clear")
            main_menu()
        else:
            print("Invalid selection, please select a table from the above.")


def choose_player() -> Player:
    player1 = Player(*[x for x in player_stats[0].values()])
    return player1


def progbar(desc, rng: int = 30) -> None:
    for i in p.track(range(rng), description=desc):
        sleep(0.1)  # Simulate work being done


def asciicards(filename: str, *lists: tuple) -> str:
    """
    Creates a side by side ASCII of two or more cards
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
    printslow("Thanks for playing!\n")
    while True:
        printslow("Would you like to save your data?\n")
        save = input("Y/N: ")
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
                quit()
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
                    if err_ex == "1" or "main" in err_ex.lower():
                        printslow("Returning to Main Menu.")
                        sleep(2)
                        return main_menu()
                    elif err_ex == "2" or "exit" in err_ex.lower():
                        printslow(
                            "\nThanks for playing, please start a new game next time you play!"
                        )
                        sleep(2)
                        os.system("clear")
                        quit()
                    else:
                        printslow("Invalid input, please try again.\n")
        elif save.lower() == "n":
            printslow("Are you sure? ")
            check = input("Y/N: ")
            if check.lower() == "y":
                return printslow("See you next time!\n"), os.system("clear"), quit()
            elif check.lower() == "n":
                continue
            else:
                printslow("Please enter either Y or N")
        else:
            printslow("Please enter either Y or N")


def meme(text: str, delay: int = 0.05) -> None:
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
    a.aprint("confused3")
    sleep(0.5)
    a.aprint("table flip")
    sleep(0.5)
    a.aprint("cry")
    sleep(0.5)
    print(co.Fore.RED + co.Style.BRIGHT + "ERROR! ERROR! " + co.Style.RESET_ALL)
    sleep(0.5)
    meme("ALL YOUR BASE ARE BELONG TO US!")
    printslow(
        "Ahem... Sorry about that. Anyway, turns out your save data is corrupted or missing, would you kindly start a new game?"
    )
    sleep(1)
    for i in range(3):
        printslow("\nWould you kindly...", delay=0.06)
        sleep(0.5)
    printslow(
        "\nOkay, enough video game references, let's go back to the Main Menu already\n"
    )
    a.aprint("happy4")
    sleep(0.5)
