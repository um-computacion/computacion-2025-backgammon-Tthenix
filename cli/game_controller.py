"""Game controller module for the Backgammon CLI.

This module handles game interactions following
the Single Responsibility Principle.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core import BackgammonGame


class GameController:
    """Handles game interactions for the CLI.

    This class is responsible only for managing game state
    and executing game actions, following SRP.
    """

    def __init__(self, game: "BackgammonGame"):
        """Initialize the game controller.

        Args:
            game: The BackgammonGame instance to control
        """
        self.__game__ = game

    def roll_dice(self) -> tuple[int, int]:
        """Roll dice for the current player.

        Returns:
            Tuple of dice values
        """
        return self.__game__.roll_dice()

    def make_move(self, from_point: int, to_point: int) -> bool:
        """Make a move on the board.

        Args:
            from_point: Source point (0-based)
            to_point: Destination point (0-based)

        Returns:
            True if move was successful, False otherwise
        """
        return self.__game__.make_move(from_point, to_point)

    def move_from_bar(self, die_value: int) -> bool:
        """Move a checker from the bar.

        Args:
            die_value: The die value to use

        Returns:
            True if move was successful, False otherwise
        """
        return self.__game__.move_from_bar(die_value)

    def bear_off_checker(self, point: int) -> bool:
        """Bear off a checker from the board.

        Args:
            point: The point to bear off from (0-based)

        Returns:
            True if bear off was successful, False otherwise
        """
        return self.__game__.bear_off_checker(point)

    def end_turn(self) -> None:
        """End the current player's turn."""
        self.__game__.__last_roll__ = None
        self.__game__.__available_moves__ = []
        self.__game__.switch_current_player()

    def get_possible_destinations(self, from_point: int) -> list[int]:
        """Get possible destinations from a point.

        Args:
            from_point: The source point (0-based)

        Returns:
            List of possible destination points
        """
        return self.__game__.get_possible_destinations(from_point)

    def get_available_points_with_pieces(self, player_num: int) -> list[int]:
        """Get points that have pieces for a player.

        Args:
            player_num: The player number (1 or 2)

        Returns:
            List of point indices with pieces (0-based)
        """
        available_points = []
        for i in range(24):
            if (
                self.__game__.__board__.__points__[i]
                and self.__game__.__board__.__points__[i][0] == player_num
            ):
                available_points.append(i)
        return available_points

    def has_valid_moves(self) -> bool:
        """Check if current player has valid moves.

        Returns:
            True if player has valid moves, False otherwise
        """
        return self.__game__.has_valid_moves()

    def must_enter_from_bar(self) -> bool:
        """Check if player must enter from bar.

        Returns:
            True if player must enter from bar, False otherwise
        """
        return self.__game__.must_enter_from_bar()

    def is_game_over(self) -> bool:
        """Check if the game is over.

        Returns:
            True if game is over, False otherwise
        """
        return self.__game__.is_game_over()

    def get_winner(self):
        """Get the winner of the game.

        Returns:
            The winner player object or None
        """
        return self.__game__.get_winner()

    def get_current_player(self):
        """Get the current player.

        Returns:
            The current player object
        """
        return self.__game__.__current_player__

    def get_game_state(self) -> dict:
        """Get the current game state.

        Returns:
            Dictionary containing game state information
        """
        return {
            "last_roll": self.__game__.__last_roll__,
            "available_moves": self.__game__.__available_moves__,
            "current_player": self.__game__.__current_player__,
            "is_game_over": self.__game__.is_game_over(),
        }
