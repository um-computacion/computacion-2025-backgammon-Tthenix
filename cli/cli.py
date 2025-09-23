"""Command-line interface skeleton for Backgammon.

Provides a minimal interactive loop and a board renderer that prints
an ASCII layout. This is a skeleton; game actions will be added later.
"""

from typing import Optional

from core import BackgammonGame


class BackgammonCLI:
    """Minimal CLI wrapper for the Backgammon game."""

    def __init__(self, game: Optional[BackgammonGame] = None) -> None:
        """Create the CLI with an existing game or a new one."""
        self.game = game or BackgammonGame()
        self._running = False

    def render_board(self) -> None:
        """Render the board skeleton to stdout."""
        print("\n  13 14 15 16 17 18    BAR    19 20 21 22 23 24")
        print(" ┌────────────────────┐     ┌────────────────────┐")
        # Rows for pieces will be added here in the future
        print(" └────────────────────┘     └────────────────────┘")
        print("  12 11 10  9  8  7           6  5  4  3  2  1\n")

    def run(self) -> None:
        """Start the interactive CLI loop."""
        self._running = True
        print("Backgammon CLI - type 'help' for commands.\n")
        self.render_board()
        while self._running:
            try:
                command = input("> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting.")
                break
            if not command:
                continue
            self._handle_command(command)
        self._running = False

    def _handle_command(self, command: str) -> None:
        """Parse and execute a single command."""
        parts = command.split()
        cmd = parts[0].lower()
        # args reserved for future subcommands
        # args = parts[1:]

        if cmd in {"q", "quit", "exit"}:
            self._running = False
            print("Bye.")
            return
        if cmd in {"h", "help"}:
            self._print_help()
            return
        if cmd in {"b", "board"}:
            self.render_board()
            return
        if cmd in {"t", "turn"}:
            print(
                f"Current player:{self.game.current_player.name} ({self.game.current_player.color})"
            )
            return
        if cmd in {"r", "roll"}:
            roll = self.game.roll_dice()
            print(
                f"Rolled: {roll[0]} and {roll[1]} | moves: {self.game.available_moves}"
            )
            return

        print("Unknown command. Type 'help'.")

    def _print_help(self) -> None:
        """Print available commands."""
        print(
            "\nCommands:\n"
            "  help (h)    Show this help\n"
            "  board (b)   Print board\n"
            "  turn (t)    Show current player\n"
            "  roll (r)    Roll dice for current player\n"
            "  quit (q)    Exit\n"
        )


def run_cli() -> None:
    """Convenience function to run the CLI."""
    BackgammonCLI().run()


if __name__ == "__main__":
    run_cli()
