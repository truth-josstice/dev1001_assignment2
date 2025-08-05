# Class and Function Usage

## Main Gameplay Loop

- ```mainloop()``` - Core game loop managing all gameplay flows and error handling.
  - Parameters:
    - None
  - Returns:
    - ```None``` (perpetual loop until exit)
  
  - Primary Workflow:
    1. ```main_menu()``` entry
    2. ```choose_table()``` selection
    3. ```t_rules()``` display
    4. Betting → Dealing → Player/Dealer turns
    5. ```results()``` evaluation
    6. Play-again prompt

  - Key Features:
    - Manages all object states, and local list management:
      - Chip tracking (```player_stats```)
      - Table bank monitoring
      - Bet list clearing
    - Visual polish:
      - ```progbar()``` loading indicators
      - Double ```os.system("clear")``` for flicker reduction
      - Consistent 2-second transitions
  - Error Handling:
    - ```IndexError```: Corrupt data → ```meme_error()```
    - ```FileNotFoundError```: Missing saves → new player prompt
    - ```KeyboardInterrupt```: Graceful exit options
    - ```SystemExit```: Clean termination
    - Universal fallback error to catch unknown errors and return to game play loop via ```main_menu()```
  - State Checks:
    - Table chip availability
    - Player chip balance
    - Play-again decisions

## Imported Classes

```Deck``` from ```playingcards``` package is a collection of cards that form a standard 52 card deck, in some cases this has been modified to 104 cards.

- Methods imported from Deck:
  - ```shuffle()``` - Shuffles the cards in the collection (via ```random``` standard module).
  - ```draw_n(n)``` - Draws a number of cards from the top of the deck.

```Card``` from ```playingcards``` is a card object with params of suit, rank and value which assists with scoring and identification of card objects.

## Custom Classes

This app contains two custom classes, Table and Player, as well as the NoLimit Table subclass.
    
```Table``` is a specific table with a finite amount of chips, minimum and maximum bet limits, and a transparent rule set based on specific blackjack standards.  
```Table``` attributes:

```python
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
```

```NoLimit``` Table subclass attributes are the same as above, but have null values for params which are no longer applicable, as well as custom functions to account for these changes.

```Player``` creates the player instance based on user input of name, with default values for starting amount of chips.  
```Player``` attributes:

```python
    # Class-level type annotations. Details what attributes the class has, and type of attribute.
    name: str  # The player’s name, used for display/tracking player
    chips: int  # Current players chip total
    hands: int  # Total hands played by player
    wins: int  # Total hands won by player
    losses: int  # Total hands lost by player
    chip_won: int  # Total chips won by player
    chip_lost: int  # Total chips lost by player
```

### ```Table``` Class Methods

*All Table methods take **self** as a param*

- ```new_table()``` - Sets up default table statistics by clearing and overwriting the local ```table_stats``` list with Table object params.
  - Parameters:
    - None
  - Returns:
    - ```None``` (modifies local ```table_stats``` list)

- ```new_deal()``` - Deals the opening hand to dealer and player (using ```Deck.draw_n()``` from ```playingcards``` package) and displays in ASCII format.
  - Parameters:
    - None
  - Returns:
    - ```None``` (prints directly to console)

- ```t_rules()``` - Prints the current Table object rules using Table object params.
  - Parameters:
    - None
  - Returns:
    - ```None``` (prints directly to console)

- ```first_hand()``` - Displays the dealer's first card rank and suit in ASCII format (using ```asciicards()``` function), and keeps second card hidden.
  - Parameters:
    - None
  - Returns:
    - ```None``` (prints directly to console)

- ```display_hand(hand)``` - Displays the cards and score of passed hand in ASCII format (using ```asciicards()``` function).
  - Parameters:
    - hand(```List```) - A list of Card objects
  - Returns:
    - ```None``` (prints directly to console)

- ```eval_hand(name, score, cards)``` - Evaluates if held cards are Blackjack or Bust. Uses ```colorama``` package for colored text display.
  - Parameters:
    - name(```str```) - Denotes either Dealer or Player hand
    - score(```int```) - Total score of evaluated cards
    - cards(```list```) - A list of Card objects
  - Returns:
    - ```None``` (prints directly to console)

