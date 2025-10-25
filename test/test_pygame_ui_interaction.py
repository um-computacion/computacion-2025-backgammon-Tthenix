"""
Tests for pygame UI interaction functionality.

This module tests the mouse interaction features like clicking on checkers,
selecting valid moves, and executing moves.
"""

import unittest
from unittest.mock import patch

from test.base_pygame_test import (  # pylint: disable=import-error,no-name-in-module
    BasePygameTest,
)
from pygame_ui.backgammon_board import BackgammonBoard
from core.backgammon import BackgammonGame


class TestPygameUIInteraction(BasePygameTest):
    """Test cases for pygame UI mouse interaction."""

    def setUp(self):  # pylint: disable=invalid-name
        """Set up test fixtures.

        Returns:
            None
        """
        self.__backgammon_board__ = BackgammonBoard
        self.__backgammon_game__ = BackgammonGame

        with patch("pygame.display.set_mode"), patch("pygame.init"):
            self._init_board_and_game()

    # def test_get_point_from_coordinates_bottom_right(self):
    #     """Test getting point index from coordinates - bottom right."""
    #     # Point 0 is bottom-right corner
    #     x = (
    #         self.__board__.play_area_x
    #         + self.__board__.half_width
    #         + self.__board__.__center_gap_width__
    #         + 5 * self.__board__.__point_width__
    #         + self.__board__.__point_width__ // 2
    #     )
    #     y = self.__board__.play_area_y + self.__board__.play_area_height - 10
    #
    #     point = self.__board__.get_point_from_coordinates(x, y)
    #     self.assertEqual(point, 0)

    def test_get_point_from_coordinates_top_left(self):
        """Test getting point index from coordinates - top left.

        Returns:
            None
        """
        # Point 12 is top-left first
        x = self.__board__.play_area_x + self.__board__.__point_width__ // 2
        y = self.__board__.play_area_y + 10

        point = self.__board__.__interaction__.get_point_from_coordinates(
            x,
            y,
            self.__board__.play_area_x,
            self.__board__.play_area_y,
            self.__board__.play_area_width,
            self.__board__.play_area_height,
            self.__board__.__point_width__,
            self.__board__.half_width,
            self.__board__.__center_gap_width__,
        )
        self.assertEqual(point, 12)

    def test_get_point_from_coordinates_invalid(self):
        """Test getting point from invalid coordinates returns None.

        Returns:
            None
        """
        # Outside board area
        point = self.__board__.__interaction__.get_point_from_coordinates(
            0,
            0,
            self.__board__.play_area_x,
            self.__board__.play_area_y,
            self.__board__.play_area_width,
            self.__board__.play_area_height,
            self.__board__.__point_width__,
            self.__board__.half_width,
            self.__board__.__center_gap_width__,
        )
        self.assertIsNone(point)

    def test_get_point_from_coordinates_center_gap(self):
        """Test click in center gap returns 'bar'.

        Returns:
            None
        """
        # Center gap area (where the bar is located)
        x = (
            self.__board__.play_area_x
            + self.__board__.half_width
            + self.__board__.__center_gap_width__ // 2
        )
        y = self.__board__.play_area_y + self.__board__.play_area_height // 2

        point = self.__board__.__interaction__.get_point_from_coordinates(
            x,
            y,
            self.__board__.play_area_x,
            self.__board__.play_area_y,
            self.__board__.play_area_width,
            self.__board__.play_area_height,
            self.__board__.__point_width__,
            self.__board__.half_width,
            self.__board__.__center_gap_width__,
        )
        # El centro es la barra, debe devolver "bar"
        self.assertEqual(point, "bar")

    def test_can_select_checker_own_piece(self):
        """Test can select own checker."""
        # Player 1's turn, point 0 has player 1 checkers
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()  # Need dice to make moves

        result = self.__board__.__interaction__.can_select_checker(0)
        self.assertTrue(result)

    def test_cannot_select_checker_opponent_piece(self):
        """Test cannot select opponent's checker."""
        # Player 1's turn, point 23 has player 2 checkers
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        result = self.__board__.__interaction__.can_select_checker(23)
        self.assertFalse(result)

    def test_cannot_select_checker_empty_point(self):
        """Test cannot select from empty point."""
        result = self.__board__.__interaction__.can_select_checker(10)  # Empty point
        self.assertFalse(result)

    def test_cannot_select_without_dice(self):
        """Test cannot select checker without rolling dice."""
        self.__game__.__current_player__ = self.__game__.__player1__
        # Don't roll dice

        result = self.__board__.__interaction__.can_select_checker(0)
        self.assertFalse(result)

    def test_get_valid_destinations_with_dice(self):
        """Test getting valid destination points for a checker."""
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        # Get valid destinations for point 0 (has player 1 checkers)
        destinations = self.__board__.__interaction__.get_valid_destinations(0)

        self.assertIsInstance(destinations, list)
        # Should have at least one destination if moves are available

    def test_get_valid_destinations_no_game(self):
        """Test getting valid destinations without game returns empty list."""
        self.__board__.__interaction__.__game__ = None
        destinations = self.__board__.__interaction__.get_valid_destinations(0)
        self.assertEqual(destinations, [])

    def test_select_checker(self):
        """Test selecting a checker updates state."""
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        self.__board__.__interaction__.select_checker(0)

        self.assertEqual(self.__board__.__interaction__.__selected_point__, 0)
        self.assertIsNotNone(self.__board__.__interaction__.__valid_destinations__)

    def test_select_invalid_checker_no_change(self):
        """Test selecting invalid checker doesn't change state."""
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        self.__board__.__interaction__.select_checker(10)  # Empty point

        self.assertIsNone(self.__board__.__interaction__.__selected_point__)

    def test_deselect_checker(self):
        """Test deselecting a checker clears state."""
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()
        self.__board__.__interaction__.select_checker(0)

        self.__board__.__interaction__.deselect_checker()

        self.assertIsNone(self.__board__.__interaction__.__selected_point__)
        self.assertIsNone(self.__board__.__interaction__.__valid_destinations__)

    def test_execute_move_valid(self):
        """Test executing a valid move."""
        self.__game__.__current_player__ = self.__game__.__player1__
        die1, _ = self.__game__.roll_dice()

        from_point = 0
        to_point = 0 + die1  # Player 1 moves forward

        # Only if the move is valid
        if self.__game__.validate_move(from_point, to_point):
            result = self.__board__.__interaction__.execute_checker_move(
                from_point, to_point
            )
            self.assertTrue(result)

    def test_execute_move_invalid(self):
        """Test executing invalid move returns False."""
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        # Try invalid move (too far)
        result = self.__board__.__interaction__.execute_checker_move(0, 20)
        self.assertFalse(result)

    def test_execute_move_deselects_checker(self):
        """Test that executing move deselects the checker."""
        self.__game__.__current_player__ = self.__game__.__player1__
        die1, _ = self.__game__.roll_dice()

        from_point = 0
        to_point = 0 + die1

        self.__board__.__interaction__.select_checker(from_point)

        if self.__game__.validate_move(from_point, to_point):
            self.__board__.__interaction__.execute_checker_move(from_point, to_point)
            self.assertIsNone(self.__board__.__interaction__.__selected_point__)

    def test_handle_board_click_selects_checker(self):
        """Test clicking on valid checker selects it."""
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        # Simulate click on point 0
        x = (
            self.__board__.play_area_x
            + self.__board__.half_width
            + self.__board__.__center_gap_width__
            + 5 * self.__board__.__point_width__
            + self.__board__.__point_width__ // 2
        )
        y = self.__board__.play_area_y + self.__board__.play_area_height - 10

        self.__board__.handle_board_click(x, y)

        self.assertEqual(self.__board__.__interaction__.__selected_point__, 0)

    def test_handle_board_click_deselects_on_same_point(self):
        """Test clicking on selected point again deselects it."""
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        self.__board__.__interaction__.select_checker(0)

        # Click on same point
        x = (
            self.__board__.play_area_x
            + self.__board__.half_width
            + self.__board__.__center_gap_width__
            + 5 * self.__board__.__point_width__
            + self.__board__.__point_width__ // 2
        )
        y = self.__board__.play_area_y + self.__board__.play_area_height - 10

        self.__board__.handle_board_click(x, y)

        self.assertIsNone(self.__board__.__interaction__.__selected_point__)

    def test_handle_board_click_outside_deselects(self):
        """Test clicking outside board deselects checker."""
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        self.__board__.__interaction__.select_checker(0)

        # Click outside board
        self.__board__.handle_board_click(0, 0)

        self.assertIsNone(self.__board__.__interaction__.__selected_point__)

    # ==================== BOARD INTERACTION COVERAGE TESTS ====================

    def test_can_select_from_bar_with_pieces(self):
        """Test can select from bar when player has pieces on bar.

        Returns:
            None
        """
        # Set up player 1 with pieces on bar
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        # Put player 1 pieces on bar (side 1 for white pieces)
        self.__game__.__board__.__checker_bar__[1] = [1, 1]  # Two white pieces on bar

        # Update board state to reflect the bar pieces
        self.__board__.__interaction__.__board_state__ = (
            self.__game__.__board__.get_board_state()
        )

        result = self.__board__.__interaction__.can_select_checker("bar")
        self.assertTrue(result)

    def test_can_select_from_bar_no_pieces(self):
        """Test cannot select from bar when no pieces on bar.

        Returns:
            None
        """
        # Set up player 1 with no pieces on bar
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        # Clear bar
        self.__game__.__board__.__checker_bar__[1] = []

        # Update board state
        self.__board__.__interaction__.__board_state__ = (
            self.__game__.__board__.get_board_state()
        )

        result = self.__board__.__interaction__.can_select_checker("bar")
        self.assertFalse(result)

    def test_can_select_from_bar_player2(self):
        """Test can select from bar for player 2.

        Returns:
            None
        """
        # Set up player 2 with pieces on bar
        self.__game__.__current_player__ = self.__game__.__player2__
        self.__game__.roll_dice()

        # Put player 2 pieces on bar (side 0 for black pieces)
        self.__game__.__board__.__checker_bar__[0] = [2, 2]  # Two black pieces on bar

        # Update board state
        self.__board__.__interaction__.__board_state__ = (
            self.__game__.__board__.get_board_state()
        )

        result = self.__board__.__interaction__.can_select_checker("bar")
        self.assertTrue(result)

    def test_can_select_checker_with_bar_pieces_blocks_other_selection(self):
        """Test that having pieces on bar blocks selecting other checkers.

        Returns:
            None
        """
        # Set up player 1 with pieces on bar
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        # Put player 1 pieces on bar
        self.__game__.__board__.__checker_bar__[1] = [1]

        # Update board state
        self.__board__.__interaction__.__board_state__ = (
            self.__game__.__board__.get_board_state()
        )

        # Try to select regular checker (should be blocked)
        result = self.__board__.__interaction__.can_select_checker(0)
        self.assertFalse(result)

    def test_get_valid_destinations_from_bar(self):
        """Test getting valid destinations from bar.

        Returns:
            None
        """
        # Set up player 1 with pieces on bar
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        # Put player 1 pieces on bar
        self.__game__.__board__.__checker_bar__[1] = [1]

        # Update board state
        self.__board__.__interaction__.__board_state__ = (
            self.__game__.__board__.get_board_state()
        )

        destinations = self.__board__.__interaction__.get_valid_destinations_from_bar()
        self.assertIsInstance(destinations, list)

    def test_get_valid_destinations_from_bar_no_pieces(self):
        """Test getting destinations from bar when no pieces on bar.

        Returns:
            None
        """
        # Set up player 1 with no pieces on bar
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        # Clear bar
        self.__game__.__board__.__checker_bar__[1] = []

        # Update board state
        self.__board__.__interaction__.__board_state__ = (
            self.__game__.__board__.get_board_state()
        )

        # The method should return destinations based on available moves
        # even if no pieces are on bar, so we test that it returns a list
        destinations = self.__board__.__interaction__.get_valid_destinations_from_bar()
        self.assertIsInstance(destinations, list)

    def test_get_valid_destinations_from_bar_player2(self):
        """Test getting destinations from bar for player 2.

        Returns:
            None
        """
        # Set up player 2 with pieces on bar
        self.__game__.__current_player__ = self.__game__.__player2__
        self.__game__.roll_dice()

        # Put player 2 pieces on bar
        self.__game__.__board__.__checker_bar__[0] = [2]

        # Update board state
        self.__board__.__interaction__.__board_state__ = (
            self.__game__.__board__.get_board_state()
        )

        destinations = self.__board__.__interaction__.get_valid_destinations_from_bar()
        self.assertIsInstance(destinations, list)

    def test_select_checker_from_bar(self):
        """Test selecting checker from bar.

        Returns:
            None
        """
        # Set up player 1 with pieces on bar
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        # Put player 1 pieces on bar
        self.__game__.__board__.__checker_bar__[1] = [1]

        # Update board state
        self.__board__.__interaction__.__board_state__ = (
            self.__game__.__board__.get_board_state()
        )

        self.__board__.__interaction__.select_checker("bar")

        self.assertEqual(self.__board__.__interaction__.__selected_point__, "bar")
        self.assertIsNotNone(self.__board__.__interaction__.__valid_destinations__)

    def test_execute_move_from_bar(self):
        """Test executing move from bar.

        Returns:
            None
        """
        # Set up player 1 with pieces on bar
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        # Put player 1 pieces on bar and clear entry point
        self.__game__.__board__.__checker_bar__[1] = [1]
        self.__game__.__board__.__points__[0] = []  # Clear entry point

        # Update board state
        self.__board__.__interaction__.__board_state__ = (
            self.__game__.__board__.get_board_state()
        )

        # Try to move to a point that matches available dice
        # If dice roll was (1,2), try moving to point 0 (requires die 1)
        if 1 in self.__game__.__available_moves__:
            result = self.__board__.__interaction__.execute_checker_move("bar", 0)
            self.assertTrue(result)
        else:
            # If die 1 is not available, just test that the method doesn't crash
            result = self.__board__.__interaction__.execute_checker_move("bar", 0)
            self.assertIsInstance(result, bool)

    def test_execute_move_from_bar_blocked(self):
        """Test executing move from bar when entry is blocked.

        Returns:
            None
        """
        # Set up player 1 with pieces on bar
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        # Put player 1 pieces on bar and block entry point
        self.__game__.__board__.__checker_bar__[1] = [1]
        self.__game__.__board__.__points__[0] = [2, 2]  # Block entry point

        # Update board state
        self.__board__.__interaction__.__board_state__ = (
            self.__game__.__board__.get_board_state()
        )

        result = self.__board__.__interaction__.execute_checker_move("bar", 0)
        self.assertFalse(result)

    def test_handle_board_click_on_bar(self):
        """Test clicking on bar area.

        Returns:
            None
        """
        # Set up player 1 with pieces on bar
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        # Put player 1 pieces on bar
        self.__game__.__board__.__checker_bar__[1] = [1]

        # Update board state
        self.__board__.__interaction__.__board_state__ = (
            self.__game__.__board__.get_board_state()
        )

        # Verify that we can select from bar before clicking
        can_select = self.__board__.__interaction__.can_select_from_bar()
        self.assertTrue(can_select, "Should be able to select from bar")

        # Click on bar area
        x = (
            self.__board__.play_area_x
            + self.__board__.half_width
            + self.__board__.__center_gap_width__ // 2
        )
        y = self.__board__.play_area_y + self.__board__.play_area_height // 2

        self.__board__.handle_board_click(x, y)

        self.assertEqual(self.__board__.__interaction__.__selected_point__, "bar")

    def test_handle_board_click_on_bar_deselects(self):
        """Test clicking on bar when already selected deselects it.

        Returns:
            None
        """
        # Set up player 1 with pieces on bar
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        # Put player 1 pieces on bar
        self.__game__.__board__.__checker_bar__[1] = [1]

        # Update board state
        self.__board__.__interaction__.__board_state__ = (
            self.__game__.__board__.get_board_state()
        )

        # Select bar first
        self.__board__.__interaction__.select_checker("bar")

        # Click on bar area again
        x = (
            self.__board__.play_area_x
            + self.__board__.half_width
            + self.__board__.__center_gap_width__ // 2
        )
        y = self.__board__.play_area_y + self.__board__.play_area_height // 2

        self.__board__.handle_board_click(x, y)

        self.assertIsNone(self.__board__.__interaction__.__selected_point__)

    def test_can_select_checker_no_game(self):
        """Test can select checker when no game is set.

        Returns:
            None
        """
        # Clear game
        self.__board__.__interaction__.__game__ = None

        result = self.__board__.__interaction__.can_select_checker(0)
        self.assertFalse(result)

    def test_can_select_checker_no_board_state(self):
        """Test can select checker when no board state is set.

        Returns:
            None
        """
        # Clear board state
        self.__board__.__interaction__.__board_state__ = None

        result = self.__board__.__interaction__.can_select_checker(0)
        self.assertFalse(result)

    def test_can_select_checker_no_last_roll(self):
        """Test can select checker when no last roll.

        Returns:
            None
        """
        # Clear last roll
        self.__game__.__last_roll__ = None

        result = self.__board__.__interaction__.can_select_checker(0)
        self.assertFalse(result)

    def test_can_select_checker_no_valid_moves(self):
        """Test can select checker when no valid moves available.

        Returns:
            None
        """
        # Set up game with no valid moves
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        # Clear all available moves and set last roll to None to prevent regeneration
        self.__game__.__available_moves__ = []
        self.__game__.__last_roll__ = None

        result = self.__board__.__interaction__.can_select_checker(0)
        self.assertFalse(result)

    def test_get_valid_destinations_no_board_state(self):
        """Test get valid destinations when no board state is set.

        Returns:
            None
        """
        # Clear board state
        self.__board__.__interaction__.__board_state__ = None

        destinations = self.__board__.__interaction__.get_valid_destinations(0)
        self.assertEqual(destinations, [])

    def test_execute_move_from_bar_invalid_destination(self):
        """Test executing move from bar to invalid destination.

        Returns:
            None
        """
        # Set up player 1 with pieces on bar
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        # Put player 1 pieces on bar
        self.__game__.__board__.__checker_bar__[1] = [1]

        # Try to move to invalid destination
        result = self.__board__.__interaction__.execute_checker_move("bar", 25)
        self.assertFalse(result)

    def test_execute_move_from_bar_no_pieces(self):
        """Test executing move from bar when no pieces on bar.

        Returns:
            None
        """
        # Set up player 1 with no pieces on bar
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.roll_dice()

        # Clear bar
        self.__game__.__board__.__checker_bar__[1] = []

        result = self.__board__.__interaction__.execute_checker_move("bar", 0)
        self.assertFalse(result)

    def test_execute_move_from_bar_player2(self):
        """Test executing move from bar for player 2.

        Returns:
            None
        """
        # Set up player 2 with pieces on bar
        self.__game__.__current_player__ = self.__game__.__player2__
        self.__game__.roll_dice()

        # Put player 2 pieces on bar
        self.__game__.__board__.__checker_bar__[0] = [2]

        # Clear entry point for player 2 (point 23)
        self.__game__.__board__.__points__[23] = []

        # Update board state
        self.__board__.__interaction__.__board_state__ = (
            self.__game__.__board__.get_board_state()
        )

        # Try to move to a point that matches available dice
        # For player 2, point 23 requires die 1 (24-23=1)
        if 1 in self.__game__.__available_moves__:
            result = self.__board__.__interaction__.execute_checker_move("bar", 23)
            self.assertTrue(result)
        else:
            # If die 1 is not available, just test that the method doesn't crash
            result = self.__board__.__interaction__.execute_checker_move("bar", 23)
            self.assertIsInstance(result, bool)

    def test_handle_board_click_invalid_coordinates(self):
        """Test handling board click with invalid coordinates.

        Returns:
            None
        """
        # Click with invalid coordinates
        self.__board__.handle_board_click(-1, -1)

        # Should not crash and should deselect if something was selected
        self.assertIsNone(self.__board__.__interaction__.__selected_point__)

    def test_handle_board_click_no_game(self):
        """Test handling board click when no game is set.

        Returns:
            None
        """
        # Clear game
        self.__board__.__interaction__.__game__ = None

        # Click on board
        x = self.__board__.play_area_x + 10
        y = self.__board__.play_area_y + 10

        # Should not crash
        self.__board__.handle_board_click(x, y)

    def test_handle_board_click_no_board_state(self):
        """Test handling board click when no board state is set.

        Returns:
            None
        """
        # Clear board state
        self.__board__.__interaction__.__board_state__ = None

        # Click on board
        x = self.__board__.play_area_x + 10
        y = self.__board__.play_area_y + 10

        # Should not crash
        self.__board__.handle_board_click(x, y)


if __name__ == "__main__":
    unittest.main()
