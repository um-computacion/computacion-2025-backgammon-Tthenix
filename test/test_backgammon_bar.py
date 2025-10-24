"""Test module for Backgammon bar functionality.

This module contains tests for bar operations, entry from bar,
and related mechanics.
"""

import unittest
from core.backgammon import BackgammonGame


class TestBackgammonBar(unittest.TestCase):
    """Test class for Backgammon bar functionality."""

    def setUp(self):
        """Set up test fixtures before each test method.

        Returns:
            None
        """
        self.__game__ = BackgammonGame()

    def test_hit_opponent_checker(self):
        """Test hitting an opponent checker.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__board__.__points__[5] = [1]
        self.__game__.__last_roll__ = (1, 2)
        result = self.__game__.make_move(23, 22)
        if result:
            self.assertGreater(len(self.__game__.__board__.__checker_bar__[1]), 0)

    def test_move_checker_from_bar(self):
        """Test moving a checker from the bar.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__board__.__checker_bar__[0] = [1]
        self.__game__.__last_roll__ = (1, 2)
        result = self.__game__.move_from_bar(1)
        self.assertIsInstance(result, bool)

    def test_move_from_bar_no_checkers(self):
        """Test moving from bar when no checkers are on bar.

        Returns:
            None
        """
        self.__game__.__last_roll__ = (1, 2)
        result = self.__game__.move_from_bar(1)
        self.assertFalse(result)

    def test_move_from_bar_blocked_entry(self):
        """Test moving from bar when entry point is blocked.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__board__.__checker_bar__[0] = [1]
        self.__game__.__board__.__points__[0] = [2, 2]
        self.__game__.__last_roll__ = (1, 2)
        result = self.__game__.move_from_bar(1)
        self.assertFalse(result)

    def test_move_from_bar_success_no_capture(self):
        """Test successful move from bar without capture.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player1__
        # Ficha blanca (1) capturada está en el lado negro (index 1)
        self.__game__.__board__.__checker_bar__[1] = [1]
        self.__game__.__available_moves__ = [6]
        # Blancas re-entran en puntos 0-5: con dado 6 → punto 5 (6-1=5)
        self.__game__.__board__.__points__[5] = []  # Ensure entry point 5 is free
        self.assertTrue(self.__game__.move_from_bar(6))
        self.assertNotIn(6, self.__game__.__available_moves__)

    def test_move_from_bar_invalid_dice(self):
        """Test move_from_bar with invalid dice value.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.__available_moves__ = [3, 4]  # Only 3 and 4 available
        self.__game__.__board__.__checker_bar__[0] = [1]  # Player 1 on bar
        # Try to use dice value 2 which is not available
        result = self.__game__.move_from_bar(2)
        self.assertFalse(result)

    def test_move_from_bar_out_of_bounds_entry_point(self):
        """Test move_from_bar with dice that would create out of bounds entry point.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.__available_moves__ = [25]  # Invalid dice value
        self.__game__.__board__.__checker_bar__[0] = [1]  # Player 1 on bar
        result = self.__game__.move_from_bar(25)
        self.assertFalse(result)

    def test_move_from_bar_success_with_capture(self):
        """Test successful move from bar with capture.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.__available_moves__ = [1]
        # Ficha blanca (1) capturada está en el lado negro (index 1)
        self.__game__.__board__.__checker_bar__[1] = [1]  # Player 1 on bar
        # Blancas re-entran en puntos 0-5: con dado 1 → punto 0 (1-1=0)
        # Place single opponent piece at entry point
        self.__game__.__board__.__points__[0] = [2]  # Single black piece at point 0
        result = self.__game__.move_from_bar(1)
        self.assertTrue(result)
        # Check that opponent was captured - Ficha negra va al lado blanco (index 0)
        self.assertGreater(len(self.__game__.__board__.__checker_bar__[0]), 0)

    def test_move_from_bar_player2(self):
        """Test move_from_bar for player 2.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player2__
        self.__game__.__available_moves__ = [2]
        # Ficha negra (2) capturada está en el lado blanco (index 0)
        self.__game__.__board__.__checker_bar__[0] = [2]  # Player 2 on bar
        # Clear the entry point to ensure it's not blocked
        self.__game__.__board__.__points__[1] = []  # Clear point 2 (0-indexed as 1)
        # Player 2 should enter at point 2 (dice_value - 1 = 1 for dice_value 2)
        result = self.__game__.move_from_bar(2)
        self.assertTrue(result)

    def test_move_checker_from_bar_object_capture_player2(self):
        """Test player 2 returning from bar and capturing opponent.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        # Put player 2 checker on bar and place a single white checker at point 2
        c2 = self.__game__.__player2_checkers__[0]
        c2.send_to_bar()
        self.__game__.__player1_checkers__[0].place_on_point(2)
        result = self.__game__.move_checker_from_bar_object(
            1, 2
        )  # to point 2 (0-indexed)
        self.assertTrue(result)
        # White checker should now be on bar
        whites_on_bar = [
            c for c in self.__game__.__player1_checkers__ if c.__is_on_bar__
        ]
        self.assertGreaterEqual(len(whites_on_bar), 1)

    def test_move_checker_from_bar_object_success(self):
        """Test moving a checker object from bar to board.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        # Put a checker on the bar
        checker = self.__game__.__player1_checkers__[0]
        checker.send_to_bar()
        # Move from bar to point 2 (0-indexed as 1)
        result = self.__game__.move_checker_from_bar_object(1, 1)
        self.assertTrue(result)
        # Verify checker is no longer on bar and is at destination
        self.assertFalse(checker.__is_on_bar__)
        self.assertEqual(checker.__position__, 2)

    def test_move_checker_from_bar_object_no_checkers(self):
        """Test move_checker_from_bar_object when no checkers on bar.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        # Bar should be empty initially
        result = self.__game__.move_checker_from_bar_object(20, 1)
        self.assertFalse(result)
