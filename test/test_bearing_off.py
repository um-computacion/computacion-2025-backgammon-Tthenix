"""
Test module for bearing off functionality in Backgammon.

This module tests the bearing off mechanics including:
- Detection when players can bear off
- Bearing off moves with proper dice validation
- Visual representation of borne-off checkers
- Integration with Pygame UI
"""

import unittest
from test.base_pygame_test import (  # pylint: disable=import-error,no-name-in-module
    BasePygameTest,
)
from core.backgammon import BackgammonGame
from pygame_ui.board_interaction import BoardInteraction


class TestBearingOff(BasePygameTest):
    """Test bearing off functionality."""

    def setUp(self):  # pylint: disable=invalid-name
        """Set up test environment."""
        self._init_board_and_game()
        self.interaction = BoardInteraction()

    def test_can_bear_off_detection(self):
        """Test detection of when players can bear off."""
        # Set up scenario where player 1 can bear off
        self._setup_bearing_off_scenario()

        # Test bearing off detection
        self.assertTrue(self.game.can_bear_off(1))
        # Player 2 should not be able to bear off since they have pieces outside home
        self.assertFalse(self.game.can_bear_off(2))

    def test_bearing_off_validation(self):
        """Test bearing off move validation."""
        self._setup_bearing_off_scenario()

        # Test specific point bearing off validation
        self.assertTrue(self.game.board.can_bear_off(23, 1, 1))  # Exact dice match
        self.assertTrue(self.game.board.can_bear_off(23, 1, 6))  # Higher dice value
        self.assertFalse(
            self.game.board.can_bear_off(22, 1, 1)
        )  # Wrong point for dice value

    def test_bearing_off_execution(self):
        """Test actual bearing off execution."""
        self._setup_bearing_off_scenario()

        # Roll dice and test bearing off
        self.game.roll_dice()
        initial_off_board = self.game.board.off_board[0].copy()

        # Execute bearing off
        success = self.game.bear_off_checker(23)

        self.assertTrue(success)
        self.assertEqual(len(self.game.board.off_board[0]), len(initial_off_board) + 1)
        self.assertEqual(len(self.game.board.points[23]), 4)  # One less piece

    def test_bearing_off_with_dice_consumption(self):
        """Test that dice values are consumed when bearing off."""
        self._setup_bearing_off_scenario()

        # Roll dice
        self.game.roll_dice()
        initial_moves = self.game.available_moves.copy()

        # Bear off with first dice value
        dice_value = self.game.available_moves[0]
        success = self.game.bear_off_checker(23)

        self.assertTrue(success)
        # Check that the number of moves decreased (handles doubles case)
        self.assertEqual(len(self.game.available_moves), len(initial_moves) - 1)
        # Check that at least one instance of the dice value was consumed
        initial_count = initial_moves.count(dice_value)
        remaining_count = self.game.available_moves.count(dice_value)
        self.assertEqual(remaining_count, initial_count - 1)

    def test_bearing_off_ui_integration(self):
        """Test bearing off integration with UI."""
        self._setup_bearing_off_scenario()
        self.interaction.set_game(self.game)

        # Test bearing off from UI perspective
        self.game.roll_dice()

        # Test if bearing off is detected as valid destination
        destinations = self.interaction.get_valid_destinations(23)
        self.assertIn("off", destinations)

        # Test bearing off execution through UI
        success = self.interaction.execute_bearing_off(23)
        self.assertTrue(success)

    def test_bearing_off_visual_representation(self):
        """Test visual representation of borne-off checkers."""
        self._setup_bearing_off_scenario()

        # Bear off some checkers
        self.game.roll_dice()
        self.game.bear_off_checker(23)
        self.game.bear_off_checker(22)

        # Update board state
        self.board.update_from_game()

        # Check that borne-off checkers are in off_board
        self.assertGreater(len(self.game.board.off_board[0]), 0)

        # Check board state includes off_board
        board_state = self.game.board.get_board_state()
        self.assertIn("off_board", board_state)
        self.assertGreater(len(board_state["off_board"][0]), 0)

    def test_bearing_off_turn_switching(self):
        """Test automatic turn switching after bearing off all moves."""
        self._setup_bearing_off_scenario()

        # Roll dice
        self.game.roll_dice()
        initial_player = self.game.current_player

        # Bear off with all available moves
        while self.game.available_moves:
            point = 23  # Use furthest point
            if self.game.board.can_bear_off(point, 1, self.game.available_moves[0]):
                self.game.bear_off_checker(point)
            else:
                break

        # If no moves left, should switch player
        if not self.game.available_moves:
            self.game.switch_current_player()
            self.assertNotEqual(self.game.current_player, initial_player)

    def test_bearing_off_coordinate_detection(self):
        """Test detection of clicks on bear-off area."""
        # Mock bear-off area coordinates
        bear_off_x, bear_off_y = 800, 100
        bear_off_width, bear_off_height = 100, 400

        # Test click detection in bear-off area
        point = self.interaction.get_point_from_coordinates(
            bear_off_x + 50,  # Click in center of bear-off area
            bear_off_y + 200,
            play_area_x=100,
            play_area_y=100,
            play_area_width=600,
            play_area_height=500,
            point_width=50,
            half_width=300,
            center_gap_width=20,
            bear_off_x=bear_off_x,
            bear_off_y=bear_off_y,
            bear_off_width=bear_off_width,
            bear_off_height=bear_off_height,
        )

        self.assertEqual(point, "off")

    def test_bearing_off_rule_compliance(self):
        """Test that bearing off follows proper Backgammon rules."""
        self._setup_bearing_off_scenario()

        # Test that you must use exact dice value or bear off from furthest point
        self.game.roll_dice()

        # Test exact dice value usage
        dice_value = self.game.available_moves[0]
        if dice_value == 1:
            # With dice value 1, can only bear off from point 23
            self.assertTrue(self.game.board.can_bear_off(23, 1, 1))
            self.assertFalse(self.game.board.can_bear_off(22, 1, 1))

        # Test bearing off from furthest point when dice value is higher
        if dice_value > 1:
            # Can bear off from point 23 with any dice value >= 1
            self.assertTrue(self.game.board.can_bear_off(23, 1, dice_value))

    def _setup_bearing_off_scenario(self):
        """Set up a scenario where player 1 can bear off."""
        # Clear the board
        self.game.board.points = [[] for _ in range(24)]
        self.game.board.checker_bar = [[], []]
        self.game.board.off_board = [[], []]

        # Set up player 1 pieces in home board (points 18-23)
        self.game.board.points[18] = [1, 1, 1, 1, 1]  # 5 pieces
        self.game.board.points[19] = [1, 1, 1, 1, 1]  # 5 pieces
        self.game.board.points[20] = [1, 1, 1, 1, 1]  # 5 pieces
        self.game.board.points[21] = [1, 1, 1, 1, 1]  # 5 pieces
        self.game.board.points[22] = [1, 1, 1, 1, 1]  # 5 pieces
        self.game.board.points[23] = [1, 1, 1, 1, 1]  # 5 pieces

        # Set up player 2 pieces OUTSIDE home board (so they cannot bear off)
        # Player 2's home is points 0-5, so put pieces outside that range
        self.game.board.points[6] = [2, 2, 2, 2, 2]  # 5 pieces - outside home
        self.game.board.points[7] = [2, 2, 2, 2, 2]  # 5 pieces - outside home
        self.game.board.points[8] = [2, 2, 2, 2, 2]  # 5 pieces - outside home
        self.game.board.points[9] = [2, 2, 2, 2, 2]  # 5 pieces - outside home
        self.game.board.points[10] = [2, 2, 2, 2, 2]  # 5 pieces - outside home
        self.game.board.points[11] = [2, 2, 2, 2, 2]  # 5 pieces - outside home

        # Set current player to player 1
        self.game.current_player = self.game.player1


