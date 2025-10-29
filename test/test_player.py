"""
Unit tests for the Player class.

This module contains a suite of unit tests for the Player class, which represents a player in a
backgammon game. The tests cover the following functionalities:
"""

import unittest
from core.player import Player

# pylint: disable=C0116  # many simple test methods without individual docstrings


class TestPlayer(unittest.TestCase):
    """Test suite for core Player behavior and edge cases."""

    def setUp(self):
        """Set up test fixtures before each test method.

        Returns:
            None
        """
        self.__player_white__ = Player("Player1", "white")
        self.__player_black__ = Player("Player2", "black")

    def test_player_initialization_with_name_and_color(self):
        """Test player initialization with name and color.

        Returns:
            None
        """
        player = Player("TestPlayer", "white")
        self.assertEqual(player.__name__, "TestPlayer")
        self.assertEqual(player.__color__, "white")

    def test_player_initialization_black_color(self):
        """Test player initialization with black color.

        Returns:
            None
        """
        player = Player("BlackPlayer", "black")
        self.assertEqual(player.__name__, "BlackPlayer")
        self.assertEqual(player.__color__, "black")

    def test_player_initial_checkers_count(self):
        """Test initial checkers count for players.

        Returns:
            None
        """
        self.assertEqual(self.__player_white__.__checkers_count__, 15)
        self.assertEqual(self.__player_black__.__checkers_count__, 15)

    def test_player_initial_captured_checkers_empty(self):
        """Test initial captured checkers count is zero.

        Returns:
            None
        """
        self.assertEqual(self.__player_white__.__captured_checkers__, 0)
        self.assertEqual(self.__player_black__.__captured_checkers__, 0)

    def test_player_initial_bear_off_count_zero(self):
        self.assertEqual(self.__player_white__.__bear_off_count__, 0)
        self.assertEqual(self.__player_black__.__bear_off_count__, 0)

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
        initial_count = self.__player_white__.__captured_checkers__
        self.__player_white__.capture_checker()
        self.assertEqual(self.__player_white__.__captured_checkers__, initial_count + 1)

    def test_capture_multiple_checkers(self):
        self.__player_white__.capture_checker()
        self.__player_white__.capture_checker()
        self.__player_white__.capture_checker()
        self.assertEqual(self.__player_white__.__captured_checkers__, 3)

    def test_release_captured_checker_decreases_count(self):
        self.__player_white__.capture_checker()
        self.__player_white__.capture_checker()
        self.__player_white__.release_captured_checker()
        self.assertEqual(self.__player_white__.__captured_checkers__, 1)

    def test_release_captured_checker_when_none_captured_raises_exception(self):
        with self.assertRaises(ValueError) as context:
            self.__player_white__.release_captured_checker()
        self.assertIn("No captured checkers to release", str(context.exception))

    def test_has_captured_checkers_true_when_captured(self):
        self.assertFalse(self.__player_white__.has_captured_checkers())
        self.__player_white__.capture_checker()
        self.assertTrue(self.__player_white__.has_captured_checkers())

    def test_bear_off_checker_increases_count(self):
        initial_count = self.__player_white__.__bear_off_count__
        self.__player_white__.bear_off_checker()
        self.assertEqual(self.__player_white__.__bear_off_count__, initial_count + 1)

    def test_bear_off_multiple_checkers(self):
        self.__player_white__.bear_off_checker()
        self.__player_white__.bear_off_checker()
        self.__player_white__.bear_off_checker()
        self.assertEqual(self.__player_white__.__bear_off_count__, 3)

    def test_bear_off_checker_decreases_available_checkers(self):
        initial_checkers = self.__player_white__.__checkers_count__
        self.__player_white__.bear_off_checker()
        self.assertEqual(self.__player_white__.__checkers_count__, initial_checkers - 1)

    def test_bear_off_when_no_checkers_available_raises_exception(self):
        for _ in range(15):
            self.__player_white__.bear_off_checker()
        with self.assertRaises(ValueError) as context:
            self.__player_white__.bear_off_checker()
        self.assertIn("No checkers available for bear off", str(context.exception))

    def test_is_winner_true_when_all_checkers_bear_off(self):
        self.assertFalse(self.__player_white__.is_winner())
        for _ in range(15):
            self.__player_white__.bear_off_checker()
        self.assertTrue(self.__player_white__.is_winner())
        self.assertEqual(self.__player_white__.__bear_off_count__, 15)
        self.assertEqual(self.__player_white__.__checkers_count__, 0)

    def test_total_checkers_consistency(self):
        total = (
            self.__player_white__.__checkers_count__
            + self.__player_white__.__captured_checkers__
            + self.__player_white__.__bear_off_count__
        )
        self.assertEqual(total, 15)

        self.__player_white__.capture_checker()
        total = (
            self.__player_white__.__checkers_count__
            + self.__player_white__.__captured_checkers__
            + self.__player_white__.__bear_off_count__
        )
        self.assertEqual(total, 15)

        self.__player_white__.bear_off_checker()
        total = (
            self.__player_white__.__checkers_count__
            + self.__player_white__.__captured_checkers__
            + self.__player_white__.__bear_off_count__
        )
        self.assertEqual(total, 15)

    def test_can_bear_off_based_on_checkers_available(self):
        self.assertTrue(self.__player_white__.can_bear_off())
        for _ in range(15):
            self.__player_white__.bear_off_checker()
        self.assertFalse(self.__player_white__.can_bear_off())

    def test_player_string_representation(self):
        # Now uses real checkers_count
        expected = "Player1 (white) - Checkers: 15, Captured: 0, Bear off: 0"
        self.assertEqual(str(self.__player_white__), expected)

        self.__player_white__.capture_checker()
        self.__player_white__.bear_off_checker()

        # After capture (-1 from board) and bear off (-1 from board, +1 off)
        # checkers_count = 13, captured = 1, bear_off = 1
        expected = "Player1 (white) - Checkers: 13, Captured: 1, Bear off: 1"
        self.assertEqual(str(self.__player_white__), expected)

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
        self.__player_white__.capture_checker()
        self.__player_white__.capture_checker()
        self.__player_white__.bear_off_checker()
        self.__player_white__.reset()
        self.assertEqual(self.__player_white__.__checkers_count__, 15)
        self.assertEqual(self.__player_white__.__captured_checkers__, 0)
        self.assertEqual(self.__player_white__.__bear_off_count__, 0)


if __name__ == "__main__":
    unittest.main()
