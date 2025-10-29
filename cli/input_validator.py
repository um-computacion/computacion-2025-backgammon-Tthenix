"""Input validation module for the Backgammon CLI.

This module handles input validation following
the Single Responsibility Principle.
"""

from typing import Optional


class InputValidator:
    """Handles input validation for the CLI.

    This class is responsible only for validating user inputs,
    following SRP.
    """

    def __init__(self):
        """Initialize the input validator."""

    def validate_point(self, point: int) -> bool:
        """Validate a point number.

        Args:
            point: The point number to validate

        Returns:
            True if point is valid, False otherwise
        """
        return 1 <= point <= 24

    def validate_die_value(self, die_value: int) -> bool:
        """Validate a die value.

        Args:
            die_value: The die value to validate

        Returns:
            True if die value is valid, False otherwise
        """
        return 1 <= die_value <= 6

    def parse_int_input(self, input_str: str) -> Optional[int]:
        """Parse and validate integer input.

        Args:
            input_str: The input string to parse

        Returns:
            Parsed integer or None if invalid
        """
        try:
            return int(input_str.strip())
        except ValueError:
            return None

    def validate_move_points(self, from_point: int, to_point: int) -> bool:
        """Validate move points.

        Args:
            from_point: The source point
            to_point: The destination point

        Returns:
            True if both points are valid, False otherwise
        """
        return self.validate_point(from_point) and self.validate_point(to_point)

    def get_validation_error_message(self, input_type: str) -> str:
        """Get error message for invalid input.

        Args:
            input_type: The type of input that was invalid

        Returns:
            Error message string
        """
        error_messages = {
            "point": "[ERROR] Point must be between 1 and 24.",
            "die": "[ERROR] Die value must be between 1 and 6.",
            "move": "[ERROR] Points must be between 1 and 24.",
            "general": "[ERROR] Invalid input. Please enter a valid number.",
        }
        return error_messages.get(input_type, error_messages["general"])
