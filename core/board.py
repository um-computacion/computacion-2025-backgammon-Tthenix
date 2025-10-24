"""Board module for the Backgammon game.

This module contains the Board class that represents the game board
with points, bar, and off-board areas for the Backgammon game.
"""

import copy


class Board:
    """Represents a backgammon board with points, bar, and off-board areas."""

    def __init__(self):
        """Initialize an empty backgammon board."""
        self.__points__ = [[] for _ in range(24)]
        # BARRA: Fichas capturadas van al lado del OPONENTE
        # Index 0 = lado blanco (fichas negras capturadas entran aquí)
        # Index 1 = lado negro (fichas blancas capturadas entran aquí)
        self.__checker_bar__ = [[], []]
        self.__off_board__ = [[], []]  # Index 0 for player 1, index 1 for player 2

    def setup_initial_position(self):
        """Set up the standard backgammon starting position."""
        # Clear the board first
        self.__points__ = [[] for _ in range(24)]
        self.__checker_bar__ = [[], []]
        self.__off_board__ = [[], []]

        # Set up Player 1 pieces
        self.__points__[0] = [1, 1]
        self.__points__[11] = [1, 1, 1, 1, 1]
        self.__points__[16] = [1, 1, 1]
        self.__points__[18] = [1, 1, 1, 1, 1]

        # Set up Player 2 pieces
        self.__points__[23] = [2, 2]
        self.__points__[12] = [2, 2, 2, 2, 2]
        self.__points__[7] = [2, 2, 2]
        self.__points__[5] = [2, 2, 2, 2, 2]

    def get_point(self, index):
        """Get information about a specific point on the board."""
        if index < 0 or index >= 24:
            raise IndexError("Point index must be between 0 and 23")

        pieces = self.__points__[index]
        count = len(pieces)
        player = pieces[0] if pieces else None

        return {"pieces": pieces.copy(), "count": count, "player": player}

    def can_move(self, from_point, to_point, player):
        """Check if a move from one point to another is valid."""
        # Can't move to the same position
        if from_point == to_point:
            return False

        # Check if there's a piece of the player at the origin
        if from_point < 0 or from_point >= 24:
            return False
        if not self.__points__[from_point] or self.__points__[from_point][0] != player:
            return False

        # Check if destination is valid
        if to_point < 0 or to_point >= 24:
            return False

        # Check destination point
        destination_pieces = self.__points__[to_point]
        if (
            destination_pieces
            and len(destination_pieces) >= 2
            and destination_pieces[0] != player
        ):
            # Blocked by opponent (2 or more pieces)
            return False

        return True

    def move_piece(self, from_point, to_point, player):
        """Move a piece from one point to another."""
        if not self.can_move(from_point, to_point, player):
            return False

        # Remove piece from origin
        piece = self.__points__[from_point].pop()

        # Handle capture if there's exactly one opponent piece
        destination_pieces = self.__points__[to_point]
        if len(destination_pieces) == 1 and destination_pieces[0] != player:
            captured_piece = self.__points__[to_point].pop()
            # CORRECTO: La ficha capturada va al lado del OPONENTE (para reentrar desde allí):
            # - Ficha blanca (1) capturada va al lado negro (index 1)
            # - Ficha negra (2) capturada va al lado blanco (index 0)
            captured_piece_bar_index = 1 if captured_piece == 1 else 0
            self.__checker_bar__[captured_piece_bar_index].append(captured_piece)

        # Place piece at destination
        self.__points__[to_point].append(piece)

        return True

    def is_all_pieces_in_home(self, player):
        """Check if all player's pieces are in their home board."""
        # Check if any pieces on bar
        # Fichas blancas (1) capturadas están en el lado negro (index 1)
        # Fichas negras (2) capturadas están en el lado blanco (index 0)
        player_bar_index = 1 if player == 1 else 0
        if self.__checker_bar__[player_bar_index]:
            return False

        # Define home and outer board based on player
        if player == 1:
            home_range = range(18, 24)
            outer_range = range(0, 18)
        else:
            home_range = range(0, 6)
            outer_range = range(6, 24)

        # Check if any pieces outside home
        for i in outer_range:
            for piece in self.__points__[i]:
                if piece == player:
                    return False

        # Make sure player has pieces in home
        has_pieces = False
        for i in home_range:
            for piece in self.__points__[i]:
                if piece == player:
                    has_pieces = True
                    break
            if has_pieces:
                break

        return has_pieces

    def can_bear_off(self, point, player, dice_value=None):
        """Check if a player can bear off a piece from a specific point."""
        # Must have all pieces in home and own a piece at the point
        if not self.is_all_pieces_in_home(player):
            return False
        if not self.__points__[point] or self.__points__[point][0] != player:
            return False

        # If no dice value specified, being in home is enough
        if dice_value is None:
            return True

        # Calculate distance to off-board and the range to check for higher points
        if player == 1:
            distance = 23 - point + 1
            higher_points_range = range(point + 1, 24)
        else:
            distance = point + 1
            higher_points_range = range(0, point)

        # Decide allowance with a single final return
        allowed = False
        if distance == dice_value:
            allowed = True
        elif distance < dice_value:
            has_higher_piece = False
            for i in higher_points_range:
                for p in self.__points__[i]:
                    if p == player:
                        has_higher_piece = True
                        break
                if has_higher_piece:
                    break
            allowed = not has_higher_piece

        return allowed

    def bear_off_piece(self, point, player):
        """Bear off a piece from the board."""
        if not self.can_bear_off(point, player):
            return False

        # Remove piece from point and add to off_board
        if self.__points__[point] and self.__points__[point][0] == player:
            piece = self.__points__[point].pop()
            player_off_index = 0 if player == 1 else 1
            self.__off_board__[player_off_index].append(piece)
            return True

        return False

    def has_pieces_on_bar(self, player):
        """Check if a player has pieces on the bar."""
        # Fichas blancas (1) capturadas están en el lado negro (index 1)
        # Fichas negras (2) capturadas están en el lado blanco (index 0)
        player_bar_index = 1 if player == 1 else 0
        return len(self.__checker_bar__[player_bar_index]) > 0

    def enter_from_bar(self, to_point, player):
        """Move a piece from the bar to a point on the board."""
        # Con lógica corregida: las fichas capturadas están en el lado del OPONENTE
        # Fichas blancas (1) capturadas están en el lado negro (index 1)
        # Fichas negras (2) capturadas están en el lado blanco (index 0)
        player_bar_index = 1 if player == 1 else 0

        # Check if player has their own pieces on opponent's side
        player_pieces_on_bar = [
            piece for piece in self.__checker_bar__[player_bar_index] if piece == player
        ]
        if not player_pieces_on_bar:
            return False

        # Check if destination is valid
        if to_point < 0 or to_point >= 24:
            return False

        # Check if destination is not blocked
        destination_pieces = self.__points__[to_point]
        if (
            destination_pieces
            and len(destination_pieces) >= 2
            and destination_pieces[0] != player
        ):
            return False

        # Store the piece to move BEFORE handling capture to avoid confusion
        # Remove the player's own piece from opponent's side
        for i, piece in enumerate(self.__checker_bar__[player_bar_index]):
            if piece == player:
                piece_to_move = self.__checker_bar__[player_bar_index].pop(i)
                break

        # Handle capture (after removing our piece from bar)
        if len(destination_pieces) == 1 and destination_pieces[0] != player:
            captured_piece = self.__points__[to_point].pop()
            # CORRECTO: La ficha capturada va al lado del OPONENTE (para reentrar desde allí):
            # - Ficha blanca (1) capturada va al lado negro (index 1)
            # - Ficha negra (2) capturada va al lado blanco (index 0)
            captured_piece_bar_index = 1 if captured_piece == 1 else 0
            self.__checker_bar__[captured_piece_bar_index].append(captured_piece)

        # Move our piece to the destination
        self.__points__[to_point].append(piece_to_move)

        return True

    def get_possible_moves(self, player, dice_values):
        """Get all possible moves for a player given dice values."""
        # Fichas blancas (1) capturadas están en el lado negro (index 1)
        # Fichas negras (2) capturadas están en el lado blanco (index 0)
        player_bar_index = 1 if player == 1 else 0
        if self.__checker_bar__[player_bar_index]:
            # Must enter from bar first
            return self._get_bar_entry_moves(player, dice_values)

        moves = []
        moves.extend(self._get_bear_off_moves(player, dice_values))
        moves.extend(self._get_regular_moves(player, dice_values))
        return moves

    def _get_bar_entry_moves(self, player, dice_values):
        """Generate legal bar entry moves for a player and dice values."""
        # REGLA BACKGAMMON: Las fichas RE-ENTRAN por la HOME del OPONENTE
        # Blancas (1) re-entran en puntos 0-5 (home de negras)
        # Negras (2) re-entran en puntos 19-24 (home de blancas)
        moves = []
        for dice in dice_values:
            entry_point = dice - 1 if player == 1 else 24 - dice
            if 0 <= entry_point < 24:
                destination_pieces = self.__points__[entry_point]
                if (
                    not destination_pieces
                    or len(destination_pieces) < 2
                    or destination_pieces[0] == player
                ):
                    moves.append({"from": "bar", "to": entry_point, "dice": dice})
        return moves

    def _get_bear_off_moves(self, player, dice_values):
        """Generate legal bearing-off moves for a player and dice values."""
        moves = []
        if not self.is_all_pieces_in_home(player):
            return moves
        home_range = range(18, 24) if player == 1 else range(0, 6)
        for point in home_range:
            if self.__points__[point] and self.__points__[point][0] == player:
                for dice in dice_values:
                    if self.can_bear_off(point, player, dice):
                        moves.append({"from": point, "to": "off", "dice": dice})
        return moves

    def _get_regular_moves(self, player, dice_values):
        """Generate legal on-board moves (non-bar, non-bear-off)."""
        moves = []
        for from_point in range(24):
            if self.__points__[from_point] and self.__points__[from_point][0] == player:
                for dice in dice_values:
                    to_point = from_point + dice if player == 1 else from_point - dice
                    if 0 <= to_point < 24 and self.can_move(
                        from_point, to_point, player
                    ):
                        moves.append({"from": from_point, "to": to_point, "dice": dice})
        return moves

    def is_game_over(self):
        """Check if the game is over (all pieces of a player are off the board)."""
        return len(self.__off_board__[0]) == 15 or len(self.__off_board__[1]) == 15

    def get_winner(self):
        """Get the winner of the game."""
        if len(self.__off_board__[0]) == 15:
            return 1
        if len(self.__off_board__[1]) == 15:
            return 2
        return None

    def count_pieces_for_player(self, player):
        """Count pieces for a player across the board."""
        # Fichas blancas (1) capturadas están en el lado negro (index 1)
        # Fichas negras (2) capturadas están en el lado blanco (index 0)
        player_bar_index = 1 if player == 1 else 0
        count = 0

        # Count pieces on board
        for point in self.__points__:
            for piece in point:
                if piece == player:
                    count += 1

        # Count pieces on bar
        # Contar SOLO las fichas del jugador en la barra
        for piece in self.__checker_bar__[player_bar_index]:
            if piece == player:
                count += 1

        # Count pieces off board
        # El off_board usa el índice basado en el jugador (0 para jugador 1, 1 para jugador 2)
        player_off_index = 0 if player == 1 else 1
        count += len(self.__off_board__[player_off_index])

        return count

    def get_board_state(self):
        """Get the complete state of the board."""
        return {
            "points": [point.copy() for point in self.__points__],
            "bar": [checker_bar.copy() for checker_bar in self.__checker_bar__],
            "off_board": [off.copy() for off in self.__off_board__],
        }

    def copy(self):
        """Create a deep copy of the board."""
        new_board = Board()
        new_board.__points__ = copy.deepcopy(self.__points__)
        new_board.__checker_bar__ = copy.deepcopy(self.__checker_bar__)
        new_board.__off_board__ = copy.deepcopy(self.__off_board__)
        return new_board
