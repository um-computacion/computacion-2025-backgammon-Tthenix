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
        """Create the CLI with proper dependency injection.

        Args:
            game (BackgammonGame, optional): Game instance to use. Defaults to None.

        Returns:
            None
        """
        self.__game__ = game or BackgammonGame()
        self.__game__.setup_initial_position()
        self.__running__ = False

        # Initialize components following Dependency Inversion Principle
        self.__board_renderer__ = BoardRenderer()
        self.__command_parser__ = CommandParser()
        self.__input_validator__ = InputValidator()
        self.__game_controller__ = GameController(self.__game__)
        self.__user_interface__ = UserInterface()

        # Register command handlers
        self._register_commands()

    def _register_commands(self) -> None:
        """Register all command handlers following Open/Closed Principle.

        Returns:
            None
        """
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
            self.__command_parser__.register_handler(cmd, handler)

    def render_board(self) -> None:
        """Render the board using the BoardRenderer component.

        Returns:
            None
        """
        self.__board_renderer__.render_board(self.__game__)

    def run(self) -> None:
        """Start the interactive CLI loop.

        Returns:
            None
        """
        self.__running__ = True
        self.__user_interface__.display_header("BACKGAMMON GAME")
        self.__user_interface__.display_message(
            "  Type 'help' or 'h' for available commands"
        )
        self.__user_interface__.display_separator("=")
        self.render_board()

        while self.__running__:
            try:
                current_player = self.__game_controller__.get_current_player()
                prompt = f"[{current_player.__name__} - {current_player.__color__}] > "
                command = self.__user_interface__.prompt_string(prompt)
            except (EOFError, KeyboardInterrupt):
                self.__user_interface__.display_message(
                    "\n\nExiting game. Thanks for playing!"
                )
                break
            if not command:
                continue
            self._handle_command(command)
        self.__running__ = False

    def _handle_command(self, command: str) -> None:
        """Parse and execute a single command using CommandParser.

        Args:
            command (str): The command string to parse and execute

        Returns:
            None
        """
        cmd, _ = self.__command_parser__.parse_command(command)
        handler = self.__command_parser__.get_handler(cmd)

        if handler:
            handler()
        else:
            self.__user_interface__.display_error("Unknown command. Type 'help'.")

    def _print_help(self) -> None:
        """Print available commands using UserInterface.

        Returns:
            None
        """
        self.__user_interface__.display_separator()
        self.__user_interface__.display_message("  AVAILABLE COMMANDS")
        self.__user_interface__.display_separator()
        self.__user_interface__.display_message("  help (h)      - Show this help menu")
        self.__user_interface__.display_message(
            "  board (b)     - Display the game board"
        )
        self.__user_interface__.display_message(
            "  turn (t)      - Show current player information"
        )
        self.__user_interface__.display_message(
            "  roll (r)      - Roll dice for current player"
        )
        self.__user_interface__.display_message(
            "  status (s)    - Show last roll and remaining moves"
        )
        self.__user_interface__.display_message(
            "  moves (mvs)   - Show possible moves (context-aware)"
        )
        self.__user_interface__.display_message(
            "  move (mv)     - Make a move (interactive prompts)"
        )
        self.__user_interface__.display_message(
            "  enter (ent)   - Enter a checker from the bar"
        )
        self.__user_interface__.display_message(
            "  bearoff (bo)  - Bear off a checker (if allowed)"
        )
        self.__user_interface__.display_message(
            "  end (e)       - End current player's turn"
        )
        self.__user_interface__.display_message("  quit (q)      - Exit the game")
        self.__user_interface__.display_separator()

    # ----- Individual command handlers -----
    def _cmd_quit(self) -> None:
        """Handle quit command.

        Sets the running flag to False and displays a goodbye message.
        """
        self.__running__ = False
        self.__user_interface__.display_message(
            "\nThanks for playing Backgammon! Goodbye."
        )

    def _cmd_help(self) -> None:
        """Handle help command.

        Displays the help menu and board rendering help.
        """
        self._print_help()
        self.__board_renderer__.render_help()

    def _cmd_board(self) -> None:
        """Handle board command.

        Returns:
            None
        """
        self.render_board()

    def _cmd_turn(self) -> None:
        """Handle turn command.

        Returns:
            None
        """
        current_player = self.__game_controller__.get_current_player()
        self.__user_interface__.display_turn_info(current_player)

        # Show additional turn status
        game_state = self.__game_controller__.get_game_state()
        if game_state["last_roll"]:
            self.__user_interface__.display_message(
                f"  Last roll: {game_state['last_roll']}"
            )
            self.__user_interface__.display_message(
                f"  Available moves: {game_state['available_moves']}"
            )
        else:
            self.__user_interface__.display_message("  No dice rolled yet")
            self.__user_interface__.display_message(
                "  Use 'roll' command to start your turn"
            )
        self.__user_interface__.display_separator()

    def _cmd_roll(self) -> None:
        """Handle roll command.

        Returns:
            None
        """
        game_state = self.__game_controller__.get_game_state()
        if game_state["last_roll"] is not None and game_state["available_moves"]:
            self.__user_interface__.display_warning("You still have moves left.")
            self.__user_interface__.display_message(
                "    Use your remaining moves or type 'end' to finish your turn."
            )
            return

        roll = self.__game_controller__.roll_dice()
        self.__user_interface__.display_message(
            f"\n[DICE] Rolled: {roll[0]} and {roll[1]}"
        )
        self.__user_interface__.display_info(
            f"Available moves: {self.__game_controller__.get_game_state()['available_moves']}"
        )

    def _cmd_status(self) -> None:
        """Handle status command.

        Returns:
            None
        """
        self.__board_renderer__.render_game_status(self.__game__)

    def _check_game_over(self) -> None:
        """Check and announce game over if a player has won.

        Returns:
            None
        """
        if self.__game_controller__.is_game_over():
            winner = self.__game_controller__.get_winner()
            if winner is not None:
                self.__user_interface__.display_game_over(winner)

    # ----- Command handlers -----

    def _cmd_moves(self) -> None:
        """Handle moves command.

        Returns:
            None
        """
        game_state = self.__game_controller__.get_game_state()
        if game_state["last_roll"] is None:
            self.__user_interface__.display_warning("You must roll the dice first.")
            return

        if self.__game_controller__.must_enter_from_bar():
            self.__user_interface__.display_warning("You have checkers on the bar.")
            self.__user_interface__.display_message(
                "    Use 'enter' command to enter them first."
            )
            return

        # Show available points with pieces
        current_player = self.__game_controller__.get_current_player()
        player_num = 1 if current_player == self.__game__.__player1__ else 2
        available_points = self.__game_controller__.get_available_points_with_pieces(
            player_num
        )

        if not available_points:
            self.__user_interface__.display_info("No pieces available to move.")
            return

        self.__user_interface__.display_info(
            f"Points with your pieces: {[p + 1 for p in available_points]}"
        )
        point_1b = self.__user_interface__.prompt_int("Enter point number (1-24): ")

        if point_1b is None:
            return

        if not self.__input_validator__.validate_point(point_1b):
            self.__user_interface__.display_error(
                self.__input_validator__.get_validation_error_message("point")
            )
            return

        from_point = point_1b - 1
        dests = self.__game_controller__.get_possible_destinations(from_point)

        if not dests:
            self.__user_interface__.display_info(
                "No valid destinations from this point."
            )
            return

        # Display as 1-based
        self.__user_interface__.display_info(
            f"Possible destinations: {[d + 1 for d in dests]}"
        )

    def _cmd_move(self) -> None:
        """Handle move command.

        Returns:
            None
        """
        game_state = self.__game_controller__.get_game_state()
        if game_state["last_roll"] is None:
            self.__user_interface__.display_warning("You must roll the dice first.")
            return

        if self.__game_controller__.must_enter_from_bar():
            self.__user_interface__.display_warning("You have checkers on the bar.")
            self.__user_interface__.display_message(
                "    Use 'enter' command to enter them first."
            )
            return

        from_1b = self.__user_interface__.prompt_int("Move from point (1-24): ")
        to_1b = self.__user_interface__.prompt_int("Move to point (1-24): ")

        if from_1b is None or to_1b is None:
            return

        if not self.__input_validator__.validate_move_points(from_1b, to_1b):
            self.__user_interface__.display_error(
                self.__input_validator__.get_validation_error_message("move")
            )
            return

        success = self.__game_controller__.make_move(from_1b - 1, to_1b - 1)
        if not success:
            self.__user_interface__.display_error("Illegal move. Please try again.")
            return

        self.__user_interface__.display_success("Move completed.")
        self.render_board()
        self._check_game_over()

        if not self.__game_controller__.get_game_state()["available_moves"]:
            self.__user_interface__.display_info(
                "No moves remaining. Type 'end' to finish your turn."
            )

    def _cmd_enter(self) -> None:
        """Handle enter command.

        Returns:
            None
        """
        game_state = self.__game_controller__.get_game_state()
        if game_state["last_roll"] is None:
            self.__user_interface__.display_warning("You must roll the dice first.")
            return

        if not self.__game_controller__.must_enter_from_bar():
            self.__user_interface__.display_info("You have no checkers on the bar.")
            return

        self.__user_interface__.display_info(
            f"Available dice: {game_state['available_moves']}"
        )
        die = self.__user_interface__.prompt_int("Enter die value to use: ")

        if die is None:
            return

        if not self.__input_validator__.validate_die_value(die):
            self.__user_interface__.display_error(
                self.__input_validator__.get_validation_error_message("die")
            )
            return

        success = self.__game_controller__.move_from_bar(die)
        if not success:
            self.__user_interface__.display_error("Cannot enter with that die value.")
            return

        self.__user_interface__.display_success("Checker entered from bar.")
        self.render_board()
        self._check_game_over()

        if not self.__game_controller__.get_game_state()["available_moves"]:
            self.__user_interface__.display_info(
                "No moves remaining. Type 'end' to finish your turn."
            )

    def _cmd_bearoff(self) -> None:
        """Handle bearoff command.

        Returns:
            None
        """
        game_state = self.__game_controller__.get_game_state()
        if game_state["last_roll"] is None:
            self.__user_interface__.display_warning("You must roll the dice first.")
            return

        point_1b = self.__user_interface__.prompt_int("Bear off from point (1-24): ")
        if point_1b is None:
            return

        if not self.__input_validator__.validate_point(point_1b):
            self.__user_interface__.display_error(
                self.__input_validator__.get_validation_error_message("point")
            )
            return

        success = self.__game_controller__.bear_off_checker(point_1b - 1)
        if not success:
            self.__user_interface__.display_error("Cannot bear off from that point.")
            return

        self.__user_interface__.display_success("Checker borne off.")
        self.render_board()
        self._check_game_over()

        if not self.__game_controller__.get_game_state()["available_moves"]:
            self.__user_interface__.display_info(
                "No moves remaining. Type 'end' to finish your turn."
            )

    def _cmd_end_turn(self) -> None:
        """Handle end turn command.

        Returns:
            None
        """
        # If game is over, announce and do not switch
        if self.__game_controller__.is_game_over():
            self._check_game_over()
            return

        # Show turn ending message
        ending_player = self.__game_controller__.get_current_player()
        self.__user_interface__.display_turn_ending(ending_player)

        # Reset dice for next player and switch
        self.__game_controller__.end_turn()

        # Show new turn with visual separator
        new_player = self.__game_controller__.get_current_player()
        self.__user_interface__.display_new_turn(new_player)


def run_cli() -> None:
    """Convenience function to run the CLI.

    Returns:
        None
    """
    BackgammonCLI().run()


if __name__ == "__main__":
    run_cli()
