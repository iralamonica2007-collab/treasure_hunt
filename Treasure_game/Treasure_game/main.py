import random
import os


LOCATIONS = ["CAMP", "FOREST", "VILLAGE", "WATCHTOWER", "RUINS",
             "CLIFF", "RIVER", "CAVE", "SWAMP", "TEMPLE"]

# destination, distance, energy cost
MAP = {
    "CAMP": [("FOREST", 4, 5), ("VILLAGE", 3, 4), ("WATCHTOWER", 6, 7)],
    "FOREST": [("CAMP", 4, 5), ("RUINS", 5, 6), ("RIVER", 6, 7)],
    "VILLAGE": [("CAMP", 3, 4), ("RUINS", 4, 5), ("RIVER", 5, 6)],
    "WATCHTOWER": [("CAMP", 6, 7), ("CLIFF", 4, 5), ("RUINS", 5, 6)],
    "RUINS": [("FOREST", 5, 6), ("VILLAGE", 4, 5),
              ("WATCHTOWER", 5, 6), ("CAVE", 4, 6), ("TEMPLE", 7, 8)],
    "CLIFF": [("WATCHTOWER", 4, 5), ("CAVE", 5, 7)],
    "RIVER": [("FOREST", 6, 7), ("VILLAGE", 5, 6),
              ("SWAMP", 4, 6), ("CAVE", 6, 8)],
    "CAVE": [("RUINS", 4, 6), ("CLIFF", 5, 7),
             ("RIVER", 6, 8), ("TEMPLE", 5, 7)],
    "SWAMP": [("RIVER", 4, 6), ("TEMPLE", 6, 8)],
    "TEMPLE": [("RUINS", 7, 8), ("CAVE", 5, 7), ("SWAMP", 6, 8)]
}

DIFFICULTY = {
    "Easy": {"energy": 42, "moves": 16, "hints": 5, "closed": 1,
             "wrong_energy": 1, "wrong_score": 15, "points": 50},
    "Medium": {"energy": 32, "moves": 13, "hints": 4, "closed": 2,
               "wrong_energy": 2, "wrong_score": 20, "points": 80},
    "Hard": {"energy": 27, "moves": 11, "hints": 3, "closed": 3,
             "wrong_energy": 3, "wrong_score": 30, "points": 120}
}

# Only recent five games are remembered while this program is running.
# Nothing is written to a file.
recent_question_games = []

# ------------------------------------------------------------
# TERMINAL COLORS
# ------------------------------------------------------------
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RED = "\033[91m"
WHITE = "\033[97m"


def enable_terminal_colors() -> None:
    """Enable ANSI colors in modern Windows terminals."""
    if os.name == "nt":
        os.system("")


def clear_screen() -> None:
    """Clear the terminal before showing a new game screen."""
    os.system("cls" if os.name == "nt" else "clear")


def show_startup_screen() -> None:
    """Show the colorful opening screen of the treasure hunt."""
    print(color_text("╔" + "═" * 68 + "╗", BLUE, True))
    print(color_text("║" + " " * 68 + "║", BLUE, True))
    print(color_text("║" + "💎 DYNAMIC TREASURE HUNT 💎".center(68) + "║", MAGENTA, True))
    print(color_text("║" + "CLUE • CHOOSE • EXPLORE • SURVIVE".center(68) + "║", CYAN, True))
    print(color_text("║" + " " * 68 + "║", BLUE, True))
    print(color_text("║" + "A colorful adventure of clues, routes and hidden treasure".center(68) + "║", YELLOW, True))
    print(color_text("║" + " " * 68 + "║", BLUE, True))
    print(color_text("╚" + "═" * 68 + "╝", BLUE, True))
    print()
    print(color_text("                 ✦ YOUR EXPEDITION BEGINS HERE ✦", GREEN, True))
    print(color_text("                 Manage energy • chances • score", WHITE))
    print()
    print(color_text("                 Press ENTER to continue...", CYAN, True))


def color_text(text: str, color: str = WHITE, bold: bool = False) -> str:
    """Return text with terminal color."""
    style = BOLD if bold else ""
    return style + color + str(text) + RESET


def print_title(title: str) -> None:
    """Print a professional colored section title."""
    print("\n" + color_text("=" * 70, BLUE, True))
    print(color_text(title.center(70), CYAN, True))
    print(color_text("=" * 70, BLUE, True))


def print_success(text: str) -> None:
    """Print a success message."""
    print(color_text(text, GREEN, True))


