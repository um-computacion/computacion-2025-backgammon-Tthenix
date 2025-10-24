"""Checker module for the Backgammon game.

This module contains the Checker class that represents individual
checker pieces in the Backgammon game.
"""


class Checker:
    """Represents a single checker piece in Backgammon.

    A checker has a color and can be in various states: on a point,
    on the bar, or borne off the board.
    """

    TOTAL_POINTS = 24

    def __init__(self, color: str) -> None:
        """Initialize a checker with a specified color.

        Args:
            color: The color of the checker ('white' or 'black').

        Raises:
            ValueError: If color is not 'white' or 'black'.
        """
        if color not in ("white", "black"):
            raise ValueError("Color must be 'white' or 'black'")
        self.__color__: str = color
        self.__position__: int | None = None
        self.__is_on_bar__: bool = False
        self.__is_borne_off__: bool = False

    def place_on_point(self, position: int) -> None:
        """Place the checker on a specific point on the board.

        Args:
            position: The point number (1-24) to place the checker.

        Raises:
            ValueError: If position is not between 1 and 24.
        """
        if position < 1 or position > self.TOTAL_POINTS:
            raise ValueError("Position must be between 1 and 24")

        self.__position__ = position
        self.__is_on_bar__ = False
        self.__is_borne_off__ = False

    def move_to_point(self, position: int) -> None:
        """Move the checker to a specific point.

        Args:
            position: The point number (1-24) to move the checker to.

        Raises:
            ValueError: If checker cannot be moved or position is invalid.
        """
        if self.__is_borne_off__:
            raise ValueError("Checker has already been removed from board")
        if self.__is_on_bar__:
            raise ValueError("Checker on bar cannot move directly")
        if self.__position__ is None:
            raise ValueError("Checker must be placed before moving")
        if 1 <= position <= self.TOTAL_POINTS:
            self.__position__ = position
        else:
            raise ValueError("Position must be between 1 and 24")

    def send_to_bar(self) -> None:
        """Send the checker to the bar.

        Raises:
            ValueError: If checker is already on the bar.
        """
        if self.__is_on_bar__:
            raise ValueError("Checker is already on bar")

        self.__position__ = None
        self.__is_on_bar__ = True
        self.__is_borne_off__ = False

    def return_from_bar(self, position: int) -> None:
        """Return the checker from the bar to a specific point.

        Args:
            position: The point number (1-24) to return the checker to.

        Raises:
            ValueError: If checker is not on bar or position is invalid.
        """
        if not self.__is_on_bar__:
            raise ValueError("Checker is not on bar")
        if position < 1 or position > self.TOTAL_POINTS:
            raise ValueError("Position must be between 1 and 24")

        self.__position__ = position
        self.__is_on_bar__ = False
        self.__is_borne_off__ = False

    def bear_off(self) -> None:
        """Remove the checker from the board (bear off).

        Raises:
            ValueError: If checker cannot be borne off.
        """
        if self.__is_borne_off__:
            raise ValueError("Checker has already been removed from board")
        if self.__is_on_bar__:
            raise ValueError("Checker on bar cannot be borne off")
        if self.__position__ is None:
            raise ValueError("Checker must be placed before bearing off")

        self.__position__ = None
        self.__is_on_bar__ = False
        self.__is_borne_off__ = True

    def can_move(self) -> bool:
        """Check if the checker can move.

        Returns:
            bool: True if checker can move, False otherwise.
        """
        return (
            self.__position__ is not None
            and not self.__is_on_bar__
            and not self.__is_borne_off__
        )

    def can_be_captured(self) -> bool:
        """Check if the checker can be captured.

        Returns:
            bool: True if checker can be captured, False otherwise.
        """
        return (
            self.__position__ is not None
            and not self.__is_on_bar__
            and not self.__is_borne_off__
        )

    def reset(self) -> None:
        """Reset the checker to its initial state."""
        self.__position__ = None
        self.__is_on_bar__ = False
        self.__is_borne_off__ = False

    def get_state(self) -> dict:
        """Get the current state of the checker.

        Returns:
            dict: Dictionary containing checker's current state.
        """
        return {
            "color": self.__color__,
            "position": self.__position__,
            "is_on_bar": self.__is_on_bar__,
            "is_borne_off": self.__is_borne_off__,
        }

    def copy(self) -> "Checker":
        """Create a copy of the checker.

        Returns:
            Checker: A new Checker instance with the same state.
        """
        new_checker = Checker(self.__color__)
        new_checker.__position__ = self.__position__
        new_checker.__is_on_bar__ = self.__is_on_bar__
        new_checker.__is_borne_off__ = self.__is_borne_off__
        return new_checker

    def __str__(self) -> str:
        """String representation of the checker.

        Returns:
            str: String representation showing checker state.
        """
        return (
            f"Checker(color={self.__color__}, position={self.__position__}, "
            f"on_bar={self.__is_on_bar__}, borne_off={self.__is_borne_off__})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality with another checker.

        Args:
            other: Another object to compare with.

        Returns:
            bool: True if checkers have same state, False otherwise.
        """
        if not isinstance(other, Checker):
            return False
        return (
            self.__color__ == other.__color__
            and self.__position__ == other.__position__
            and self.__is_on_bar__ == other.__is_on_bar__
            and self.__is_borne_off__ == other.__is_borne_off__
        )

    def __hash__(self) -> int:
        """Generate hash for the checker.

        Returns:
            int: Hash value based on checker state.
        """
        return hash(
            (
                self.__color__,
                self.__position__,
                self.__is_on_bar__,
                self.__is_borne_off__,
            )
        )
