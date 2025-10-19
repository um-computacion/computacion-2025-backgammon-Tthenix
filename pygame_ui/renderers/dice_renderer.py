"""
Dice Renderer Module

This module handles rendering of dice on the backgammon board.
"""

from typing import Tuple, Dict, Optional

import pygame  # pylint: disable=import-error


class DiceRenderer:
    """Handles rendering of dice."""

    def __init__(
        self,
        colors: Dict[str, Tuple[int, int, int]],
        dice_size: int,
        dice_dot_radius: int,
    ) -> None:
        """
        Initialize the dice renderer.

        Args:
            colors: Dictionary of color definitions
            dice_size: Size of dice (width and height)
            dice_dot_radius: Radius of dice dots
        """
        self.colors = colors
        self.dice_size = dice_size
        self.dice_dot_radius = dice_dot_radius

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
        self._draw_dots_for_value(surface, value, center_x, center_y, offset)

    def _draw_dots_for_value(  # pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-branches
        self,
        surface: pygame.Surface,
        value: int,
        center_x: int,
        center_y: int,
        offset: int,
    ) -> None:
        """
        Draw dots on a die face based on the value.

        Args:
            surface: Surface to draw on
            value: Die value (1-6)
            center_x: X coordinate of die center
            center_y: Y coordinate of die center
            offset: Offset for dot positions
        """
        if value == 1:
            self._draw_dot(surface, center_x, center_y)
        elif value == 2:
            self._draw_dot(surface, center_x - offset, center_y - offset)
            self._draw_dot(surface, center_x + offset, center_y + offset)
        elif value == 3:
            self._draw_dot(surface, center_x - offset, center_y - offset)
            self._draw_dot(surface, center_x, center_y)
            self._draw_dot(surface, center_x + offset, center_y + offset)
        elif value == 4:
            self._draw_dot(surface, center_x - offset, center_y - offset)
            self._draw_dot(surface, center_x + offset, center_y - offset)
            self._draw_dot(surface, center_x - offset, center_y + offset)
            self._draw_dot(surface, center_x + offset, center_y + offset)
        elif value == 5:
            self._draw_dot(surface, center_x - offset, center_y - offset)
            self._draw_dot(surface, center_x + offset, center_y - offset)
            self._draw_dot(surface, center_x, center_y)
            self._draw_dot(surface, center_x - offset, center_y + offset)
            self._draw_dot(surface, center_x + offset, center_y + offset)
        elif value == 6:
            self._draw_dot(surface, center_x - offset, center_y - offset)
            self._draw_dot(surface, center_x - offset, center_y)
            self._draw_dot(surface, center_x - offset, center_y + offset)
            self._draw_dot(surface, center_x + offset, center_y - offset)
            self._draw_dot(surface, center_x + offset, center_y)
            self._draw_dot(surface, center_x + offset, center_y + offset)

    def _draw_dot(self, surface: pygame.Surface, x: int, y: int) -> None:
        """
        Draw a single dot on a die face.

        Args:
            surface: Surface to draw on
            x: X coordinate of dot center
            y: Y coordinate of dot center
        """
        pygame.draw.circle(
            surface,
            self.colors["dice_dot"],
            (x, y),
            self.dice_dot_radius,
        )

    def draw_dice(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        surface: pygame.Surface,
        dice_values: Optional[Tuple[int, int]],
        dice_x: int,
        dice_y: int,
    ) -> None:
        """
        Draw the dice on the board if dice values are set.

        Args:
            surface: Surface to draw on
            dice_values: Tuple of (die1, die2) or None
            dice_x: Base X position for dice
            dice_y: Base Y position for dice
        """
        if not dice_values:
            return

        die1, die2 = dice_values

        # Si es doble, mostrar cuatro dados con el mismo valor; si no, dos dados
        if die1 == die2:
            values = [die1, die1, die1, die1]
        else:
            values = [die1, die2]

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
            self.draw_die_face(surface, dice_x + off_x, dice_y + off_y, val)
