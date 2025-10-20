"""
Checker Renderer Module

This module handles rendering of checkers on the board,
including checkers on points, bar, and bear-off area.
"""

from typing import Tuple, Dict, List

import pygame  # pylint: disable=import-error


class CheckerRenderer:
    """Handles rendering of checkers."""

    def __init__(
        self, colors: Dict[str, Tuple[int, int, int]], checker_radius: int
    ) -> None:
        """
        Initialize the checker renderer.

        Args:
            colors: Dictionary of color definitions
            checker_radius: Radius of checker circles
        """
        self.colors = colors
        self.checker_radius = checker_radius

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

    def draw_checkers_on_point(  # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals
        self,
        surface: pygame.Surface,
        point_index: int,
        checkers: List[int],
        play_area_x: int,
        play_area_y: int,
        play_area_height: int,
        point_width: int,
        point_height: int,
        half_width: int,
        center_gap_width: int,
    ) -> None:
        """
        Draw checkers stacked on a specific point.

        Args:
            surface: Surface to draw on
            point_index: Point index (0-23)
            checkers: List of player numbers representing checkers on this point
            play_area_x: X position of play area
            play_area_y: Y position of play area
            play_area_height: Height of play area
            point_width: Width of each point
            point_height: Height of each point
            half_width: Width of half board
            center_gap_width: Width of center gap
        """
        if not checkers:
            return

        # Determine if point is on top or bottom half
        is_top_half = point_index >= 12

        # Calculate point X position
        if point_index < 6:
            # Right side, bottom
            point_x = (
                play_area_x
                + half_width
                + center_gap_width
                + (5 - point_index) * point_width
            )
        elif point_index < 12:
            # Left side, bottom
            point_x = play_area_x + (11 - point_index) * point_width
        elif point_index < 18:
            # Left side, top
            point_x = play_area_x + (point_index - 12) * point_width
        else:
            # Right side, top
            point_x = (
                play_area_x
                + half_width
                + center_gap_width
                + (point_index - 18) * point_width
            )

        # Center of the point
        checker_x = point_x + point_width // 2

        # Draw checkers stacked vertically
        max_visible_checkers = 5
        checker_count = len(checkers)

        if checker_count <= max_visible_checkers:
            # Normal spacing
            spacing = self.checker_radius * 2 + 2
        else:
            # Condensed spacing for many checkers
            spacing = (point_height - self.checker_radius * 2) // (checker_count - 1)
            spacing = max(spacing, self.checker_radius + 2)

        for i, player in enumerate(checkers):
            if is_top_half:
                # Stack downward from top
                checker_y = play_area_y + self.checker_radius + 5 + i * spacing
            else:
                # Stack upward from bottom
                checker_y = (
                    play_area_y
                    + play_area_height
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
            pass

    def draw_checkers_on_bar(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        surface: pygame.Surface,
        player1_bar: List[int],
        player2_bar: List[int],
        bar_center_x: int,
        play_area_y: int,
        play_area_height: int,
    ) -> None:
        """
        Draw checkers on the bar (captured pieces).
        """
        # Draw pieces on white side (bottom half of bar)
        # These are pieces that must re-enter from white side (captured black pieces)
        for i, player in enumerate(player1_bar):
            checker_y = (
                play_area_y
                + play_area_height // 2
                + 20
                + i * (self.checker_radius * 2 + 2)
            )
            self.draw_checker(surface, bar_center_x, checker_y, player)

        # Draw pieces on black side (top half of bar)
        # These are pieces that must re-enter from black side (captured white pieces)
        for i, player in enumerate(player2_bar):
            checker_y = (
                play_area_y
                + play_area_height // 2
                - 20
                - i * (self.checker_radius * 2 + 2)
            )
            self.draw_checker(surface, bar_center_x, checker_y, player)

    def draw_borne_off_checkers(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        surface: pygame.Surface,
        player1_off: List[int],
        player2_off: List[int],
        bear_off_center_x: int,
        bear_off_y: int,
        board_height: int,
    ) -> None:
        """
        Draw borne-off checkers in the bear-off area.

        Args:
            surface: Surface to draw on
            player1_off: List of player 1 borne-off checkers
            player2_off: List of player 2 borne-off checkers
            bear_off_center_x: X coordinate of bear-off area center
            bear_off_y: Y position of bear-off area
            board_height: Total board height
        """
        # Draw player 1 (white) checkers in bottom half
        for i, player in enumerate(player1_off):
            row = i // 3  # 3 checkers per row
            col = i % 3
            col_offset = (col - 1) * (self.checker_radius * 2 + 4)
            checker_x = bear_off_center_x + col_offset - self.checker_radius
            checker_y = (
                bear_off_y + 3 * board_height // 4 + row * (self.checker_radius * 2 + 2)
            )
            self.draw_checker(surface, checker_x, checker_y, player)

        # Draw player 2 (black) checkers in top half
        for i, player in enumerate(player2_off):
            row = i // 3  # 3 checkers per row
            col = i % 3
            col_offset = (col - 1) * (self.checker_radius * 2 + 4)
            checker_x = bear_off_center_x + col_offset - self.checker_radius
            checker_y = (
                bear_off_y + board_height // 4 + row * (self.checker_radius * 2 + 2)
            )
            self.draw_checker(surface, checker_x, checker_y, player)
