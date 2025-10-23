"""Command parsing module for the Backgammon CLI.

This module handles command parsing and routing following
the Single Responsibility Principle.
"""

from typing import Callable, Dict, Tuple


class CommandParser:
    """Handles command parsing and routing for the CLI.

    This class is responsible only for parsing user commands
    and routing them to appropriate handlers, following SRP.
    """

    def __init__(self):
        """Initialize the command parser."""
        self._command_handlers: Dict[str, Callable] = {}

    def register_handler(self, command: str, handler: Callable) -> None:
        """Register a command handler.

        Args:
            command: The command string
            handler: The function to handle the command
        """
        self._command_handlers[command] = handler

    def parse_command(self, command: str) -> Tuple[str, list[str]]:
        """Parse a command string into command and arguments.

        Args:
            command: The raw command string from user input

        Returns:
            Tuple of (command, arguments)
        """
        parts = command.split()
        if not parts:
            return "", []

        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        return cmd, args

    def get_handler(self, command: str) -> Callable | None:
        """Get the handler for a command.

        Args:
            command: The command to get handler for

        Returns:
            The handler function or None if not found
        """
        return self._command_handlers.get(command)

    def is_valid_command(self, command: str) -> bool:
        """Check if a command is valid.

        Args:
            command: The command to check

        Returns:
            True if command is valid, False otherwise
        """
        return command in self._command_handlers

    def get_available_commands(self) -> list[str]:
        """Get list of available commands.

        Returns:
            List of available command strings
        """
        return list(self._command_handlers.keys())
