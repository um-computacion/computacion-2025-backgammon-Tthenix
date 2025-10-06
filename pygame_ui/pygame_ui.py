"""
Backgammon Pygame UI Module

This module provides a visual representation of a backgammon board using Pygame.
Based on the reference image, it creates a realistic board with proper colors,
triangular points, central bar, and bearing off area.
"""

import sys
from typing import Tuple

import pygame  # pylint: disable=import-error


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

        # Game state - will be set by external game logic
        self.board_state = None

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
        pygame.draw.circle(surface, self.colors["black"], (x, y), self.checker_radius, 2)

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
                self.play_area_x + self.half_width + self.center_gap_width +
                (5 - point_index) * self.point_width
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
                self.play_area_x + self.half_width + self.center_gap_width +
                (point_index - 18) * self.point_width
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
            spacing = (self.point_height - self.checker_radius * 2) // (checker_count - 1)
            spacing = max(spacing, self.checker_radius + 2)

        for i, player in enumerate(checkers):
            if is_top_half:
                # Stack downward from top
                checker_y = self.play_area_y + self.checker_radius + 5 + i * spacing
            else:
                # Stack upward from bottom
                checker_y = (
                    self.play_area_y + self.play_area_height - self.checker_radius - 5 - i * spacing
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
                self.play_area_y + self.play_area_height // 2 +
                20 + i * (self.checker_radius * 2 + 2)
            )
            self.draw_checker(surface, bar_center_x, checker_y, player)

        # Draw player 2 checkers (top half of bar)
        for i, player in enumerate(player2_bar):
            checker_y = (
                self.play_area_y + self.play_area_height // 2 -
                20 - i * (self.checker_radius * 2 + 2)
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
                self.bear_off_y + 3 * self.board_height // 4 +
                row * (self.checker_radius * 2 + 2)
            )
            self.draw_checker(surface, checker_x, checker_y, player)

        # Draw player 2 (black) checkers in top half
        for i, player in enumerate(player2_off):
            row = i // 3  # 3 checkers per row
            col = i % 3
            col_offset = (col - 1) * (self.checker_radius * 2 + 4)
            checker_x = bear_off_center_x + col_offset - self.checker_radius
            checker_y = (
                self.bear_off_y + self.board_height // 4 +
                row * (self.checker_radius * 2 + 2)
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

    # Create initial board state with standard backgammon setup
    initial_state = {
        "points": [[] for _ in range(24)],
        "checker_bar": [[], []],
        "off_board": [[], []],
    }

    # Set up Player 1 pieces (white)
    initial_state["points"][0] = [1, 1]  # Point 1
    initial_state["points"][11] = [1, 1, 1, 1, 1]  # Point 12
    initial_state["points"][16] = [1, 1, 1]  # Point 17
    initial_state["points"][18] = [1, 1, 1, 1, 1]  # Point 19

    # Set up Player 2 pieces (black)
    initial_state["points"][23] = [2, 2]  # Point 24
    initial_state["points"][12] = [2, 2, 2, 2, 2]  # Point 13
    initial_state["points"][7] = [2, 2, 2]  # Point 8
    initial_state["points"][5] = [2, 2, 2, 2, 2]  # Point 6

    # Set the board state
    board.set_board_state(initial_state)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                running = False
            elif event.type == pygame.KEYDOWN:  # pylint: disable=no-member
                if event.key == pygame.K_ESCAPE:  # pylint: disable=no-member
                    running = False

        # Clear screen with a neutral background
        board.screen.fill((50, 50, 50))  # Dark gray background

        # Draw the board
        board.draw_board()

        # Update display
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()  # pylint: disable=no-member
    sys.exit()


if __name__ == "__main__":
    main()
