# Installation

## Requirements

- Python 3.10+ (3.12 recommended)
- PIP (python package installer)
- Windows, Linux or MacOS
- Active internet connection

## Installation Instructions

- [Linux/WSL/Mac](#linuxwslmac)
- [Windows CMD](#windows)

### Linux/WSL/Mac

1. Verify version

   ```bash
   python3 --version # Should show 3.10 or higher
   ```

2. Download and extract ZIP folder to desired directory
   **OR**
   Clone from [this github repository](https://github.com/truth-josstice/dev1001_assignment2)

   ```bash
   git clone https://github.com/truth-josstice/dev1001_assignment2
   cd dev1001_assignment2
   ```

3. Create and activate the Virtual Environment

   ```bash
   python3 -m venv .venv # Creates virtual environment
   source .venv/bin/activate # Activates virtual environment
   ```

4. Install dependencies

   ```bash
   pip install -r requirements.txt # Depending on pip version, pip3 may be required instead
   ```

5. Run application!

   ```bash
   python3 blackjack.py
   ```

6. Deactivate when finished

   ```bash
   deactivate
   ```

### Windows

**_Use CMD not Powershell_**

1. Verify version

   ```cmd
   python --version # Should show 3.10 or higher
   ```

2. Download and extract ZIP folder to desired directory
   **OR**
   Clone from [this github repository](https://github.com/truth-josstice/dev1001_assignment2)

   ```cmd
   git clone https://github.com/truth-josstice/dev1001_assignment2
   cd dev1001_assignment2
   ```

3. Create the Virtual Environment

   ```cmd
   python -m venv .venv # Creates virtual environment
   .venv\Scripts\activate # Activates Virtual Environment
   ```

4. Install dependencies

   ```cmd
   pip install -r requirements.txt # Depending on pip version, pip3 may be required instead
   ```

5. Run application!

   ```cmd
   python blackjack.py
   ```

6. Deactivate when finished

   ```cmd
   deactivate
   ```