def print_warning(text: str) -> None:
    """Print a warning message."""
    print(color_text(text, YELLOW, True))


def print_error(text: str) -> None:
    """Print an error message."""
    print(color_text(text, RED, True))


def print_info(text: str) -> None:
    """Print an information message."""
    print(color_text(text, CYAN))


def print_option(number: int, text: str) -> None:
    """Print a menu or answer option."""
    print(color_text(str(number) + ". ", MAGENTA, True) + color_text(text, WHITE))



def make_route_key(place: str, destination: str) -> tuple[str, str]:
    """Create one ID for a connection between two locations."""
    return tuple(sorted((place, destination)))


def get_all_routes() -> list[tuple[str, str]]:
    """Return every unique connection in the map."""
    routes = []

    for place in MAP:
        for destination, distance, energy in MAP[place]:
            route = make_route_key(place, destination)
            if route not in routes:
                routes.append(route)

    return routes

def show_map(game: dict | None = None) -> None:
    """Display the fixed treasure-hunt map."""

    print_title("TREASURE HUNT MAP")

    closed = game["closed"] if game else set()

    def place(name: str) -> str:
        if game and name == game["current"]:
            return color_text("[" + name + "]", GREEN, True)
        return color_text("[" + name + "]", CYAN, True)

    def road(label: str, a: str, b: str) -> str:
        if make_route_key(a, b) in closed:
            return color_text("X " + label + " X", RED, True)
        return color_text(label, YELLOW, True)

    print()

    print("                           " + place("CAMP"))
    print("                         /    |    \\")
    print("                      3 km   4 km   6 km")
    print("                       /      |      \\")
    print("                      /       |       \\")
    print("               " + place("VILLAGE") +
          "   " + place("FOREST") +
          "  " + place("WATCHTOWER"))

    print("                  |  \\         |          /  \\")
    print("                4 km  5 km    5 km       4 km  5 km")
    print("                  |    \\       |        /      \\")
    print("                  |     \\      |       /        \\")

    print("               " + place("RUINS") +
          "──" + road("5 km", "RUINS", "RIVER") +
          "──" + place("RIVER") +
          "───" + road("7 km", "RIVER", "CLIFF") +
          "──" + place("CLIFF"))

    print("                |  \\            |                 |")
    print("              4 km  7 km       4 km               5 km")
    print("                |      \\        |                 |")
    print("                |       \\       |                 |")
    print("             " + place("CAVE") +
          "       \\   " + place("SWAMP") +
          "─────────────┘")

    print("                |          \\      |")
    print("               5 km         \\    6 km")
    print("                |            \\    |")
    print("                |             \\   |")
    print("                └──────────────" + place("TEMPLE"))

    print()

    print_info("MAP GUIDE")
    print_info("Each yellow label is the distance of that road in km.")
    print_info("Follow the clues to decide where you must travel.")
    print_info("The treasure location is hidden.")

    print_info(
        "Legend: " +
        color_text("[GREEN] = You", GREEN, True) +
        "   " + color_text("[CYAN] = Location", CYAN, True) +
        "   " + color_text("[YELLOW] = Distance", YELLOW, True)
    )

    if closed:
        print_error("Red X marks a currently closed road.")
    else:
        print_success("All roads are currently open.")

    print(color_text("=" * 70, BLUE, True))

def get_open_routes(location: str, game: dict) -> list[tuple[str, int, int]]:
    """Return the open routes from the player's current location."""
    routes = []

    for destination, distance, energy in MAP[location]:
        route = make_route_key(location, destination)

        if route not in game["closed"]:
            routes.append((destination, distance, energy))

    return routes


def is_reachable(start: str, target: str, game: dict) -> bool:
    """Check whether the target can still be reached."""
    visited = {start}
    queue = [start]

    while queue:
        current = queue.pop(0)

        if current == target:
            return True

        for destination, distance, energy in MAP[current]:
            route = make_route_key(current, destination)

            if route not in game["closed"] and destination not in visited:
                visited.add(destination)
                queue.append(destination)

    return False


def close_initial_routes(game: dict) -> None:
    """Randomly close routes at the start of an expedition."""
    number_to_close = DIFFICULTY[game["level"]]["closed"]
    routes = get_all_routes()
    random.shuffle(routes)

    for route in routes:
        if len(game["closed"]) == number_to_close:
            break
        game["closed"].add(route)


