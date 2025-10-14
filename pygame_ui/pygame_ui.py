"""
Backgammon Pygame UI Module

This module provides a visual representation of a backgammon board using Pygame.
Based on the reference image, it creates a realistic board with proper colors,
triangular points, central bar, and bearing off area.
"""

from typing import Tuple, Optional, List

import pygame  # pylint: disable=import-error
from core.backgammon import BackgammonGame


class Button:
    """A simple button class for pygame UI."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        *,
        color: Tuple[int, int, int] = (139, 69, 19),
        hover_color: Tuple[int, int, int] = (160, 82, 45),
        text_color: Tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        """
        Initialize a button.

        Args:
            x: X position of button
            y: Y position of button
            width: Button width
            height: Button height
            text: Button text
            color: Normal button color
            hover_color: Button color when hovered
            text_color: Text color
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the button on the surface.

        Args:
            surface: Surface to draw on
        """
        # Choose color based on hover state
        current_color = self.hover_color if self.is_hovered else self.color

        # Draw button background with rounded corners
        pygame.draw.rect(surface, current_color, self.rect, border_radius=10)

        # Draw button border
        border_color = (0, 0, 0)
        pygame.draw.rect(surface, border_color, self.rect, 3, border_radius=10)

        # Draw button text
        try:
            font = pygame.font.Font(None, 28)
            text_surface = font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)
        except pygame.error:  # pylint: disable=no-member
            pass  # If font fails, button will still be visible

    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse events for the button.

        Args:
            event: Pygame event

        Returns:
            True if button was clicked, False otherwise
        """
        if event.type == pygame.MOUSEMOTION:  # pylint: disable=no-member
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False


