"""
Board Interaction Module

This module handles mouse interactions and coordinate conversions
for the backgammon board.
"""

from typing import Optional, List

from core.backgammon import BackgammonGame


class BoardInteraction:
    """Handles mouse interactions and game state management for the board."""

    def __init__(self) -> None:
        """Initialize the board interaction handler."""
        self.selected_point: Optional[int] = None
        self.valid_destinations: Optional[List[int]] = None
        self.game: Optional[BackgammonGame] = None
        self.board_state: Optional[dict] = None

    def set_game(self, game: BackgammonGame) -> None:
        """
        Set the game instance to use for game logic.

        Args:
            game: BackgammonGame instance
        """
        self.game = game

    def set_board_state(self, board_state: dict) -> None:
        """
        Set the current board state.

        Args:
            board_state: Dictionary containing board state
        """
        self.board_state = board_state

    def get_point_from_coordinates(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        x: int,
        y: int,
        play_area_x: int,
        play_area_y: int,
        play_area_width: int,
        play_area_height: int,
        point_width: int,
        half_width: int,
        center_gap_width: int,
    ) -> Optional[int]:
        """
        Convert screen coordinates to board point index.

        Args:
            x: X coordinate on screen
            y: Y coordinate on screen
            play_area_x: X position of play area
            play_area_y: Y position of play area
            play_area_width: Width of play area
            play_area_height: Height of play area
            point_width: Width of each point
            half_width: Width of half board
            center_gap_width: Width of center gap

        Returns:
            Point index (0-23) or None if not on a valid point
        """
        # Check if click is within play area
        if not (
            play_area_x <= x <= play_area_x + play_area_width
            and play_area_y <= y <= play_area_y + play_area_height
        ):
            return None

        # Determine if click is in top or bottom half
        mid_y = play_area_y + play_area_height // 2
        is_top_half = y < mid_y

        # Calculate relative x position
        rel_x = x - play_area_x

        # Check if in center gap
        if half_width <= rel_x <= half_width + center_gap_width:
            return None  # Click in center gap (bar area)

        # Determine which side (left or right of center gap)
        if rel_x < half_width:
            # Left side
            point_index_in_quadrant = int(rel_x / point_width)
            if is_top_half:
                # Top-left: points 12-17
                return 12 + point_index_in_quadrant
            # Bottom-left: points 11-6
            return 11 - point_index_in_quadrant

        # Right side
        rel_x_right = rel_x - half_width - center_gap_width
        point_index_in_quadrant = int(rel_x_right / point_width)
        if is_top_half:
            # Top-right: points 18-23
            return 18 + point_index_in_quadrant
        # Bottom-right: points 5-0
        return 5 - point_index_in_quadrant

    def can_select_checker(self, point: int) -> bool:
        """
        Check if a checker at the given point can be selected.

        Args:
            point: Point index to check

        Returns:
            True if checker can be selected, False otherwise
        """
        if not self.game or not self.board_state:
            return False

        # Must have dice rolled
        if not self.game.last_roll:
            return False

        # Check if point has checkers
        if point >= len(self.board_state["points"]):
            return False

        checkers = self.board_state["points"][point]
        if not checkers:
            return False

        # Check if checker belongs to current player
        current_player_num = 1 if self.game.current_player == self.game.player1 else 2
        return checkers[0] == current_player_num

    def get_valid_destinations(self, from_point: int) -> List[int]:
        """
        Get list of valid destination points for a checker.

        Args:
            from_point: Source point index

        Returns:
            List of valid destination point indices
        """
        if not self.game:
            return []

        # Use core game logic to get possible destinations
        return self.game.get_possible_destinations(from_point)

    def select_checker(self, point: int) -> None:
        """
        Select a checker at the given point.

        Args:
            point: Point index to select
        """
        if self.can_select_checker(point):
            self.selected_point = point
            self.valid_destinations = self.get_valid_destinations(point)

    def deselect_checker(self) -> None:
        """Deselect the currently selected checker."""
        self.selected_point = None
        self.valid_destinations = None

    def execute_checker_move(self, from_point: int, to_point: int) -> bool:
        """
        Execute a checker move from one point to another.

        Args:
            from_point: Source point index
            to_point: Destination point index

        Returns:
            True if move was successful, False otherwise
        """
        if not self.game:
            return False

        # Validate and execute the move
        if self.game.validate_move(from_point, to_point):
            success = self.game.make_move(from_point, to_point)
            if success:
                # Deseleccionar ficha
                self.deselect_checker()
                # Si no quedan movimientos disponibles, finalizar turno automáticamente
                if not self.game.available_moves:
                    # Reiniciar dados y movimientos y cambiar turno
                    self.game.last_roll = None
                    self.game.available_moves = []
                    self.game.switch_current_player()
                return True

        return False

    def handle_board_click(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        x: int,
        y: int,
        play_area_x: int,
        play_area_y: int,
        play_area_width: int,
        play_area_height: int,
        point_width: int,
        half_width: int,
        center_gap_width: int,
    ) -> None:
        """
        Handle a mouse click on the board.

        Args:
            x: X coordinate of click
            y: Y coordinate of click
            play_area_x: X position of play area
            play_area_y: Y position of play area
            play_area_width: Width of play area
            play_area_height: Height of play area
            point_width: Width of each point
            half_width: Width of half board
            center_gap_width: Width of center gap
        """
        point = self.get_point_from_coordinates(
            x,
            y,
            play_area_x,
            play_area_y,
            play_area_width,
            play_area_height,
            point_width,
            half_width,
            center_gap_width,
        )
        if point is None:
            # Click outside valid area - deselect
            self.deselect_checker()
            return

        # If no checker selected, try to select one
        if self.selected_point is None:
            self.select_checker(point)
        else:
            # If clicked on selected point again, deselect
            if point == self.selected_point:
                self.deselect_checker()
            # If clicked on valid destination, execute move
            elif self.valid_destinations and point in self.valid_destinations:
                self.execute_checker_move(self.selected_point, point)
            # Otherwise, try to select new checker
            else:
                self.deselect_checker()
                self.select_checker(point)
