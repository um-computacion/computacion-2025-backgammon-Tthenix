"""
Backgammon Board Module

This module provides the main coordinator class for the visual
representation of a backgammon board using Pygame.
"""

from typing import Tuple

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
        """
        pygame.init()  # pylint: disable=no-member
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Backgammon Board")

        # Color definitions
        self.colors = {
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
        self.board_margin = 30
        self.border_width = 20
        self.center_gap_width = 40
        self.bear_off_width = 80

        # Calculate main board area
        self._calculate_dimensions()

        # Checker properties
        self.checker_radius = min(self.point_width // 2 - 4, 20)

        # Dice properties
        self.dice_size = 40
        self.dice_dot_radius = 4

        # Initialize renderers
        self.board_renderer = BoardRenderer(self.colors)
        self.checker_renderer = CheckerRenderer(self.colors, self.checker_radius)
        self.dice_renderer = DiceRenderer(
            self.colors, self.dice_size, self.dice_dot_radius
        )

        # Initialize interaction handler
        self.interaction = BoardInteraction()

        # Game state
        self.board_state = None
        self.dice_values = None
        self.game = None

        # Create roll dice button
        button_width = 100
        button_height = 50
        self.roll_button = Button(
            x=self.bear_off_x + (self.bear_off_width - button_width) // 2,
            y=self.bear_off_y + self.board_height // 2 - button_height // 2,
            width=button_width,
            height=button_height,
            text="ROLL DICE",
            color=(139, 69, 19),
            hover_color=(160, 82, 45),
            text_color=(255, 255, 255),
        )

    def _calculate_dimensions(self) -> None:
        """Calculate all board dimensions and positions."""
        self.board_width = self.width - 2 * self.board_margin - self.bear_off_width
        self.board_height = self.height - 2 * self.board_margin
        self.board_x = self.board_margin
        self.board_y = self.board_margin

        # Calculate playing area (inside borders)
        self.play_area_x = self.board_x + self.border_width
        self.play_area_y = self.board_y + self.border_width
        self.play_area_width = self.board_width - 2 * self.border_width
        self.play_area_height = self.board_height - 2 * self.border_width

        # Calculate half areas
        self.half_width = (self.play_area_width - self.center_gap_width) // 2
        self.point_width = self.half_width // 6
        self.point_height = (self.play_area_height - 40) // 2

        # Bear off area dimensions
        self.bear_off_x = self.board_x + self.board_width
        self.bear_off_y = self.board_y

    def set_game(self, game: BackgammonGame) -> None:
        """
        Set the game instance to use for game logic.

        Args:
            game: BackgammonGame instance
        """
        self.game = game
        self.interaction.set_game(game)

    def set_board_state(self, board_state: dict) -> None:
        """
        Set the current board state to display.

        Args:
            board_state: Dictionary containing board state
        """
        self.board_state = board_state
        self.interaction.set_board_state(board_state)

    def set_dice_values(self, die1: int, die2: int) -> None:
        """
        Set the current dice values to display.

        Args:
            die1: First die value (1-6)
            die2: Second die value (1-6)
        """
        self.dice_values = (die1, die2)

    def update_from_game(self) -> None:
        """Update the visual board state from the game instance."""
        if not self.game:
            return

        # Get board state from game
        board_state = self.game.board.get_board_state()
        self.set_board_state(board_state)

        # Update dice values if available
        if self.game.last_roll:
            self.set_dice_values(self.game.last_roll[0], self.game.last_roll[1])

    def draw_board(self) -> None:
        """Draw the complete backgammon board."""
        # Create wood textured background
        wood_surface = self.board_renderer.create_wood_texture_surface(
            self.board_width, self.board_height
        )
        self.screen.blit(wood_surface, (self.board_x, self.board_y))

        # Draw dark border around the entire board
        border_rect = pygame.Rect(
            self.board_x, self.board_y, self.board_width, self.board_height
        )
        pygame.draw.rect(
            self.screen, self.colors["border_dark"], border_rect, self.border_width
        )

        # Draw triangular points
        self.board_renderer.draw_points(
            self.screen,
            self.play_area_x,
            self.play_area_y,
            self.play_area_height,
            self.point_width,
            self.point_height,
            self.half_width,
            self.center_gap_width,
        )

        # Draw center gap
        gap_x = self.play_area_x + self.half_width
        gap_y = self.play_area_y
        self.board_renderer.draw_center_gap(
            self.screen, gap_x, gap_y, self.center_gap_width, self.play_area_height
        )

        # Draw bear off area
        self.board_renderer.draw_bear_off_area(
            self.screen,
            self.bear_off_x,
            self.bear_off_y,
            self.bear_off_width,
            self.board_height,
        )

        # Draw checkers if board state is set
        if self.board_state:
            self.draw_all_checkers()

        # Draw selection highlights
        self.draw_selection_highlights()

        # Draw dice if dice values are set
        self.draw_dice()

        # Draw roll dice button
        self.roll_button.draw(self.screen)

        # Draw current player indicator
        self._draw_current_player_indicator()

    def draw_all_checkers(self) -> None:
        """Draw all checkers on the board based on current game state."""
        if not self.board_state:
            return

        # Draw checkers on each point
        for point_index in range(24):
            if point_index < len(self.board_state["points"]):
                checkers = self.board_state["points"][point_index]
                self.checker_renderer.draw_checkers_on_point(
                    self.screen,
                    point_index,
                    checkers,
                    self.play_area_x,
                    self.play_area_y,
                    self.play_area_height,
                    self.point_width,
                    self.point_height,
                    self.half_width,
                    self.center_gap_width,
                )

        # Draw checkers on the bar
        if "checker_bar" in self.board_state:
            player1_bar = self.board_state["checker_bar"][0]
            player2_bar = self.board_state["checker_bar"][1]
            bar_center_x = (
                self.play_area_x + self.half_width + self.center_gap_width // 2
            )
            self.checker_renderer.draw_checkers_on_bar(
                self.screen,
                player1_bar,
                player2_bar,
                bar_center_x,
                self.play_area_y,
                self.play_area_height,
            )

        # Draw borne-off checkers
        if "off_board" in self.board_state:
            player1_off = self.board_state["off_board"][0]
            player2_off = self.board_state["off_board"][1]
            bear_off_center_x = self.bear_off_x + self.bear_off_width // 2
            self.checker_renderer.draw_borne_off_checkers(
                self.screen,
                player1_off,
                player2_off,
                bear_off_center_x,
                self.bear_off_y,
                self.board_height,
            )

    def draw_dice(self) -> None:
        """Draw the dice on the board if dice values are set."""
        # Position for dice (right of center gap)
        dice_x = self.play_area_x + self.half_width + self.center_gap_width + 20
        dice_y = self.play_area_y + self.play_area_height // 2 - self.dice_size

        self.dice_renderer.draw_dice(self.screen, self.dice_values, dice_x, dice_y)

    def draw_selection_highlights(self) -> None:
        """Draw visual highlights for selected checker and valid moves."""
        if self.interaction.selected_point is None:
            return

        # Highlight selected point
        self._highlight_point(
            self.interaction.selected_point, self.colors["selected_highlight"]
        )

        # Highlight valid destination points
        if self.interaction.valid_destinations:
            for dest in self.interaction.valid_destinations:
                self._highlight_point(dest, self.colors["valid_move_highlight"])

    def _highlight_point(self, point: int, color: Tuple[int, int, int]) -> None:
        """
        Draw a highlight circle on a specific point.

        Args:
            point: Point index to highlight
            color: RGB color tuple for highlight
        """
        # Calculate point position
        if point < 6:
            # Right side, bottom
            point_x = (
                self.play_area_x
                + self.half_width
                + self.center_gap_width
                + (5 - point) * self.point_width
            )
            point_y = self.play_area_y + self.play_area_height - self.point_height // 2
        elif point < 12:
            # Left side, bottom
            point_x = self.play_area_x + (11 - point) * self.point_width
            point_y = self.play_area_y + self.play_area_height - self.point_height // 2
        elif point < 18:
            # Left side, top
            point_x = self.play_area_x + (point - 12) * self.point_width
            point_y = self.play_area_y + self.point_height // 2
        else:
            # Right side, top
            point_x = (
                self.play_area_x
                + self.half_width
                + self.center_gap_width
                + (point - 18) * self.point_width
            )
            point_y = self.play_area_y + self.point_height // 2

        # Center of the point
        center_x = point_x + self.point_width // 2

        # Draw highlight using board renderer
        self.board_renderer.draw_highlight(
            self.screen, center_x, int(point_y), self.checker_radius + 5, color
        )

    def _draw_current_player_indicator(self) -> None:
        """Draw the current player indicator."""
        try:
            font = pygame.font.Font(None, 28)
            if self.game and self.game.current_player:
                jugador = self.game.current_player
                texto = f"Turno: {jugador.name} ({jugador.color})"
                color = self.colors["white"]
                texto_surface = font.render(texto, True, color)
                self.screen.blit(texto_surface, (self.board_margin, 5))
        except pygame.error:  # pylint: disable=no-member
            pass

    def handle_board_click(self, x: int, y: int) -> None:
        """
        Handle a mouse click on the board.

        Args:
            x: X coordinate of click
            y: Y coordinate of click
        """
        self.interaction.handle_board_click(
            x,
            y,
            self.play_area_x,
            self.play_area_y,
            self.play_area_width,
            self.play_area_height,
            self.point_width,
            self.half_width,
            self.center_gap_width,
        )
        # Update board state after interaction
        self.update_from_game()