class BackgammonBoard:
    """
    A class representing the visual backgammon board.

    This class handles the drawing and rendering of all board elements
    including triangular points, central bar, borders, and bearing off area.

    Note: This class holds many visual properties (colors, dimensions, positions)
    which justifies the high attribute count for proper rendering.
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

        # Color definitions based on the reference image
        self.colors = {
            "wood_light": (210, 180, 140),  # Light tan/beige for board background
            "wood_dark": (139, 119, 101),  # Darker brown for board texture
            "border_dark": (101, 67, 33),  # Dark brown border
            "point_light": (222, 184, 135),  # Light tan triangular points
            "point_dark": (160, 82, 45),  # Dark brown triangular points
            "center_gap": (120, 85, 60),  # Darker brown for recessed center gap
            "center_gap_shadow": (90, 60, 40),  # Even darker for shadow effect
            "bear_off_bg": (190, 160, 120),  # Light brown for bear off background
            "bear_off_border": (110, 75, 45),  # Darker brown for bear off borders
            "black": (0, 0, 0),
            "white": (255, 255, 255),
            "checker_white": (245, 245, 245),  # White checker main color
            "checker_white_highlight": (255, 255, 255),  # White checker highlight
            "checker_white_shadow": (200, 200, 200),  # White checker shadow
            "checker_black": (40, 40, 40),  # Black checker main color
            "checker_black_highlight": (80, 80, 80),  # Black checker highlight
            "checker_black_shadow": (10, 10, 10),  # Black checker shadow
            "dice_white": (255, 255, 255),  # White dice color
            "dice_shadow": (180, 180, 180),  # Dice shadow
            "dice_dot": (30, 30, 30),  # Dice dot color
            "dice_border": (50, 50, 50),  # Dice border color
            "selected_highlight": (255, 215, 0),  # Gold for selected checker
            "valid_move_highlight": (50, 205, 50),  # Lime green for valid destinations
        }

        # Board layout dimensions
        self.board_margin = 30
        self.border_width = 20
        self.center_gap_width = 40  # Reduced width for natural wooden gap
        self.bear_off_width = 80  # Width for bear off area

        # Calculate main board area (with bear off area)
        self._calculate_dimensions()

        # Checker properties
        self.checker_radius = min(self.point_width // 2 - 4, 20)
        self.checker_spacing = self.checker_radius * 2 + 2

        # Dice properties
        self.dice_size = 40
        self.dice_dot_radius = 4

        # Game state - will be set by external game logic
        self.board_state = None
        self.dice_values = None  # Will store tuple of (die1, die2)
        # Game instance
        self.game = None

        # Selection state for mouse interaction
        self.selected_point: Optional[int] = None
        self.valid_destinations: Optional[List[int]] = None

        # Create roll dice button in the bear-off area (right side)
        button_width = 100
        button_height = 50
        self.roll_button = Button(
            x=self.bear_off_x + (self.bear_off_width - button_width) // 2,
            y=self.bear_off_y + self.board_height // 2 - button_height // 2,
            width=button_width,
            height=button_height,
            text="ROLL DICE",
            color=(139, 69, 19),  # Saddle brown
            hover_color=(160, 82, 45),  # Sienna (lighter brown)
            text_color=(255, 255, 255),  # White text
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

        # Calculate half areas (left and right sides of the center gap)
        self.half_width = (self.play_area_width - self.center_gap_width) // 2
        self.point_width = self.half_width // 6
        self.point_height = (self.play_area_height - 40) // 2  # 40px gap in middle

        # Bear off area dimensions
        self.bear_off_x = self.board_x + self.board_width
        self.bear_off_y = self.board_y

    def create_wood_texture_surface(self, width: int, height: int) -> pygame.Surface:
        """
        Create a surface with wood-like texture.

        Args:
            width: Surface width
            height: Surface height

        Returns:
            Surface with wood texture pattern
        """
        surface = pygame.Surface((width, height))
        base_color = self.colors["wood_light"]

        # Fill with base wood color
        surface.fill(base_color)

        # Add wood grain lines
        for y in range(0, height, 8):
            line_color = (
                max(0, base_color[0] - 15),
                max(0, base_color[1] - 15),
                max(0, base_color[2] - 15),
            )
            pygame.draw.line(surface, line_color, (0, y), (width, y), 1)

        return surface

    def draw_triangular_point(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        color: Tuple[int, int, int],
        pointing_up: bool = True,
    ) -> None:
        """
        Draw a triangular point on the board.

        Args:
            surface: Surface to draw on
            x: X position of the triangle base
            y: Y position of the triangle base
            width: Width of the triangle base
            height: Height of the triangle
            color: RGB color tuple
            pointing_up: True if triangle points up, False if pointing down
        """
        if pointing_up:
            points = [
                (x, y + height),  # Bottom left
                (x + width, y + height),  # Bottom right
                (x + width // 2, y),  # Top center
            ]
        else:
            points = [
                (x, y),  # Top left
                (x + width, y),  # Top right
                (x + width // 2, y + height),  # Bottom center
            ]

        pygame.draw.polygon(surface, color, points)
        pygame.draw.polygon(surface, self.colors["black"], points, 2)

    def draw_center_gap(self, surface: pygame.Surface) -> None:
        """
        Draw the center gap that divides the board halves.
        Creates a recessed wooden area with natural brown tones.

        Args:
            surface: Surface to draw on
        """
        gap_x = self.play_area_x + self.half_width
        gap_y = self.play_area_y
        gap_rect = pygame.Rect(
            gap_x, gap_y, self.center_gap_width, self.play_area_height
        )

        # Fill with darker brown for recessed effect
        pygame.draw.rect(surface, self.colors["center_gap"], gap_rect)

        # Add shadow effect on the left side
        shadow_width = 4
        shadow_rect = pygame.Rect(gap_x, gap_y, shadow_width, self.play_area_height)
        pygame.draw.rect(surface, self.colors["center_gap_shadow"], shadow_rect)

        # Add shadow effect on the right side
        shadow_rect = pygame.Rect(
            gap_x + self.center_gap_width - shadow_width,
            gap_y,
            shadow_width,
            self.play_area_height,
        )
        pygame.draw.rect(surface, self.colors["center_gap_shadow"], shadow_rect)

        # Add wood grain texture to the gap
        for i in range(0, self.center_gap_width, 6):
            line_color = (
                max(0, self.colors["center_gap"][0] - 10),
                max(0, self.colors["center_gap"][1] - 10),
                max(0, self.colors["center_gap"][2] - 10),
            )
            pygame.draw.line(
                surface,
                line_color,
                (gap_x + i, gap_y),
                (gap_x + i, gap_y + self.play_area_height),
                1,
            )

        # Add horizontal wood grain lines for natural texture
        for y in range(gap_y, gap_y + self.play_area_height, 12):
            line_color = (
                max(0, self.colors["center_gap"][0] - 15),
                max(0, self.colors["center_gap"][1] - 15),
                max(0, self.colors["center_gap"][2] - 15),
            )
            pygame.draw.line(
                surface,
                line_color,
                (gap_x + 2, y),
                (gap_x + self.center_gap_width - 2, y),
                1,
            )

    def draw_bear_off_area(self, surface: pygame.Surface) -> None:
        """
        Draw the bear off area where borne-off checkers are placed.

        Args:
            surface: Surface to draw on
        """
        bear_off_rect = pygame.Rect(
            self.bear_off_x, self.bear_off_y, self.bear_off_width, self.board_height
        )

        # Fill with light brown background
        pygame.draw.rect(surface, self.colors["bear_off_bg"], bear_off_rect)

        # Add wood grain texture
        for i in range(0, self.bear_off_width, 8):
            line_color = (
                max(0, self.colors["bear_off_bg"][0] - 15),
                max(0, self.colors["bear_off_bg"][1] - 15),
                max(0, self.colors["bear_off_bg"][2] - 15),
            )
            pygame.draw.line(
                surface,
                line_color,
                (self.bear_off_x + i, self.bear_off_y),
                (self.bear_off_x + i, self.bear_off_y + self.board_height),
                1,
            )

        # Draw border around bear off area
        pygame.draw.rect(surface, self.colors["bear_off_border"], bear_off_rect, 3)

        # Draw dividing line in the middle to separate white and black bear off areas
        middle_y = self.bear_off_y + self.board_height // 2
        pygame.draw.line(
            surface,
            self.colors["bear_off_border"],
            (self.bear_off_x, middle_y),
            (self.bear_off_x + self.bear_off_width, middle_y),
            2,
        )

        # Add labels for the bear off areas
        self._draw_bear_off_labels(surface)

    def _draw_bear_off_labels(self, surface: pygame.Surface) -> None:
        """Draw labels for the bear off areas."""
        try:
            # Try to use a font if available
            font = pygame.font.Font(None, 24)

            # White player bear off area (top)
            white_text = font.render("WHITE", True, self.colors["black"])
            white_rect = white_text.get_rect()
            white_rect.center = (
                self.bear_off_x + self.bear_off_width // 2,
                self.bear_off_y + self.board_height // 4,
            )
            surface.blit(white_text, white_rect)

            # Black player bear off area (bottom)
            black_text = font.render("BLACK", True, self.colors["black"])
            black_rect = black_text.get_rect()
            black_rect.center = (
                self.bear_off_x + self.bear_off_width // 2,
                self.bear_off_y + 3 * self.board_height // 4,
            )
            surface.blit(black_text, black_rect)

        except pygame.error:  # pylint: disable=no-member
            # If font loading fails, draw simple geometric indicators
            # White area indicator (circle)
            pygame.draw.circle(
                surface,
                self.colors["white"],
                (
                    self.bear_off_x + self.bear_off_width // 2,
                    self.bear_off_y + self.board_height // 4,
                ),
                8,
            )
            pygame.draw.circle(
                surface,
                self.colors["black"],
                (
                    self.bear_off_x + self.bear_off_width // 2,
                    self.bear_off_y + self.board_height // 4,
                ),
                8,
                2,
            )

            # Black area indicator (filled circle)
            pygame.draw.circle(
                surface,
                self.colors["black"],
                (
                    self.bear_off_x + self.bear_off_width // 2,
                    self.bear_off_y + 3 * self.board_height // 4,
                ),
                8,
            )

    def draw_checker(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        player: int,
    ) -> None:
        """
        Draw a single checker with 3D effect.

        Args:
            surface: Surface to draw on
            x: X position (center of checker)
            y: Y position (center of checker)
            player: Player number (1 for white, 2 for black)
        """
        # Determine colors based on player
        if player == 1:
            main_color = self.colors["checker_white"]
            highlight_color = self.colors["checker_white_highlight"]
            shadow_color = self.colors["checker_white_shadow"]
        else:
            main_color = self.colors["checker_black"]
            highlight_color = self.colors["checker_black_highlight"]
            shadow_color = self.colors["checker_black_shadow"]

        # Draw shadow (bottom-right offset)
        shadow_offset = 2
        pygame.draw.circle(
            surface,
            shadow_color,
            (x + shadow_offset, y + shadow_offset),
            self.checker_radius,
        )

        # Draw main checker body
        pygame.draw.circle(surface, main_color, (x, y), self.checker_radius)

        # Draw highlight (top-left partial circle for 3D effect)
        highlight_radius = self.checker_radius // 3
        highlight_offset_x = -self.checker_radius // 3
        highlight_offset_y = -self.checker_radius // 3
        pygame.draw.circle(
            surface,
            highlight_color,
            (x + highlight_offset_x, y + highlight_offset_y),
            highlight_radius,
        )

        # Draw border
        pygame.draw.circle(
            surface, self.colors["black"], (x, y), self.checker_radius, 2
        )

    def draw_checkers_on_point(
        self,
        surface: pygame.Surface,
        point_index: int,
        checkers: list,
    ) -> None:
        """
        Draw checkers stacked on a specific point.

        Args:
            surface: Surface to draw on
            point_index: Point index (0-23)
            checkers: List of player numbers representing checkers on this point
        """
        if not checkers:
            return

        # Determine if point is on top or bottom half
        is_top_half = point_index >= 12

        # Calculate point X position
        if point_index < 6:
            # Right side, bottom
            point_x = (
                self.play_area_x
                + self.half_width
                + self.center_gap_width
                + (5 - point_index) * self.point_width
            )
        elif point_index < 12:
            # Left side, bottom
            point_x = self.play_area_x + (11 - point_index) * self.point_width
        elif point_index < 18:
            # Left side, top
            point_x = self.play_area_x + (point_index - 12) * self.point_width
        else:
            # Right side, top
            point_x = (
                self.play_area_x
                + self.half_width
                + self.center_gap_width
                + (point_index - 18) * self.point_width
            )

        # Center of the point
        checker_x = point_x + self.point_width // 2

        # Draw checkers stacked vertically
        max_visible_checkers = 5  # Show max 5 checkers before condensing
        checker_count = len(checkers)

        if checker_count <= max_visible_checkers:
            # Normal spacing
            spacing = self.checker_radius * 2 + 2
        else:
            # Condensed spacing for many checkers
            spacing = (self.point_height - self.checker_radius * 2) // (
                checker_count - 1
            )
            spacing = max(spacing, self.checker_radius + 2)

        for i, player in enumerate(checkers):
            if is_top_half:
                # Stack downward from top
                checker_y = self.play_area_y + self.checker_radius + 5 + i * spacing
            else:
                # Stack upward from bottom
                checker_y = (
                    self.play_area_y
                    + self.play_area_height
                    - self.checker_radius
                    - 5
                    - i * spacing
                )

            self.draw_checker(surface, checker_x, checker_y, player)

        # Draw count number if more than 5 checkers
        if checker_count > 5:
            self._draw_checker_count(surface, checker_x, checker_y, checker_count)

    def _draw_checker_count(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        count: int,
    ) -> None:
        """
        Draw the count number on top of stacked checkers.

        Args:
            surface: Surface to draw on
            x: X position
            y: Y position
            count: Number of checkers
        """
        try:
            font = pygame.font.Font(None, 20)
            text = font.render(str(count), True, self.colors["white"])
            text_rect = text.get_rect(center=(x, y))
            surface.blit(text, text_rect)
        except pygame.error:  # pylint: disable=no-member
            pass  # If font fails, just skip the count

    def draw_checkers_on_bar(
        self,
        surface: pygame.Surface,
        player1_bar: list,
        player2_bar: list,
    ) -> None:
        """
        Draw checkers on the bar (captured pieces).

        Args:
            surface: Surface to draw on
            player1_bar: List of player 1 checkers on bar
            player2_bar: List of player 2 checkers on bar
        """
        bar_center_x = self.play_area_x + self.half_width + self.center_gap_width // 2

        # Draw player 1 checkers (bottom half of bar)
        for i, player in enumerate(player1_bar):
            checker_y = (
                self.play_area_y
                + self.play_area_height // 2
                + 20
                + i * (self.checker_radius * 2 + 2)
            )
            self.draw_checker(surface, bar_center_x, checker_y, player)

        # Draw player 2 checkers (top half of bar)
        for i, player in enumerate(player2_bar):
            checker_y = (
                self.play_area_y
                + self.play_area_height // 2
                - 20
                - i * (self.checker_radius * 2 + 2)
            )
            self.draw_checker(surface, bar_center_x, checker_y, player)

    def draw_borne_off_checkers(
        self,
        surface: pygame.Surface,
        player1_off: list,
        player2_off: list,
    ) -> None:
        """
        Draw borne-off checkers in the bear-off area.

        Args:
            surface: Surface to draw on
            player1_off: List of player 1 borne-off checkers
            player2_off: List of player 2 borne-off checkers
        """
        bear_off_center_x = self.bear_off_x + self.bear_off_width // 2

        # Draw player 1 (white) checkers in bottom half
        for i, player in enumerate(player1_off):
            row = i // 3  # 3 checkers per row
            col = i % 3
            col_offset = (col - 1) * (self.checker_radius * 2 + 4)
            checker_x = bear_off_center_x + col_offset - self.checker_radius
            checker_y = (
                self.bear_off_y
                + 3 * self.board_height // 4
                + row * (self.checker_radius * 2 + 2)
            )
            self.draw_checker(surface, checker_x, checker_y, player)

        # Draw player 2 (black) checkers in top half
        for i, player in enumerate(player2_off):
            row = i // 3  # 3 checkers per row
            col = i % 3
            col_offset = (col - 1) * (self.checker_radius * 2 + 4)
            checker_x = bear_off_center_x + col_offset - self.checker_radius
            checker_y = (
                self.bear_off_y
                + self.board_height // 4
                + row * (self.checker_radius * 2 + 2)
            )
            self.draw_checker(surface, checker_x, checker_y, player)

    def set_board_state(self, board_state: dict) -> None:
        """
        Set the current board state to display.

        Args:
            board_state: Dictionary containing board state with points, bar, and off_board
        """
        self.board_state = board_state

    def draw_board(self) -> None:
        """Draw the complete backgammon board."""
        # Create wood textured background
        wood_surface = self.create_wood_texture_surface(
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
        self.draw_points()

        # Draw center gap
        self.draw_center_gap(self.screen)

        # Draw bear off area
        self.draw_bear_off_area(self.screen)

        # Draw checkers if board state is set
        if self.board_state:
            self.draw_all_checkers()

        # Draw selection highlights
        self.draw_selection_highlights()

        # Draw dice if dice values are set
        self.draw_dice()

        # Draw roll dice button
        self.roll_button.draw(self.screen)

        # Dibujar indicador de jugador actual (arriba a la izquierda)
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

    def draw_all_checkers(self) -> None:
        """Draw all checkers on the board based on current game state."""
        if not self.board_state:
            return

        # Draw checkers on each point
        for point_index in range(24):
            if point_index < len(self.board_state["points"]):
                checkers = self.board_state["points"][point_index]
                self.draw_checkers_on_point(self.screen, point_index, checkers)

        # Draw checkers on the bar
        if "checker_bar" in self.board_state:
            player1_bar = self.board_state["checker_bar"][0]
            player2_bar = self.board_state["checker_bar"][1]
            self.draw_checkers_on_bar(self.screen, player1_bar, player2_bar)

        # Draw borne-off checkers
        if "off_board" in self.board_state:
            player1_off = self.board_state["off_board"][0]
            player2_off = self.board_state["off_board"][1]
            self.draw_borne_off_checkers(self.screen, player1_off, player2_off)

    def draw_die_face(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        value: int,
    ) -> None:
        """
        Draw a single die with the given value.

        Args:
            surface: Surface to draw on
            x: X position (top-left corner)
            y: Y position (top-left corner)
            value: Die value (1-6)
        """
        # Draw shadow
        shadow_offset = 3
        shadow_rect = pygame.Rect(
            x + shadow_offset,
            y + shadow_offset,
            self.dice_size,
            self.dice_size,
        )
        pygame.draw.rect(
            surface, self.colors["dice_shadow"], shadow_rect, border_radius=5
        )

        # Draw main die body
        die_rect = pygame.Rect(x, y, self.dice_size, self.dice_size)
        pygame.draw.rect(surface, self.colors["dice_white"], die_rect, border_radius=5)

        # Draw border
        pygame.draw.rect(
            surface, self.colors["dice_border"], die_rect, 2, border_radius=5
        )

        # Calculate dot positions
        center_x = x + self.dice_size // 2
        center_y = y + self.dice_size // 2
        offset = self.dice_size // 4

        # Draw dots based on value
        if value == 1:
            # Center dot
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x, center_y),
                self.dice_dot_radius,
            )
        elif value == 2:
            # Top-left and bottom-right
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x - offset, center_y - offset),
                self.dice_dot_radius,
            )
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x + offset, center_y + offset),
                self.dice_dot_radius,
            )
        elif value == 3:
            # Diagonal line (top-left, center, bottom-right)
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x - offset, center_y - offset),
                self.dice_dot_radius,
            )
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x, center_y),
                self.dice_dot_radius,
            )
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x + offset, center_y + offset),
                self.dice_dot_radius,
            )
        elif value == 4:
            # Four corners
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x - offset, center_y - offset),
                self.dice_dot_radius,
            )
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x + offset, center_y - offset),
                self.dice_dot_radius,
            )
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x - offset, center_y + offset),
                self.dice_dot_radius,
            )
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x + offset, center_y + offset),
                self.dice_dot_radius,
            )
        elif value == 5:
            # Four corners + center
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x - offset, center_y - offset),
                self.dice_dot_radius,
            )
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x + offset, center_y - offset),
                self.dice_dot_radius,
            )
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x, center_y),
                self.dice_dot_radius,
            )
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x - offset, center_y + offset),
                self.dice_dot_radius,
            )
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x + offset, center_y + offset),
                self.dice_dot_radius,
            )
        elif value == 6:
            # Two columns of three
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x - offset, center_y - offset),
                self.dice_dot_radius,
            )
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x - offset, center_y),
                self.dice_dot_radius,
            )
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x - offset, center_y + offset),
                self.dice_dot_radius,
            )
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x + offset, center_y - offset),
                self.dice_dot_radius,
            )
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x + offset, center_y),
                self.dice_dot_radius,
            )
            pygame.draw.circle(
                surface,
                self.colors["dice_dot"],
                (center_x + offset, center_y + offset),
                self.dice_dot_radius,
            )

    def draw_dice(self) -> None:
        """Draw the dice on the board if dice values are set."""
        if not self.dice_values:
            return

        die1, die2 = self.dice_values

        # Si es doble, mostrar cuatro dados con el mismo valor; si no, dos dados
        if die1 == die2:
            values = [die1, die1, die1, die1]
        else:
            values = [die1, die2]

        # Posición base para dados (a la derecha de la barra central)
        dice_x = self.play_area_x + self.half_width + self.center_gap_width + 20
        dice_y = self.play_area_y + self.play_area_height // 2 - self.dice_size

        # Dibujar dados con desplazamientos agradables
        offsets = []
        if len(values) == 2:
            offsets = [(0, 0), (self.dice_size + 10, 15)]
        else:
            # 4 dados en fila con ligeros desplazamientos verticales
            step = self.dice_size + 10
            offsets = [(0, 0), (step, 15), (2 * step, 0), (3 * step, 15)]

        for i, val in enumerate(values):
            off_x, off_y = offsets[i]
            self.draw_die_face(self.screen, dice_x + off_x, dice_y + off_y, val)

    def set_dice_values(self, die1: int, die2: int) -> None:
        """
        Set the current dice values to display.

        Args:
            die1: First die value (1-6)
            die2: Second die value (1-6)
        """
        self.dice_values = (die1, die2)

    def set_game(self, game: "BackgammonGame") -> None:
        """
        Set the game instance to use for game logic.

        Args:
            game: BackgammonGame instance
        """
        self.game = game

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

    def get_point_from_coordinates(self, x: int, y: int) -> Optional[int]:
        """
        Convert screen coordinates to board point index.

        Args:
            x: X coordinate on screen
            y: Y coordinate on screen

        Returns:
            Point index (0-23) or None if not on a valid point
        """
        # Check if click is within play area
        if not (
            self.play_area_x <= x <= self.play_area_x + self.play_area_width
            and self.play_area_y <= y <= self.play_area_y + self.play_area_height
        ):
            return None

        # Determine if click is in top or bottom half
        mid_y = self.play_area_y + self.play_area_height // 2
        is_top_half = y < mid_y

        # Calculate relative x position
        rel_x = x - self.play_area_x

        # Check if in center gap
        if self.half_width <= rel_x <= self.half_width + self.center_gap_width:
            return None  # Click in center gap (bar area)

        # Determine which side (left or right of center gap)
        if rel_x < self.half_width:
            # Left side
            point_index_in_quadrant = int(rel_x / self.point_width)
            if is_top_half:
                # Top-left: points 12-17
                return 12 + point_index_in_quadrant
            # Bottom-left: points 11-6
            return 11 - point_index_in_quadrant

        # Right side
        rel_x_right = rel_x - self.half_width - self.center_gap_width
        point_index_in_quadrant = int(rel_x_right / self.point_width)
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
                # Actualizar estado del tablero tras mover
                self.update_from_game()
                # Deseleccionar ficha
                self.deselect_checker()
                # Si no quedan movimientos disponibles, finalizar turno automáticamente
                if not self.game.available_moves:
                    # Reiniciar dados y movimientos (como en CLI) y cambiar turno
                    self.game.last_roll = None
                    self.game.available_moves = []
                    self.game.switch_current_player()
                    # Refrescar vista con nuevo jugador actual
                    self.update_from_game()
                return True

        return False

    def handle_board_click(self, x: int, y: int) -> None:
        """
        Handle a mouse click on the board.

        Args:
            x: X coordinate of click
            y: Y coordinate of click
        """
        point = self.get_point_from_coordinates(x, y)
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

    def draw_selection_highlights(self) -> None:
        """Draw visual highlights for selected checker and valid moves."""
        if self.selected_point is None:
            return

        # Highlight selected point
        self._highlight_point(self.selected_point, self.colors["selected_highlight"])

        # Highlight valid destination points
        if self.valid_destinations:
            for dest in self.valid_destinations:
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
        # Draw highlight circle
        pygame.draw.circle(
            self.screen, color, (center_x, int(point_y)), self.checker_radius + 5, 3
        )

    def draw_points(self) -> None:
        """Draw all 24 triangular points on the board."""
        # Left side points (points 13-18 top, 7-12 bottom)
        for i in range(6):
            point_x = self.play_area_x + i * self.point_width

            # Top points (13-18) - pointing down
            color = (
                self.colors["point_light"] if i % 2 == 0 else self.colors["point_dark"]
            )
            self.draw_triangular_point(
                self.screen,
                point_x,
                self.play_area_y,
                self.point_width,
                self.point_height,
                color,
                pointing_up=False,
            )

            # Bottom points (12-7) - pointing up
            color = (
                self.colors["point_dark"] if i % 2 == 0 else self.colors["point_light"]
            )
            self.draw_triangular_point(
                self.screen,
                point_x,
                self.play_area_y + self.play_area_height - self.point_height,
                self.point_width,
                self.point_height,
                color,
                pointing_up=True,
            )

        # Right side points (points 19-24 top, 1-6 bottom)
        right_start_x = self.play_area_x + self.half_width + self.center_gap_width
        for i in range(6):
            point_x = right_start_x + i * self.point_width

            # Top points (19-24) - pointing down
            color = (
                self.colors["point_dark"] if i % 2 == 0 else self.colors["point_light"]
            )
            self.draw_triangular_point(
                self.screen,
                point_x,
                self.play_area_y,
                self.point_width,
                self.point_height,
                color,
                pointing_up=False,
            )

            # Bottom points (6-1) - pointing up
            color = (
                self.colors["point_light"] if i % 2 == 0 else self.colors["point_dark"]
            )
            self.draw_triangular_point(
                self.screen,
                point_x,
                self.play_area_y + self.play_area_height - self.point_height,
                self.point_width,
                self.point_height,
                color,
                pointing_up=True,
            )


def main() -> None:
    """Main function to run the backgammon board display."""
    board = BackgammonBoard()
    clock = pygame.time.Clock()
    running = True

    # Create game instance
    game = BackgammonGame()
    game.setup_initial_position()

    # Set the game instance in the board
    board.set_game(game)

    # Update board from game state
    board.update_from_game()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                running = False
            elif event.type == pygame.KEYDOWN:  # pylint: disable=no-member
                if event.key == pygame.K_ESCAPE:  # pylint: disable=no-member
                    running = False
                elif event.key == pygame.K_SPACE:  # pylint: disable=no-member
                    # Presiona espacio para tirar dados (si corresponde)
                    if game.last_roll is None or not game.available_moves:
                        game.roll_dice()
                        board.update_from_game()
                elif event.key == pygame.K_r:  # pylint: disable=no-member
                    # Press 'r' to reset game
                    game.reset_game()
                    game.setup_initial_position()
                    board.update_from_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
                # Handle mouse clicks on board
                mouse_x, mouse_y = event.pos
                board.handle_board_click(mouse_x, mouse_y)

            # Handle button clicks
            if board.roll_button.handle_event(event):
                # Tirar dados desde botón (si corresponde)
                if game.last_roll is None or not game.available_moves:
                    game.roll_dice()
                    board.update_from_game()

        # Clear screen with a neutral background
        board.screen.fill((50, 50, 50))  # Dark gray background

        # Draw the board
        board.draw_board()

        # Update display
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()  # pylint: disable=no-member


if __name__ == "__main__":
    main()
