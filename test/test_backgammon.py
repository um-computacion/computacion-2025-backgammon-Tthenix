"""Test module for Backgammon game integration.

This module contains integration tests and complex scenarios
that require the full BackgammonGame functionality.
"""

import unittest
from core.backgammon import BackgammonGame


class TestBackgammonIntegration(unittest.TestCase):
    """Test class for Backgammon game integration."""

    def setUp(self):
        """Set up test fixtures before each test method.

        Returns:
            None
        """
        self.__game__ = BackgammonGame()

    def test_validate_complete_turn_invalid_dice(self):
        """Test validate_complete_turn with invalid dice distances.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]
        moves = [(0, 3)]  # distance 3 not available
        self.assertFalse(self.__game__.validate_complete_turn(moves))

    def test_execute_turn_invalid(self):
        """Test execute_turn when validation fails.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]
        moves = [(0, 3)]
        self.assertFalse(self.__game__.execute_turn(moves))

    def test_is_blocked_position_out_of_bounds(self):
        """Test is_blocked_position with out of bounds positions.

        Returns:
            None
        """
        self.assertFalse(self.__game__.is_blocked_position(-1, 1))
        self.assertFalse(self.__game__.is_blocked_position(24, 1))

    def test_can_hit_opponent_out_of_bounds(self):
        """Test can_hit_opponent with out of bounds positions.

        Returns:
            None
        """
        self.assertFalse(self.__game__.can_hit_opponent(-1, 1))
        self.assertFalse(self.__game__.can_hit_opponent(24, 1))

    def test_get_available_moves_no_last_roll(self):
        """Test get_available_moves when no dice have been rolled.

        Returns:
            None
        """
        self.__game__.__last_roll__ = None
        moves = self.__game__.get_available_moves()
        self.assertEqual(moves, [])

    def test_integration_complete_game_flow(self):
        """Test integration scenario for complete game flow.

        Returns:
            None
        """
        # Test a complete game flow integration
        self.__game__.setup_initial_position()
        # Test game state after setup
        self.assertFalse(self.__game__.is_game_over())
        self.assertIsNone(self.__game__.get_winner())

        # Test dice rolling
        roll = self.__game__.roll_dice()
        self.assertIsInstance(roll, tuple)
        self.assertEqual(len(roll), 2)

        # Test game state after dice roll
        self.assertIsNotNone(self.__game__.__last_roll__)
        self.assertIsInstance(self.__game__.get_available_moves(), list)