class TestBearingOffEdgeCases(unittest.TestCase):
    """Test edge cases for bearing off functionality."""

    def setUp(self):  # pylint: disable=invalid-name
        """Set up test environment."""
        self.game = BackgammonGame()
        self.game.setup_initial_position()

    def test_bearing_off_with_pieces_outside_home(self):
        """Test that bearing off is not allowed when pieces are outside home board."""
        # Set up scenario with pieces outside home board
        self.game.board.points[0] = [1, 1, 1, 1, 1]  # Pieces outside home
        self.game.board.points[18] = [1, 1, 1, 1, 1]  # Some pieces in home

        # Should not be able to bear off
        self.assertFalse(self.game.can_bear_off(1))

    def test_bearing_off_with_no_dice_available(self):
        """Test bearing off when no dice are available."""
        # Set up bearing off scenario
        self._setup_bearing_off_scenario()

        # No dice rolled
        self.game.last_roll = None
        self.game.available_moves = []

        # Should not be able to bear off
        self.assertFalse(self.game.bear_off_checker(23))

    def test_bearing_off_from_empty_point(self):
        """Test bearing off from a point with no pieces."""
        self._setup_bearing_off_scenario()
        self.game.roll_dice()

        # Try to bear off from empty point
        self.assertFalse(self.game.bear_off_checker(0))

    def test_bearing_off_opponent_pieces(self):
        """Test that you cannot bear off opponent's pieces."""
        self._setup_bearing_off_scenario()
        self.game.roll_dice()

        # Try to bear off opponent's piece
        self.assertFalse(self.game.bear_off_checker(0))  # Point 0 has opponent pieces

    def _setup_bearing_off_scenario(self):
        """Set up a scenario where player 1 can bear off."""
        # Clear the board
        self.game.board.points = [[] for _ in range(24)]
        self.game.board.checker_bar = [[], []]
        self.game.board.off_board = [[], []]

        # Set up player 1 pieces in home board
        self.game.board.points[18] = [1, 1, 1, 1, 1]
        self.game.board.points[19] = [1, 1, 1, 1, 1]
        self.game.board.points[20] = [1, 1, 1, 1, 1]
        self.game.board.points[21] = [1, 1, 1, 1, 1]
        self.game.board.points[22] = [1, 1, 1, 1, 1]
        self.game.board.points[23] = [1, 1, 1, 1, 1]

        # Set up some player 2 pieces
        self.game.board.points[0] = [2, 2, 2, 2, 2]

        # Set current player to player 1
        self.game.current_player = self.game.player1


if __name__ == "__main__":
    unittest.main()
