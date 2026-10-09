# ============================================================
# DYNAMIC TREASURE HUNT
# GAME LOGIC
# ============================================================
# This file contains ONLY pure functions.
#
# Pure function rules:
# - No input()
# - No print()
# - No global state modification
# - No argument mutation
# - Same inputs -> same output
# ============================================================


# ============================================================
# 1. ROUTE KEY
# ============================================================

def make_route_key(place, destination):
    """
    Create a unique route key for two connected locations.
    """
    return tuple(sorted((place, destination)))


# ============================================================
# 2. GET ALL ROUTES
# ============================================================

def get_all_routes(game_map):
    """
    Return all unique routes available in the map.
    """
    routes = []

    for place in game_map:
        for destination, distance, energy in game_map[place]:
            route = make_route_key(place, destination)

            if route not in routes:
                routes.append(route)

    return routes


# ============================================================
# 3. GET OPEN ROUTES
# ============================================================

def get_open_routes(location, game_map, closed_routes):
    """
    Return all routes from the current location
    that are not closed.
    """
    routes = []

    for destination, distance, energy in game_map[location]:
        route = make_route_key(location, destination)

        if route not in closed_routes:
            routes.append((destination, distance, energy))

    return routes


# ============================================================
# 4. CHECK REACHABILITY
# ============================================================

def is_reachable(start, target, game_map, closed_routes):
    """
    Check whether the target location can be reached
    from the starting location using currently open routes.
    """
    visited = {start}
    queue = [start]

    while queue:
        current = queue.pop(0)

        if current == target:
            return True

        for destination, distance, energy in game_map[current]:
            route = make_route_key(current, destination)

            if route not in closed_routes and destination not in visited:
                visited.add(destination)
                queue.append(destination)

    return False


# ============================================================
# 5. CREATE CLUE ID
# ============================================================

def make_clue_id(clue):
    """
    Create a unique identifier for a clue
    using its question and options.
    """
    return (
        clue["question"],
        tuple(sorted(clue["options"]))
    )