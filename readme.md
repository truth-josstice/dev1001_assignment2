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

- Python 3.12 or above (Tested and recommended Python Version 3.12.1) — earlier versions may work but are not guaranteed to be fully compatible.
- Note: If you encounter compatibility issues on Python versions below 3.13, please check library versions in requirements.txt or consider upgrading Python.


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


<!-- Nhi -->

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


### Ethical Considerations

As a developer of a simulated gambling application, I recognise the ethical responsibilities involved in minimising harm, promoting fair play and ensuring legal compliance. While this current development project is a non-commercial, educational simulation with no real money involved, future development updates will aim to include integrations towards aligning with responsible design principles to comply with regulations and meet ethical best practices including:

**1. Responsible Design and Prevention of Harm**
- Minimise Risk of Addiction:
Avoided features that encourage excessive play or mimic addictive mechanics such as reward loops and rapid replay. The slow print integration minimises the speed at which players are able to be able to replay rapidly however limits of play may be introduced to minimise excessive gameplay.
- Transparent Communication:
This document clearly communicates to users that the application is a simulation for educational and entertainment purposes and does not invvolve real money or financial loss or gain. This is to avoid misleading representations that may contribute to risky behaviours.

<!-- Research source: Simulated gambling environments can normalise betting behavior and increase the risk of problem gambling, even when no real money is involved. -->

**2. Legal and Regulatory Compliance**
- Age Restrictions:
Future development considerations would be to integrate age verification with age check to comply with local laws.

<!-- Research source: Compliance with Local Laws:
Ensure the game does not violate online gambling regulations, such as those outlined in the Australian Interactive Gambling Act. Even simulated gambling may fall under regulatory scrutiny if it promotes betting or could be mistaken for real gambling.-->

**3. Data Privacy and Player Protection**
- Protection of User Data:
Future development considerations would be to integrate user profile authentication to protect user profile and player data.
Personal data is not collected or shared and no sensitive information to users are stored or collected.
App includes data files which are stored locally upon installing application and user profile data can be manually deleted from files by user.

<!-- Research source: Applications should responsibly handle any personal or gameplay data, ensuring privacy and security. Persistent storage of statistics or profiles should not expose sensitive information. -->

**3.Promotion of Fair Play**
- Algorithmic Fairness:
Randomisation of card dealing and outcome determination is genuinely random (not rigged to favor the house or induce losses).

<!-- Can probably consider including a documented logic (like flowshare) to show how functions use randomisation/ai to support fairness in gameplay. -->

<!-- Research source: Disclosure of Odds and Rules: Game rules, odds, and payout structures must be accessible and understandable to all users. Hidden mechanics or unclear rules undermine informed user choice. -->

**4. Social and Psychological Impact**
- Mental Health Awareness:
While this application is not intended to be widely distributed or open-source, I acknowledge the potential influence of simulated gambling environments on user behaviour and mental wellbeing.

I encourage all users to engage responsibly and be mindful of the psychological impacts associated with gambling related activities (even in a simulated context). If you or someone you know is experiencing gambling related concerns or requires mental health support, please reach out to the following Australian support services:

- Gambling Help Online (24/7 support) – https://www.gamblinghelponline.org.au
- Lifeline Australia (Crisis Support & Suicide Prevention) – 13 11 14 | https://www.lifeline.org.au
- Beyond Blue (Mental Health Support Services) – 1300 22 4636 | https://www.beyondblue.org.au
- Relationships Australia (Gambling Counselling & Family Support) – https://www.relationships.org.au

For additional resources and regulations, please consult local laws and guidelines relevant to gambling activities in your region.

<!-- Research source: Consider including resources or warnings about problem gambling and offer links to support services if the game is widely distributed.
Avoiding Social Harm: Developers should be aware that simulated gambling can influence attitudes towards real gambling, potentially leading to harmful behaviors over time.-->


<!-- IMPORTANT TO NOTE FOR THIS DEVELOPMENT PROJECT:
"Developers working on gambling simulations bear ethical responsibilities to minimise harm, comply with relevant laws, protect user data, and promote fair, transparent play. Referencing regulatory and academic guidance is essential to ensure that such projects do not inadvertently contribute to gambling-related harms or regulatory breaches."

I've done the research relevant to this ethical concern of simulated gambling using the below resources/references:
1. [ACMA Interactive Gambling Act Overview](https://www.acma.gov.au/about-interactive-gambling-act)
2. [Academic Analysis (TandF)](https://www.tandfonline.com/doi/full/10.1080/15256480.2025.2494575?src=exp-la)
3. [Parliamentary Report - Simulated Gambling](https://www.aph.gov.au/Parliamentary_Business/Committees/House/Social_Policy_and_Legal_Affairs/Onlinegamblingimpacts/Report/Chapter_6_-_Simulated_gambling_and_gambling-like_activities) -->
