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
        self.game.setup_initial_position()  # Initialize the board
        self._running = False

    def render_board(self) -> None:
        """Render the board skeleton to stdout with current counts."""
        board = self.game.board

        # Helpers to format a point as owner initial + count or blanks
        def fmt_point(idx: int) -> str:
            pieces = board.points[idx]
            if not pieces:
                return "  "
            owner = "W" if pieces[0] == 1 else "B"
            count = len(pieces)
            return f"{owner}{count}" if count < 10 else f"{owner}+"  # cap at +

        # Top half (points 13-24)
        print("\n  13 14 15 16 17 18    BAR    19 20 21 22 23 24")
        print(" ┌────────────────────┐     ┌────────────────────┐")

        left_top = [fmt_point(i) for i in range(12, 18)]  # 13..18
        right_top = [fmt_point(i) for i in range(18, 24)]  # 19..24
        bar_w = len(board.checker_bar[0])
        bar_b = len(board.checker_bar[1])
        print(f"  {' '.join(left_top)}    W:{bar_w}|B:{bar_b}    {' '.join(right_top)}")

        print(" └────────────────────┘     └────────────────────┘")

        # Bottom half (points 12-1)
        # Insert a line showing bottom points counts before labels
        left_bot = [fmt_point(i) for i in range(11, 5, -1)]  # 12..7
        right_bot = [fmt_point(i) for i in range(5, -1, -1)]  # 6..1
        print(f"  {' '.join(left_bot)}               {' '.join(right_bot)}")
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

        # Command dispatch table to reduce return statements
        command_handlers = {
            "q": self._cmd_quit,
            "quit": self._cmd_quit,
            "exit": self._cmd_quit,
            "h": self._cmd_help,
            "help": self._cmd_help,
            "b": self._cmd_board,
            "board": self._cmd_board,
            "t": self._cmd_turn,
            "turn": self._cmd_turn,
            "r": self._cmd_roll,
            "roll": self._cmd_roll,
            "s": self._cmd_status,
            "status": self._cmd_status,
            "mvs": self._cmd_moves,
            "moves": self._cmd_moves,
            "mv": self._cmd_move,
            "move": self._cmd_move,
            "ent": self._cmd_enter,
            "enter": self._cmd_enter,
            "bo": self._cmd_bearoff,
            "bearoff": self._cmd_bearoff,
            "e": self._cmd_end_turn,
            "end": self._cmd_end_turn,
        }

        handler = command_handlers.get(cmd)
        if handler:
            handler()
        else:
            print("Unknown command. Type 'help'.")

    def _print_help(self) -> None:
        """Print available commands."""
        print(
            "\nCommands:\n"
            "  help (h)    Show this help\n"
            "  board (b)   Print board\n"
            "  turn (t)    Show current player\n"
            "  roll (r)    Roll dice for current player\n"
            "  status (s)  Show last roll and remaining moves\n"
            "  moves       Show possible moves (context-aware)\n"
            "  move        Make a move (interactive prompts)\n"
            "  enter       Enter from bar using a die\n"
            "  bearoff     Bear off a checker (if allowed)\n"
            "  end (e)     End current player's turn\n"
            "  quit (q)    Exit\n"
        )

    # ----- Individual command handlers -----
    def _cmd_quit(self) -> None:
        """Handle quit command."""
        self._running = False
        print("Bye.")

    def _cmd_help(self) -> None:
        """Handle help command."""
        self._print_help()

    def _cmd_board(self) -> None:
        """Handle board command."""
        self.render_board()

    def _cmd_turn(self) -> None:
        """Handle turn command."""
        print(
            f"Current player: {self.game.current_player.name} ({self.game.current_player.color})"
        )

    def _cmd_roll(self) -> None:
        """Handle roll command."""
        if self.game.last_roll is not None and self.game.available_moves:
            print("You still have moves left. Use them or 'end' the turn.")
            return
        roll = self.game.roll_dice()
        print(f"Rolled: {roll[0]} and {roll[1]} | moves: {self.game.available_moves}")

    def _cmd_status(self) -> None:
        """Handle status command."""
        print(f"Last roll: {self.game.last_roll} | moves: {self.game.available_moves}")

    # ----- Command handlers -----
    def _prompt_int(self, message: str) -> int | None:
        try:
            value = int(input(message).strip())
            return value
        except ValueError:
            print("Please enter a number.")
            return None

    def _cmd_moves(self) -> None:
        if self.game.last_roll is None:
            print("Roll first.")
            return
        if self.game.must_enter_from_bar():
            print("You must enter from bar. Use 'enter'.")
            return

        # Show available points with pieces
        player_num = 1 if self.game.current_player == self.game.player1 else 2
        available_points = []
        for i in range(24):
            if self.game.board.points[i] and self.game.board.points[i][0] == player_num:
                available_points.append(i + 1)  # Convert to 1-based

        if not available_points:
            print("No pieces available to move.")
            return

        print(f"Available points with your pieces: {available_points}")
        point_1b = self._prompt_int("From point (1-24): ")
        if point_1b is None:
            return
        if not 1 <= point_1b <= 24:
            print("Point must be 1-24.")
            return
        from_point = point_1b - 1
        dests = self.game.get_possible_destinations(from_point)
        if not dests:
            print("No destinations.")
            return
        # Display as 1-based
        print("Destinations:", [d + 1 for d in dests])

    def _cmd_move(self) -> None:
        if self.game.last_roll is None:
            print("Roll first.")
            return
        if self.game.must_enter_from_bar():
            print("You must enter from bar first. Use 'enter'.")
            return
        from_1b = self._prompt_int("From (1-24): ")
        to_1b = self._prompt_int("To (1-24): ")
        if from_1b is None or to_1b is None:
            return
        if not 1 <= from_1b <= 24 and 1 <= to_1b <= 24:
            print("Points must be 1-24.")
            return
        ok = self.game.make_move(from_1b - 1, to_1b - 1)
        if not ok:
            print("Illegal move.")
            return
        print("Moved.")
        self.render_board()
        if not self.game.available_moves:
            print("No moves left. 'end' to switch player.")

    def _cmd_enter(self) -> None:
        if self.game.last_roll is None:
            print("Roll first.")
            return
        if not self.game.must_enter_from_bar():
            print("No checkers on bar.")
            return
        die = self._prompt_int("Die value to use: ")
        if die is None:
            return
        ok = self.game.move_from_bar(die)
        if not ok:
            print("Cannot enter with that die.")
            return
        print("Entered from bar.")
        self.render_board()
        if not self.game.available_moves:
            print("No moves left. 'end' to switch player.")

    def _cmd_bearoff(self) -> None:
        if self.game.last_roll is None:
            print("Roll first.")
            return
        point_1b = self._prompt_int("From point to bear off (1-24): ")
        if point_1b is None:
            return
        if not 1 <= point_1b <= 24:
            print("Point must be 1-24.")
            return
        ok = self.game.bear_off_checker(point_1b - 1)
        if not ok:
            print("Cannot bear off from there.")
            return
        print("Borne off.")
        self.render_board()
        if not self.game.available_moves:
            print("No moves left. 'end' to switch player.")

    def _cmd_end_turn(self) -> None:
        # Reset dice for next player and switch
        self.game.last_roll = None
        self.game.available_moves = []
        self.game.switch_current_player()
        print(
            f"Now it's {self.game.current_player.name} ({self.game.current_player.color})"
        )


def run_cli() -> None:
    """Convenience function to run the CLI."""
    BackgammonCLI().run()


if __name__ == "__main__":
    run_cli()
