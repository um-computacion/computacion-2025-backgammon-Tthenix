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

        # Display current turn prominently
        current_player = self.game.current_player
        print("\n" + "=" * 60)
        print(f"  CURRENT TURN: {current_player.name} ({current_player.color})")
        print("=" * 60)

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
        print(" +--------------------+     +--------------------+")

        left_top = [fmt_point(i) for i in range(12, 18)]  # 13..18
        right_top = [fmt_point(i) for i in range(18, 24)]  # 19..24
        bar_w = len(board.checker_bar[0])
        bar_b = len(board.checker_bar[1])
        print(f"  {' '.join(left_top)}    W:{bar_w}|B:{bar_b}    {' '.join(right_top)}")

        print(" +--------------------+     +--------------------+")

        # Bottom half (points 12-1)
        # Insert a line showing bottom points counts before labels
        left_bot = [fmt_point(i) for i in range(11, 5, -1)]  # 12..7
        right_bot = [fmt_point(i) for i in range(5, -1, -1)]  # 6..1
        print(f"  {' '.join(left_bot)}               {' '.join(right_bot)}")
        print("  12 11 10  9  8  7           6  5  4  3  2  1")

        # Display borne off checkers
        white_off = len(board.off_board[0])
        black_off = len(board.off_board[1])
        print(f"\n  Bearing off - White: {white_off} | Black: {black_off}")
        print("=" * 60 + "\n")

    def run(self) -> None:
        """Start the interactive CLI loop."""
        self._running = True
        print("\n" + "=" * 60)
        print("  BACKGAMMON GAME")
        print("=" * 60)
        print("  Type 'help' or 'h' for available commands")
        print("=" * 60)
        self.render_board()
        while self._running:
            try:
                # Show current player in prompt
                current_player = self.game.current_player
                prompt = f"[{current_player.name} - {current_player.color}] > "
                command = input(prompt).strip()
            except (EOFError, KeyboardInterrupt):
                print("\n\nExiting game. Thanks for playing!")
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
        print("\n" + "-" * 60)
        print("  AVAILABLE COMMANDS")
        print("-" * 60)
        print("  help (h)      - Show this help menu")
        print("  board (b)     - Display the game board")
        print("  turn (t)      - Show current player information")
        print("  roll (r)      - Roll dice for current player")
        print("  status (s)    - Show last roll and remaining moves")
        print("  moves (mvs)   - Show possible moves (context-aware)")
        print("  move (mv)     - Make a move (interactive prompts)")
        print("  enter (ent)   - Enter a checker from the bar")
        print("  bearoff (bo)  - Bear off a checker (if allowed)")
        print("  end (e)       - End current player's turn")
        print("  quit (q)      - Exit the game")
        print("-" * 60 + "\n")

    # ----- Individual command handlers -----
    def _cmd_quit(self) -> None:
        """Handle quit command."""
        self._running = False
        print("\nThanks for playing Backgammon! Goodbye.")

    def _cmd_help(self) -> None:
        """Handle help command."""
        self._print_help()

    def _cmd_board(self) -> None:
        """Handle board command."""
        self.render_board()

    def _cmd_turn(self) -> None:
        """Handle turn command."""
        current_player = self.game.current_player
        print("\n" + "-" * 60)
        print(f"  CURRENT TURN: {current_player.name} ({current_player.color})")
        print("-" * 60)

        # Show additional turn status
        if self.game.last_roll:
            print(f"  Last roll: {self.game.last_roll}")
            print(f"  Available moves: {self.game.available_moves}")
        else:
            print("  No dice rolled yet")
            print("  Use 'roll' command to start your turn")
        print("-" * 60 + "\n")

    def _cmd_roll(self) -> None:
        """Handle roll command."""
        if self.game.last_roll is not None and self.game.available_moves:
            print("\n[!] You still have moves left.")
            print("    Use your remaining moves or type 'end' to finish your turn.\n")
            return
        roll = self.game.roll_dice()
        print(f"\n[DICE] Rolled: {roll[0]} and {roll[1]}")
        print(f"[INFO] Available moves: {self.game.available_moves}\n")

    def _cmd_status(self) -> None:
        """Handle status command."""
        print("\n" + "-" * 60)
        print("  GAME STATUS")
        print("-" * 60)
        print(f"  Last roll: {self.game.last_roll if self.game.last_roll else 'None'}")
        print(f"  Remaining moves: {self.game.available_moves}")
        print("-" * 60 + "\n")

    def _check_game_over(self) -> None:
        """Check and announce game over if a player has won."""
        if self.game.is_game_over():
            winner = self.game.get_winner()
            if winner is not None:
                print("\n" + "=" * 60)
                print("  GAME OVER!")
                print("=" * 60)
                print(f"  WINNER: {winner.name} ({winner.color})")
                print("=" * 60)
                print("  Type 'quit' to exit")
                print("=" * 60 + "\n")

    # ----- Command handlers -----
    def _prompt_int(self, message: str) -> int | None:
        try:
            value = int(input(message).strip())
            return value
        except ValueError:
            print("[ERROR] Invalid input. Please enter a valid number.")
            return None

    def _cmd_moves(self) -> None:
        if self.game.last_roll is None:
            print("\n[!] You must roll the dice first.\n")
            return
        if self.game.must_enter_from_bar():
            print("\n[!] You have checkers on the bar.")
            print("    Use 'enter' command to enter them first.\n")
            return

        # Show available points with pieces
        player_num = 1 if self.game.current_player == self.game.player1 else 2
        available_points = []
        for i in range(24):
            if self.game.board.points[i] and self.game.board.points[i][0] == player_num:
                available_points.append(i + 1)  # Convert to 1-based

        if not available_points:
            print("\n[INFO] No pieces available to move.\n")
            return

        print(f"\n[INFO] Points with your pieces: {available_points}")
        point_1b = self._prompt_int("Enter point number (1-24): ")
        if point_1b is None:
            return
        if not 1 <= point_1b <= 24:
            print("[ERROR] Point must be between 1 and 24.\n")
            return
        from_point = point_1b - 1
        dests = self.game.get_possible_destinations(from_point)
        if not dests:
            print("[INFO] No valid destinations from this point.\n")
            return
        # Display as 1-based
        print(f"[INFO] Possible destinations: {[d + 1 for d in dests]}\n")

    def _cmd_move(self) -> None:
        if self.game.last_roll is None:
            print("\n[!] You must roll the dice first.\n")
            return
        if self.game.must_enter_from_bar():
            print("\n[!] You have checkers on the bar.")
            print("    Use 'enter' command to enter them first.\n")
            return
        from_1b = self._prompt_int("Move from point (1-24): ")
        to_1b = self._prompt_int("Move to point (1-24): ")
        if from_1b is None or to_1b is None:
            return
        if not 1 <= from_1b <= 24 and 1 <= to_1b <= 24:
            print("[ERROR] Points must be between 1 and 24.\n")
            return
        ok = self.game.make_move(from_1b - 1, to_1b - 1)
        if not ok:
            print("\n[ERROR] Illegal move. Please try again.\n")
            return
        print("\n[SUCCESS] Move completed.")
        self.render_board()
        self._check_game_over()
        if not self.game.available_moves:
            print("[INFO] No moves remaining. Type 'end' to finish your turn.\n")

    def _cmd_enter(self) -> None:
        if self.game.last_roll is None:
            print("\n[!] You must roll the dice first.\n")
            return
        if not self.game.must_enter_from_bar():
            print("\n[INFO] You have no checkers on the bar.\n")
            return
        print(f"[INFO] Available dice: {self.game.available_moves}")
        die = self._prompt_int("Enter die value to use: ")
        if die is None:
            return
        ok = self.game.move_from_bar(die)
        if not ok:
            print("\n[ERROR] Cannot enter with that die value.\n")
            return
        print("\n[SUCCESS] Checker entered from bar.")
        self.render_board()
        self._check_game_over()
        if not self.game.available_moves:
            print("[INFO] No moves remaining. Type 'end' to finish your turn.\n")

    def _cmd_bearoff(self) -> None:
        if self.game.last_roll is None:
            print("\n[!] You must roll the dice first.\n")
            return
        point_1b = self._prompt_int("Bear off from point (1-24): ")
        if point_1b is None:
            return
        if not 1 <= point_1b <= 24:
            print("[ERROR] Point must be between 1 and 24.\n")
            return
        ok = self.game.bear_off_checker(point_1b - 1)
        if not ok:
            print("\n[ERROR] Cannot bear off from that point.\n")
            return
        print("\n[SUCCESS] Checker borne off.")
        self.render_board()
        self._check_game_over()
        if not self.game.available_moves:
            print("[INFO] No moves remaining. Type 'end' to finish your turn.\n")

    def _cmd_end_turn(self) -> None:
        """Handle end turn command."""
        # If game is over, announce and do not switch
        if self.game.is_game_over():
            self._check_game_over()
            return

        # Show turn ending message
        ending_player = self.game.current_player
        print("\n" + "-" * 60)
        print(f"  {ending_player.name}'s turn has ended")
        print("-" * 60)

        # Reset dice for next player and switch
        self.game.last_roll = None
        self.game.available_moves = []
        self.game.switch_current_player()

        # Show new turn with visual separator
        new_player = self.game.current_player
        print("\n" + "=" * 60)
        print(f"  {new_player.name} ({new_player.color})'s turn begins")
        print("=" * 60)
        print("  Type 'roll' to roll the dice")
        print("=" * 60 + "\n")


def run_cli() -> None:
    """Convenience function to run the CLI."""
    BackgammonCLI().run()


if __name__ == "__main__":
    run_cli()
