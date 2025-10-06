"""Minimal entry point to launch the Backgammon game."""

import sys
from cli.cli import run_cli
from pygame_ui.pygame_ui import main as run_pygame_ui


def main() -> None:
    """Run the Backgammon game."""
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        run_pygame_ui()
    else:
        run_cli()


if __name__ == "__main__":
    main()