- ```scores(hand)``` - Assigns specific points to each card as per blackjack rules, converts any held Aces to wild (11 or 1) depending on total score to avoid busting.
  - Parameters:
    - hand(```str```) - Denotes either Dealer of Player hand
  - Returns:
    - ```int``` - Adjusted total of all cards in hand
  - Example use:

```python
# If player's hand is [Ace, King, 5]:
scores("player")  
# Returns 16 (Ace=11, King=10, 5 → 26 → adjusted to 16)
```

- ```player_bet()``` - Input request to user for bet amount with validation checks for Table object minimum and maximum bet params.
  - Parameters:
    - None
  - Returns:
    - ```None``` (appends valid bets to ```player_bet_list``` initiated by this function)

- ```double_down()``` - Input request to user to double bet before making a move.
  - Parameters:
    - None
  - Returns:
    - ```None``` (modifies ```player_bet_list``` in-place if doubling is accepted)

- ```player_move()``` - Handles player's turn actions (hit/stand) with card limit enforcement, triggers dealers turn (using ```dealer_ai()```), automatically stands on bust.
  - Parameters:
    - None
  - Returns:
    - ```None``` (prints directly to console)

- ```dealer_ai()``` - Manages the display of the dealer's turn logic and hand display, triggers decision making (using ```ai_threshold()```), automatically stands after blackjack. Uses ```colorama``` package for colored text display.
  - Parameters:
    - None
  - Returns:
    - ```None``` (prints directly to console)

- ```ai_threshold()``` - Implements dealer's hit/stand decision logic based on table rules and dealer score (using ```scores()```) and prints message for dealer's chosen move.
  - Parameters:
    - None
  - Returns:
    - ```None``` (prints directly to console)

- ```results(bet)``` - Evaluates hand outcomes and updates player_stats list accordingly depending on win/loss/tie conditions, displays the results in formatted string.
  - Parameters:
    - ```bet``` (int) - User's input bet amount
  - Returns:
    - ```str``` - Formatted result message
  - Example output:

```
"Blackjack earns extra chips! You won $30!\n"
(From a $20 bet at 1.5x payout)

"Player 19 beats dealer 17. You won $20!"

"Hand was a tie, no chips gained or lost!"

"You lost $20!"
```

- ```update_stats(**kwargs)``` - Increments current Table object table_stats list index using keyword arguments.
  - Parameters:
    - ```**kwargs``` (dict) - Key-value pairs of stats to update (e.g., `bank=100`)
  - Returns:
    - ```None``` (updates `table_stats` in-place)
  - Example use:

```python
    update_stats(bank=-50) # subtracts from table bank
    update_stats(max_bet=200) # adjusts bet limits
```

### ```NoLimit``` Subclass Methods

- ```t_rules()``` - Displays customized table rules whilst removing the parent class params which are no longer applicable.
  - Parameters:
    - None
  - Returns:
    - ```None``` (prints directly to console)

- ```player_bet()``` - Handles player betting with no maximum limit (```NoLimit``` table version).
  - Parameters:
    - None
  - Returns:
    - ```None``` (appends valid bets to ```player_bet_list```)

- ```results(bet)``` - Customised from parent class function, no longer includes incremental changes to ```self.bank``` as this table has no bank amount.
  - Parameters:
    - ```bet``` (int) - User's input bet amount
  - Returns:
    - ```str``` - Formatted result message

### ```Player``` Class Methods

- ```new_save()``` - Creates a new player profile by clearing and appending the default Player object params to ```player_stats``` list.
  - Parameters:
    - None
  - Returns:
    - ```None``` (appends ```player_stats``` list)

- ```update_stats(**kwargs)``` - Modifies player statistics using keyword arguments.
  - Parameters:
    - ```**kwargs``` (dict) - Key-value pairs to update (e.g., `wins=1`, `chips=50`)
  - Returns:
    - ```None``` (updates ```player_stats``` in-place)
  - Example use:

```python
# After a winning hand:
player.update_stats(
    chips=40,       # Add $40 to player chip total
    wins=1,          # Increment win counter
    hands=1,         # Add to total hands played
    chip_won=40     # Add to total amount of won chips
)

# After a losing hand
player.update_stats(
    chips=-50,       # Remove lost chips from chip total
    losses=1,        # Increment loss counter
    hands=1,         # Add to total hands played
    chip_lost=50     # Record total amount of lost chips
)
```

