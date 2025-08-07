# Installation Guide

---

## Table of Contents

- [Installation Guide](#installation-guide)
  - [Table of Contents](#table-of-contents)
  - [System Requirements](#system-requirements)
  - [Installation Instructions](#installation-instructions)
    - [Installing for Linux/WSL/Mac](#installing-for-linuxwslmac)
    - [Installing for Windows](#installing-for-windows)

[⇨ Go to Usage Instructions](./USAGE_INSTRUCTIONS.md)
[⇦ Back to README](./readme.md)

---

## System Requirements

- Python 3.10+ (3.12 recommended)
- PIP (python package installer)
- Windows, Linux, WSL or MacOS
- Active internet connection for cloning dependencies

## Installation Instructions

Before you begin, please select your operating system to follow the correct setup steps:

- [Linux/WSL/Mac](#linuxwslmac)
- [Windows CMD](#windows)

> ⚠️ **IMPORTANT: Make sure to follow the steps for your specific system to avoid command errors or path issues.**

---

### Installing for Linux/WSL/Mac

1. **Verify Python Version**

   ```bash
   python3 --version  # Should display Python 3.10 or higher
   ```

2. **Choose one of the following methods:**
   - Download and extract the ZIP folder to your desired directory
   **OR**
   - Clone directly from [this github repository](https://github.com/truth-josstice/dev1001_assignment2)

   ```bash
   git clone https://github.com/truth-josstice/dev1001_assignment2
   cd dev1001_assignment2
   ```

3. **Create and Activate Virtual Environment**

   ```bash
   python3 -m venv .venv  # Creates virtual environment
   source .venv/bin/activate  # Activates virtual environment
   ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt  # Depending on pip version, pip3 may be required instead
   ```

5. **Run the Application**

   ```bash
   python3 blackjack.py
   ```

6. **Deactivate Virtual Environment when Finished**

   ```bash
   deactivate
   ```

> ✅ **NEXT STEPS:** Once installation is complete, proceed to the **[Usage Instructions](./USAGE_INSTRUCTIONS.md)** to learn how to run and play the game.

---

### Installing for Windows

> ⚠️ **IMPORTANT: Use Command Prompt (CMD) - not PowerShell.**

1. **Verify Python Version**

   ```cmd
   python --version  # Should display Python 3.10 or higher
   ```

2. **Choose one of the following methods:**
   - Download and extract the ZIP folder to your desired directory
   **OR**
   Clone directly from [this github repository](https://github.com/truth-josstice/dev1001_assignment2)

   ```cmd
   git clone https://github.com/truth-josstice/dev1001_assignment2
   cd dev1001_assignment2
   ```

3. **Create and Activate Virtual Environment**

   ```cmd
   python -m venv .venv  # Creates virtual environment
   .venv\Scripts\activate  # Activates Virtual Environment
   ```

4. **Install Dependencies**

   ```cmd
   pip install -r requirements.txt  # Depending on pip version, pip3 may be required instead
   ```

5. **Run the Application**

   ```cmd
   python run_blackjack.py
   ```

6. **Deactivate Virtual Environment when Finished**

   ```cmd
   deactivate
   ```

> ✅ **NEXT STEPS:** Once installation is complete, proceed to the **[Usage Instructions](./USAGE_INSTRUCTIONS.md)** to learn how to run and play the game.

---

[⇧ Back to Top](#installation-guide) | [⇦ Back to README](./readme.md) | [⇨ Usage Instructions](./USAGE_INSTRUCTIONS.md)
