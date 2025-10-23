"""Board rendering module for the Backgammon CLI.

This module handles the visual representation of the game board
following the Single Responsibility Principle.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core import BackgammonGame


class BoardRenderer:
    """Handles board rendering logic for the CLI.

    This class is responsible only for rendering the game board
    and related visual elements, following SRP.
    """

    def __init__(self):
        """Initialize the board renderer."""
        self.board_width = 60
        self.separator_char = "="

    def render_board(self, game: "BackgammonGame") -> None:
        """Render the complete game board with current state.

        Args:
            game: The BackgammonGame instance to render
        """
        board = game.board
        current_player = game.current_player

        # Display current turn prominently
        self._render_turn_header(current_player)

        # Render the main board
        self._render_main_board(board)

        # Render bearing off information
        self._render_bearing_off_info(board)

    def _render_turn_header(self, current_player) -> None:
        """Render the current turn header.

        Args:
            current_player: The current player object
        """
        print("\n" + self.separator_char * self.board_width)
        print(f"  CURRENT TURN: {current_player.name} ({current_player.color})")
        print(self.separator_char * self.board_width)

    def _render_main_board(self, board) -> None:
        """Render the main game board.

        Args:
            board: The board object to render
        """
        # Top half (points 13-24)
        print("\n  13 14 15 16 17 18    BAR    19 20 21 22 23 24")
        print(" +--------------------+     +--------------------+")

        left_top = [self._format_point(board, i) for i in range(12, 18)]  # 13..18
        right_top = [self._format_point(board, i) for i in range(18, 24)]  # 19..24
        bar_w = len(board.checker_bar[0])
        bar_b = len(board.checker_bar[1])
        print(f"  {' '.join(left_top)}    W:{bar_w}|B:{bar_b}    {' '.join(right_top)}")

        print(" +--------------------+     +--------------------+")

        # Bottom half (points 12-1)
        left_bot = [self._format_point(board, i) for i in range(11, 5, -1)]  # 12..7
        right_bot = [self._format_point(board, i) for i in range(5, -1, -1)]  # 6..1
        print(f"  {' '.join(left_bot)}               {' '.join(right_bot)}")
        print("  12 11 10  9  8  7           6  5  4  3  2  1")

    def _render_bearing_off_info(self, board) -> None:
        """Render bearing off information.

        Args:
            board: The board object to render
        """
        white_off = len(board.off_board[0])
        black_off = len(board.off_board[1])
        print(f"\n  Bearing off - White: {white_off} | Black: {black_off}")
        print(self.separator_char * self.board_width + "\n")

    def _format_point(self, board, idx: int) -> str:
        """Format a point for display.

        Args:
            board: The board object
            idx: Point index to format

        Returns:
            Formatted string representation of the point
        """
        pieces = board.points[idx]
        if not pieces:
            return "  "
        owner = "W" if pieces[0] == 1 else "B"
        count = len(pieces)
        return f"{owner}{count}" if count < 10 else f"{owner}+"  # cap at +

    def render_game_status(self, game: "BackgammonGame") -> None:
        """Render the current game status information.

        Args:
            game: The BackgammonGame instance to render status for
        """
        print("\n" + self.separator_char * self.board_width)
        print("  GAME STATUS")
        print(self.separator_char * self.board_width)

        # Show current player
        current_player = game.current_player
        print(f"  Current Player: {current_player.name} ({current_player.color})")

        # Show dice information
        if game.last_roll:
            print(f"  Last Roll: {game.last_roll[0]} and {game.last_roll[1]}")
            print(f"  Available Moves: {game.available_moves}")
        else:
            print("  No dice rolled yet")

        # Show game over status
        if game.is_game_over():
            winner = game.get_winner()
            if winner:
                print(f"  GAME OVER - Winner: {winner.name} ({winner.color})")
            else:
                print("  GAME OVER - Draw")
        else:
            print("  Game in progress")

        print(self.separator_char * self.board_width)

    def render_help(self) -> None:
        """Render the help information for the board display."""
        print("\n" + self.separator_char * self.board_width)
        print("  BOARD DISPLAY HELP")
        print(self.separator_char * self.board_width)
        print("  Board Layout:")
        print("    - Points 1-24 are numbered from bottom to top")
        print("    - W = White pieces, B = Black pieces")
        print("    - Numbers show piece count (W5 = 5 white pieces)")
        print("    - BAR shows captured pieces")
        print("    - Bearing off shows pieces removed from board")
        print("  Commands:")
        print("    - 'board' or 'b' to display this board")
        print("    - 'status' or 's' for game status")
        print("    - 'help' or 'h' for all commands")
        print(self.separator_char * self.board_width)

    def set_board_width(self, width: int) -> None:
        """Set the board display width.

        Args:
            width: The width for board display
        """
        self.board_width = max(40, min(120, width))  # Clamp between 40 and 120

    def set_separator_char(self, char: str) -> None:
        """Set the separator character for board display.

        Args:
            char: The character to use for separators
        """
        self.separator_char = char if char else "="
