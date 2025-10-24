"""Test module for Backgammon checker objects functionality.

This module contains tests for checker object operations,
integration with the game, and related mechanics.
"""

import unittest
from core.backgammon import BackgammonGame
from core.checker import Checker


class TestBackgammonCheckers(unittest.TestCase):
    """Test class for Backgammon checker objects functionality."""

    def setUp(self):
        """Set up test fixtures before each test method.

        Returns:
            None
        """
        self.__game__ = BackgammonGame()

    def test_checker_objects_initialization(self):
        """Test that checker objects are created for each player.

        Returns:
            None
        """
        self.assertEqual(len(self.__game__.__player1_checkers__), 15)
        self.assertEqual(len(self.__game__.__player2_checkers__), 15)
        for checker in self.__game__.__player1_checkers__:
            self.assertIsInstance(checker, Checker)
            self.assertEqual(checker.__color__, "white")
        for checker in self.__game__.__player2_checkers__:
            self.assertIsInstance(checker, Checker)
            self.assertEqual(checker.__color__, "black")

    def test_get_checkers_at_point(self):
        """Test getting checker objects at a specific point.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        # Point 1 (0-indexed as 0) should have 2 white checkers
        checkers = self.__game__.get_checkers_at_point(0, 1)
        self.assertEqual(len(checkers), 2)
        for checker in checkers:
            self.assertIsInstance(checker, Checker)
            self.assertEqual(checker.__color__, "white")
            self.assertEqual(checker.__position__, 1)
        # Point 24 (0-indexed as 23) should have 2 black checkers
        checkers = self.__game__.get_checkers_at_point(23, 2)
        self.assertEqual(len(checkers), 2)
        for checker in checkers:
            self.assertIsInstance(checker, Checker)
            self.assertEqual(checker.__color__, "black")
            self.assertEqual(checker.__position__, 24)

    def test_get_checkers_on_bar_empty(self):
        """Test getting checkers on bar when none are there.

        Returns:
            None
        """
        checkers_p1 = self.__game__.get_checkers_on_bar(1)
        checkers_p2 = self.__game__.get_checkers_on_bar(2)
        self.assertEqual(len(checkers_p1), 0)
        self.assertEqual(len(checkers_p2), 0)

    def test_get_checkers_on_bar_with_checkers(self):
        """Test getting checkers on bar when there are some.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        # Send a checker to the bar
        checker = self.__game__.__player1_checkers__[0]
        checker.place_on_point(1)
        checker.send_to_bar()
        checkers = self.__game__.get_checkers_on_bar(1)
        self.assertEqual(len(checkers), 1)
        self.assertTrue(checkers[0].__is_on_bar__)
        self.assertEqual(checkers[0].__color__, "white")

    def test_get_borne_off_checkers_empty(self):
        """Test getting borne off checkers when none are borne off.

        Returns:
            None
        """
        checkers_p1 = self.__game__.get_borne_off_checkers(1)
        checkers_p2 = self.__game__.get_borne_off_checkers(2)
        self.assertEqual(len(checkers_p1), 0)
        self.assertEqual(len(checkers_p2), 0)

    def test_get_borne_off_checkers_with_checkers(self):
        """Test getting borne off checkers when some are borne off.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        # Bear off a checker
        checker = self.__game__.__player1_checkers__[0]
        checker.place_on_point(24)
        checker.bear_off()
        checkers = self.__game__.get_borne_off_checkers(1)
        self.assertEqual(len(checkers), 1)
        self.assertTrue(checkers[0].__is_borne_off__)
        self.assertEqual(checkers[0].__color__, "white")

    def test_move_checker_object_success(self):
        """Test moving a checker object from one point to another.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        # Move from point 1 (0-indexed as 0) to point 2 (0-indexed as 1)
        result = self.__game__.move_checker_object(0, 1, 1)
        self.assertTrue(result)
        # Verify the checker moved
        checkers_at_origin = self.__game__.get_checkers_at_point(0, 1)
        checkers_at_destination = self.__game__.get_checkers_at_point(1, 1)
        self.assertEqual(len(checkers_at_origin), 1)  # One less at origin
        self.assertEqual(len(checkers_at_destination), 1)  # One at destination

    def test_move_checker_object_capture(self):
        """Test checker object capturing opponent checker.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        # Place a single opponent checker at destination
        self.__game__.__player2_checkers__[0].place_on_point(2)
        # Move player 1 checker to capture
        result = self.__game__.move_checker_object(
            0, 1, 1
        )  # Move to point 2 (0-indexed as 1)
        self.assertTrue(result)
        # Verify opponent checker is on bar
        captured_checkers = self.__game__.get_checkers_on_bar(2)
        self.assertEqual(len(captured_checkers), 1)
        self.assertEqual(captured_checkers[0].__color__, "black")

    def test_move_checker_object_no_checkers_at_point(self):
        """Test move_checker_object when no checkers at source point.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        # Try to move from an empty point
        result = self.__game__.move_checker_object(
            10, 11, 1
        )  # Point 11(0-indexed 10)is empty initially
        self.assertFalse(result)

    def test_reset_game_resets_checkers(self):
        """Test that reset_game resets all checker objects.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        # Modify some checkers
        self.__game__.__player1_checkers__[0].send_to_bar()
        self.__game__.__player2_checkers__[0].bear_off()
        # Reset the game
        self.__game__.reset_game()
        # Verify all checkers are reset
        for checker in self.__game__.__player1_checkers__:
            self.assertIsNone(checker.__position__)
            self.assertFalse(checker.__is_on_bar__)
            self.assertFalse(checker.__is_borne_off__)
        for checker in self.__game__.__player2_checkers__:
            self.assertIsNone(checker.__position__)
            self.assertFalse(checker.__is_on_bar__)
            self.assertFalse(checker.__is_borne_off__)

    def test_make_move_with_history_capture_info(self):
        """Test make_move saves capture information in history.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]
        # Set up capture scenario
        self.__game__.__board__.__points__[1] = [2]  # Single black piece
        self.__game__.__board__.__points__[0] = [1, 1]  # White pieces to move
        initial_history_length = len(self.__game__.__move_history__)
        result = self.__game__.make_move(0, 1)
        self.assertTrue(result)
        self.assertEqual(
            len(self.__game__.__move_history__), initial_history_length + 1
        )
        # Check that capture was recorded
        last_move = self.__game__.__move_history__[-1]
        self.assertEqual(last_move["captured"], 2)  # Player 2 was captured
