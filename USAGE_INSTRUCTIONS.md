# Using the App

## Main Menu Options

After launching the game, you will be presented with a menu displaying the following options:

```bash
============ Welcome to Blackjack! ============
                1. New Game
                2. Play Some Blackjack!
                3. Rules for Playing
                4. See Your Stats
                5. See Table Chips Remaining
                6. Quit
    -----------------------------------------------
            Press Ctrl+C to quit at any time.
    ===============================================
                Please select an option:
```

### **1.** `New Game`

For creating a new user profile. Grants the following options -

- `Confirm new player (Y or N)?:`
  - `Y`. Creates new player profile
    - `Please enter a name for your player:` Enter name for new user profile and return to main menu
  - `N`. Returns to main menu

### **2.** `Play Some Blackjack!`

For commencing a game of blackjack. If no current active user profile, will prompt to select `New Game` prior to returning to main menu. Grants the following options -

- `Continue your game as <user_name>? (Y/N):`
  - `Y`. Confirms currently active user profile before proceeding to [Table Menu](#table-menu)
  - `N`. Prompts to select `New Game` and returns to main menu

#### `Table Menu:`

Displays the different table options as follows, with each table selection detailing max and min bet, chips remaining at the table, and deck size -

```bash
1. Low Rollers Table
2. Mid Rollers Table
3. High Rollers Table
4. No Limit Table
5. Exit to Main Menu
```

- `How much would you like to bet?:` Enter amount desired for betting, ensuring that the bet size is between the min and max amount and that you currently have enough chips
  - `Would you like to double your bet?:`
    - `Y`. Doubles the amount of chips for the bet (if you have enough)
    - `N`. Keeps bet amount the same

Hands are then dealt to dealer and player

- `Would you like to hit or stand?:`
  - `Y`. Draws another card for the player, busting if total exceeds 21
  - `N`. Keeps player hand the same, waiting for dealer to reveal their hand and draw or stand as required until they hit 17 or above, or bust

After the player either wins, loses or draws the hand, chip totals are updated and player is presented the `How much would you like to bet?` prompt once more

### **3.** `Rules for Playing`

Displays the House Rules and Gameplay Rules for the blackjack application, with any key selection returning you to the main menu.

### **4.** `See Your Stats`

Displays the current statistics (e.g. current chips) for the current user profile, with any key selection returning you to the main menu.

### **5.** `See Table Chips Remaining`

Displays the current chips remaining at each table that the player can win!

### **6.** `Quit`

Grants the following options -

- `Would you like to save your data?`
  - `Y`. Saves user profile before exiting application
  - `N`. Exits application without saving user profile
