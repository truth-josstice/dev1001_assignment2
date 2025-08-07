# Using the App

## Table of Contents

- [Using the App](#using-the-app)
  - [Table of Contents](#table-of-contents)
  - [Main Menu Options](#main-menu-options)
    - [**1.** `New Game`](#1-new-game)
    - [**2.** `Play Some Blackjack!`](#2-play-some-blackjack)
      - [`Table Menu:`](#table-menu)
    - [**3.** `Rules for Playing`](#3-rules-for-playing)
    - [**4.** `See Your Stats`](#4-see-your-stats)
    - [**5.** `See Table Chips Remaining`](#5-see-table-chips-remaining)
    - [**6.** `Quit`](#6-quit)
  - [Data Management and Privacy](#data-management-and-privacy)

[⇨ Go to Installation Guide](./INSTALLATION.md)
[⇦ Back to README](./readme.md)

---

## Main Menu Options

After launching the game by executing `run_blackjack.py` in the terminal, you will be presented with a menu displaying the following options:

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

---

### **1.** `New Game`

For creating a new user profile. Grants the following options -

- `Confirm new player (Y or N)?:`
  - `Y`. Creates new player profile
    - `Please enter a name for your player:` Enter name for new user profile and return to main menu
  - `N`. Returns to main menu

---

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

---

### **3.** `Rules for Playing`

Displays the House Rules and Gameplay Rules for the blackjack application, with any key selection returning you to the main menu.

![House Rules and Gameplay Rules](/images/house-gameplay-rules.png "House Rules and Gameplay Rules")

---

### **4.** `See Your Stats`

Displays the current statistics (e.g. current chips) for the current user profile, with any key selection returning you to the main menu.

---

### **5.** `See Table Chips Remaining`

Displays the current chips remaining at each table that the player can win!

---

### **6.** `Quit`

Grants the following options -

- `Would you like to save your data?`
  - `Y`. Saves user profile before exiting application
  - `N`. Exits application without saving user profile

---

## Data Management and Privacy

**How to Delete Player Game Data (Manual Reset Guide)**

All game progress is saved in a local file called `playerstats.json` located in the project folder.
If you want to reset your game stats without deleting the file, you can manually clear the data by editing it.

To reset your player data, follow these steps:

1. **Open `playerstats.json`:**

   - Navigate to your project folder.
   - Locate and open the file named `playerstats.json` using a text editor (eg VS Code).

2. **Replace the Data with Default Values:**
   - Replace the existing content with the following structure to reset all progress:

```json
{
  "name": "YourName",
  "chips": 100,
  "hands": 0,
  "wins": 0,
  "losses": 0,
  "chip_won": 0,
  "chip_lost": 0
}
```

3. **Save the File:**
   - After updating, save the file.
   - On the next game launch, the stats will be reset as if you're starting fresh.

> ⚠️ **Important Notes:** > **DO NOT DELETE** the `playerstats.json` file itself - only edit the contents inside.
> Editing the contents of this file will reset your chips, statistics and progress back to default.
> Make sure you keep the structure (curly braces {}, commas, and field names) exactly as shown in code snippet above.
> No sensitive or personal data is stored in the JSON file.

---

[⇧ Back to Top](#usage-instructions) | [⇦ Back to README](./readme.md) | [⇨ Installation Guide](./INSTALLATION.md)
