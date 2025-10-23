"""Command-line interface for Backgammon.

Refactored to follow SOLID principles with proper separation of concerns.
"""

from typing import Optional
from core import BackgammonGame
from cli.board_renderer import BoardRenderer
from cli.command_parser import CommandParser
from cli.input_validator import InputValidator
from cli.game_controller import GameController
from cli.user_interface import UserInterface


class BackgammonCLI:
    """Main CLI coordinator following SOLID principles.

    This class now acts as a coordinator, delegating responsibilities
    to specialized classes, following the Single Responsibility Principle.
    """

    def __init__(self, game: Optional[BackgammonGame] = None) -> None:
        """Create the CLI with proper dependency injection."""
        self.game = game or BackgammonGame()
        self.game.setup_initial_position()
        self._running = False

        # Initialize components following Dependency Inversion Principle
        self.board_renderer = BoardRenderer()
        self.command_parser = CommandParser()
        self.input_validator = InputValidator()
        self.game_controller = GameController(self.game)
        self.user_interface = UserInterface()

        # Register command handlers
        self._register_commands()

    def _register_commands(self) -> None:
        """Register all command handlers following Open/Closed Principle."""
        commands = {
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

        for cmd, handler in commands.items():
            self.command_parser.register_handler(cmd, handler)

    def render_board(self) -> None:
        """Render the board using the BoardRenderer component."""
        self.board_renderer.render_board(self.game)

    def run(self) -> None:
        """Start the interactive CLI loop."""
        self._running = True
        self.user_interface.display_header("BACKGAMMON GAME")
        self.user_interface.display_message(
            "  Type 'help' or 'h' for available commands"
        )
        self.user_interface.display_separator("=")
        self.render_board()

        while self._running:
            try:
                current_player = self.game_controller.get_current_player()
                prompt = f"[{current_player.name} - {current_player.color}] > "
                command = self.user_interface.prompt_string(prompt)
            except (EOFError, KeyboardInterrupt):
                self.user_interface.display_message(
                    "\n\nExiting game. Thanks for playing!"
                )
                break
            if not command:
                continue
            self._handle_command(command)
        self._running = False

    def _handle_command(self, command: str) -> None:
        """Parse and execute a single command using CommandParser."""
        cmd, _ = self.command_parser.parse_command(command)
        handler = self.command_parser.get_handler(cmd)

        if handler:
            handler()
        else:
            self.user_interface.display_error("Unknown command. Type 'help'.")

    def _print_help(self) -> None:
        """Print available commands using UserInterface."""
        self.user_interface.display_separator()
        self.user_interface.display_message("  AVAILABLE COMMANDS")
        self.user_interface.display_separator()
        self.user_interface.display_message("  help (h)      - Show this help menu")
        self.user_interface.display_message("  board (b)     - Display the game board")
        self.user_interface.display_message(
            "  turn (t)      - Show current player information"
        )
        self.user_interface.display_message(
            "  roll (r)      - Roll dice for current player"
        )
        self.user_interface.display_message(
            "  status (s)    - Show last roll and remaining moves"
        )
        self.user_interface.display_message(
            "  moves (mvs)   - Show possible moves (context-aware)"
        )
        self.user_interface.display_message(
            "  move (mv)     - Make a move (interactive prompts)"
        )
        self.user_interface.display_message(
            "  enter (ent)   - Enter a checker from the bar"
        )
        self.user_interface.display_message(
            "  bearoff (bo)  - Bear off a checker (if allowed)"
        )
        self.user_interface.display_message(
            "  end (e)       - End current player's turn"
        )
        self.user_interface.display_message("  quit (q)      - Exit the game")
        self.user_interface.display_separator()

    # ----- Individual command handlers -----
    def _cmd_quit(self) -> None:
        """Handle quit command."""
        self._running = False
        self.user_interface.display_message("\nThanks for playing Backgammon! Goodbye.")

    def _cmd_help(self) -> None:
        """Handle help command."""
        self._print_help()
        self.board_renderer.render_help()

    def _cmd_board(self) -> None:
        """Handle board command."""
        self.render_board()

    def _cmd_turn(self) -> None:
        """Handle turn command."""
        current_player = self.game_controller.get_current_player()
        self.user_interface.display_turn_info(current_player)

        # Show additional turn status
        game_state = self.game_controller.get_game_state()
        if game_state["last_roll"]:
            self.user_interface.display_message(
                f"  Last roll: {game_state['last_roll']}"
            )
            self.user_interface.display_message(
                f"  Available moves: {game_state['available_moves']}"
            )
        else:
            self.user_interface.display_message("  No dice rolled yet")
            self.user_interface.display_message(
                "  Use 'roll' command to start your turn"
            )
        self.user_interface.display_separator()

    def _cmd_roll(self) -> None:
        """Handle roll command."""
        game_state = self.game_controller.get_game_state()
        if game_state["last_roll"] is not None and game_state["available_moves"]:
            self.user_interface.display_warning("You still have moves left.")
            self.user_interface.display_message(
                "    Use your remaining moves or type 'end' to finish your turn."
            )
            return

        roll = self.game_controller.roll_dice()
        self.user_interface.display_message(f"\n[DICE] Rolled: {roll[0]} and {roll[1]}")
        self.user_interface.display_info(
            f"Available moves: {self.game_controller.get_game_state()['available_moves']}"
        )

    def _cmd_status(self) -> None:
        """Handle status command."""
        self.board_renderer.render_game_status(self.game)

    def _check_game_over(self) -> None:
        """Check and announce game over if a player has won."""
        if self.game_controller.is_game_over():
            winner = self.game_controller.get_winner()
            if winner is not None:
                self.user_interface.display_game_over(winner)

    # ----- Command handlers -----

    def _cmd_moves(self) -> None:
        game_state = self.game_controller.get_game_state()
        if game_state["last_roll"] is None:
            self.user_interface.display_warning("You must roll the dice first.")
            return

        if self.game_controller.must_enter_from_bar():
            self.user_interface.display_warning("You have checkers on the bar.")
            self.user_interface.display_message(
                "    Use 'enter' command to enter them first."
            )
            return

        # Show available points with pieces
        current_player = self.game_controller.get_current_player()
        player_num = 1 if current_player == self.game.player1 else 2
        available_points = self.game_controller.get_available_points_with_pieces(
            player_num
        )

        if not available_points:
            self.user_interface.display_info("No pieces available to move.")
            return

        self.user_interface.display_info(
            f"Points with your pieces: {[p + 1 for p in available_points]}"
        )
        point_1b = self.user_interface.prompt_int("Enter point number (1-24): ")

        if point_1b is None:
            return

        if not self.input_validator.validate_point(point_1b):
            self.user_interface.display_error(
                self.input_validator.get_validation_error_message("point")
            )
            return

        from_point = point_1b - 1
        dests = self.game_controller.get_possible_destinations(from_point)

        if not dests:
            self.user_interface.display_info("No valid destinations from this point.")
            return

        # Display as 1-based
        self.user_interface.display_info(
            f"Possible destinations: {[d + 1 for d in dests]}"
        )

    def _cmd_move(self) -> None:
        game_state = self.game_controller.get_game_state()
        if game_state["last_roll"] is None:
            self.user_interface.display_warning("You must roll the dice first.")
            return

        if self.game_controller.must_enter_from_bar():
            self.user_interface.display_warning("You have checkers on the bar.")
            self.user_interface.display_message(
                "    Use 'enter' command to enter them first."
            )
            return

        from_1b = self.user_interface.prompt_int("Move from point (1-24): ")
        to_1b = self.user_interface.prompt_int("Move to point (1-24): ")

        if from_1b is None or to_1b is None:
            return

        if not self.input_validator.validate_move_points(from_1b, to_1b):
            self.user_interface.display_error(
                self.input_validator.get_validation_error_message("move")
            )
            return

        success = self.game_controller.make_move(from_1b - 1, to_1b - 1)
        if not success:
            self.user_interface.display_error("Illegal move. Please try again.")
            return

        self.user_interface.display_success("Move completed.")
        self.render_board()
        self._check_game_over()

        if not self.game_controller.get_game_state()["available_moves"]:
            self.user_interface.display_info(
                "No moves remaining. Type 'end' to finish your turn."
            )

    def _cmd_enter(self) -> None:
        game_state = self.game_controller.get_game_state()
        if game_state["last_roll"] is None:
            self.user_interface.display_warning("You must roll the dice first.")
            return

        if not self.game_controller.must_enter_from_bar():
            self.user_interface.display_info("You have no checkers on the bar.")
            return

        self.user_interface.display_info(
            f"Available dice: {game_state['available_moves']}"
        )
        die = self.user_interface.prompt_int("Enter die value to use: ")

        if die is None:
            return

        if not self.input_validator.validate_die_value(die):
            self.user_interface.display_error(
                self.input_validator.get_validation_error_message("die")
            )
            return

        success = self.game_controller.move_from_bar(die)
        if not success:
            self.user_interface.display_error("Cannot enter with that die value.")
            return

        self.user_interface.display_success("Checker entered from bar.")
        self.render_board()
        self._check_game_over()

        if not self.game_controller.get_game_state()["available_moves"]:
            self.user_interface.display_info(
                "No moves remaining. Type 'end' to finish your turn."
            )

    def _cmd_bearoff(self) -> None:
        game_state = self.game_controller.get_game_state()
        if game_state["last_roll"] is None:
            self.user_interface.display_warning("You must roll the dice first.")
            return

        point_1b = self.user_interface.prompt_int("Bear off from point (1-24): ")
        if point_1b is None:
            return

        if not self.input_validator.validate_point(point_1b):
            self.user_interface.display_error(
                self.input_validator.get_validation_error_message("point")
            )
            return

        success = self.game_controller.bear_off_checker(point_1b - 1)
        if not success:
            self.user_interface.display_error("Cannot bear off from that point.")
            return

        self.user_interface.display_success("Checker borne off.")
        self.render_board()
        self._check_game_over()

        if not self.game_controller.get_game_state()["available_moves"]:
            self.user_interface.display_info(
                "No moves remaining. Type 'end' to finish your turn."
            )

    def _cmd_end_turn(self) -> None:
        """Handle end turn command."""
        # If game is over, announce and do not switch
        if self.game_controller.is_game_over():
            self._check_game_over()
            return

        # Show turn ending message
        ending_player = self.game_controller.get_current_player()
        self.user_interface.display_turn_ending(ending_player)

        # Reset dice for next player and switch
        self.game_controller.end_turn()

        # Show new turn with visual separator
        new_player = self.game_controller.get_current_player()
        self.user_interface.display_new_turn(new_player)


def run_cli() -> None:
    """Convenience function to run the CLI."""
    BackgammonCLI().run()


if __name__ == "__main__":
    run_cli()
