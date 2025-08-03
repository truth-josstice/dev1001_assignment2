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

