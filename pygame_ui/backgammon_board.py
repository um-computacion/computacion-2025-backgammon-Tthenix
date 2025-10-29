"""
Backgammon Board Module

This module provides the main coordinator class for the visual
representation of a backgammon board using Pygame.
"""

from typing import Tuple, Optional

import pygame  # pylint: disable=import-error
from core.backgammon import BackgammonGame
from pygame_ui.button import Button
from pygame_ui.board_interaction import BoardInteraction
from pygame_ui.renderers import BoardRenderer, CheckerRenderer, DiceRenderer


class BackgammonBoard:
    """
    Main coordinator class for the backgammon board visualization.

    This class manages the board dimensions, colors, and coordinates
    the rendering and interaction components.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, width: int = 1000, height: int = 700) -> None:
        """
        Initialize the backgammon board.

        Args:
            width: Screen width in pixels
            height: Screen height in pixels

        Returns:
            None
        """
        pygame.init()  # pylint: disable=no-member
        self.__width__ = width
        self.__height__ = height
        self.__screen__ = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Backgammon Board")

        # Color definitions
        self.__colors__ = {
            "wood_light": (210, 180, 140),
            "wood_dark": (139, 119, 101),
            "border_dark": (101, 67, 33),
            "point_light": (222, 184, 135),
            "point_dark": (160, 82, 45),
            "center_gap": (120, 85, 60),
            "center_gap_shadow": (90, 60, 40),
            "bear_off_bg": (190, 160, 120),
            "bear_off_border": (110, 75, 45),
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "checker_white": (245, 245, 245),
            "checker_white_highlight": (255, 255, 255),
            "checker_white_shadow": (200, 200, 200),
            "checker_black": (40, 40, 40),
            "checker_black_highlight": (80, 80, 80),
            "checker_black_shadow": (10, 10, 10),
            "dice_white": (255, 255, 255),
            "dice_shadow": (180, 180, 180),
            "dice_dot": (30, 30, 30),
            "dice_border": (50, 50, 50),
            "selected_highlight": (255, 215, 0),
            "valid_move_highlight": (50, 205, 50),
        }

        # Board layout dimensions
        self.__board_margin__ = 30
        self.__border_width__ = 20
        self.__center_gap_width__ = 40
        self.__bear_off_width__ = 80

        # Calculate main board area
        self._calculate_dimensions()

        # Checker properties
        self.__checker_radius__ = min(self.__point_width__ // 2 - 4, 20)

        # Dice properties
        self.__dice_size__ = 40
        self.__dice_dot_radius__ = 4

        # Initialize renderers
        self.__board_renderer__ = BoardRenderer(self.__colors__)
        self.__checker_renderer__ = CheckerRenderer(
            self.__colors__, self.__checker_radius__
        )
        self.__dice_renderer__ = DiceRenderer(
            self.__colors__, self.__dice_size__, self.__dice_dot_radius__
        )

        # Initialize interaction handler
        self.__interaction__ = BoardInteraction()

        # Game state
        self.__board_state__ = None
        self.__dice_values__ = None
        self.__game__ = None
        self.__save_message__ = None
        self.__save_message_timer__ = 0

        # Create roll dice button
        button_width = 100
        button_height = 50
        self.__roll_button__ = Button(
            x=self.bear_off_x + (self.__bear_off_width__ - button_width) // 2,
            y=self.bear_off_y + self.board_height // 2 - button_height // 2,
            width=button_width,
            height=button_height,
            text="ROLL DICE",
            color=(139, 69, 19),
            hover_color=(160, 82, 45),
            text_color=(255, 255, 255),
        )

        # Create save game button (positioned at bottom of board)
        self.__save_button__ = Button(
            x=self.board_x + 20,
            y=self.board_y + self.board_height + -20,
            width=button_width,
            height=button_height,
            text="SAVE",
            color=(34, 139, 34),
            hover_color=(0, 128, 0),
            text_color=(255, 255, 255),
        )

        # Create load game button (positioned next to save button)
        self.__load_button__ = Button(
            x=self.board_x + button_width + 40,
            y=self.board_y + self.board_height + -20,
            width=button_width,
            height=button_height,
            text="LOAD",
            color=(70, 130, 180),
            hover_color=(100, 149, 237),
            text_color=(255, 255, 255),
        )

    def _calculate_dimensions(self) -> None:
        """Calculate all board dimensions and positions.

        Returns:
            None
        """
        self.board_width = (
            self.__width__ - 2 * self.__board_margin__ - self.__bear_off_width__
        )
        self.board_height = self.__height__ - 2 * self.__board_margin__
        self.board_x = self.__board_margin__
        self.board_y = self.__board_margin__

        # Calculate playing area (inside borders)
        self.play_area_x = self.board_x + self.__border_width__
        self.play_area_y = self.board_y + self.__border_width__
        self.play_area_width = self.board_width - 2 * self.__border_width__
        self.play_area_height = self.board_height - 2 * self.__border_width__

        # Calculate half areas
        self.half_width = (self.play_area_width - self.__center_gap_width__) // 2
        self.__point_width__ = self.half_width // 6
        self.__point_height__ = (self.play_area_height - 40) // 2

        # Bear off area dimensions
        self.bear_off_x = self.board_x + self.board_width
        self.bear_off_y = self.board_y

    def set_game(self, game: BackgammonGame) -> None:
        """
        Set the game instance to use for game logic.

        Args:
            game: BackgammonGame instance

        Returns:
            None
        """
        self.__game__ = game
        self.__interaction__.set_game(game)

    def set_board_state(self, board_state: dict) -> None:
        """
        Set the current board state to display.

        Args:
            board_state: Dictionary containing board state

        Returns:
            None
        """
        self.__board_state__ = board_state
        self.__interaction__.set_board_state(board_state)

    def set_dice_values(self, die1: int, die2: int) -> None:
        """
        Set the current dice values to display.

        Args:
            die1: First die value (1-6)
            die2: Second die value (1-6)

        Returns:
            None
        """
        self.__dice_values__ = (die1, die2)

    def update_from_game(self) -> None:
        """Update the visual board state from the game instance.

        Returns:
            None
        """
        if not self.__game__:
            return

        # Get board state from game
        board_state = self.__game__.__board__.get_board_state()
        self.set_board_state(board_state)

        # Update dice values if available
        if self.__game__.__last_roll__:
            self.set_dice_values(
                self.__game__.__last_roll__[0], self.__game__.__last_roll__[1]
            )

    def draw_board(self) -> None:
        """Draw the complete backgammon board.

        Returns:
            None
        """
        # Create wood textured background
        wood_surface = self.__board_renderer__.create_wood_texture_surface(
            self.board_width, self.board_height
        )
        self.__screen__.blit(wood_surface, (self.board_x, self.board_y))

        # Draw dark border around the entire board
        border_rect = pygame.Rect(
            self.board_x, self.board_y, self.board_width, self.board_height
        )
        pygame.draw.rect(
            self.__screen__,
            self.__colors__["border_dark"],
            border_rect,
            self.__border_width__,
        )

        # Draw triangular points
        self.__board_renderer__.draw_points(
            self.__screen__,
            self.play_area_x,
            self.play_area_y,
            self.play_area_height,
            self.__point_width__,
            self.__point_height__,
            self.half_width,
            self.__center_gap_width__,
        )

        # Draw center gap
        gap_x = self.play_area_x + self.half_width
        gap_y = self.play_area_y
        self.__board_renderer__.draw_center_gap(
            self.__screen__,
            gap_x,
            gap_y,
            self.__center_gap_width__,
            self.play_area_height,
        )

        # Draw bear off area
        self.__board_renderer__.draw_bear_off_area(
            self.__screen__,
            self.bear_off_x,
            self.bear_off_y,
            self.__bear_off_width__,
            self.board_height,
        )

        # Draw checkers if board state is set
        if self.__board_state__:
            self.draw_all_checkers()

        # Draw selection highlights
        self.draw_selection_highlights()

        # Draw dice if dice values are set
        self.draw_dice()

        # Draw roll dice button
        self.__roll_button__.draw(self.__screen__)

        # Draw save game button (with conditional styling)
        self._draw_save_button()

        # Draw load game button
        self.__load_button__.draw(self.__screen__)

        # Draw current player indicator
        self._draw_current_player_indicator()

        # Draw save message
        self.draw_save_message()

    def draw_all_checkers(self) -> None:
        """Draw all checkers on the board based on current game state.

        Returns:
            None
        """
        if not self.__board_state__:
            return

        # Draw checkers on each point
        for point_index in range(24):
            if point_index < len(self.__board_state__["points"]):
                checkers = self.__board_state__["points"][point_index]
                self.__checker_renderer__.draw_checkers_on_point(
                    self.__screen__,
                    point_index,
                    checkers,
                    self.play_area_x,
                    self.play_area_y,
                    self.play_area_height,
                    self.__point_width__,
                    self.__point_height__,
                    self.half_width,
                    self.__center_gap_width__,
                )

        # Draw checkers on the bar
        if "bar" in self.__board_state__:
            player1_bar = self.__board_state__["bar"][0]
            player2_bar = self.__board_state__["bar"][1]
            bar_center_x = (
                self.play_area_x + self.half_width + self.__center_gap_width__ // 2
            )
            self.__checker_renderer__.draw_checkers_on_bar(
                self.__screen__,
                player1_bar,
                player2_bar,
                bar_center_x,
                self.play_area_y,
                self.play_area_height,
            )

        # Draw borne-off checkers
        if "off_board" in self.__board_state__:
            player1_off = self.__board_state__["off_board"][0]
            player2_off = self.__board_state__["off_board"][1]
            bear_off_center_x = self.bear_off_x + self.__bear_off_width__ // 2
            self.__checker_renderer__.draw_borne_off_checkers(
                self.__screen__,
                player1_off,
                player2_off,
                bear_off_center_x,
                self.bear_off_y,
                self.board_height,
            )

    def draw_dice(self) -> None:
        """Draw the dice on the board if dice values are set.

        Returns:
            None
        """
        # Position for dice (right of center gap)
        dice_x = self.play_area_x + self.half_width + self.__center_gap_width__ + 20
        dice_y = self.play_area_y + self.play_area_height // 2 - self.__dice_size__

        self.__dice_renderer__.draw_dice(
            self.__screen__, self.__dice_values__, dice_x, dice_y
        )

    def draw_selection_highlights(self) -> None:
        """Draw visual highlights for selected checker and valid moves.

        Returns:
            None
        """
        if self.__interaction__.__selected_point__ is None:
            return

        # Highlight selected point or bar
        if self.__interaction__.__selected_point__ == "bar":
            self._highlight_bar(self.__colors__["selected_highlight"])
        else:
            self._highlight_point(
                self.__interaction__.__selected_point__,
                self.__colors__["selected_highlight"],
            )

        # Highlight valid destination points
        if self.__interaction__.__valid_destinations__:
            for dest in self.__interaction__.__valid_destinations__:
                if dest == "off":
                    # Highlight bear-off area
                    self._highlight_bear_off_area(
                        self.__colors__["valid_move_highlight"]
                    )
                else:
                    self._highlight_point(dest, self.__colors__["valid_move_highlight"])

    def _highlight_point(self, point, color: Tuple[int, int, int]) -> None:
        """
        Draw a highlight circle on a specific point.

        Args:
            point: Point index to highlight (or "off" for bear-off area)
            color: RGB color tuple for highlight

        Returns:
            None
        """
        # Handle special cases like "off" for bear-off area
        if not isinstance(point, int):
            return

        # Calculate point position
        if point < 6:
            # Right side, bottom
            point_x = (
                self.play_area_x
                + self.half_width
                + self.__center_gap_width__
                + (5 - point) * self.__point_width__
            )
            point_y = (
                self.play_area_y + self.play_area_height - self.__point_height__ // 2
            )
        elif point < 12:
            # Left side, bottom
            point_x = self.play_area_x + (11 - point) * self.__point_width__
            point_y = (
                self.play_area_y + self.play_area_height - self.__point_height__ // 2
            )
        elif point < 18:
            # Left side, top
            point_x = self.play_area_x + (point - 12) * self.__point_width__
            point_y = self.play_area_y + self.__point_height__ // 2
        else:
            # Right side, top
            point_x = (
                self.play_area_x
                + self.half_width
                + self.__center_gap_width__
                + (point - 18) * self.__point_width__
            )
            point_y = self.play_area_y + self.__point_height__ // 2

        # Center of the point
        center_x = point_x + self.__point_width__ // 2

        # Draw highlight using board renderer
        self.__board_renderer__.draw_highlight(
            self.__screen__, center_x, int(point_y), self.__checker_radius__ + 5, color
        )

    def _highlight_bear_off_area(self, color: Tuple[int, int, int]) -> None:
        """
        Highlight the bear-off area.

        Args:
            color: RGB color tuple for highlight

        Returns:
            None
        """
        # Draw a border around the bear-off area
        border_rect = pygame.Rect(
            self.bear_off_x - 5,
            self.bear_off_y - 5,
            self.__bear_off_width__ + 10,
            self.board_height + 10,
        )
        pygame.draw.rect(self.__screen__, color, border_rect, 5)

    def _highlight_bar(self, color: Tuple[int, int, int]) -> None:
        """
        Draw a highlight on the bar area.

        Args:
            color: RGB color tuple for highlight

        Returns:
            None
        """
        bar_center_x = (
            self.play_area_x + self.half_width + self.__center_gap_width__ // 2
        )

        # Draw highlight rectangle on the bar
        pygame.draw.rect(
            self.__screen__,
            color,
            (
                bar_center_x - self.__center_gap_width__ // 2 + 5,
                self.play_area_y + 10,
                self.__center_gap_width__ - 10,
                self.play_area_height - 20,
            ),
            3,
        )

    def _draw_current_player_indicator(self) -> None:
        """Draw the current player indicator.

        Returns:
            None
        """
        try:
            font = pygame.font.Font(None, 28)
            if self.__game__ and self.__game__.__current_player__:
                jugador = self.__game__.__current_player__
                texto = f"Turn: {jugador.__name__} ({jugador.__color__})"
                color = self.__colors__["white"]
                texto_surface = font.render(texto, True, color)
                self.__screen__.blit(texto_surface, (self.__board_margin__, 5))
        except pygame.error:  # pylint: disable=no-member,broad-exception-caught
            pass

    def handle_board_click(self, x: int, y: int) -> None:
        """
        Handle a mouse click on the board.

        Args:
            x: X coordinate of click
            y: Y coordinate of click

        Returns:
            None
        """
        self.__interaction__.handle_board_click(
            x,
            y,
            self.play_area_x,
            self.play_area_y,
            self.play_area_width,
            self.play_area_height,
            self.__point_width__,
            self.half_width,
            self.__center_gap_width__,
            bear_off_x=self.bear_off_x,
            bear_off_y=self.bear_off_y,
            bear_off_width=self.__bear_off_width__,
            bear_off_height=self.board_height,
        )
        # Update board state after interaction
        self.update_from_game()

    def get_point_from_mouse(self, mouse_pos) -> Optional[int]:
        """
        Get point index from mouse coordinates.

        Args:
            mouse_pos: Tuple of (x, y) mouse coordinates

        Returns:
            Point index (0-23) or None if not on a valid point
        """
        x, y = mouse_pos
        return self.__interaction__.get_point_from_coordinates(
            x,
            y,
            self.play_area_x,
            self.play_area_y,
            self.play_area_width,
            self.play_area_height,
            self.__point_width__,
            self.half_width,
            self.__center_gap_width__,
        )

    def set_selected_point(self, point: Optional[int]) -> None:
        """Set the selected point for highlighting.

        Args:
            point: Point index to select or None to deselect

        Returns:
            None
        """
        if point is not None:
            self.__interaction__.selected_point = point
        else:
            self.__interaction__.selected_point = None

    def set_possible_destinations(self, destinations: list) -> None:
        """Set the possible destinations for highlighting.

        Args:
            destinations: List of valid destination points

        Returns:
            None
        """
        self.__interaction__.valid_destinations = destinations

    def handle_save_button_click(self, event) -> bool:
        """
        Handle save button click event.

        Args:
            event: Pygame event

        Returns:
            True if button was clicked, False otherwise
        """
        return self.__save_button__.handle_event(event)

    def handle_load_button_click(self, event) -> bool:
        """
        Handle load button click event.

        Args:
            event: Pygame event

        Returns:
            True if button was clicked, False otherwise
        """
        return self.__load_button__.handle_event(event)

    def show_save_message(self, message: str) -> None:
        """
        Show a save confirmation message.

        Args:
            message: Message to display

        Returns:
            None
        """
        self.__save_message__ = message
        self.__save_message_timer__ = 180  # Show for 3 seconds at 60 FPS

    def update_save_message_timer(self) -> None:
        """
        Update the save message timer.

        Returns:
            None
        """
        if self.__save_message_timer__ > 0:
            self.__save_message_timer__ -= 1
            if self.__save_message_timer__ == 0:
                self.__save_message__ = None

    def _draw_save_button(self) -> None:
        """
        Draw the save button with conditional styling based on game state.

        Returns:
            None
        """
        # Check if save should be disabled (dice rolled but no moves made)
        if (
            self.__game__
            and self.__game__.__last_roll__ is not None
            and self.__game__.__available_moves__
        ):
            # Draw disabled save button
            self.__save_button__.__color__ = (128, 128, 128)  # Gray
            self.__save_button__.__hover_color__ = (128, 128, 128)  # Gray
            self.__save_button__.__text_color__ = (200, 200, 200)  # Light gray text
        else:
            # Draw normal save button
            self.__save_button__.__color__ = (34, 139, 34)  # Green
            self.__save_button__.__hover_color__ = (0, 128, 0)  # Dark green
            self.__save_button__.__text_color__ = (255, 255, 255)  # White text

        self.__save_button__.draw(self.__screen__)

    def draw_save_message(self) -> None:
        """
        Draw the save confirmation message.

        Returns:
            None
        """
        if not self.__save_message__:
            return

        try:
            font = pygame.font.Font(None, 36)
            text_surface = font.render(self.__save_message__, True, (0, 255, 0))
            text_rect = text_surface.get_rect(center=(self.__width__ // 2, 50))

            # Draw background rectangle
            bg_rect = text_rect.inflate(20, 10)
            pygame.draw.rect(self.__screen__, (0, 0, 0), bg_rect)
            pygame.draw.rect(self.__screen__, (255, 255, 255), bg_rect, 2)

            self.__screen__.blit(text_surface, text_rect)
        except pygame.error:  # pylint: disable=no-member,broad-exception-caught
            pass
