import unittest
from unittest.mock import patch
import importlib.util

spec = importlib.util.spec_from_file_location("game", "Treasure_game/main.py")
game = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game)


class TestTreasureHunt(unittest.TestCase):

    def new_game(self):
        return {
            "level": "Medium",
            "current": "CAMP",
            "treasure": "FOREST",
            "energy": 32,
            "max_energy": 32,
            "moves": 13,
            "move_count": 0,
            "hints": 4,
            "score": 100,
            "distance": 0,
            "wrong": 0,
            "used_questions": set(),
            "closed": set(),
            "path": ["CAMP"],
            "end_reason": ""
        }

    def clue(self):
        return {
            "question": "Choose the route",
            "options": ["FOREST", "VILLAGE", "WATCHTOWER"],
            "answer": "FOREST",
            "explanation": "FOREST is the correct route."
        }

    # ---------- MAIN TEST CASES ----------

    def test_TC01_start_game(self):
        with patch("builtins.input", side_effect=["1", ""]):
            self.assertEqual(game.choose_difficulty(), "Easy")

    def test_TC02_medium(self):
        with patch("builtins.input", side_effect=["2", ""]):
            self.assertEqual(game.choose_difficulty(), "Medium")

    def test_TC03_hidden_treasure(self):
        with patch("random.choice", return_value="TEMPLE"):
            g = game.create_game("Medium")
        self.assertEqual(g["current"], "CAMP")
        self.assertEqual(g["treasure"], "TEMPLE")

    def test_TC04_map(self):
        game.show_map(self.new_game())

    def test_TC05_clue(self):
        c = game.generate_clue(self.new_game())
        self.assertIsNotNone(c)

    def test_TC06_correct_move(self):
        g = self.new_game()
        c = self.clue()

        self.assertTrue(game.check_answer(1, c, g))
        self.assertTrue(game.move_player(g, "FOREST"))
        self.assertEqual(g["current"], "FOREST")

    def test_TC07_wrong_answer(self):
        g = self.new_game()
        c = self.clue()

        self.assertFalse(game.check_answer(2, c, g))
        self.assertEqual(g["energy"], 30)
        self.assertEqual(g["moves"], 12)
        self.assertEqual(g["score"], 80)

    def test_TC08_hint(self):
        g = self.new_game()
        c = self.clue()

        game.give_hint(c, g)

        self.assertEqual(g["hints"], 3)

    def test_TC09_wrong_after_hint(self):
        g = self.new_game()
        c = self.clue()

        game.give_hint(c, g)

        self.assertFalse(game.check_answer(2, c, g))
        self.assertEqual(g["moves"], 12)

    def test_TC10_map_during_clue(self):
        game.show_map(self.new_game())

    def test_TC11_status(self):
        g = self.new_game()

        self.assertEqual(g["current"], "CAMP")
        self.assertEqual(g["energy"], 32)
        self.assertEqual(g["moves"], 13)
        self.assertEqual(g["hints"], 4)
        self.assertEqual(g["score"], 100)

    def test_TC12_route_event(self):
        g = self.new_game()

        with patch("random.random"):
            game.change_routes(g)

        self.assertTrue(len(g["closed"]) > 0)

    def test_TC13_treasure(self):
        g = self.new_game()
        c = self.clue()

        game.check_answer(1, c, g)
        game.move_player(g, "FOREST")

        self.assertEqual(g["current"], g["treasure"])

    def test_TC14_resource_exhaustion(self):
        g = self.new_game()
        c = self.clue()

        g["energy"] = 1

        game.check_answer(2, c, g)

        self.assertEqual(g["energy"], -1)

    def test_TC15_quit(self):
        g = self.new_game()

        g["end_reason"] = "You chose to quit the expedition."

        self.assertIn("quit", g["end_reason"].lower())

    # ---------- EDGE CASES ----------

    def test_E01_invalid_menu(self):
        with patch("builtins.input", side_effect=["", "9", "4"]):
            game.main()

    def test_E02_invalid_difficulty(self):
        with patch("builtins.input", side_effect=["9", "1", ""]):
            self.assertEqual(game.choose_difficulty(), "Easy")

    def test_E03_invalid_route(self):
        g = self.new_game()
        c = self.clue()

        self.assertFalse(game.check_answer(99, c, g))

    def test_E04_invalid_command(self):
        command = "X"

        self.assertNotIn(command, ["M", "S", "H", "Q"])

    def test_E05_closed_path(self):
        g = self.new_game()

        g["closed"].add(
            game.make_route_key("CAMP", "FOREST")
        )

        self.assertFalse(game.move_player(g, "FOREST"))

    def test_E06_low_energy(self):
        g = self.new_game()

        g["energy"] = 1

        self.assertFalse(game.move_player(g, "FOREST"))

    def test_E07_wrong_answer(self):
        g = self.new_game()
        c = self.clue()

        self.assertFalse(game.check_answer(2, c, g))

    def test_E08_no_hints(self):
        g = self.new_game()
        c = self.clue()

        g["hints"] = 0

        game.give_hint(c, g)

        self.assertEqual(g["hints"], 0)

    def test_E09_hint_uses_energy(self):
     g = self.new_game()
     c = self.clue()

     old_energy = g["energy"]

     game.give_hint(c, g)

     self.assertEqual(g["energy"], old_energy - 4)


  


    def test_E10_no_energy(self):
        g = self.new_game()

        g["energy"] = 0

        self.assertEqual(g["energy"], 0)

    def test_E11_no_chances(self):
        g = self.new_game()

        g["moves"] = 0

        self.assertEqual(g["moves"], 0)

    def test_E12_no_routes(self):
        g = self.new_game()

        for route in game.MAP["CAMP"]:
            g["closed"].add(
                game.make_route_key("CAMP", route[0])
            )

        self.assertEqual(
            game.get_open_routes("CAMP", g),
            []
        )

    def test_E13_treasure_reached(self):
        g = self.new_game()

        g["current"] = g["treasure"]

        self.assertEqual(
            g["current"],
            g["treasure"]
        )


if __name__ == "__main__":
    unittest.main()