- ```read_stats()``` - Displays formatted player statistics based on ```Player``` object params.
  - Parameters:
    - None
  - Returns:
    - ```None``` (prints directly to console)
  - Example output:

```text
============= Player Stats =============
    Player: Alex
    Current chip total: $120
    Total hands played: 40
    Total hands won: 21
    Total hands lost: 19
    Total chips won: $920
    Total chips lost: $800
========================================
```

### Global Functions

Many of the global functions interact with external file data, either in CSV or JSON format. Though not directly tied to any Class, class data or objects may be created here for use in gameplay loop.

- ```new_tables()``` - Initializes table data by loading default values from JSON file and appending to ```table_stats``` list.
  - Parameters:
    - None
  - Returns:
    - ```None``` (modifies global ```table_stats``` list)

- ```save_tables()``` - Saves current table statistics to a JSON file allowing user to continue from saved state.
  - Parameters:
    - None
  - Returns:
    - ```None``` (writes to file system)

- ```load_tables()``` - Loads previous gameplay data from JSON and dumps into ```table_stats``` list.
  - Parameters:
    - None
  - Returns:
    - ```None``` (updates global ```table_stats``` list)

- ```load_stats()``` - Loads saved player data from JSON and dumps into ```player_stats``` list.
  - Parameters:
    - None
  - Returns:
    - ```None``` (modifies global ```player_stats``` list)

- ```save_stats()``` - Saves current player data to a JSON file allowing user to continue from saved state.
  - Parameters:
    - None
  - Returns:
    - ```None``` (writes to filesystem)

- ```new_player()``` - Creates a new ```Player``` object and appends local ```player_stats``` list, prompts user for confirmation due to overwriting existing data. 
  - Parameters:
    - None
  - Returns:
    - ```Player``` object (initialized with new player data)

- ```printslow(text, delay)``` - Prints text character by character.
  - Parameters:
    - ```text``` (str) - String to print
    - ```delay``` (float, optional) - Seconds between characters (default: 0.05)
  - Returns:
    - ```None``` (prints directly to console)

- ```main_menu()``` - High level navigation hub with interactive menu system and user input prompts.
  - Parameters:
    - None
  - Returns:
    - ```None``` (recursively calls itself to ensure Main Menu display on decline or completion of choices)

- ```house_rules()``` - Displays "Casino of Truth and Josstice" blackjack rules and gameplay instructions.
  - Parameters:
    - None
  - Returns:
    - ```None``` (returns to ```main_menu()``` after interaction)

- ```choose_table()``` - A table selection menu which prompts for user input and creates a ```Table``` object using list comprehension.
  - Parameters:
    - None
  - Returns:
    - ```Table | NoLimit``` object (selected table instance)

- ```choose_player()``` - Creates a ```Player``` object based on currently saved player data using list comprehension.
  - Parameters:
    - None
  - Returns:
    - ```Player``` object (initialized with saved player data)

- ```progbar()``` - Modified progress bar function from ```rich``` package (using ```rich.track```) to simulate task progress as a form of visual feedback.
  - Parameters:
    - ```desc``` (str) - Displayed at left of progress bar for clean visuals
    - ```rng``` (int, optional) - Number of steps the progress bar will increment by (default: 30)
  - Returns:
    - ```None``` (visual output only)

- ```asciicards()``` - Generates and displays side-by-side ASCII card art by rewriting external CSV data files.
  - Parameters:
    - ```filename``` (str) - Target CSV file path
    - ```*lists``` (tuple) - Card art tuples to combine
  - Returns:
    - ```str``` (prints ASCII card art to console)

- ```custom_quit()``` - Handles graceful program termination with save options.
  - Parameters:
    - None
  - Returns:
    - ```None``` (terminates program via ```sys.exit()```)

- ```meme()``` - A modified version of printslow, also uses mimics input to move cursor and overwrite text.
  - Parameters:
    - ```text``` (str) - Text to display and erase  
    - ```delay``` (int, optional) - Typing speed in seconds (default: 0.05)
  - Returns:
    - ```None``` (visual effect only)

- ```meme_error()``` - A "humorous" custom error message which automatically prints text and returns to the main menu.
  - Parameters:
    - None
  - Returns:
    - ```None``` (eventually returns to ```main_menu()```)