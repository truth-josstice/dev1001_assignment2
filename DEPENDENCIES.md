# Dependencies/Third Party Imports

## External Libraries/Package licenses

| **Package/Library** | **Version** |                                             **License**                                              |                                     **Purpose**                                      |
| :-----------------: | :---------: | :--------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------: |
|         art         |     6.5     |                              [MIT](https://opensource.org/license/MIT)                               |                     Python lib for text converting to ASCII art                      |
|      colorama       |    0.4.6    |                     [BSD-3-Clause](https://opensource.org/license/BSD-3-Clause)                      |                           Producing colored terminal text                            |
|      iniconfig      |    2.1.0    |                              [MIT](https://opensource.org/license/MIT)                               |                                INI-file parser module                                |
|   markdown-it-py    |    3.0.0    |                              [MIT](https://opensource.org/license/MIT)                               |                                   Markdown parser                                    |
|        mdurl        |    0.1.2    |                              [MIT](https://opensource.org/license/MIT)                               |                        URL utilities for markdown-it parser.                         |
|      packaging      |    25.0     | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0), [MIT](https://opensource.org/license/MIT) | Reusable core utilities for various Python Packaging interoperability specifications |
|   playingcards.py   |    1.1.1    |                              [MIT](https://opensource.org/license/MIT)                               |                         Advanced Python Playing Card Module                          |
|       pluggy        |    1.6.0    |                              [MIT](https://opensource.org/license/MIT)                               |                            Core framework used by pytest                             |
|      Pygments       |   2.19.1    |                     [BSD-2-Clause](https://opensource.org/license/BSD-2-Clause)                      |                             Syntax highlighting package                              |
|       pytest        |    8.4.1    |                              [MIT](https://opensource.org/license/MIT)                               |                                Used for testing code                                 |
|   timezonefinder    |    6.5.9    |                              [MIT](https://opensource.org/license/MIT)                               |                          Detects timezones with coordinates                          |
|        rich         |   14.0.0    |                              [MIT](https://opensource.org/license/MIT)                               |                    Provides rich text and formatting in terminal                     |

## Security Impacts

| **Package/Library** |                                  **Potential Risks**                                   |                         **Mitigation Used**                          |
| :-----------------: | :------------------------------------------------------------------------------------: | :------------------------------------------------------------------: |
|         art         | Console rendering attacks - potential for terminal output to be changed by an attacker |            Renders predefined ASCII only, not user-input.            |
|   playingcards.py   |                            Executing unsafe or buggy logic                             | Used only for card deck and shuffling, uses only trusted logic paths |
|       pluggy        |                                    Plugin injection                                    |   Used internally by `pytest`; no custom plugins loaded in runtime   |
