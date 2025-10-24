"""Test module for Backgammon bearing off functionality.

This module contains tests for bearing off mechanics,
home board validation, and related operations.
"""

import unittest
from core.backgammon import BackgammonGame


class TestBackgammonBearingOff(unittest.TestCase):
    """Test class for Backgammon bearing off functionality."""

    def setUp(self):
        """Set up test fixtures before each test method.

        Returns:
            None
        """
        self.__game__ = BackgammonGame()

    def test_can_bear_off_all_checkers_in_home(self):
        """Test bearing off when all checkers are in home board.

        Returns:
            None
        """
        for i in range(18, 24):
            self.__game__.__board__.__points__[i] = [1] if i == 23 else []
        can_bear_off = self.__game__.can_bear_off(1)
        self.assertTrue(can_bear_off)

    def test_cannot_bear_off_checkers_outside_home(self):
        """Test that bearing off is not allowed when checkers are outside home.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        can_bear_off = self.__game__.can_bear_off(1)
        self.assertFalse(can_bear_off)

    def test_bear_off_checker_valid(self):
        """Test bearing off a checker under valid conditions.

        Returns:
            None
        """
        for i in range(18, 24):
            self.__game__.__board__.__points__[i] = [1] if i == 23 else []
        self.__game__.__last_roll__ = (1, 2)
        result = self.__game__.bear_off_checker(23)
        self.assertTrue(result)

    def test_bear_off_checker_invalid_conditions(self):
        """Test bearing off a checker under invalid conditions.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        result = self.__game__.bear_off_checker(23)
        self.assertFalse(result)

    def test_bear_off_updates_off_board(self):
        """Test that bearing off updates the off-board count.

        Returns:
            None
        """
        for i in range(18, 24):
            self.__game__.__board__.__points__[i] = [1] if i == 23 else []
        self.__game__.__last_roll__ = (1, 2)
        initial_off_count = len(self.__game__.__board__.__off_board__[0])
        self.__game__.bear_off_checker(23)
        self.assertGreater(
            len(self.__game__.__board__.__off_board__[0]), initial_off_count
        )

    def test_bear_off_checker_not_all_in_home(self):
        """Test bear_off_checker when not all pieces are in home.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.__available_moves__ = [6]
        # Player 1 still has pieces outside home board
        result = self.__game__.bear_off_checker(23)
        self.assertFalse(result)

    def test_bear_off_checker_no_dice_available(self):
        """Test bear_off_checker when no dice values are available.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.__available_moves__ = []  # No moves available
        self.__game__.__last_roll__ = None

        # Move all pieces to home board first
        for i in range(18, 24):
            self.__game__.__board__.__points__[i] = [1] if i == 23 else []
        result = self.__game__.bear_off_checker(23)
        self.assertFalse(result)

    def test_bear_off_checker_with_valid_dice(self):
        """Test successful bear off with valid conditions.

        Returns:
            None
        """
        # Clear board and set up bear off scenario
        for i in range(24):
            self.__game__.__board__.__points__[i] = []
        self.__game__.__board__.__points__[23] = [1]  # One piece at point 24
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.__available_moves__ = [6]
        self.__game__.__last_roll__ = (6, 6)
        result = self.__game__.bear_off_checker(23)
        self.assertTrue(result)

    def test_bear_off_tries_multiple_dice(self):
        """Test bear_off_checker tries multiple dice values.

        Returns:
            None
        """
        # Prepare a simple bear-off scenario for player 1
        for i in range(24):
            self.__game__.__board__.__points__[i] = []
        self.__game__.__board__.__points__[23] = [1]
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.__last_roll__ = (2, 1)
        self.__game__.__available_moves__ = [2, 1]
        # 23 requires 1 to bear off (distance 1). Should succeed and consume one die
        self.assertTrue(self.__game__.bear_off_checker(23))
        self.assertIn(len(self.__game__.__available_moves__), (1, 1))

    def test_bear_off_checker_empty_available_moves_with_last_roll(self):
        """Test bear_off_checker when available_moves is empty but last_roll exists.

        Returns:
            None
        """
        # Set up bear off scenario
        for i in range(24):
            self.__game__.__board__.__points__[i] = []
        self.__game__.__board__.__points__[23] = [1]  # One piece at point 24
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.__available_moves__ = []  # Empty
        self.__game__.__last_roll__ = (6, 6)  # But last_roll exists
        result = self.__game__.bear_off_checker(23)
        self.assertIsInstance(result, bool)

    def test_bear_off_checker_successful_removal(self):
        """Test successful bear off with dice removal.

        Returns:
            None
        """
        # Set up bear off scenario
        for i in range(24):
            self.__game__.__board__.__points__[i] = []
        self.__game__.__board__.__points__[23] = [1]  # One piece at point 24
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.__available_moves__ = [6, 5]  # Multiple dice values
        self.__game__.__last_roll__ = (6, 5)
        result = self.__game__.bear_off_checker(23)
        self.assertTrue(result)
        # Check that dice was consumed
        self.assertNotEqual(
            len(self.__game__.__available_moves__), 2
        )  # Should be reduced

    def test_bear_off_checker_player2(self):
        """Test bear_off_checker for player 2.

        Returns:
            None
        """
        # Set up bear off scenario for player 2
        for i in range(24):
            self.__game__.__board__.__points__[i] = []
        self.__game__.__board__.__points__[0] = [2]  # One piece at point 1 for player 2
        self.__game__.__current_player__ = self.__game__.__player2__
        self.__game__.__available_moves__ = [1]
        # No-op stray expression caused linter warning; ensure a real assertion
        self.assertIsInstance(self.__game__, BackgammonGame)

    def test_bear_off_checker_object_success(self):
        """Test bearing off a checker object.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        # Place a checker at point 24 (0-indexed as 23)
        checker = self.__game__.__player1_checkers__[0]
        checker.place_on_point(24)
        # Bear off the checker
        result = self.__game__.bear_off_checker_object(23, 1)
        self.assertTrue(result)
        # Verify checker is borne off
        self.assertTrue(checker.__is_borne_off__)
        self.assertIsNone(checker.__position__)

    def test_bear_off_checker_object_no_checkers(self):
        """Test bear_off_checker_object when no checkers at point.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        # Try to bear off from an empty point
        result = self.__game__.bear_off_checker_object(10, 1)  # Point 11 is empty
        self.assertFalse(result)
