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

    def render_board(self) -> None:
        """Render the board skeleton to stdout."""
        print("\n  13 14 15 16 17 18    BAR    19 20 21 22 23 24")
        print(" ┌────────────────────┐     ┌────────────────────┐")
        # Rows for pieces will be added here in the future
        print(" └────────────────────┘     └────────────────────┘")
        print("  12 11 10  9  8  7           6  5  4  3  2  1\n")

    def run(self) -> None:
        """Run a minimal loop showing the board once and exiting."""
        self.render_board()
        # Future: handle user input, rolling dice, making moves, etc.


def run_cli() -> None:
    """Convenience function to run the CLI."""
    BackgammonCLI().run()


if __name__ == "__main__":
    run_cli()
