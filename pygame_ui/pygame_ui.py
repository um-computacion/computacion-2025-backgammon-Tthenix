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
    """

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
        }

        # Board layout dimensions
        self.board_margin = 30
        self.border_width = 20
        self.center_gap_width = 40  # Reduced width for natural wooden gap
        self.bear_off_width = 80  # Width for bear off area

        # Calculate main board area (with bear off area)
        self._calculate_dimensions()

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

    def draw_triangular_point(
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
