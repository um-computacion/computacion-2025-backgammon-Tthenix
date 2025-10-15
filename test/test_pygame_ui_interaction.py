"""
Tests for pygame UI interaction functionality.

This module tests the mouse interaction features like clicking on checkers,
selecting valid moves, and executing moves.
"""

import unittest
from unittest.mock import patch

from test.base_pygame_test import (
    BasePygameTest,
)
from pygame_ui.pygame_ui import BackgammonBoard
from core.backgammon import BackgammonGame


class TestPygameUIInteraction(BasePygameTest):
    """Test cases for pygame UI mouse interaction."""

    def setUp(self):
        """Set up test fixtures."""
        self.backgammon_board = BackgammonBoard
        self.backgammon_game = BackgammonGame

        with patch("pygame.display.set_mode"), patch("pygame.init"):
            self._init_board_and_game()

    # def test_get_point_from_coordinates_bottom_right(self):
    #     """Test getting point index from coordinates - bottom right."""
    #     # Point 0 is bottom-right corner
    #     x = (
    #         self.board.play_area_x
    #         + self.board.half_width
    #         + self.board.center_gap_width
    #         + 5 * self.board.point_width
    #         + self.board.point_width // 2
    #     )
    #     y = self.board.play_area_y + self.board.play_area_height - 10

    #     point = self.board.get_point_from_coordinates(x, y)
    #     self.assertEqual(point, 0)

    def test_get_point_from_coordinates_top_left(self):
        """Test getting point index from coordinates - top left."""
        # Point 12 is top-left first
        x = self.board.play_area_x + self.board.point_width // 2
        y = self.board.play_area_y + 10

        point = self.board.get_point_from_coordinates(x, y)
        self.assertEqual(point, 12)

    def test_get_point_from_coordinates_invalid(self):
        """Test getting point from invalid coordinates returns None."""
        # Outside board area
        point = self.board.get_point_from_coordinates(0, 0)
        self.assertIsNone(point)

    def test_get_point_from_coordinates_center_gap(self):
        """Test click in center gap returns None."""
        # Center gap area
        x = (
            self.board.play_area_x
            + self.board.half_width
            + self.board.center_gap_width // 2
        )
        y = self.board.play_area_y + self.board.play_area_height // 2

        point = self.board.get_point_from_coordinates(x, y)
        self.assertIsNone(point)

    def test_can_select_checker_own_piece(self):
        """Test can select own checker."""
        # Player 1's turn, point 0 has player 1 checkers
        self.game.current_player = self.game.player1
        self.game.roll_dice()  # Need dice to make moves

        result = self.board.can_select_checker(0)
        self.assertTrue(result)

    def test_cannot_select_checker_opponent_piece(self):
        """Test cannot select opponent's checker."""
        # Player 1's turn, point 23 has player 2 checkers
        self.game.current_player = self.game.player1
        self.game.roll_dice()

        result = self.board.can_select_checker(23)
        self.assertFalse(result)

    def test_cannot_select_checker_empty_point(self):
        """Test cannot select from empty point."""
        result = self.board.can_select_checker(10)  # Empty point
        self.assertFalse(result)

    def test_cannot_select_without_dice(self):
        """Test cannot select checker without rolling dice."""
        self.game.current_player = self.game.player1
        # Don't roll dice

        result = self.board.can_select_checker(0)
        self.assertFalse(result)

    def test_get_valid_destinations_with_dice(self):
        """Test getting valid destination points for a checker."""
        self.game.current_player = self.game.player1
        self.game.roll_dice()

        # Get valid destinations for point 0 (has player 1 checkers)
        destinations = self.board.get_valid_destinations(0)

        self.assertIsInstance(destinations, list)
        # Should have at least one destination if moves are available

    def test_get_valid_destinations_no_game(self):
        """Test getting valid destinations without game returns empty list."""
        self.board.game = None
        destinations = self.board.get_valid_destinations(0)
        self.assertEqual(destinations, [])

    def test_select_checker(self):
        """Test selecting a checker updates state."""
        self.game.current_player = self.game.player1
        self.game.roll_dice()

        self.board.select_checker(0)

        self.assertEqual(self.board.selected_point, 0)
        self.assertIsNotNone(self.board.valid_destinations)

    def test_select_invalid_checker_no_change(self):
        """Test selecting invalid checker doesn't change state."""
        self.game.current_player = self.game.player1
        self.game.roll_dice()

        self.board.select_checker(10)  # Empty point

        self.assertIsNone(self.board.selected_point)

    def test_deselect_checker(self):
        """Test deselecting a checker clears state."""
        self.game.current_player = self.game.player1
        self.game.roll_dice()
        self.board.select_checker(0)

        self.board.deselect_checker()

        self.assertIsNone(self.board.selected_point)
        self.assertIsNone(self.board.valid_destinations)

    def test_execute_move_valid(self):
        """Test executing a valid move."""
        self.game.current_player = self.game.player1
        die1, _ = self.game.roll_dice()

        from_point = 0
        to_point = 0 + die1  # Player 1 moves forward

        # Only if the move is valid
        if self.game.validate_move(from_point, to_point):
            result = self.board.execute_checker_move(from_point, to_point)
            self.assertTrue(result)

    def test_execute_move_invalid(self):
        """Test executing invalid move returns False."""
        self.game.current_player = self.game.player1
        self.game.roll_dice()

        # Try invalid move (too far)
        result = self.board.execute_checker_move(0, 20)
        self.assertFalse(result)

    def test_execute_move_deselects_checker(self):
        """Test that executing move deselects the checker."""
        self.game.current_player = self.game.player1
        die1, _ = self.game.roll_dice()

        from_point = 0
        to_point = 0 + die1

        self.board.select_checker(from_point)

        if self.game.validate_move(from_point, to_point):
            self.board.execute_checker_move(from_point, to_point)
            self.assertIsNone(self.board.selected_point)

    def test_handle_board_click_selects_checker(self):
        """Test clicking on valid checker selects it."""
        self.game.current_player = self.game.player1
        self.game.roll_dice()

        # Simulate click on point 0
        x = (
            self.board.play_area_x
            + self.board.half_width
            + self.board.center_gap_width
            + 5 * self.board.point_width
            + self.board.point_width // 2
        )
        y = self.board.play_area_y + self.board.play_area_height - 10

        self.board.handle_board_click(x, y)

        self.assertEqual(self.board.selected_point, 0)

    def test_handle_board_click_deselects_on_same_point(self):
        """Test clicking on selected point again deselects it."""
        self.game.current_player = self.game.player1
        self.game.roll_dice()

        self.board.select_checker(0)

        # Click on same point
        x = (
            self.board.play_area_x
            + self.board.half_width
            + self.board.center_gap_width
            + 5 * self.board.point_width
            + self.board.point_width // 2
        )
        y = self.board.play_area_y + self.board.play_area_height - 10

        self.board.handle_board_click(x, y)

        self.assertIsNone(self.board.selected_point)

    def test_handle_board_click_outside_deselects(self):
        """Test clicking outside board deselects checker."""
        self.game.current_player = self.game.player1
        self.game.roll_dice()

        self.board.select_checker(0)

        # Click outside board
        self.board.handle_board_click(0, 0)

        self.assertIsNone(self.board.selected_point)


if __name__ == "__main__":
    unittest.main()
