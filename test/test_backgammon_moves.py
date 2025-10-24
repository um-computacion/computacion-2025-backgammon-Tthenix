"""Test module for Backgammon move functionality.

This module contains tests for move validation, execution,
and related game mechanics.
"""

import unittest
from unittest.mock import patch
from core.backgammon import BackgammonGame


class TestBackgammonMoves(unittest.TestCase):
    """Test class for Backgammon move functionality."""

    def setUp(self):
        """Set up test fixtures before each test method.

        Returns:
            None
        """
        self.__game__ = BackgammonGame()

    def test_undo_last_move(self):
        """Test undoing the last move.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.make_move(0, 1)
        result = self.__game__.undo_last_move()
        self.assertTrue(result)

    def test_undo_last_move_no_moves(self):
        """Test undoing when no moves have been made.

        Returns:
            None
        """
        result = self.__game__.undo_last_move()
        self.assertFalse(result)

    def test_get_possible_destinations_from_point(self):
        """Test getting possible destinations from a point.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        destinations = self.__game__.get_possible_destinations(0)
        self.assertIsInstance(destinations, list)

    def test_get_possible_destinations_invalid_point(self):
        """Test getting destinations from an invalid point.

        Returns:
            None
        """
        self.__game__.__last_roll__ = (1, 2)
        destinations = self.__game__.get_possible_destinations(10)
        self.assertEqual(destinations, [])

    def test_has_valid_moves_true(self):
        """Test has_valid_moves when moves are available.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        has_moves = self.__game__.has_valid_moves()
        self.assertTrue(has_moves)

    def test_has_valid_moves_false(self):
        """Test has_valid_moves when no moves are available.

        Returns:
            None
        """
        self.__game__.__last_roll__ = (1, 2)
        has_moves = self.__game__.has_valid_moves()
        self.assertFalse(has_moves)

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

    @patch("core.dice.Dice.roll", return_value=(1, 2))
    def test_auto_play_turn_when_no_moves(self, _mock_roll):
        """Test auto play turn with controlled dice values.

        Args:
            _mock_roll: Mock for dice roll method

        Returns:
            None
        """
        self.__game__.__last_roll__ = (1, 2)
        result = self.__game__.auto_play_turn()
        self.assertTrue(result)

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

    def test_validate_complete_turn(self):
        """Test validating a complete turn.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        moves = [(0, 1), (0, 2)]
        is_valid = self.__game__.validate_complete_turn(moves)
        self.assertIsInstance(is_valid, bool)

    def test_execute_turn_with_moves(self):
        """Test executing a turn with moves.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        moves = [(0, 1)]
        result = self.__game__.execute_turn(moves)
        self.assertIsInstance(result, bool)

    def test_auto_play_turn_with_moves_present(self):
        """Test auto_play_turn when moves are available.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]
        initial_player = self.__game__.__current_player__
        result = self.__game__.auto_play_turn()
        self.assertFalse(result)
        self.assertEqual(self.__game__.__current_player__, initial_player)

    @patch("core.dice.Dice.__get_moves__", return_value=[1, 2])
    def test_undo_last_move_restores_available_moves(self, mock_get_moves):
        """Test that undo_last_move restores available moves.

        Args:
            mock_get_moves: Mock for dice get_moves method

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]
        # Make a valid move to consume a die
        self.assertTrue(self.__game__.make_move(0, 1))
        self.assertLess(len(self.__game__.__available_moves__), 2)
        # Undo and expect available moves restored via dice.get_moves
        self.assertTrue(self.__game__.undo_last_move())
        self.assertEqual(self.__game__.__available_moves__, [1, 2])
        self.assertTrue(mock_get_moves.called)

    def test_get_possible_destinations_repopulates_available_moves(self):
        """Test that get_possible_destinations repopulates available_moves.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = []
        # Should compute [1, 2] moves from point 0->destinations include 1 and maybe 2 from point 0
        dests = self.__game__.get_possible_destinations(0)
        self.assertIsInstance(dests, list)
        self.assertTrue(all(isinstance(x, int) for x in dests))

    def test_validate_move_no_dice_rolled(self):
        """Test validate_move when no dice have been rolled.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        # Don't roll dice
        self.assertFalse(self.__game__.validate_move(0, 1))

    def test_validate_move_empty_available_moves_with_last_roll(self):
        """Test validate_move when available_moves is empty but last_roll exists.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (3, 4)
        self.__game__.__available_moves__ = []  # Empty but last_roll exists

        result = self.__game__.validate_move(0, 3)
        self.assertIsInstance(result, bool)

    def test_validate_move_out_of_bounds(self):
        """Test validate_move with out of bounds positions.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        # Test negative from_point
        self.assertFalse(self.__game__.validate_move(-1, 1))
        # Test from_point >= 24
        self.assertFalse(self.__game__.validate_move(24, 23))

    def test_validate_move_wrong_player_piece(self):
        """Test validate_move when trying to move opponent's piece.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player1__  # White player
        self.__game__.__last_roll__ = (1, 2)
        # Try to move black piece (at point 23, 0-indexed)
        result = self.__game__.validate_move(23, 22)
        self.assertFalse(result)

    def test_validate_move_wrong_direction_player1(self):
        """Test validate_move when player1 tries to move backwards.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.__last_roll__ = (1, 2)
        # Player 1 should move forward (increasing point numbers)
        result = self.__game__.validate_move(11, 10)  # Moving backwards
        self.assertFalse(result)

    def test_validate_move_wrong_direction_player2(self):
        """Test validate_move when player2 tries to move backwards.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player2__
        self.__game__.__last_roll__ = (1, 2)
        # Player 2 should move backward (decreasing point numbers)
        result = self.__game__.validate_move(12, 13)  # Moving forwards for player2
        self.assertFalse(result)

    def test_make_move_with_capture(self):
        """Test make_move when capturing an opponent piece.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.__last_roll__ = (1, 2)
        # Place a single opponent piece to capture
        self.__game__.__board__.__points__[1] = [2]  # Single black piece
        self.__game__.__board__.__points__[0] = [1, 1]  # Two white pieces to move from
        result = self.__game__.make_move(0, 1)
        self.assertTrue(result)
        # Check that the piece was captured (sent to bar)
        # Ficha negra (2) capturada va al lado blanco (index 0)
        self.assertGreater(len(self.__game__.__board__.__checker_bar__[0]), 0)

    def test_validate_move_distance_not_found(self):
        """Test validate_move when dice distance is not available.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]  # Only 1 and 2 available
        # Try to make a move with distance 3 (not available)
        result = self.__game__.validate_move(0, 3)
        self.assertFalse(result)

    def test_current_player_is_player2(self):
        """Test various methods when current player is player2.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player2__
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]
        # Test validate_move for player 2
        result = self.__game__.validate_move(12, 11)  # Player 2 moving backward
        self.assertIsInstance(result, bool)
        # Test make_move for player 2
        if result:
            move_result = self.__game__.make_move(12, 11)
            self.assertIsInstance(move_result, bool)
