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
        bear_off_x: int = None,
        bear_off_y: int = None,
        bear_off_width: int = None,
        bear_off_height: int = None,
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
        # Check if click is in bear-off area first
        if (
            bear_off_x is not None
            and bear_off_y is not None
            and bear_off_width is not None
            and bear_off_height is not None
        ):
            if (
                bear_off_x <= x <= bear_off_x + bear_off_width
                and bear_off_y <= y <= bear_off_y + bear_off_height
            ):
                return "off"  # Click in bear-off area

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

        # Check if in center gap (bar area)
        if half_width <= rel_x <= half_width + center_gap_width:
            return "bar"  # Click in center gap (bar area)

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

    def can_select_checker(self, point) -> bool:
        """
        Check if a checker at the given point can be selected.

        Args:
            point: Point index to check, or "bar" for bar selection

        Returns:
            True if checker can be selected, False otherwise
        """
        # Early validation checks
        if not self._can_select_checker_basic_validation():
            return False

        # Handle bar selection
        if point == "bar":
            return self.can_select_from_bar()

        # Check if player has pieces on bar (prevents moving other pieces)
        if self._player_has_pieces_on_bar():
            return False

        # Validate point selection
        return self._can_select_point_checker(point)

    def _can_select_checker_basic_validation(self) -> bool:
        """Check basic validation for checker selection."""
        if not self.game or not self.board_state:
            return False
        if not self.game.last_roll:
            return False
        return self.game.has_valid_moves()

    def _player_has_pieces_on_bar(self) -> bool:
        """Check if current player has pieces on bar."""
        current_player_num = 1 if self.game.current_player == self.game.player1 else 2
        player_bar_index = 1 if current_player_num == 1 else 0

        if "bar" not in self.board_state:
            return False

        player_pieces_on_bar = [
            piece
            for piece in self.board_state["bar"][player_bar_index]
            if piece == current_player_num
        ]
        return len(player_pieces_on_bar) > 0

    def _can_select_point_checker(self, point) -> bool:
        """Check if a point checker can be selected."""
        # Handle special cases like "off" or "bar"
        if not isinstance(point, int):
            return False

        if point >= len(self.board_state["points"]):
            return False

        checkers = self.board_state["points"][point]
        if not checkers:
            return False

        current_player_num = 1 if self.game.current_player == self.game.player1 else 2
        return checkers[0] == current_player_num

    def can_select_from_bar(self) -> bool:
        """
        Check if a checker can be selected from the bar.

        Returns:
            True if current player has their own pieces on opponent's side, False otherwise
        """
        if not self.game or not self.board_state:
            return False

        current_player_num = 1 if self.game.current_player == self.game.player1 else 2

        # Check if current player has THEIR pieces on opponent's side
        # Fichas blancas (1) capturadas están en el lado negro (index 1)
        # Fichas negras (2) capturadas están en el lado blanco (index 0)
        if "bar" not in self.board_state:
            return False

        if current_player_num == 1:
            # Jugador blanco verifica el lado negro (index 1) para sus fichas blancas
            bar_pieces = self.board_state["bar"][1]
            return any(piece == 1 for piece in bar_pieces)

        # Jugador negro verifica el lado blanco (index 0) para sus fichas negras
        bar_pieces = self.board_state["bar"][0]
        return any(piece == 2 for piece in bar_pieces)

    def get_valid_destinations_from_bar(self) -> List[int]:
        """
        Get valid destinations for checkers entering from bar.

        Returns:
            List of valid destination point indices
        """
        if not self.game:
            return []

        destinations = []
        current_player_num = 1 if self.game.current_player == self.game.player1 else 2

        # Check each available dice value

        for dice_value in self.game.available_moves:
            if current_player_num == 1:

                entry_point = dice_value - 1
            else:

                entry_point = 24 - dice_value

            # Check if entry point is valid and not blocked
            if 0 <= entry_point < 24:
                destination_pieces = self.game.board.points[entry_point]
                if (
                    len(destination_pieces) == 0
                    or len(destination_pieces) < 2
                    or destination_pieces[0] == current_player_num
                ):
                    destinations.append(entry_point)

        return destinations

    def get_valid_destinations(self, from_point) -> List:
        """
        Get list of valid destination points for a checker.

        Args:
            from_point: Source point index or "bar"

        Returns:
            List of valid destination point indices or "off" for bearing off
        """
        if not self.game:
            return []

        # Handle bar destinations
        if from_point == "bar":
            return self.get_valid_destinations_from_bar()

        # Get regular destinations
        destinations = self.game.get_possible_destinations(from_point)

        # Check if bearing off is possible
        if self._can_bear_off_from_point(from_point):
            destinations.append("off")

        return destinations

    def _can_bear_off_from_point(self, from_point: int) -> bool:
        """
        Check if a checker can be borne off from a specific point.

        Args:
            from_point: Source point index

        Returns:
            True if bearing off is possible, False otherwise
        """
        if not self.game:
            return False

        current_player_num = 1 if self.game.current_player == self.game.player1 else 2

        # Check if player can bear off at all
        if not self.game.can_bear_off(current_player_num):
            return False

        # Check if the specific point can bear off with available dice
        for dice_value in self.game.available_moves:
            if self.game.board.can_bear_off(from_point, current_player_num, dice_value):
                return True

        return False

    def select_checker(self, point) -> None:
        """
        Select a checker at the given point.

        Args:
            point: Point index to select or "bar"
        """
        if self.can_select_checker(point):
            self.selected_point = point
            self.valid_destinations = self.get_valid_destinations(point)

    def deselect_checker(self) -> None:
        """Deselect the currently selected checker."""
        self.selected_point = None
        self.valid_destinations = None

    def execute_checker_move(self, from_point, to_point) -> bool:
        """
        Execute a checker move from one point to another.

        Args:
            from_point: Source point index or "bar"
            to_point: Destination point index or "off" for bearing off

        Returns:
            True if move was successful, False otherwise
        """
        if not self.game:
            return False

        # Handle move from bar
        if from_point == "bar":
            return self.execute_move_from_bar(to_point)

        # Handle bearing off
        if to_point == "off":
            return self.execute_bearing_off(from_point)

        # Validate and execute regular move
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

    def execute_move_from_bar(self, to_point: int) -> bool:
        """
        Execute a move from bar to a point.

        Args:
            to_point: Destination point index

        Returns:
            True if move was successful, False otherwise
        """
        if not self.game:
            return False

        current_player_num = 1 if self.game.current_player == self.game.player1 else 2

        # Calculate required dice value

        if current_player_num == 1:

            required_dice = to_point + 1
        else:

            required_dice = 24 - to_point

        # Check if we have the required dice value
        if required_dice not in self.game.available_moves:
            return False

        # Use the game's move_from_bar method
        success = self.game.move_from_bar(required_dice)

        if success:
            self.deselect_checker()

            if not self.game.available_moves:
                self.game.last_roll = None
                self.game.available_moves = []
                self.game.switch_current_player()
            return True
        return False

    def execute_bearing_off(self, from_point: int) -> bool:
        """
        Execute bearing off a checker from the board.

        Args:
            from_point: Source point index

        Returns:
            True if bearing off was successful, False otherwise
        """
        if not self.game:
            return False

        # Execute bearing off using game logic
        success = self.game.bear_off_checker(from_point)
        if success:
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
        bear_off_x: int = None,
        bear_off_y: int = None,
        bear_off_width: int = None,
        bear_off_height: int = None,
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
        # Verificar si el jugador tiene movimientos válidos
        if self.game and self.game.last_roll and not self.game.has_valid_moves():
            # Si no hay movimientos válidos, cambiar turno automáticamente
            self.game.switch_current_player()
            return

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
            bear_off_x,
            bear_off_y,
            bear_off_width,
            bear_off_height,
        )

        # Handle click outside valid area
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