def create_game(level: str) -> dict:
    """Create a new expedition and set its hidden treasure."""
    settings = DIFFICULTY[level]

    game = {
        "level": level,
        "current": "CAMP",
        "treasure": random.choice(LOCATIONS[1:]),
        "energy": settings["energy"],
        "max_energy": settings["energy"],
        "moves": settings["moves"],
          "move_count": 0,
        "hints": settings["hints"],
        "score": 100,
        "distance": 0,
        "wrong": 0,
        "used_questions": set(),
        "closed": set(),
        "path": ["CAMP"],
        "end_reason": ""
    }

    close_initial_routes(game)

    if not is_reachable("CAMP", game["treasure"], game):
        game["closed"].clear()

    return game


def make_direct_clue(game: dict, routes: list[tuple[str, int, int]]) -> dict:
    """Create a level-based clue about an open route."""
    route = random.choice(routes)
    answer = route[0]
    options = [r[0] for r in routes]

    if game["level"] == "Easy":
        question = (
            f"You are at {game['current']}. Which location can you reach "
            "directly through an OPEN route?"
        )
    elif game["level"] == "Medium":
        question = (
            f"From {game['current']}, which OPEN route is exactly "
            f"{route[1]} km away and costs {route[2]} energy?"
        )
    else:
        question = (
            f"HARD CLUE: From {game['current']}, identify the location "
            f"connected by the OPEN route with distance {route[1]} km "
            f"and energy cost {route[2]}."
        )

    return {
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": (
            f"The map confirms that {game['current']} connects to {answer} "
            f"({route[1]} km, {route[2]} energy)."
        )
    }


def make_distance_clue(game: dict, routes: list[tuple[str, int, int]]) -> dict:
    """Create a clue that requires comparing route distances."""
    if len(routes) < 2:
        return make_direct_clue(game, routes)

    route = random.choice(routes)
    answer = route[0]
    options = [r[0] for r in routes]

    if game["level"] == "Easy":
        question = (
            f"Which open route from {game['current']} is exactly "
            f"{route[1]} km long?"
        )
    elif game["level"] == "Medium":
        shorter = [r for r in routes if r[1] < route[1]]
        if shorter:
            comparison = max(shorter, key=lambda r: r[1])
            answer = comparison[0]
            question = (
                f"MEDIUM CLUE: From {game['current']}, which route is the "
                f"longest route that is still shorter than {route[1]} km?"
            )
        else:
            question = (
                f"MEDIUM CLUE: Which route from {game['current']} has "
                f"distance {route[1]} km?"
            )
    else:
        farthest = max(routes, key=lambda r: (r[1], r[2]))
        answer = farthest[0]
        question = (
            f"HARD CLUE: From {game['current']}, compare all OPEN routes. "
            f"Which destination has the greatest travel distance?"
        )

    return {
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": (
            f"The route to {answer} is {next(r[1] for r in routes if r[0] == answer)} km "
            f"with energy cost {next(r[2] for r in routes if r[0] == answer)}."
        )
    }


def make_map_clue(game: dict, routes: list[tuple[str, int, int]]) -> dict | None:
    """Create a multi-step map reasoning clue."""
    pairs = []

    for route in routes:
        first = route[0]
        for next_route in get_open_routes(first, game):
            second = next_route[0]
            if second != game["current"]:
                pairs.append((first, second))

    if not pairs:
        return None

    first, second = random.choice(pairs)
    options = [r[0] for r in routes]

    if game["level"] == "Easy":
        question = (
            f"MAP CLUE: From {game['current']}, which location can you "
            f"reach first and then continue directly to {second}?"
        )
    elif game["level"] == "Medium":
        first_route = next(r for r in routes if r[0] == first)
        question = (
            f"MEDIUM MAP CLUE: You need to reach {second} in two steps. "
            f"Which first destination from {game['current']} makes this possible "
            f"while using a route costing {first_route[2]} energy?"
        )
    else:
        first_route = next(r for r in routes if r[0] == first)
        second_routes = get_open_routes(first, game)
        second_route = next(r for r in second_routes if r[0] == second)
        total = first_route[2] + second_route[2]
        question = (
            f"HARD MAP CLUE: Find a two-step path from {game['current']} to {second}. "
            f"The total energy cost of the two routes must be {total}. Which "
            f"location should you visit first?"
        )

    return {
        "question": question,
        "options": options,
        "answer": first,
        "explanation": (
            f"The correct first step is {first}; from there the map provides "
            f"an open route to {second}."
        )
    }


def make_clue_id(clue: dict) -> str:
    """Create a simple ID so a clue can be recognized as already used."""
    return clue["question"] + "|" + "|".join(sorted(clue["options"]))


