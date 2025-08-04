# Blackjack of Truth and Josstice!
This is both my first Python project, and my first coding project ever! It is also the second assessment in my first term of CoderAcademy! Welcome fellow alumni and fellow cohort members!

## Gameplay and Features
Player and table data is either initialised through a new game, or loaded from JSON files to continue progress. There are multiple control flows and loops used to not only parse and create data, but to enable the player to play a realistic blackjack simulator!
Specific features and functions:
- Save file creation: Creates new player data and tables with base stats in JSON format.
- Play poker: Loads in data from previous saved files, allows player to play at four different tables with different rulesets and bet limits. Individual tables have specific amounts of chips to be won.
- Poker hands using customised asciicard function: Allows player cards to be displayed in line and calculated using CSV files.
- "AI" and results: Many control flows for bet amounts, a rudimentary AI for the dealer, finally ammendments made to stat files to change player and table stats.
- Error catching: multiple bespoke error handling methods.
    - Please note, whilst I have accounted for most errors, some may still occur due to key combinations native to python.
    - A file marked "newtables_DONOTDELETE.json" is an essential file. If this file is missing please re-clone or download from the remote repo.

### System Requirements
- Operating System - Linux, MacOS, Windows
- Python 3.12 or above
- Bash Terminal
    - Ubuntu is preferred.
    <https://ubuntu.com/>
- An active internet connection to download necessary packages and/or clone repo

### Step by Step Setup Guide
1. Clone or download the repo to a local folder: <https://github.com/truth-josstice/dev1001_assignment2>
2. Open Bash Terminal and navigate to local folder:
    ```bash
    cd path/to/directory
    ```
3. Creating a virtual environment is generally best practice when installing packages. This helps to ensure you do not overwrite any globally installed packages. To create a new virtual environment enter the below in the project folder on Terminal:
    ```bash
    python3 -m venv .venv
    ```
4. Activate the virtual environment using the below code:
    ```bash
    python3 source .venv/bin/activate/
    ```
5. Install all required packages via the pip install code below:
    ```bash
    pip3 install -r requirements.txt
    ```
6. Ensure you are set up correctly to run the program using the code below:
    ```bash
    pip3 list
    ```
7. Run the blackjack.py program:
    ```bash
    python3 blackjack.py
    ```

### Licenses
The following third party libraries were used:
| **Package Name** | License | Link |
| --- | --- | ---|
|**colorama**| OSI Approved - BSD License |<https://github.com/tartley/colorama/blob/master/LICENSE.txt> |
| **rich**| OSI Approved - MIT License |<https://github.com/Textualize/rich/blob/master/LICENSE>|
| **art** | OSI Approved - MIT License |<https://github.com/sepandhaghighi/art/blob/master/LICENSE>|
| **playingcards**|OSI Approved - MIT License|<https://github.com/blakepotvin/playingcards.py/blob/master/LICENSE>|

#### Notes:
*All libraries are used in accordance with their individual licenses. Colorama copyright information contained in this readme file in accordance with BSD license.*
*User data (Player Name) is only collected via input from the user, and is stored locally. No sensetive information is requested or stored either locally or online. No third parties have access to user stored data.*

### Purpose of the App

This project is part of a student based learning assessment to develop a command-line Python application. This project app simulates the classic card game 'Blackjack'. It allows users to interact with different table types, learn house and gameplay rules, practice strategies and manage chips in a simple-interface and interactive environment.

### Usage of the App

This application is designed to be intended for educational and recreational/entertainment purposes only. It does not involve any real money or gambling. We encourage responsible gameplay and discourage excessive or compulsive play.

It is used to allow users to:
- Learn basic Blackjack gameplay rules and strategies.
- Practice managing chips and decision-making across various tables
- Engage in gameplay that reinforces understanding of house rules and betting scenarios — without involving real money

The app provides a simple menu-driven interface that enables users to interact with different virtual tables, track their gameplay statistics, and explore the flow of a typical Blackjack session. It serves as a foundational tool for those wanting to understand Blackjack in a risk free, simulation based setting.

<!-- Think it would be good to include this description below but this would be after the implementation of the above functionality:

"The app is designed to comply with relevant legal and ethical standards, including age restrictions and data privacy. Please consult local laws for further information, and seek support if you believe you may be at risk for problem gambling."-->


### Features of the App

- Easy navigation via a menu-driven interface
- Creation of new user profile with optional choice to save gameplay data to their existing user profile after gameplay
- Multiple table types to play. Each table starts with a default amount of chips remaining to win when starting new game including:
    - Low Rollers: $200 chips
    - Mid Rollers: $500 chips
    - High Rollers: $1000 chips
    - No Limit (Win as many chips as you like)
- Displays the current chips remaining at each table that the player can win
- Displays player statistics for current user including:
    - Current chip total
    - Total hands played
    - Total hands lost
    - Total chips won
    - Total chips lost
- Enhanced visuals with ASCII card play display
- Includes in app 'House Rules' and 'Gameplay Rules' on how to play this app's version of 'Blackjack'
![House Rules and Gameplay Rules](/images/house-gameplay-rules.png "House Rules and Gameplay Rules")
