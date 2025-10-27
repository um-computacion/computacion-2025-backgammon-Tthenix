"""Backgammon game module.

This module contains the main BackgammonGame class that orchestrates
the entire Backgammon game, managing players, board, dice, and game logic.
"""

from .player import Player
from .board import Board
from .dice import Dice
from .checker import Checker


class BackgammonGame:
    """Main Backgammon game class.

    Note: This class holds core game state and therefore carries several
    instance attributes by design. The attribute count is justified by the
    domain model (players, board, dice, history, etc.).
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, player1=None, player2=None):
        """Initialize a new backgammon game.

        Args:
            player1 (Player, optional): First player. Defaults to None.
            player2 (Player, optional): Second player. Defaults to None.

        Returns:
            None
        """
        if player1 is None:
            self.__player1__ = Player("Player 1", "white")
        else:
            self.__player1__ = player1

        if player2 is None:
            self.__player2__ = Player("Player 2", "black")
        else:
            self.__player2__ = player2

        self.__board__ = Board()
        self.__dice__ = Dice()
        self.__current_player__ = self.__player1__
        self.__last_roll__ = None
        self.__available_moves__ = []
        self.__move_history__ = []

        # Initialize checker objects for each player
        self.__player1_checkers__ = [Checker("white") for _ in range(15)]
        self.__player2_checkers__ = [Checker("black") for _ in range(15)]

    def setup_initial_position(self):
        """Set up the initial board position using Checker objects.

        Returns:
            None
        """
        self.__board__.setup_initial_position()

        # Reset all checkers
        for checker in self.__player1_checkers__:
            checker.reset()
        for checker in self.__player2_checkers__:
            checker.reset()

        # Place player 1 checkers in their initial positions
        checker_index = 0
        # Point 1 (0-indexed as 0): 2 checkers
        for _ in range(2):
            self.__player1_checkers__[checker_index].place_on_point(1)
            checker_index += 1
        # Point 12 (0-indexed as 11): 5 checkers
        for _i in range(5):
            self.__player1_checkers__[checker_index].place_on_point(12)
            checker_index += 1
        # Point 17 (0-indexed as 16): 3 checkers
        for _i in range(3):
            self.__player1_checkers__[checker_index].place_on_point(17)
            checker_index += 1
        # Point 19 (0-indexed as 18): 5 checkers
        for _i in range(5):
            self.__player1_checkers__[checker_index].place_on_point(19)
            checker_index += 1

        # Place player 2 checkers in their initial positions
        checker_index = 0
        # Point 24 (0-indexed as 23): 2 checkers
        for _i in range(2):
            self.__player2_checkers__[checker_index].place_on_point(24)
            checker_index += 1
        # Point 13 (0-indexed as 12): 5 checkers
        for _i in range(5):
            self.__player2_checkers__[checker_index].place_on_point(13)
            checker_index += 1
        # Point 8 (0-indexed as 7): 3 checkers
        for _i in range(3):
            self.__player2_checkers__[checker_index].place_on_point(8)
            checker_index += 1
        # Point 6 (0-indexed as 5): 5 checkers
        for _i in range(5):
            self.__player2_checkers__[checker_index].place_on_point(6)
            checker_index += 1

    def get_checkers_at_point(self, point, player_num):
        """Get all checker objects at a specific point for a player.

        Args:
            point (int): Point index (0-23)
            player_num (int): Player number (1 or 2)

        Returns:
            list: List of Checker objects at the specified point
        """
        checkers = []
        if player_num == 1:
            for checker in self.__player1_checkers__:
                if checker.__position__ == point + 1:  # Convert 0-based to 1-based
                    checkers.append(checker)
        else:
            for checker in self.__player2_checkers__:
                if checker.__position__ == point + 1:  # Convert 0-based to 1-based
                    checkers.append(checker)
        return checkers

    def get_checkers_on_bar(self, player_num):
        """Get all checker objects on the bar for a player.

        Args:
            player_num (int): Player number (1 or 2)

        Returns:
            list: List of Checker objects on the bar
        """
        checkers = []
        if player_num == 1:
            for checker in self.__player1_checkers__:
                if checker.__is_on_bar__:
                    checkers.append(checker)
        else:
            for checker in self.__player2_checkers__:
                if checker.__is_on_bar__:
                    checkers.append(checker)
        return checkers

    def get_borne_off_checkers(self, player_num):
        """Get all checker objects that have been borne off for a player.

        Args:
            player_num (int): Player number (1 or 2)

        Returns:
            list: List of Checker objects that have been borne off
        """
        checkers = []
        if player_num == 1:
            for checker in self.__player1_checkers__:
                if checker.__is_borne_off__:
                    checkers.append(checker)
        else:
            for checker in self.__player2_checkers__:
                if checker.__is_borne_off__:
                    checkers.append(checker)
        return checkers

    def move_checker_object(self, from_point, to_point, player_num):
        """Move a checker object from one point to another.

        Args:
            from_point (int): Source point index (0-23)
            to_point (int): Destination point index (0-23)
            player_num (int): Player number (1 or 2)

        Returns:
            bool: True if the move was successful, False otherwise
        """
        checkers_at_point = self.get_checkers_at_point(from_point, player_num)
        if not checkers_at_point:
            return False

        checker = checkers_at_point[0]  # Move the first checker

        # Check if there's an opponent checker to capture
        opponent_num = 2 if player_num == 1 else 1
        opponent_checkers = self.get_checkers_at_point(to_point, opponent_num)

        if len(opponent_checkers) == 1:
            # Capture the opponent checker
            opponent_checker = opponent_checkers[0]
            opponent_checker.send_to_bar()

        # Move our checker
        checker.move_to_point(to_point + 1)  # Convert 0-based to 1-based
        return True

    def move_checker_from_bar_object(self, to_point, player_num):
        """Move a checker object from the bar to a point.

        Args:
            to_point (int): Destination point index (0-23)
            player_num (int): Player number (1 or 2)

        Returns:
            bool: True if the move was successful, False otherwise
        """
        checkers_on_bar = self.get_checkers_on_bar(player_num)
        if not checkers_on_bar:
            return False

        checker = checkers_on_bar[0]  # Move the first checker from bar

        # Check if there's an opponent checker to capture
        opponent_num = 2 if player_num == 1 else 1
        opponent_checkers = self.get_checkers_at_point(to_point, opponent_num)

        if len(opponent_checkers) == 1:
            # Capture the opponent checker
            opponent_checker = opponent_checkers[0]
            opponent_checker.send_to_bar()

        # Return checker from bar
        checker.return_from_bar(to_point + 1)  # Convert 0-based to 1-based
        return True

    def bear_off_checker_object(self, point, player_num):
        """Bear off a checker object from a point.

        Args:
            point (int): Point index (0-23)
            player_num (int): Player number (1 or 2)

        Returns:
            bool: True if the bear off was successful, False otherwise
        """
        checkers_at_point = self.get_checkers_at_point(point, player_num)
        if not checkers_at_point:
            return False

        checker = checkers_at_point[0]  # Bear off the first checker
        checker.bear_off()
        return True

    def roll_dice(self):
        """Roll dice and update game state.

        Returns:
            tuple: The dice roll result (die1, die2)
        """
        roll = self.__dice__.roll()
        self.__last_roll__ = roll
        self.__available_moves__ = self.__dice__.__get_moves__(roll)
        return roll

    def get_available_moves(self):
        """Get available moves based on last dice roll.

        Returns:
            list: List of available move distances
        """
        if self.__last_roll__ is None:
            return []
        return self.__dice__.__get_moves__(self.__last_roll__)

    def validate_move(self, from_point, to_point):
        """Validate if a move is legal.

        Args:
            from_point (int): Source point index (0-23)
            to_point (int): Destination point index (0-23)

        Returns:
            bool: True if the move is legal, False otherwise
        """
        # Ensure dice have been rolled and moves are available
        if not self._ensure_moves_available():
            return False

        player_num = self._get_current_player_num()

        # Validate origin ownership and bounds
        if not self._has_player_piece_at(from_point, player_num):
            return False

        distance = abs(to_point - from_point)

        # Validate distance and direction
        if not self._is_distance_available(distance):
            return False
        if not self._is_correct_direction(from_point, to_point, player_num):
            return False

        # Delegate final validation to the board
        return self.__board__.can_move(from_point, to_point, player_num)

    # ---- Internal helpers to keep validate_move simple (reduce branches/returns) ----
    def _ensure_moves_available(self):
        """Return True if there is a last roll and available moves are populated.

        Returns:
            bool: True if moves are available, False otherwise
        """
        if self.__last_roll__ is None:
            return False
        if len(self.__available_moves__) == 0:
            self.__available_moves__ = self.__dice__.__get_moves__(self.__last_roll__)
        return len(self.__available_moves__) > 0

    def _get_current_player_num(self):
        """Return 1 for player1, 2 for player2.

        Returns:
            int: Player number (1 or 2)
        """
        return 1 if self.__current_player__ == self.__player1__ else 2

    def _has_player_piece_at(self, from_point, player_num):
        """Check bounds and that the top checker at from_point belongs to player_num.

        Args:
            from_point (int): Point index (0-23)
            player_num (int): Player number (1 or 2)

        Returns:
            bool: True if player has piece at point, False otherwise
        """
        if from_point < 0 or from_point >= 24:
            return False
        if len(self.__board__.__points__[from_point]) == 0:
            return False
        return self.__board__.__points__[from_point][0] == player_num

    def _is_distance_available(self, distance):
        """Check whether the rolled distances include the given distance.

        Args:
            distance (int): Distance to check

        Returns:
            bool: True if distance is available, False otherwise
        """
        for move_distance in self.__available_moves__:
            if move_distance == distance:
                return True
        return False

    def _is_correct_direction(self, from_point, to_point, player_num):
        """Validate that the move goes in the correct direction for the player.

        Args:
            from_point (int): Source point index (0-23)
            to_point (int): Destination point index (0-23)
            player_num (int): Player number (1 or 2)

        Returns:
            bool: True if direction is correct, False otherwise
        """
        if player_num == 1 and to_point <= from_point:
            return False
        if player_num == 2 and to_point >= from_point:
            return False
        return True

    def make_move(self, from_point, to_point):
        """Execute a move on the board.

        Args:
            from_point (int): Source point index (0-23)
            to_point (int): Destination point index (0-23)

        Returns:
            bool: True if the move was successful, False otherwise
        """
        if not self.validate_move(from_point, to_point):
            return False

        if self.__current_player__ == self.__player1__:
            player_num = 1
        else:
            player_num = 2

        distance = abs(to_point - from_point)

        # Save previous state for history
        old_board = self.__board__.copy()
        move_info = {
            "from": from_point,
            "to": to_point,
            "player": player_num,
            "captured": None,
            "board_state": old_board,
        }

        # Check if there's a capture
        if len(self.__board__.__points__[to_point]) > 0:
            if len(self.__board__.__points__[to_point]) == 1:
                if self.__board__.__points__[to_point][0] != player_num:
                    move_info["captured"] = self.__board__.__points__[to_point][0]

        # Execute movement
        success = self.__board__.move_piece(from_point, to_point, player_num)

        if success:
            # Remove used dice value - find and remove the first matching distance
            for i, move in enumerate(self.__available_moves__):
                if move == distance:
                    self.__available_moves__.pop(i)
                    break
            self.__move_history__.append(move_info)

        return success

    def move_from_bar(self, dice_value):
        """Move a checker from the bar to the board.

        Args:
            dice_value (int): Dice value to use for the move

        Returns:
            bool: True if the move was successful, False otherwise
        """
        # Check if the dice value is available
        found_dice = False
        for move in self.__available_moves__:
            if move == dice_value:
                found_dice = True
                break
        if not found_dice:
            return False

        if self.__current_player__ == self.__player1__:
            player_num = 1
            # Fichas blancas (1) capturadas están en el lado negro (index 1)
            player_bar_index = 1
        else:
            player_num = 2
            # Fichas negras (2) capturadas están en el lado blanco (index 0)
            player_bar_index = 0

        # Check if player has their own checkers on opponent's side
        player_pieces_on_bar = [
            piece
            for piece in self.__board__.__checker_bar__[player_bar_index]
            if piece == player_num
        ]
        if len(player_pieces_on_bar) == 0:
            return False

        # Calculate entry point
        # REGLA BACKGAMMON: Las fichas RE-ENTRAN por la HOME del OPONENTE
        # Blancas (1) re-entran en puntos 0-5 (home de negras)
        # Negras (2) re-entran en puntos 19-24 (home de blancas)
        if player_num == 1:
            entry_point = dice_value - 1  # Blancas entran en 0-5
        else:
            entry_point = 24 - dice_value  # Negras entran en 19-24

        # Validate entry point
        if entry_point < 0 or entry_point >= 24:
            return False

        # Save move for history
        old_board = self.__board__.copy()
        move_info = {
            "from": "bar",
            "to": entry_point,
            "player": player_num,
            "captured": None,
            "board_state": old_board,
        }

        # Execute movement
        success = self.__board__.enter_from_bar(entry_point, player_num)

        if success:
            # Remove used dice value - find and remove the first matching dice value
            for i, move in enumerate(self.__available_moves__):
                if move == dice_value:
                    self.__available_moves__.pop(i)
                    break
            self.__move_history__.append(move_info)

        return success

    def can_bear_off(self, player_num):
        """Check if a player can bear off checkers.

        Args:
            player_num (int): Player number (1 or 2)

        Returns:
            bool: True if player can bear off, False otherwise
        """
        return self.__board__.is_all_pieces_in_home(player_num)

    def bear_off_checker(self, point):
        """Bear off a checker from the board.

        Args:
            point (int): Point index (0-23)

        Returns:
            bool: True if the bear off was successful, False otherwise
        """
        if self.__current_player__ == self.__player1__:
            player_num = 1
        else:
            player_num = 2

        if not self.can_bear_off(player_num):
            return False

        # Update available moves if they are empty
        if len(self.__available_moves__) == 0 and self.__last_roll__ is not None:
            self.__available_moves__ = self.__dice__.__get_moves__(self.__last_roll__)

        # Check if there are valid dice values
        if len(self.__available_moves__) == 0:
            return False

        # Try each available dice value
        for i, dice_value in enumerate(self.__available_moves__):
            if self.__board__.can_bear_off(point, player_num, dice_value):
                # Save move for history
                old_board = self.__board__.copy()
                move_info = {
                    "from": point,
                    "to": "off",
                    "player": player_num,
                    "captured": None,
                    "board_state": old_board,
                }

                success = self.__board__.bear_off_piece(point, player_num)
                if success:
                    # Remove the used dice value
                    self.__available_moves__.pop(i)
                    self.__move_history__.append(move_info)
                    return True

        return False

    def switch_current_player(self):
        """Switch to the other player.

        Returns:
            None
        """
        if self.__current_player__ == self.__player1__:
            self.__current_player__ = self.__player2__
        else:
            self.__current_player__ = self.__player1__

        # Clear dice state when switching players
        self.__last_roll__ = None
        self.__available_moves__ = []

    def is_game_over(self):
        """Check if the game is over.

        Returns:
            bool: True if the game is over, False otherwise
        """
        return self.__board__.is_game_over()

    def get_winner(self):
        """Get the winner of the game.

        Returns:
            Player: The winning player, or None if no winner yet
        """
        winner_num = self.__board__.get_winner()
        if winner_num == 1:
            return self.__player1__
        if winner_num == 2:
            return self.__player2__
        return None

    def get_game_state(self):
        """Get the current game state.

        Returns:
            dict: Dictionary containing the complete game state
        """
        state = {}
        state["board"] = self.__board__.get_board_state()
        state["current_player"] = self.__current_player__
        state["last_roll"] = self.__last_roll__
        state["available_moves"] = []
        for move in self.__available_moves__:
            state["available_moves"].append(move)
        state["game_over"] = self.is_game_over()
        return state

    def get_serializable_state(self):
        """Get a serializable version of the game state.

        Returns:
            dict: Dictionary containing serializable game state
        """
        state = {
            "board": self.__board__.get_board_state(),
            "current_player": {
                "name": self.__current_player__.__name__,
                "color": self.__current_player__.__color__,
            },
            "player1": {
                "name": self.__player1__.__name__,
                "color": self.__player1__.__color__,
            },
            "player2": {
                "name": self.__player2__.__name__,
                "color": self.__player2__.__color__,
            },
            "last_roll": self.__last_roll__,
            "available_moves": self.__available_moves__,
            "move_history": self.__move_history__,
            "game_over": self.is_game_over(),
        }
        return state

    def restore_from_state(self, state):
        """Restore game state from serializable data.

        Args:
            state: Dictionary containing serialized game state

        Returns:
            None
        """
        # Restore board state
        self.__board__.set_board_state(state["board"])

        # Restore current player
        current_player_name = state["current_player"]["name"]
        if current_player_name == self.__player1__.__name__:
            self.__current_player__ = self.__player1__
        else:
            self.__current_player__ = self.__player2__

        # Restore game state
        self.__last_roll__ = state["last_roll"]
        self.__available_moves__ = state["available_moves"]
        self.__move_history__ = state["move_history"]

    def get_player_by_color(self, color):
        """Get player by color.

        Args:
            color (str): Player color ('white' or 'black')

        Returns:
            Player: The player with the specified color, or None if not found
        """
        if self.__player1__.__color__ == color:
            return self.__player1__
        if self.__player2__.__color__ == color:
            return self.__player2__
        return None

    def reset_game(self):
        """Reset the game to initial state.

        Returns:
            None
        """
        self.__board__ = Board()
        self.__current_player__ = self.__player1__
        self.__last_roll__ = None
        self.__available_moves__ = []
        self.__move_history__ = []
        self.__player1__.reset()
        self.__player2__.reset()

        # Reset all checker objects
        for checker in self.__player1_checkers__:
            checker.reset()
        for checker in self.__player2_checkers__:
            checker.reset()

    def copy_game_state(self):
        """Create a copy of the current game state.

        Returns:
            dict: Dictionary containing a copy of the game state
        """
        state = {}
        state["board"] = self.__board__.copy()
        state["players"] = {}
        state["players"]["player1"] = Player(
            self.__player1__.__name__, self.__player1__.__color__
        )
        state["players"]["player2"] = Player(
            self.__player2__.__name__, self.__player2__.__color__
        )
        state["current_player"] = self.__current_player__
        state["last_roll"] = self.__last_roll__
        state["available_moves"] = []
        for move in self.__available_moves__:
            state["available_moves"].append(move)
        state["move_history"] = []
        for move in self.__move_history__:
            state["move_history"].append(move)
        return state

    def undo_last_move(self):
        """Undo the last move.

        Returns:
            bool: True if undo was successful, False otherwise
        """
        if len(self.__move_history__) == 0:
            return False

        last_move = self.__move_history__.pop()
        self.__board__ = last_move["board_state"]

        # Restore available moves
        if self.__last_roll__ is not None:
            self.__available_moves__ = self.__dice__.__get_moves__(self.__last_roll__)

        return True

    def get_possible_destinations(self, from_point):
        """Get possible destinations from a given point.

        Args:
            from_point (int): Source point index (0-23)

        Returns:
            list: List of valid destination points
        """
        # Update available moves if they are empty
        if len(self.__available_moves__) == 0 and self.__last_roll__ is not None:
            self.__available_moves__ = self.__dice__.__get_moves__(self.__last_roll__)

        if len(self.__available_moves__) == 0:
            return []

        if self.__current_player__ == self.__player1__:
            player_num = 1
        else:
            player_num = 2

        # Check if there's a piece at the origin
        if from_point < 0 or from_point >= 24:
            return []
        if len(self.__board__.__points__[from_point]) == 0:
            return []
        if self.__board__.__points__[from_point][0] != player_num:
            return []

        destinations = []
        for move_dist in self.__available_moves__:
            if player_num == 1:
                to_point = from_point + move_dist
            else:
                to_point = from_point - move_dist

            if 0 <= to_point < 24:
                if self.__board__.can_move(from_point, to_point, player_num):
                    destinations.append(to_point)

        return destinations

    def has_valid_moves(self):
        """Check if current player has valid moves.

        Returns:
            bool: True if player has valid moves, False otherwise
        """
        # Update available moves if they are empty
        if len(self.__available_moves__) == 0 and self.__last_roll__ is not None:
            self.__available_moves__ = self.__dice__.__get_moves__(self.__last_roll__)

        if len(self.__available_moves__) == 0:
            return False

        if self.__current_player__ == self.__player1__:
            player_num = 1
        else:
            player_num = 2

        # Check if player must enter from bar first
        if self.must_enter_from_bar():
            return self.can_enter_from_bar(player_num)

        # Check regular moves
        for point in range(24):
            destinations = self.get_possible_destinations(point)
            if len(destinations) > 0:
                return True

        # Finally, check bearing off possibilities
        return self._can_bear_off_any(player_num)

    def can_enter_from_bar(self, player_num):
        """Return True if the player can legally enter from the bar with any die.

        Args:
            player_num (int): Player number (1 or 2)

        Returns:
            bool: True if player can enter from bar, False otherwise
        """
        for dice_value in self.__available_moves__:
            if player_num == 1:
                entry_point = dice_value - 1  # Blancas entran en 0-5
            else:
                entry_point = 24 - dice_value  # Negras entran en 19-24
            if 0 <= entry_point < 24:
                point = self.__board__.__points__[entry_point]
                if len(point) == 0:
                    return True
                if len(point) < 2:
                    return True
                if point[0] == player_num:
                    return True
        return False

    def _can_bear_off_any(self, player_num):
        """Return True if any bearing off move is possible with current dice.

        Args:
            player_num (int): Player number (1 or 2)

        Returns:
            bool: True if bearing off is possible, False otherwise
        """
        if not self.can_bear_off(player_num):
            return False

        home_points = (
            [18, 19, 20, 21, 22, 23] if player_num == 1 else [0, 1, 2, 3, 4, 5]
        )

        for point in home_points:
            if (
                not self.__board__.__points__[point]
                or self.__board__.__points__[point][0] != player_num
            ):
                continue
            for dice_value in self.__available_moves__:
                if self.__board__.can_bear_off(point, player_num, dice_value):
                    return True
        return False

    def must_enter_from_bar(self):
        """Check if current player must enter checkers from bar.

        Returns:
            bool: True if player must enter from bar, False otherwise
        """
        if self.__current_player__ == self.__player1__:
            player_num = 1
        else:
            player_num = 2
        return self.__board__.has_pieces_on_bar(player_num)

    def get_pip_count(self, player):
        """Calculate pip count for a player.

        Args:
            player (Player): The player to calculate pip count for

        Returns:
            int: The pip count for the player
        """
        if player == self.__player1__:
            player_num = 1
        else:
            player_num = 2

        pip_count = 0

        # Count pips for pieces on board
        for point_idx in range(24):
            point = self.__board__.__points__[point_idx]
            for piece in point:
                if piece == player_num:
                    if player_num == 1:
                        pip_count = pip_count + (24 - point_idx)
                    else:
                        pip_count = pip_count + (point_idx + 1)

        # Count pips for pieces on bar
        if player_num == 1:
            player_bar_index = 1
            bar_pieces = sum(
                1
                for piece in self.__board__.__checker_bar__[player_bar_index]
                if piece == 1
            )
            pip_count = pip_count + (bar_pieces * 25)
        else:
            player_bar_index = 0
            bar_pieces = sum(
                1
                for piece in self.__board__.__checker_bar__[player_bar_index]
                if piece == 2
            )
            pip_count = pip_count + (bar_pieces * 24)

        return pip_count

    def auto_play_turn(self):
        """Automatically play a turn.

        Returns:
            bool: True if turn was played, False otherwise
        """
        if not self.has_valid_moves():
            self.switch_current_player()
            return True
        return False

    def is_blocked_position(self, point, player_num):
        """Check if a position is blocked by opponent.

        Args:
            point (int): Point index (0-23)
            player_num (int): Player number (1 or 2)

        Returns:
            bool: True if position is blocked, False otherwise
        """
        if point < 0 or point >= 24:
            return False

        pieces = self.__board__.__points__[point]
        if len(pieces) >= 2 and pieces[0] != player_num:
            return True
        return False

    def can_hit_opponent(self, point, player_num):
        """Check if player can hit opponent at given point.

        Args:
            point (int): Point index (0-23)
            player_num (int): Player number (1 or 2)

        Returns:
            bool: True if player can hit opponent, False otherwise
        """
        if point < 0 or point >= 24:
            return False

        pieces = self.__board__.__points__[point]
        if len(pieces) == 1 and pieces[0] != player_num:
            return True
        return False

    def apply_game_rules(self):
        """Apply game rules.

        Returns:
            bool: Always returns True
        """
        return True

    def validate_complete_turn(self, moves):
        """Validate a complete turn with multiple moves.

        Args:
            moves (list): List of moves to validate

        Returns:
            bool: True if all moves are valid, False otherwise
        """
        # Create a temporary board to test moves
        temp_board = self.__board__.copy()
        temp_moves = []
        for move in self.__available_moves__:
            temp_moves.append(move)

        if self.__current_player__ == self.__player1__:
            player_num = 1
        else:
            player_num = 2

        for move in moves:
            from_point = move[0]
            to_point = move[1]
            distance = abs(to_point - from_point)

            found_distance = False
            for i, move in enumerate(temp_moves):
                if move == distance:
                    found_distance = True
                    temp_moves.pop(i)
                    break
            if not found_distance:
                return False

            if not temp_board.can_move(from_point, to_point, player_num):
                return False

            temp_board.move_piece(from_point, to_point, player_num)

        return True

    def execute_turn(self, moves):
        """Execute a complete turn with multiple moves.

        Args:
            moves (list): List of moves to execute

        Returns:
            bool: True if all moves were executed successfully, False otherwise
        """
        if not self.validate_complete_turn(moves):
            return False

        for move in moves:
            from_point = move[0]
            to_point = move[1]
            if not self.make_move(from_point, to_point):
                return False

        return True
