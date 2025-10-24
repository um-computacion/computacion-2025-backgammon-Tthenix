"""Player module for the Backgammon game.

This module contains the Player class that represents a player
in the Backgammon game with their state and actions.
"""


class Player:
    """Represents a player in the Backgammon game.

    A player has a name, color, and tracks their checkers throughout the game.
    """

    TOTAL_CHECKERS = 15

    def __init__(self, name, color):
        """Initialize a new player.

        Args:
            name (str): The player's name.
            color (str): The player's color ('white' or 'black').

        Raises:
            ValueError: If name is empty or color is invalid.
        """
        if not name:
            raise ValueError("The name cannot be empty")

        color = color.lower()
        if color not in ("white", "black"):
            raise ValueError("Color should be 'white' o 'black'")

        self.__name__ = name
        self.__color__ = color
        self.__checkers_count__ = self.TOTAL_CHECKERS
        self.__captured_checkers__ = 0
        self.__bear_off_count__ = 0

    def capture_checker(self):
        """Capture a checker (send it to the bar)."""
        self.__captured_checkers__ += 1
        if self.__checkers_count__ > 0:
            self.__checkers_count__ -= 1

    def release_captured_checker(self):
        """Release a captured checker (return from bar).

        Raises:
            ValueError: If no captured checkers to release.
        """
        if self.__captured_checkers__ <= 0:
            raise ValueError("No captured checkers to release")
        self.__captured_checkers__ -= 1
        self.__checkers_count__ += 1

    def has_captured_checkers(self):
        """Check if player has captured checkers.

        Returns:
            bool: True if player has captured checkers, False otherwise.
        """
        return self.__captured_checkers__ > 0

    def bear_off_checker(self):
        """Bear off a checker (remove from board).

        Raises:
            ValueError: If no checkers available for bear off.
        """
        if self.__checkers_count__ <= 0:
            raise ValueError("No checkers available for bear off")
        self.__checkers_count__ -= 1
        self.__bear_off_count__ += 1

    def can_bear_off(self):
        """Check if player can bear off checkers.

        Returns:
            bool: True if player has checkers to bear off, False otherwise.
        """
        return self.__checkers_count__ > 0

    def is_winner(self):
        """Check if player has won the game.

        Returns:
            bool: True if all checkers are borne off, False otherwise.
        """
        return self.__bear_off_count__ == self.TOTAL_CHECKERS

    def reset(self):
        """Reset player state to initial values."""
        self.__checkers_count__ = self.TOTAL_CHECKERS
        self.__captured_checkers__ = 0
        self.__bear_off_count__ = 0

    def __str__(self):
        """Return string representation of the player.

        Returns:
            str: String with player name, color, and checker counts.
        """
        return (
            f"{self.__name__} ({self.__color__}) - Checkers: {self.__checkers_count__}, "
            f"Captured: {self.__captured_checkers__}, Bear off: {self.__bear_off_count__}"
        )

    def __eq__(self, other):
        """Check equality with another player.

        Args:
            other: Another object to compare with.

        Returns:
            bool: True if players have same name and color, False otherwise.
        """
        return (
            isinstance(other, Player)
            and self.__name__ == other.__name__
            and self.__color__ == other.__color__
        )

    def __hash__(self):
        """Return hash of the player.

        Returns:
            int: Hash based on name and color.
        """
        return hash((self.__name__, self.__color__))
