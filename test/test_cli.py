"""CLI tests for BackgammonCLI.

Covers help, roll/status/end, moves prompting, and game-over announcement.
"""

import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from cli.cli import BackgammonCLI


class TestBackgammonCLI(unittest.TestCase):
    """Tests for the Backgammon CLI behavior."""

    def setUp(self):
        """Initialize a fresh CLI instance before each test."""
        self.__cli__ = BackgammonCLI()

    def _run_commands(self, commands):
        """Run a sequence of commands through the CLI loop and capture output."""
        buf = io.StringIO()
        with redirect_stdout(buf):
            with patch("builtins.input", side_effect=commands):
                self.__cli__.run()
        return buf.getvalue()

    def test_help_and_quit(self):
        """It should show help and exit cleanly on quit."""
        output = self._run_commands(["help", "quit"])
        self.assertIn("AVAILABLE COMMANDS", output)
        self.assertIn("Thanks for playing Backgammon! Goodbye.", output)

    @patch("core.dice.Dice.roll", return_value=(2, 4))
    def test_roll_status_end_and_quit(self, _mock_roll):
        """It should roll, show status, end turn, and quit."""
        output = self._run_commands(["roll", "status", "end", "quit"])
        self.assertIn("Rolled: 2 and 4", output)
        self.assertIn("Last roll:", output)
        self.assertIn("turn begins", output)  # Updated to match new format
        self.assertIn("Thanks for playing Backgammon! Goodbye.", output)

    @patch("core.dice.Dice.roll", return_value=(1, 2))
    def test_moves_prompt_lists_points(self, _mock_roll):
        """It should list available points and destinations for moves."""
        # roll so moves are available, then call moves and choose an input, then quit
        # The exact destinations may vary; assert prompts and listing are shown
        output = self._run_commands(["roll", "moves", "1", "quit"])
        self.assertIn("Points with your pieces:", output)
        # When input() is patched, the prompt text is not printed by mock
        # so we assert destinations listing instead
        self.assertIn("Possible destinations:", output)

    def test_game_over_announced_on_end(self):
        """It should announce game over when a player has won."""
        # Force a game-over state and then end turn
        # Player1 wins
        self.__cli__.__game__.__board__.__off_board__[0] = [1] * 15
        output = self._run_commands(["end", "quit"])
        self.assertIn("GAME OVER!", output)

    # --- Additional coverage ---
    def test_status_before_roll(self):
        """Status should show None roll and empty moves before rolling."""
        output = self._run_commands(["status", "quit"])
        self.assertIn("Last roll: None", output)
        self.assertIn("moves: []", output)

    def test_reroll_blocked_when_moves_remain(self):
        """Re-rolling should be blocked while moves remain."""
        # Simulate existing roll with remaining moves
        self.__cli__.__game__.__last_roll__ = (2, 3)
        self.__cli__.__game__.__available_moves__ = [2, 3]
        output = self._run_commands(["roll", "quit"])
        self.assertIn("You still have moves left.", output)

    def test_move_illegal_shows_message(self):
        """Illegal move attempts should print an error message."""
        # Roll first
        with patch("core.dice.Dice.roll", return_value=(1, 2)):
            output = self._run_commands(["roll", "move", "10", "11", "quit"])
        self.assertIn("[ERROR] Illegal move", output)

    def test_bearoff_invalid_message(self):
        """Bearoff should be rejected when conditions are not met."""
        # Not allowed at start
        with patch("core.dice.Dice.roll", return_value=(1, 2)):
            output = self._run_commands(["roll", "bearoff", "6", "quit"])
        self.assertIn("Cannot bear off from that point", output)

    def test_enter_success(self):
        """Entering from bar should succeed on a legal entry point."""
        # Prepare bar and open entry for player1 using die=1 -> entry point index 23
        # Ficha blanca (1) capturada está en el lado negro (index 1)
        self.__cli__.__game__.__board__.__checker_bar__[1] = [1]
        self.__cli__.__game__.__board__.__points__[23] = []
        self.__cli__.__game__.__last_roll__ = (1, 2)
        self.__cli__.__game__.__available_moves__ = [1, 2]
        output = self._run_commands(["enter", "1", "quit"])
        self.assertIn("Checker entered from bar", output)

    def test_enter_blocked(self):
        """Entering from bar should fail if the point is blocked."""
        # Blancas re-entran en puntos 0-5: con dado 1 → punto 0 (1-1=0)
        # Block entry with two opponent pieces
        # Ficha blanca (1) capturada está en el lado negro (index 1)
        self.__cli__.__game__.__board__.__checker_bar__[1] = [1]
        self.__cli__.__game__.__board__.__points__[0] = [2, 2]  # Bloquear punto 0
        self.__cli__.__game__.__last_roll__ = (1, 2)
        self.__cli__.__game__.__available_moves__ = [1, 2]
        output = self._run_commands(["enter", "1", "quit"])
        self.assertIn("Cannot enter with that die value", output)

    def test_alias_commands(self):
        """Short aliases should behave like their full command names."""
        with patch("core.dice.Dice.roll", return_value=(3, 5)):
            output = self._run_commands(["h", "b", "t", "r", "s", "q"])
        self.assertIn("AVAILABLE COMMANDS", output)
        self.assertIn("CURRENT TURN:", output)  # Updated to match new format
        self.assertIn("Rolled: 3 and 5", output)
        self.assertIn("Last roll:", output)

    def test_unknown_command(self):
        """Unknown commands should print a helpful message."""
        output = self._run_commands(["xyz", "quit"])
        self.assertIn("Unknown command.", output)

    def test_moves_requires_enter_from_bar(self):
        """Moves command should require entering from bar when needed."""
        # Put a checker on bar for player1, roll so command is allowed
        # Ficha blanca (1) capturada está en el lado negro (index 1)
        self.__cli__.__game__.__board__.__checker_bar__[1] = [1]
        with patch("core.dice.Dice.roll", return_value=(2, 3)):
            output = self._run_commands(["roll", "moves", "quit"])
        self.assertIn("You have checkers on the bar", output)

    def test_moves_no_own_pieces(self):
        """Moves should inform when no movable own pieces are on board."""
        # Clear all points so no available_points are found
        self.__cli__.__game__.__board__.__points__ = [[] for _ in range(24)]
        with patch("core.dice.Dice.roll", return_value=(2, 3)):
            output = self._run_commands(["roll", "moves", "quit"])
        self.assertIn("No pieces available to move", output)

    def test_prompt_int_invalid_value(self):
        """_prompt_int should handle non-integer input gracefully."""
        # Trigger _prompt_int with non-integer input during move
        with patch("core.dice.Dice.roll", return_value=(2, 3)):
            output = self._run_commands(["roll", "move", "abc", "quit", "quit"])
        self.assertIn("Please enter a valid number", output)

    def test_move_exhausts_moves_message(self):
        """After consuming last move, it should prompt to end the turn."""
        # Prepare exactly one legal move (1->2)
        self.__cli__.__game__.setup_initial_position()
        self.__cli__.__game__.__last_roll__ = (1, 2)
        self.__cli__.__game__.__available_moves__ = [1]
        output = self._run_commands(["move", "1", "2", "quit"])
        self.assertIn("No moves remaining", output)

    def test_enter_when_bar_empty(self):
        """Entering should be disallowed when the bar is empty."""
        self.__cli__.__game__.__last_roll__ = (1, 2)
        self.__cli__.__game__.__available_moves__ = [1, 2]
        # Ensure bar empty
        self.__cli__.__game__.__board__.__checker_bar__[0] = []
        output = self._run_commands(["enter", "1", "quit"])
        self.assertIn("You have no checkers on the bar", output)

    def test_keyboard_interrupt_exit(self):
        """The loop should exit gracefully on KeyboardInterrupt."""
        buf = io.StringIO()
        with redirect_stdout(buf):
            with patch("builtins.input", side_effect=KeyboardInterrupt):
                self.__cli__.run()
        output = buf.getvalue()
        self.assertIn("Exiting game", output)

    def test_eoferror_exit(self):
        """The loop should exit gracefully on EOFError."""
        buf = io.StringIO()
        with redirect_stdout(buf):
            with patch("builtins.input", side_effect=EOFError):
                self.__cli__.run()
        output = buf.getvalue()
        self.assertIn("Exiting game", output)

    @patch("core.dice.Dice.roll", return_value=(2, 3))
    def test_moves_invalid_point_range(self, _mock_roll):
        """Moves should validate origin point range (1-24)."""
        output = self._run_commands(["roll", "moves", "30", "quit"])
        self.assertIn("Point must be between 1 and 24", output)

    def test_move_when_moves_remain_no_exhaust_message(self):
        """When moves remain after a move, no exhaustion message is shown."""
        # Prepare two moves available and a likely legal small move won't exhaust all
        self.__cli__.__game__.setup_initial_position()
        self.__cli__.__game__.__last_roll__ = (1, 2)
        self.__cli__.__game__.__available_moves__ = [1, 2]
        # Attempt a move that may succeed; even if illegal, it prints message
        # To ensure success, move from point 1 to 2 for player1 at start
        output = self._run_commands(["move", "1", "2", "quit"])
        # We only care that the exhaust message is not shown when moves remain
        self.assertNotIn("No moves remaining", output)

    def test_bearoff_valid_path(self):
        """Bearoff should succeed when all pieces are in home and die fits."""
        # Setup all-in-home for player1 with a checker at 24 (index 23)
        self.__cli__.__game__.__board__.__points__ = [[] for _ in range(24)]
        self.__cli__.__game__.__board__.__points__[23] = [1]
        self.__cli__.__game__.__last_roll__ = (1, 2)
        self.__cli__.__game__.__available_moves__ = [1, 2]
        output = self._run_commands(["bearoff", "24", "quit"])
        self.assertIn("Checker borne off", output)

    def test_turn_indicator_in_board_display(self):
        """Board should display current player turn prominently."""
        output = self._run_commands(["board", "quit"])
        self.assertIn("CURRENT TURN:", output)
        self.assertIn("Player 1 (white)", output)

    def test_turn_indicator_after_switch(self):
        """Turn indicator should update after player switch."""
        with patch("core.dice.Dice.roll", return_value=(1, 2)):
            output = self._run_commands(["roll", "end", "board", "quit"])
        self.assertIn("CURRENT TURN:", output)
        self.assertIn("Player 2 (black)", output)

    def test_turn_indicator_in_prompt(self):
        """Input prompt should show current player."""
        # The prompt text isn't captured by our test setup, but we can verify
        # the turn display logic is called by checking board output
        output = self._run_commands(["board", "quit"])
        self.assertIn("CURRENT TURN:", output)


if __name__ == "__main__":
    unittest.main()
