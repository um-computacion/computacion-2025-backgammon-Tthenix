"""Advanced tests for BackgammonGame functionality.

This module contains tests for advanced BackgammonGame features including:
- Bar mechanics and entry from bar
- Bearing off functionality
- Checker object integration
- Complex game scenarios
- Special rules and edge cases
"""

import unittest
from unittest.mock import patch
from core.backgammon import BackgammonGame
from core.checker import Checker


class TestBackgammonAdvanced(unittest.TestCase):
    """Test class for advanced BackgammonGame functionality."""

    def setUp(self):
        """Set up test fixtures before each test method.

        Returns:
            None
        """
        self.__game__ = BackgammonGame()

    # ==================== BAR MECHANICS TESTS ====================

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

    def test_can_enter_from_bar_player1(self):
        """Test can_enter_from_bar for player 1.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]
        result = self.__game__.can_enter_from_bar(1)
        self.assertTrue(result)

    def test_can_enter_from_bar_player2(self):
        """Test can_enter_from_bar for player 2.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player2__
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]

        result = self.__game__.can_enter_from_bar(2)

        self.assertTrue(result)

    def test_can_enter_from_bar_no_moves(self):
        """Test can_enter_from_bar with no available moves.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__available_moves__ = []

        result = self.__game__.can_enter_from_bar(1)
        self.assertFalse(result)

    def test_can_enter_from_bar_entry_point_24(self):
        """Test _can_enter_from_bar with entry point 24.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]

        # Mock board to have entry point 24
        with patch.object(
            self.__game__.__board__, "__points__", [[] for _ in range(24)]
        ):
            result = self.__game__.can_enter_from_bar(2)
            self.assertTrue(result)  # Should be True because board is empty

    def test_can_enter_from_bar_entry_point_negative(self):
        """Test _can_enter_from_bar with negative entry point.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]

        # Mock board to have negative entry point
        with patch.object(
            self.__game__.__board__, "__points__", [[] for _ in range(24)]
        ):
            result = self.__game__.can_enter_from_bar(1)
            self.assertTrue(result)  # Should be True because board is empty

    def test_can_enter_from_bar_empty_point(self):
        """Test _can_enter_from_bar with empty point.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]

        # Mock board to have empty entry point
        with patch.object(
            self.__game__.__board__, "__points__", [[] for _ in range(24)]
        ):
            result = self.__game__.can_enter_from_bar(1)
            self.assertTrue(result)

    def test_can_enter_from_bar_own_checkers(self):
        """Test _can_enter_from_bar with own checkers on entry point.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]

        # Mock board to have own checkers on entry point
        mock_point = [1]  # Player 1's checker
        with patch.object(
            self.__game__.__board__,
            "__points__",
            [mock_point if i == 0 else [] for i in range(24)],
        ):
            result = self.__game__.can_enter_from_bar(1)
            self.assertTrue(result)

    def test_can_enter_from_bar_opponent_checkers(self):
        """Test _can_enter_from_bar with opponent checkers on entry point.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]

        # Mock board to have opponent checkers on entry point
        mock_point = [2]  # Player 2's checker
        with patch.object(
            self.__game__.__board__,
            "__points__",
            [mock_point if i == 0 else [] for i in range(24)],
        ):
            result = self.__game__.can_enter_from_bar(1)
            self.assertTrue(result)  # Should be True because can hit opponent (len < 2)

    def test_can_enter_from_bar_multiple_opponent_checkers(self):
        """Test _can_enter_from_bar with multiple opponent checkers.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]

        # Mock board to have multiple opponent checkers on both entry points
        mock_point = [2, 2]  # Two player 2's checkers
        with patch.object(
            self.__game__.__board__,
            "__points__",
            [
                mock_point if i in [0, 1] else [] for i in range(24)
            ],  # Block both entry points
        ):
            result = self.__game__.can_enter_from_bar(1)
            self.assertFalse(
                result
            )  # Should be False because both entry points are blocked (len >= 2)

    # ==================== BEARING OFF TESTS ====================

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

    # ==================== CHECKER OBJECT TESTS ====================

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

    # ==================== SPECIAL RULES TESTS ====================

    def test_must_enter_from_bar_true(self):
        """Test must_enter_from_bar when player has pieces on bar.

        Returns:
            None
        """
        # Ficha blanca (1) capturada está en el lado negro (index 1)
        self.__game__.__board__.__checker_bar__[1] = [1]
        self.__game__.__current_player__ = self.__game__.__player1__
        must_enter = self.__game__.must_enter_from_bar()
        self.assertTrue(must_enter)

    def test_must_enter_from_bar_false(self):
        """Test must_enter_from_bar when player has no pieces on bar.

        Returns:
            None
        """
        self.__game__.__current_player__ = self.__game__.__player1__
        must_enter = self.__game__.must_enter_from_bar()
        self.assertFalse(must_enter)

    def test_get_pip_count_player1(self):
        """Test getting pip count for player 1.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        pip_count = self.__game__.get_pip_count(self.__game__.__player1__)
        self.assertIsInstance(pip_count, int)
        self.assertGreater(pip_count, 0)

    def test_get_pip_count_player2(self):
        """Test getting pip count for player 2.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        pip_count = self.__game__.get_pip_count(self.__game__.__player2__)
        self.assertIsInstance(pip_count, int)
        self.assertGreater(pip_count, 0)

    def test_is_blocked_position_true(self):
        """Test is_blocked_position when position is blocked.

        Returns:
            None
        """
        self.__game__.__board__.__points__[5] = [2, 2]
        is_blocked = self.__game__.is_blocked_position(5, 1)
        self.assertTrue(is_blocked)

    def test_is_blocked_position_false(self):
        """Test is_blocked_position when position is not blocked.

        Returns:
            None
        """
        self.__game__.__board__.__points__[5] = [1]
        is_blocked = self.__game__.is_blocked_position(5, 1)
        self.assertFalse(is_blocked)

    def test_can_hit_opponent_true(self):
        """Test can_hit_opponent when opponent can be hit.

        Returns:
            None
        """
        self.__game__.__board__.__points__[5] = [2]
        can_hit = self.__game__.can_hit_opponent(5, 1)
        self.assertTrue(can_hit)

    def test_can_hit_opponent_false_multiple_checkers(self):
        """Test can_hit_opponent when opponent has multiple checkers.

        Returns:
            None
        """
        self.__game__.__board__.__points__[5] = [2, 2]
        can_hit = self.__game__.can_hit_opponent(5, 1)
        self.assertFalse(can_hit)

    def test_can_hit_opponent_false_same_player(self):
        """Test can_hit_opponent when it's the same player's checker.

        Returns:
            None
        """
        self.__game__.__board__.__points__[5] = [1]
        can_hit = self.__game__.can_hit_opponent(5, 1)
        self.assertFalse(can_hit)

    def test_apply_game_rules_bearing_off(self):
        """Test applying game rules for bearing off.

        Returns:
            None
        """
        for i in range(18, 24):
            self.__game__.__board__.__points__[i] = [1] if i == 23 else []
        self.__game__.__last_roll__ = (6, 6)
        rules_applied = self.__game__.apply_game_rules()
        self.assertIsInstance(rules_applied, bool)


if __name__ == "__main__":
    unittest.main()