def clue_was_recent(clue: dict, game: dict) -> bool:
    """Check current and previous five games for the same clue."""
    clue_id = make_clue_id(clue)

    if clue_id in game["used_questions"]:
        return True

    for old_game in recent_question_games:
        if clue_id in old_game:
            return True

    return False


def remember_clue(clue: dict, game: dict) -> None:
    """Remember the clue for the current game."""
    clue_id = make_clue_id(clue)
    game["used_questions"].add(clue_id)


def save_game_questions(game: dict) -> None:
    """Keep this game's questions as part of the recent five games."""
    recent_question_games.append(set(game["used_questions"]))

    while len(recent_question_games) > 5:
        recent_question_games.pop(0)


def generate_clue(game: dict) -> dict | None:
    """Generate a clue and keep its correct answer in the clue dictionary."""
    routes = get_open_routes(game["current"], game)

    if not routes:
        return None

    for _ in range(100):
        clue_type = random.randint(1, 3)

        if clue_type == 1:
            clue = make_direct_clue(game, routes)
        elif clue_type == 2:
            clue = make_distance_clue(game, routes)
        else:
            clue = make_map_clue(game, routes)

        if clue is not None and not clue_was_recent(clue, game):
            remember_clue(clue, game)
            return clue

    # Prevent the game from stopping if the available clue pool is small.
    clue = make_direct_clue(game, routes)

    if make_clue_id(clue) not in game["used_questions"]:
        remember_clue(clue, game)
        return clue

    return None


def check_answer(choice: int, clue: dict, game: dict, hint_used: bool = False) -> bool:
    """Compare the player's answer with the correct answer."""
    if choice < 1 or choice > len(clue["options"]):
        print_warning("Invalid answer.")
        return False

    selected_answer = clue["options"][choice - 1]

    if selected_answer == clue["answer"]:
        points = DIFFICULTY[game["level"]]["points"]
        game["score"] += points
        print_success("\n✓ Correct!")
        print_success("Points gained: " + str(points))
        print(clue["explanation"])
        return True

    energy_loss = DIFFICULTY[game["level"]]["wrong_energy"]
    score_loss = DIFFICULTY[game["level"]]["wrong_score"]

    game["wrong"] += 1

    if hint_used:
     energy_loss = 0
     score_loss *= 2
     chance_loss = 1
    else:
     chance_loss = 1

    game["energy"] -= energy_loss
    game["moves"] -= chance_loss
    game["score"] = max(0, game["score"] - score_loss)

    print_error("\n✗ WRONG ANSWER!")
    print_warning("Energy lost: " + str(energy_loss))
    print_warning("Chance lost: 1")
    print_warning("Score lost: " + str(score_loss))
    print_info("Energy remaining: " + str(max(0, game["energy"])))
    print_info("Chances remaining: " + str(max(0, game["moves"])))
    print_info("Score remaining: " + str(game["score"]))

    if game["energy"] <= 0 or game["moves"] <= 0:
        print_error("Your resources have reached zero. The expedition ends now.")
        return False

    print_info("Try the clue again.")
    
    return False


def give_hint(clue: dict, game: dict) -> None:
    """Remove one wrong option when a hint is used."""
    if game["hints"] == 0:
        print_warning("No hints remaining.")
        return

    game["hints"] -= 1

    hint_energy = DIFFICULTY[game["level"]]["wrong_energy"] * 2
    game["energy"] -= hint_energy

    print_warning("Energy lost for using hint: " + str(hint_energy))
    print_info("Energy remaining: " + str(max(0, game["energy"])))

    wrong_options = [
        option for option in clue["options"]
        if option != clue["answer"]
    ]

    if wrong_options:
        removed = random.choice(wrong_options)
        clue["options"].remove(removed)
        print_info("Hint: " + removed + " is not the correct answer.")
    else:
        print("Hint: Study the map carefully.")


