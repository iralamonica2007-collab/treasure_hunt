# 💎 Dynamic Treasure Hunt

## 1. Project Overview

Dynamic Treasure Hunt is a Python terminal game where the player starts
at **CAMP** and tries to find a hidden treasure. The player solves clues
to choose routes and must manage energy, chances, hints, and score while
exploring the map.

## 2. Project Documents

-   **PRD (`game_prd.docx`)** --- Describes the game's purpose,
    requirements, player commands, difficulty levels, rules, and
    expected behaviour.
-   **Design Document
    (`Dynamic_Treasure_Hunt_Revised_Design_Document.docx`)** ---
    Describes the game flow, formulas, data structures, and organisation
    of the program.

## 3. Source Code

-   **`Treasure_game/main.py`** --- Runs the game, displays the menu and
    map, handles player input, presents clues, updates the expedition,
    and displays results.
-   **`Treasure_game/logic_file.py`** --- Contains helper logic for
    route keys, finding routes, checking whether locations are
    reachable, and creating clue IDs.
-   **`Treasure_game/test_main.py`** --- Contains automated tests for
    game setup, clues, answers, movement, hints, routes, resources, and
    selected edge cases.

## 4. Main Features

-   Three difficulty levels: Easy, Medium, and Hard
-   Hidden treasure selected at the start of an expedition
-   Map with 10 locations and connected routes
-   Clues based on available routes
-   Energy, chances, hints, score, and distance tracking
-   Map and status views during a clue
-   Dynamic route changes while keeping the treasure reachable
-   Protection against repeating recent clues
-   Expedition end conditions and result messages

## 5. Starting Resources

  Difficulty     Energy   Chances/Moves   Hints
  ------------ -------- --------------- -------
  Easy               42              16       5
  Medium             32              13       4
  Hard               27              11       3

Each expedition starts at `CAMP` with a score of **100** and a distance
of **0 km**, according to the PRD.

## 6. How to Play

1.  Start a new expedition from the main menu.
2.  Select Easy, Medium, or Hard.
3.  Read the clue and choose an answer.
4.  Use `H` for a hint, `M` to view the map, `S` to view status, or `Q`
    to quit.
5.  Choose routes carefully to preserve energy and chances.
6.  Find the hidden treasure before the expedition ends.

## 7. Rules and Scoring

-   A correct answer awards points based on the selected difficulty and
    moves the player to the chosen destination.
-   A wrong answer applies the difficulty-based penalty.
-   Hints remove an incorrect option and consume a hint and energy.
-   Routes may close or reopen during the expedition.
-   The game ends when the treasure is found or the player cannot
    continue.

## 8. Data Structures and Algorithms

-   **Dictionary:** stores game state and map information.
-   **List:** stores routes and the player's journey.
-   **Set:** stores closed routes and used questions.
-   **Tuple:** represents route connections.
-   **Breadth-First Search (BFS):** checks whether a destination remains
    reachable through open routes.
-   The PRD/design documents also describe shortest-path route guidance
    and clue-history checks.

## 9. How to Run

Open a terminal in the project folder and run:

``` bash
python Treasure_game/main.py
```

## 10. How to Run Tests

From the project root folder, run:

``` bash
python -m unittest discover -s Treasure_game -p "test_main.py" -v
```

Tests compare actual results with expected results. If a test fails,
check the test name and assertion message.

## 11. Project Structure

``` text
Treasure_game (2)/
├── game_prd.docx
├── Dynamic_Treasure_Hunt_Revised_Design_Document.docx
└── Treasure_game/
    ├── main.py
    ├── logic_file.py
    └── test_main.py
```

## 12. Technologies Used

-   Python
-   Python `unittest` testing framework
-   Graph-based map and route logic

------------------------------------------------------------------------

**Project summary:** The PRD defines what the game should do, the Design
Document explains how it is organised, `main.py` runs the game,
`logic_file.py` provides route-related helper functions, and
`test_main.py` checks selected behaviours.
