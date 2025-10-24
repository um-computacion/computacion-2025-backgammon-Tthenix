"""
Button Component Module

This module provides a simple button class for pygame UI interactions.
"""

from typing import Tuple

import pygame  # pylint: disable=import-error


class Button:
    """A simple button class for pygame UI."""

    def __init__(  # pylint: disable=too-many-arguments,too-many-positional-arguments
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
        self.__rect__ = pygame.Rect(x, y, width, height)
        self.__text__ = text
        self.__color__ = color
        self.__hover_color__ = hover_color
        self.__text_color__ = text_color
        self.__is_hovered__ = False

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the button on the surface.

        Args:
            surface: Surface to draw on
        """
        # Choose color based on hover state
        current_color = self.__hover_color__ if self.__is_hovered__ else self.__color__

        # Draw button background with rounded corners
        pygame.draw.rect(surface, current_color, self.__rect__, border_radius=10)

        # Draw button border
        border_color = (0, 0, 0)
        pygame.draw.rect(surface, border_color, self.__rect__, 3, border_radius=10)

        # Draw button text
        try:
            font = pygame.font.Font(None, 28)
            text_surface = font.render(self.__text__, True, self.__text_color__)
            text_rect = text_surface.get_rect(center=self.__rect__.center)
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
            self.__is_hovered__ = self.__rect__.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
            if event.button == 1 and self.__rect__.collidepoint(event.pos):
                return True
        return False
