import unittest
from core.player import Player


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player_white = Player("Player1", "white")
        self.player_black = Player("Player2", "black")

    def test_player_initialization_with_name_and_color(self):
        player = Player("TestPlayer", "white")
        self.assertEqual(player.name, "TestPlayer")
        self.assertEqual(player.color, "white")

    def test_player_initialization_black_color(self):
        player = Player("BlackPlayer", "black")
        self.assertEqual(player.name, "BlackPlayer")
        self.assertEqual(player.color, "black")

    def test_player_initial_checkers_count(self):
        self.assertEqual(self.player_white.checkers_count, 15)
        self.assertEqual(self.player_black.checkers_count, 15)

    def test_player_initial_captured_checkers_empty(self):
        self.assertEqual(self.player_white.captured_checkers, 0)
        self.assertEqual(self.player_black.captured_checkers, 0)

    def test_player_initial_bear_off_count_zero(self):
        self.assertEqual(self.player_white.bear_off_count, 0)
        self.assertEqual(self.player_black.bear_off_count, 0)

    def test_invalid_color_raises_exception(self):
        with self.assertRaises(ValueError) as context:
            Player("TestPlayer", "red")
        self.assertIn("Color should be 'white' o 'black'", str(context.exception))

    def test_empty_name_raises_exception(self):
        with self.assertRaises(ValueError) as context:
            Player("", "white")
        self.assertIn("The name cannot be empty", str(context.exception))

    def test_none_name_raises_exception(self):
        with self.assertRaises(ValueError) as context:
            Player(None, "white")
        self.assertIn("The name cannot be empty", str(context.exception))

    def test_capture_checker_increases_count(self):
        initial_count = self.player_white.captured_checkers
        self.player_white.capture_checker()
        self.assertEqual(self.player_white.captured_checkers, initial_count + 1)

    def test_capture_multiple_checkers(self):
        self.player_white.capture_checker()
        self.player_white.capture_checker()
        self.player_white.capture_checker()
        self.assertEqual(self.player_white.captured_checkers, 3)

    def test_release_captured_checker_decreases_count(self):
        self.player_white.capture_checker()
        self.player_white.capture_checker()
        self.player_white.release_captured_checker()
        self.assertEqual(self.player_white.captured_checkers, 1)

    def test_release_captured_checker_when_none_captured_raises_exception(self):
        with self.assertRaises(ValueError) as context:
            self.player_white.release_captured_checker()
        self.assertIn("No captured checkers to release", str(context.exception))

    def test_has_captured_checkers_true_when_captured(self):
        self.assertFalse(self.player_white.has_captured_checkers())
        self.player_white.capture_checker()
        self.assertTrue(self.player_white.has_captured_checkers())

    def test_bear_off_checker_increases_count(self):
        initial_count = self.player_white.bear_off_count
        self.player_white.bear_off_checker()
        self.assertEqual(self.player_white.bear_off_count, initial_count + 1)

    def test_bear_off_multiple_checkers(self):
        self.player_white.bear_off_checker()
        self.player_white.bear_off_checker()
        self.player_white.bear_off_checker()
        self.assertEqual(self.player_white.bear_off_count, 3)

    def test_bear_off_checker_decreases_available_checkers(self):
        initial_checkers = self.player_white.checkers_count
        self.player_white.bear_off_checker()
        self.assertEqual(self.player_white.checkers_count, initial_checkers - 1)

    def test_bear_off_when_no_checkers_available_raises_exception(self):
        for _ in range(15):
            self.player_white.bear_off_checker()
        with self.assertRaises(ValueError) as context:
            self.player_white.bear_off_checker()
        self.assertIn("No checkers available for bear off", str(context.exception))

    def test_is_winner_true_when_all_checkers_bear_off(self):
        self.assertFalse(self.player_white.is_winner())
        for _ in range(15):
            self.player_white.bear_off_checker()
        self.assertTrue(self.player_white.is_winner())
        self.assertEqual(self.player_white.bear_off_count, 15)
        self.assertEqual(self.player_white.checkers_count, 0)

    def test_total_checkers_consistency(self):
        total = (
            self.player_white.checkers_count
            + self.player_white.captured_checkers
            + self.player_white.bear_off_count
        )
        self.assertEqual(total, 15)

        self.player_white.capture_checker()
        total = (
            self.player_white.checkers_count
            + self.player_white.captured_checkers
            + self.player_white.bear_off_count
        )
        self.assertEqual(total, 15)

        self.player_white.bear_off_checker()
        total = (
            self.player_white.checkers_count
            + self.player_white.captured_checkers
            + self.player_white.bear_off_count
        )
        self.assertEqual(total, 15)

    def test_can_bear_off_based_on_checkers_available(self):
        self.assertTrue(self.player_white.can_bear_off())
        for _ in range(15):
            self.player_white.bear_off_checker()
        self.assertFalse(self.player_white.can_bear_off())

    def test_player_string_representation(self):
        # Now uses real checkers_count
        expected = "Player1 (white) - Checkers: 15, Captured: 0, Bear off: 0"
        self.assertEqual(str(self.player_white), expected)

        self.player_white.capture_checker()
        self.player_white.bear_off_checker()

        # After capture (-1 from board) and bear off (-1 from board, +1 off)
        # checkers_count = 13, captured = 1, bear_off = 1
        expected = "Player1 (white) - Checkers: 13, Captured: 1, Bear off: 1"
        self.assertEqual(str(self.player_white), expected)

    def test_player_equality_based_on_name_and_color(self):
        player1 = Player("Test", "white")
        player2 = Player("Test", "white")
        player3 = Player("Test", "black")
        player4 = Player("Other", "white")
        self.assertEqual(player1, player2)
        self.assertNotEqual(player1, player3)
        self.assertNotEqual(player1, player4)

    def test_player_hash_consistency(self):
        player1 = Player("Test", "white")
        player2 = Player("Test", "white")
        self.assertEqual(hash(player1), hash(player2))

    def test_reset_player_state(self):
        self.player_white.capture_checker()
        self.player_white.capture_checker()
        self.player_white.bear_off_checker()
        self.player_white.reset()
        self.assertEqual(self.player_white.checkers_count, 15)
        self.assertEqual(self.player_white.captured_checkers, 0)
        self.assertEqual(self.player_white.bear_off_count, 0)


if __name__ == "__main__":
    unittest.main()
