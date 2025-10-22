"""
Board Renderer Module

This module handles rendering of the backgammon board structure,
including triangular points, borders, center gap, and bear-off area.
"""

from typing import Tuple, Dict

import pygame  # pylint: disable=import-error


class BoardRenderer:
    """Handles rendering of the board structure."""

    def __init__(self, colors: Dict[str, Tuple[int, int, int]]) -> None:
        """
        Initialize the board renderer.

        Args:
            colors: Dictionary of color definitions
        """
        self.colors = colors

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

    def _add_wood_texture(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        base_color: Tuple[int, int, int],
    ) -> None:
        """
        Add wood grain texture to a rectangular area.

        Args:
            surface: Surface to draw on
            x: X position of area
            y: Y position of area
            width: Width of area
            height: Height of area
            base_color: Base color for texture
        """
        # Add wood grain texture
        for i in range(0, width, 8):
            line_color = (
                max(0, base_color[0] - 15),
                max(0, base_color[1] - 15),
                max(0, base_color[2] - 15),
            )
            pygame.draw.line(
                surface,
                line_color,
                (x + i, y),
                (x + i, y + height),
                1,
            )

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

    def draw_center_gap(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        surface: pygame.Surface,
        gap_x: int,
        gap_y: int,
        gap_width: int,
        gap_height: int,
    ) -> None:
        """
        Draw the center gap that divides the board halves.

        Args:
            surface: Surface to draw on
            gap_x: X position of the gap
            gap_y: Y position of the gap
            gap_width: Width of the gap
            gap_height: Height of the gap
        """
        gap_rect = pygame.Rect(gap_x, gap_y, gap_width, gap_height)

        # Fill with darker brown for recessed effect
        pygame.draw.rect(surface, self.colors["center_gap"], gap_rect)

        # Add shadow effect on the left side
        shadow_width = 4
        shadow_rect = pygame.Rect(gap_x, gap_y, shadow_width, gap_height)
        pygame.draw.rect(surface, self.colors["center_gap_shadow"], shadow_rect)

        # Add shadow effect on the right side
        shadow_rect = pygame.Rect(
            gap_x + gap_width - shadow_width,
            gap_y,
            shadow_width,
            gap_height,
        )
        pygame.draw.rect(surface, self.colors["center_gap_shadow"], shadow_rect)

        # Add wood grain texture to the gap
        for i in range(0, gap_width, 6):
            line_color = (
                max(0, self.colors["center_gap"][0] - 10),
                max(0, self.colors["center_gap"][1] - 10),
                max(0, self.colors["center_gap"][2] - 10),
            )
            pygame.draw.line(
                surface,
                line_color,
                (gap_x + i, gap_y),
                (gap_x + i, gap_y + gap_height),
                1,
            )

        # Add horizontal wood grain lines for natural texture
        for y in range(gap_y, gap_y + gap_height, 12):
            line_color = (
                max(0, self.colors["center_gap"][0] - 15),
                max(0, self.colors["center_gap"][1] - 15),
                max(0, self.colors["center_gap"][2] - 15),
            )
            pygame.draw.line(
                surface,
                line_color,
                (gap_x + 2, y),
                (gap_x + gap_width - 2, y),
                1,
            )

    def draw_bear_off_area(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        surface: pygame.Surface,
        bear_off_x: int,
        bear_off_y: int,
        bear_off_width: int,
        bear_off_height: int,
    ) -> None:
        """
        Draw the bear off area where borne-off checkers are placed.

        Args:
            surface: Surface to draw on
            bear_off_x: X position of bear-off area
            bear_off_y: Y position of bear-off area
            bear_off_width: Width of bear-off area
            bear_off_height: Height of bear-off area
        """
        # Calculate zone dimensions
        zone_height = bear_off_height // 2

        # Draw WHITE zone (top) - light wood
        white_zone_rect = pygame.Rect(
            bear_off_x, bear_off_y, bear_off_width, zone_height
        )
        pygame.draw.rect(surface, self.colors["bear_off_bg"], white_zone_rect)

        # Add wood grain texture to white zone
        self._add_wood_texture(
            surface,
            bear_off_x,
            bear_off_y,
            bear_off_width,
            zone_height,
            self.colors["bear_off_bg"],
        )

        # Draw BLACK zone (bottom) - dark wood
        black_zone_rect = pygame.Rect(
            bear_off_x, bear_off_y + zone_height, bear_off_width, zone_height
        )
        # Use darker wood color for black zone
        dark_wood = (
            max(0, self.colors["bear_off_bg"][0] - 40),
            max(0, self.colors["bear_off_bg"][1] - 40),
            max(0, self.colors["bear_off_bg"][2] - 40),
        )
        pygame.draw.rect(surface, dark_wood, black_zone_rect)

        # Add wood grain texture to black zone
        self._add_wood_texture(
            surface,
            bear_off_x,
            bear_off_y + zone_height,
            bear_off_width,
            zone_height,
            dark_wood,
        )

        # Draw border around entire bear off area
        bear_off_rect = pygame.Rect(
            bear_off_x, bear_off_y, bear_off_width, bear_off_height
        )
        pygame.draw.rect(surface, self.colors["bear_off_border"], bear_off_rect, 3)

        # Draw dividing line between zones
        middle_y = bear_off_y + bear_off_height // 2
        pygame.draw.line(
            surface,
            self.colors["bear_off_border"],
            (bear_off_x, middle_y),
            (bear_off_x + bear_off_width, middle_y),
            2,
        )

        # Add labels for the bear off areas
        self._draw_bear_off_labels(
            surface, bear_off_x, bear_off_y, bear_off_width, bear_off_height
        )
        # Slots removed per nueva especificación visual: solo fichas centradas

    def _draw_bear_off_labels(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        surface: pygame.Surface,
        bear_off_x: int,
        bear_off_y: int,
        bear_off_width: int,
        bear_off_height: int,
    ) -> None:
        """Draw labels for the bear off areas."""
        try:
            font = pygame.font.Font(None, 24)

            # White player bear off area (top)
            white_text = font.render("WHITE", True, self.colors["black"])
            white_rect = white_text.get_rect()
            white_rect.center = (
                bear_off_x + bear_off_width // 2,
                bear_off_y + bear_off_height // 4,
            )
            surface.blit(white_text, white_rect)

            # Black player bear off area (bottom)
            black_text = font.render("BLACK", True, self.colors["black"])
            black_rect = black_text.get_rect()
            black_rect.center = (
                bear_off_x + bear_off_width // 2,
                bear_off_y + 3 * bear_off_height // 4,
            )
            surface.blit(black_text, black_rect)

        except pygame.error:  # pylint: disable=no-member
            # If font loading fails, draw simple geometric indicators
            pygame.draw.circle(
                surface,
                self.colors["white"],
                (
                    bear_off_x + bear_off_width // 2,
                    bear_off_y + bear_off_height // 4,
                ),
                8,
            )
            pygame.draw.circle(
                surface,
                self.colors["black"],
                (
                    bear_off_x + bear_off_width // 2,
                    bear_off_y + bear_off_height // 4,
                ),
                8,
                2,
            )

            pygame.draw.circle(
                surface,
                self.colors["black"],
                (
                    bear_off_x + bear_off_width // 2,
                    bear_off_y + 3 * bear_off_height // 4,
                ),
                8,
            )

    # Slots removed per nueva especificación visual: solo fichas centradas

    def draw_points(  # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
        self,
        surface: pygame.Surface,
        play_area_x: int,
        play_area_y: int,
        play_area_height: int,
        point_width: int,
        point_height: int,
        half_width: int,
        center_gap_width: int,
    ) -> None:
        """
        Draw all 24 triangular points on the board.

        Args:
            surface: Surface to draw on
            play_area_x: X position of play area
            play_area_y: Y position of play area
            play_area_height: Height of play area
            point_width: Width of each point
            point_height: Height of each point
            half_width: Width of half board
            center_gap_width: Width of center gap
        """
        # Left side points (points 13-18 top, 7-12 bottom)
        for i in range(6):
            point_x = play_area_x + i * point_width

            # Top points (13-18) - pointing down
            color = (
                self.colors["point_light"] if i % 2 == 0 else self.colors["point_dark"]
            )
            self.draw_triangular_point(
                surface,
                point_x,
                play_area_y,
                point_width,
                point_height,
                color,
                pointing_up=False,
            )

            # Bottom points (12-7) - pointing up
            color = (
                self.colors["point_dark"] if i % 2 == 0 else self.colors["point_light"]
            )
            self.draw_triangular_point(
                surface,
                point_x,
                play_area_y + play_area_height - point_height,
                point_width,
                point_height,
                color,
                pointing_up=True,
            )

        # Right side points (points 19-24 top, 1-6 bottom)
        right_start_x = play_area_x + half_width + center_gap_width
        for i in range(6):
            point_x = right_start_x + i * point_width

            # Top points (19-24) - pointing down
            color = (
                self.colors["point_dark"] if i % 2 == 0 else self.colors["point_light"]
            )
            self.draw_triangular_point(
                surface,
                point_x,
                play_area_y,
                point_width,
                point_height,
                color,
                pointing_up=False,
            )

            # Bottom points (6-1) - pointing up
            color = (
                self.colors["point_light"] if i % 2 == 0 else self.colors["point_dark"]
            )
            self.draw_triangular_point(
                surface,
                point_x,
                play_area_y + play_area_height - point_height,
                point_width,
                point_height,
                color,
                pointing_up=True,
            )

    def draw_highlight(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        surface: pygame.Surface,
        center_x: int,
        center_y: int,
        radius: int,
        color: Tuple[int, int, int],
    ) -> None:
        """
        Draw a highlight circle at the specified position.

        Args:
            surface: Surface to draw on
            center_x: X coordinate of circle center
            center_y: Y coordinate of circle center
            radius: Radius of highlight circle
            color: RGB color tuple
        """
        pygame.draw.circle(surface, color, (center_x, int(center_y)), radius, 3)
