"""Integration tests for BackgammonGame functionality.

This module contains integration tests and complex scenarios that require
the full BackgammonGame functionality including:
- Complete game flows
- Complex move sequences
- Turn validation and execution
- Error handling and edge cases
- Performance and stress tests
"""

import unittest
from unittest.mock import patch
from core.backgammon import BackgammonGame


class TestBackgammonIntegration(unittest.TestCase):
    """Test class for Backgammon game integration."""

    def setUp(self):
        """Set up test fixtures before each test method.

        Returns:
            None
        """
        self.__game__ = BackgammonGame()

    # ==================== COMPLETE GAME FLOW TESTS ====================

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

    def test_validate_complete_turn_valid(self):
        """Test validate_complete_turn with valid moves.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]
        moves = [(0, 1), (0, 2)]

        result = self.__game__.validate_complete_turn(moves)
        self.assertTrue(result)

    def test_validate_complete_turn_invalid_moves(self):
        """Test validate_complete_turn with invalid moves.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]
        moves = [(0, 3)]  # Invalid distance

        result = self.__game__.validate_complete_turn(moves)
        self.assertFalse(result)

    def test_execute_turn_valid(self):
        """Test execute_turn with valid moves.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]
        moves = [(0, 1)]

        result = self.__game__.execute_turn(moves)
        self.assertTrue(result)

    def test_execute_turn_invalid_moves(self):
        """Test execute_turn with invalid moves.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]
        moves = [(0, 3)]  # Invalid distance

        result = self.__game__.execute_turn(moves)
        self.assertFalse(result)

    # ==================== MOVE SEQUENCE TESTS ====================

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

    # ==================== COMPLEX SCENARIO TESTS ====================

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

    # def test_validate_move_distance_not_found(self):
    #     """Test validate_move when dice distance is not available.

    #     Returns:
    #         None
    #     """
    #     self.__game__.setup_initial_position()
    #     self.__game__.__current_player__ = self.__game__.__player1__
    #     self.__game__.__last_roll__ = (1, 2)
    #     self.__game__.__available_moves__ = [1, 2]  # Only 1 and 2 available
    #     # Try to make a move with distance 3 (not available)
    #     result = self.__game__.validate_move(0, 3)
    #     self.assertFalse(result)

    # def test_current_player_is_player2(self):
    #     """Test various methods when current player is player2.

    #     Returns:
    #         None
    #     """
    #     self.__game__.setup_initial_position()
    #     self.__game__.__current_player__ = self.__game__.__player2__
    #     self.__game__.__last_roll__ = (1, 2)
    #     self.__game__.__available_moves__ = [1, 2]
    #     # Test validate_move for player 2
    #     result = self.__game__.validate_move(12, 11)  # Player 2 moving backward
    #     self.assertIsInstance(result, bool)
    #     # Test make_move for player 2
    #     if result:
    #         move_result = self.__game__.make_move(12, 11)
    #         self.assertIsInstance(move_result, bool)

    # ==================== EDGE CASE TESTS ====================

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

    def test_validate_move_no_dice_rolled(self):
        """Test validate_move when no dice have been rolled.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        # Don't roll dice
        self.assertFalse(self.__game__.validate_move(0, 1))

    # ==================== AUTO PLAY TESTS ====================

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

    # ==================== UNDO FUNCTIONALITY TESTS ====================

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

    # ==================== PERFORMANCE TESTS ====================

    def test_multiple_moves_performance(self):
        """Test performance with multiple moves.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)

        # Make several moves
        for _ in range(5):
            if self.__game__.__available_moves__:
                from_point = 0
                to_point = from_point + self.__game__.__available_moves__[0]
                if to_point < 24:
                    self.__game__.make_move(from_point, to_point)

        # Verify game state is still consistent
        self.assertIsInstance(self.__game__.get_game_state(), dict)

    def test_large_move_history(self):
        """Test handling of large move history.

        Returns:
            None
        """
        self.__game__.setup_initial_position()

        # Simulate many moves
        for i in range(10):
            self.__game__.__last_roll__ = (1, 2)
            self.__game__.__available_moves__ = [1, 2]
            if i % 2 == 0:
                self.__game__.make_move(0, 1)
            else:
                self.__game__.make_move(23, 22)
            self.__game__.switch_current_player()

        # Verify history is manageable
        self.assertLessEqual(len(self.__game__.__move_history__), 10)

    # ==================== ERROR HANDLING TESTS ====================

    def test_invalid_move_handling(self):
        """Test handling of invalid moves.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)

        # Try various invalid moves
        invalid_moves = [
            (-1, 1),  # Negative from point
            (0, 25),  # Out of bounds to point
            (0, 0),  # Same point
            (10, 11),  # No piece at origin
        ]

        for from_point, to_point in invalid_moves:
            result = self.__game__.validate_move(from_point, to_point)
            self.assertFalse(
                result, f"Move ({from_point}, {to_point}) should be invalid"
            )

    def test_game_state_consistency(self):
        """Test that game state remains consistent after operations.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        # initial_state = self.__game__.get_game_state()  # Not used in this test

        # Perform some operations
        self.__game__.roll_dice()
        self.__game__.make_move(0, 1)
        self.__game__.switch_current_player()

        # Verify state is still valid
        current_state = self.__game__.get_game_state()
        self.assertIsInstance(current_state, dict)
        self.assertIn("board", current_state)
        self.assertIn("current_player", current_state)

    # ==================== INTEGRATION WITH COMPONENTS ====================

    def test_board_integration(self):
        """Test integration with Board component.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        board_state = self.__game__.__board__.get_board_state()
        self.assertIsInstance(board_state, dict)
        self.assertIn("points", board_state)

    def test_dice_integration(self):
        """Test integration with Dice component.

        Returns:
            None
        """
        roll = self.__game__.roll_dice()
        self.assertIsInstance(roll, tuple)
        self.assertEqual(len(roll), 2)
        self.assertTrue(1 <= roll[0] <= 6)
        self.assertTrue(1 <= roll[1] <= 6)

    def test_player_integration(self):
        """Test integration with Player components.

        Returns:
            None
        """
        self.__game__.setup_initial_position()

        # Test player access
        player1 = self.__game__.get_player_by_color("white")
        player2 = self.__game__.get_player_by_color("black")

        self.assertIsNotNone(player1)
        self.assertIsNotNone(player2)
        self.assertEqual(player1.__color__, "white")
        self.assertEqual(player2.__color__, "black")

    def test_checker_integration(self):
        """Test integration with Checker objects.

        Returns:
            None
        """
        self.__game__.setup_initial_position()

        # Test checker objects
        self.assertEqual(len(self.__game__.__player1_checkers__), 15)
        self.assertEqual(len(self.__game__.__player2_checkers__), 15)

        # Test checker operations
        checker = self.__game__.__player1_checkers__[0]
        self.assertIsInstance(checker, type(self.__game__.__player1_checkers__[0]))


if __name__ == "__main__":
    unittest.main()
