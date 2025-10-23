"""User interface module for the Backgammon CLI.

This module handles user interactions following
the Single Responsibility Principle.
"""

from typing import Optional


class UserInterface:
    """Handles user interface interactions for the CLI.

    This class is responsible only for user input/output
    operations, following SRP.
    """

    def __init__(self):
        """Initialize the user interface."""

    def prompt_int(self, message: str) -> Optional[int]:
        """Prompt user for integer input.

        Args:
            message: The prompt message

        Returns:
            Parsed integer or None if invalid
        """
        try:
            value = int(input(message).strip())
            return value
        except ValueError:
            print("[ERROR] Invalid input. Please enter a valid number.")
            return None

    def prompt_string(self, message: str) -> str:
        """Prompt user for string input.

        Args:
            message: The prompt message

        Returns:
            User input string
        """
        return input(message).strip()

    def display_message(self, message: str) -> None:
        """Display a message to the user.

        Args:
            message: The message to display
        """
        print(message)

    def display_error(self, message: str) -> None:
        """Display an error message to the user.

        Args:
            message: The error message to display
        """
        print(f"[ERROR] {message}")

    def display_success(self, message: str) -> None:
        """Display a success message to the user.

        Args:
            message: The success message to display
        """
        print(f"[SUCCESS] {message}")

    def display_info(self, message: str) -> None:
        """Display an info message to the user.

        Args:
            message: The info message to display
        """
        print(f"[INFO] {message}")

    def display_warning(self, message: str) -> None:
        """Display a warning message to the user.

        Args:
            message: The warning message to display
        """
        print(f"[!] {message}")

    def display_separator(self, char: str = "-", length: int = 60) -> None:
        """Display a separator line.

        Args:
            char: Character to use for separator
            length: Length of the separator line
        """
        print(char * length)

    def display_header(self, title: str, char: str = "=", length: int = 60) -> None:
        """Display a header with title.

        Args:
            title: The header title
            char: Character to use for border
            length: Length of the header
        """
        print("\n" + char * length)
        print(f"  {title}")
        print(char * length)

    def display_game_over(self, winner) -> None:
        """Display game over message.

        Args:
            winner: The winner player object
        """
        self.display_header("GAME OVER!")
        self.display_message(f"  WINNER: {winner.name} ({winner.color})")
        self.display_separator("=")
        self.display_message("  Type 'quit' to exit")
        self.display_separator("=")

    def display_turn_info(self, current_player) -> None:
        """Display current turn information.

        Args:
            current_player: The current player object
        """
        self.display_header(
            f"CURRENT TURN: {current_player.name} ({current_player.color})"
        )

    def display_turn_ending(self, ending_player) -> None:
        """Display turn ending message.

        Args:
            ending_player: The player whose turn is ending
        """
        self.display_separator()
        self.display_message(f"  {ending_player.name}'s turn has ended")
        self.display_separator()

    def display_new_turn(self, new_player) -> None:
        """Display new turn message.

        Args:
            new_player: The player whose turn is starting
        """
        self.display_header(f"{new_player.name} ({new_player.color})'s turn begins")
        self.display_message("  Type 'roll' to roll the dice")
        self.display_separator("=")