def move_player(game: dict, destination: str) -> bool:
    """Move the player and update energy, chances, distance and path."""
    for route in get_open_routes(game["current"], game):
        if route[0] == destination:
            distance = route[1]
            energy_cost = route[2]

            if game["energy"] < energy_cost:
                game["end_reason"] = (
                    "You do not have enough energy to make the selected next move. "
                    "The expedition must end."
                )
                print_error("NOT ENOUGH ENERGY FOR THE NEXT MOVE!")
                print_warning("Required energy: " + str(energy_cost))
                print_warning("Energy remaining: " + str(game["energy"]))
                return False

            game["energy"] -= energy_cost
            game["moves"] -= 1
            game["move_count"] += 1
            game["distance"] += distance
            game["current"] = destination
            game["path"].append(destination)

            print_success("\n✓ You moved to " + destination)
            print_info("Distance travelled: " + str(distance) + " km")
            print_info("Energy used for route: " + str(energy_cost))
            print_info("Energy remaining: " + str(max(0, game["energy"])))
            print_info("Chances remaining: " + str(max(0, game["moves"])))
            return True

    game["end_reason"] = "The selected route is not available."
    print_warning("That route is not available.")
    return False

def change_routes(game: dict) -> None:
    """Randomly close or reopen a route without blocking the treasure."""
    if game["move_count"] % 2 != 0:
     return

    if game["closed"] and random.random() < 0.5:
        route = random.choice(list(game["closed"]))
        game["closed"].remove(route)
        print_info("\n★ EVENT: A blocked route has reopened!")
        return

    routes = get_all_routes()
    random.shuffle(routes)

    for route in routes:
        if route not in game["closed"]:
            game["closed"].add(route)

            if is_reachable(game["current"], game["treasure"], game):
                print_warning("\n★ EVENT: A route has temporarily closed!")
                return

            game["closed"].remove(route)


def play_game(level: str) -> None:
    """Run one complete treasure-hunt expedition."""
    game = create_game(level)

    print_title("NEW TREASURE EXPEDITION — " + level.upper())
    print_info("Follow the clues to decide where you must go.")
    print_info("You cannot choose your own route.")

    while game["energy"] > 0 and game["moves"] > 0:

        if game["current"] == game["treasure"]:
            print("\n" + color_text("╔" + "═" * 68 + "╗", GREEN, True))
            print(
                color_text(
                    "║" + "💎 VICTORY! YOU FOUND THE TREASURE!".center(68) + "║",
                    GREEN,
                    True
                )
            )
            print(color_text("╚" + "═" * 68 + "╝", GREEN, True))
            print_success("\n✨ CONGRATULATIONS! ✨")
            print_success(
                "💎 TREASURE FOUND AT: " + game["treasure"] + " 💎"
            )
            print_info(
                "You followed the clues and reached the hidden treasure."
            )
            print_info("Score: " + str(game["score"]))
            print_info("Distance travelled: " + str(game["distance"]) + " km")
            save_game_questions(game)
            input(color_text("\nPress ENTER to continue...", CYAN, True))
            clear_screen()
            show_startup_screen()
            input()
            clear_screen()
            return

        clue = generate_clue(game)

        if clue is None:
            game["end_reason"] = "No new clue is available for this expedition."
            break

         # The same clue remains active until the player solves it.
        hint_used = False
        while True:
            print("\n" + color_text("-" * 70, MAGENTA, True))
            print(color_text("CLUE".center(70), CYAN, True))
            print(color_text("-" * 70, MAGENTA, True))
            print(
                color_text(
                    game["level"].upper() + " CLUE: ",
                    YELLOW,
                    True
                ) + clue["question"]
            )

            for number, option in enumerate(clue["options"], 1):
                print_option(number, option)

            print(
                "\n" + color_text(
                    "H = Hint | M = Map | S = Status | Q = Quit",
                    CYAN,
                    True
                )
            )
            command = input("Your choice: ").strip().upper()

            if command == "M":
                clear_screen()
                show_map(game)
                input(
                    color_text(
                        "\nPress ENTER to return to the clue...",
                        CYAN,
                        True
                    )
                )
                clear_screen()

            elif command == "S":
                print_info("\nCURRENT STATUS")
                print_info("Location: " + game["current"])
                print_info("Energy: " + str(max(0, game["energy"])))
                print_info("Chances: " + str(max(0, game["moves"])))
                print_info("Hints: " + str(game["hints"]))
                print_info("Score: " + str(game["score"]))

            elif command == "H":
                give_hint(clue, game)
                hint_used = True

            elif command == "Q":
                game["end_reason"] = "You chose to quit the expedition."
                break

            elif command.isdigit():
                if check_answer(int(command), clue, game,hint_used):
                    # The clue decides the destination. The player does not
                    # get a separate route-choice screen.
                    destination = clue["answer"]

                    print_info(
                        "\nCLUE SOLVED — FOLLOWING THE CLUE TO "
                        + destination
                    )

                    if not move_player(game, destination):
                        break

                    break

            else:
                print_warning("Invalid command.")

            if game["energy"] <= 0 or game["moves"] <= 0:
                break

        if game["end_reason"]:
            break

        if game["energy"] <= 0 or game["moves"] <= 0:
            break

        # Dynamic route changes happen after the clue-directed movement.
        change_routes(game)

    # Final loss screen.
    print("\n" + color_text("╔" + "═" * 68 + "╗", RED, True))
    print(
        color_text(
            "║" + "☠ YOU LOSE — EXPEDITION ENDED".center(68) + "║",
            RED,
            True
        )
    )
    print(color_text("╚" + "═" * 68 + "╝", RED, True))

    if game["end_reason"]:
        print_error("Reason: " + game["end_reason"])
    elif game["energy"] <= 0 and game["moves"] <= 0:
        print_error("Reason: Your energy and chances have both run out.")
    elif game["energy"] <= 0:
        print_error(
            "Reason: You do not have enough energy to make the next move."
        )
    elif game["moves"] <= 0:
        print_error(
            "Reason: You have used all your available chances/moves."
        )
    else:
        print_error(
            "Reason: The expedition cannot continue."
        )

    print_warning(
        "Energy used: " +
        str(max(0, game["max_energy"] - game["energy"]))
    )
    print_warning(
        "Energy remaining: " +
        str(max(0, game["energy"]))
    )
    print_warning(
        "Chances remaining: " +
        str(max(0, game["moves"]))
    )
    print_info(
        "The expedition has ended. You will return to a fresh main menu."
    )

    save_game_questions(game)
    input(color_text("\nPress ENTER to continue...", CYAN, True))
    clear_screen()
    show_startup_screen()
    input()
    clear_screen()



