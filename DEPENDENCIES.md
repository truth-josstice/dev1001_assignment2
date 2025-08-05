# Dependencies

---

## Table of Contents

- [Dependencies](#dependencies)
  - [Table of Contents](#table-of-contents)
  - [Third Party Packages/Libraries Licenses](#third-party-packageslibraries-licenses)
  - [Custom-Modified Libraries Used](#custom-modified-libraries-used)
    - [Summary of Modifications](#summary-of-modifications)
      - [Custom Modified Version Details](#custom-modified-version-details)
    - [License Versions](#license-versions)
  - [Security Impacts](#security-impacts)

[⇦ Back to README](./readme.md)

---

## Third Party Packages/Libraries Licenses

| **Package/Library** | **Version** | **License** | **Purpose** |
| :-----------------: | :---------: | :---------: | :---------: |
|      `art`       |   6.5   | [MIT](https://opensource.org/license/MIT) | Python lib for text converting to ASCII art |
|     `colorama`   |  0.4.6  | [BSD-3-Clause](https://opensource.org/license/BSD-3-Clause) | Producing colored terminal text |
|    `iniconfig`   |  2.1.0  | [MIT](https://opensource.org/license/MIT) | INI-file parser module |
| `markdown-it-py` |  3.0.0  | [MIT](https://opensource.org/license/MIT) | Markdown parser |
|     `mdurl`      |  0.1.2  | [MIT](https://opensource.org/license/MIT) | URL utilities for markdown-it parser. |
|   `packaging`    |  25.0   | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0), [MIT](https://opensource.org/license/MIT) | Reusable core utilities for various Python Packaging interoperability specifications |
|      `pluggy`    |  1.6.0  | [MIT](https://opensource.org/license/MIT) | Core framework used by pytest |
|    `Pygments`    |  2.19.1 | [BSD-2-Clause](https://opensource.org/license/BSD-2-Clause) | Syntax highlighting package |
|     `pytest`     |  8.4.1  | [MIT](https://opensource.org/license/MIT) | Used for testing code |
|      `rich`      |  14.0.0 | [MIT](https://opensource.org/license/MIT) | Provides rich text and formatting in terminal |

---

## Custom-Modified Libraries Used

This project includes a custom-modified version of the `playingcards.py` library customised to suit the specific needs of my project CLI game app for “Blackjack of Truth & Josstice!”.

| **Package/Library** | **Version** | **License** | **Purpose** |
| :-----------------: | :---------: |:----------: | :---------: |
|  `playingcards.py` (custom-modified) |  1.1.1  | [MIT](https://opensource.org/license/MIT) | Advanced Python Playing Card Module |

### Summary of Modifications

| **Module** | **Function/Class/Method** | **Modification Description** | **Purpose** |
| :--------: | :-----------------------: | :--------------------------: | :---------: |
| | `def __init__(self, deck: list = None)` | Customised version of Deck class, allows for max of 104 cards per Deck object. 2-Deck variations of Blackjack have more equitable outcomes for player and dealer. | Extend the core deck functionality to support advanced Blackjack rules. |
| | `def __generate_deck(self)` | Customised version of __generate_deck to create deck of 104 cards. | As above |
| | `def __generate_img1(self)` | Customised version of __generate_img used to obscure rank and suit of dealer card. | Enhance functionality and improve terminal-based card rendering. |

#### Custom Modified Version Details

Original Author: Blake Potvin
Original Repository: [playingcards.py](https://github.com/blakepotvin/playingcards.py)
License: [MIT License](https://opensource.org/license/MIT)

Modifications by: Joss Raine
Date of Modification: 05/08/2025

> **Note:**
> All original credits and licensing remain attributed to the original author.
> This project is under the MIT License and its custom modifications continue to comply with the MIT License terms.
> The included `playingcards.py` module retains its original MIT license attribution.

---

### License Versions

Each library is open-source and Licenced to allow for educational and personal use under their respective Licences. I acknowledge and respect the work of the open-source community in making these tools available. For more details on each Licence, please visit the respective project pages on PyPI or via their official repositories.

---

## Security Impacts

| **Package/Library** |                                    **Potential Risks**                                    |                                       **Mitigation Used**                                        |
| :-----------------: | :---------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------: |
|         `art`         |      Terminal output could potential be broken or flooded from malicious user input       |                Only pre-determined output is displayed through art, no user input                |
|      `colorama`       |                   Can break/bug display if malicious user input is used                   |                     As above, only pre-determined output used, no user input                     |
|   `playingcards.py`   |     As a smaller library, buggy or hidden code could unexpectedly alter game outcome      | Code behavior was checked and was consistent with expectations of standard 52 card deck behavior |
|        `rich`         | Complex code and features are easy to break with user input accidentally or intentionally |          Only used for basic pre-defined output (e.g. loading bars) and not user input           |

---

[⇧ Back to Top](#dependencies) | [⇦ Back to README](./readme.md)