def choose_difficulty() -> str:
    """Ask for the difficulty and show starting resources after selection."""
    while True:
        print_title("CHOOSE DIFFICULTY")
        print_option(1, "Easy")
        print_option(2, "Medium")
        print_option(3, "Hard")

        choice = input("Choose difficulty: ").strip()

        if choice == "1":
            level = "Easy"
        elif choice == "2":
            level = "Medium"
        elif choice == "3":
            level = "Hard"
        else:
            print_warning("Invalid difficulty. Please choose 1, 2 or 3.")
            continue

        settings = DIFFICULTY[level]
        clear_screen()
        print_title("EXPEDITION READY")
        print_success("Difficulty selected: " + level.upper())
        print()
        print_info("STARTING RESOURCES")
        print(color_text("  ⚡ Energy   : " + str(settings["energy"]), YELLOW, True))
        print(color_text("  🎯 Chances  : " + str(settings["moves"]), MAGENTA, True))
        print(color_text("  💡 Hints    : " + str(settings["hints"]), CYAN, True))
        print()
        print_info("Your treasure location is hidden.")
        print_info("Follow the clues, use hints when needed, and manage your resources.")
        input(color_text("\nPress ENTER to start the expedition...", GREEN, True))
        clear_screen()
        return level

def show_instructions() -> None:
    """Display the rules and commands."""
    print_title("HOW TO PLAY")
    print("1. Start at CAMP.")
    print("2. The treasure location is hidden.")
    print("3. Solve each clue to determine where you must go next.")
    print("4. The clue decides your next destination; you cannot choose a route yourself.")
    print("5. Press M whenever you need the map.")
    print("6. Press H to use a hint.")
    print("7. Press S to view your status.")
    print("8. Wrong answers reduce energy, score, and one chance.")
    print("9. The game ends immediately when energy OR chances reach zero.")
    print("10. Routes can dynamically close or reopen.")
    print("11. Reach the treasure before your resources run out.")
    print("=" * 70)


def main() -> None:
    """Display the main menu and start expeditions."""
    enable_terminal_colors()
    clear_screen()
    show_startup_screen()
    input()
    clear_screen()
    while True:
        print_title("TREASURE HUNT")
        print_option(1, "START NEW EXPEDITION")
        print_option(2, "VIEW MAP")
        print_option(3, "HOW TO PLAY")
        print_option(4, "EXIT")
        print("=" * 70)

        choice = input("Choose an option: ").strip()

        if choice == "1":
            level = choose_difficulty()
            play_game(level)

        elif choice == "2":
            clear_screen()
            show_map()
            input(color_text("\nPress ENTER to return to the main menu...", CYAN, True))
            clear_screen()

        elif choice == "3":
            show_instructions()

        elif choice == "4":
            print_success("You have exited the game.")
            break

        else:
            print_error("Invalid choice. Please choose 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()