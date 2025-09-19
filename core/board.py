import copy
import random
class Board:
    """Represents a backgammon board with points, bar, and off-board areas."""
    
    def __init__(self):
        """Initialize an empty backgammon board."""
        self.points = [[] for _ in range(24)]
        self.bar = [[], []]  # Index 0 for player 1, index 1 for player 2
        self.off_board = [[], []]  # Index 0 for player 1, index 1 for player 2
    
    def setup_initial_position(self):
        """Set up the standard backgammon starting position."""
        # Clear the board first
        self.points = [[] for _ in range(24)]
        self.bar = [[], []]
        self.off_board = [[], []]
        
        # Set up Player 1 pieces
        self.points[0] = [1, 1]
        self.points[11] = [1, 1, 1, 1, 1]
        self.points[16] = [1, 1, 1]
        self.points[18] = [1, 1, 1, 1, 1]
        
        # Set up Player 2 pieces
        self.points[23] = [2, 2]
        self.points[12] = [2, 2, 2, 2, 2]
        self.points[7] = [2, 2, 2]
        self.points[5] = [2, 2, 2, 2, 2]
    
    def get_point(self, index):
        """Get information about a specific point on the board."""
        if index < 0 or index >= 24:
            raise IndexError("Point index must be between 0 and 23")
        
        pieces = self.points[index]
        count = len(pieces)
        player = pieces[0] if pieces else None
        
        return {
            'pieces': pieces.copy(),
            'count': count,
            'player': player
        }
    
    def can_move(self, from_point, to_point, player):
        """Check if a move from one point to another is valid."""
        # Can't move to the same position
        if from_point == to_point:
            return False
        
        # Check if there's a piece of the player at the origin
        if from_point < 0 or from_point >= 24:
            return False
        if not self.points[from_point] or self.points[from_point][0] != player:
            return False
        
        # Check if destination is valid
        if to_point < 0 or to_point >= 24:
            return False
        
        # Check destination point
        destination_pieces = self.points[to_point]
        if destination_pieces and len(destination_pieces) >= 2 and destination_pieces[0] != player:
            # Blocked by opponent (2 or more pieces)
            return False
        
        return True
    
    def move_piece(self, from_point, to_point, player):
        """Move a piece from one point to another."""
        if not self.can_move(from_point, to_point, player):
            return False
        
        # Remove piece from origin
        piece = self.points[from_point].pop()
        
        # Handle capture if there's exactly one opponent piece
        destination_pieces = self.points[to_point]
        if len(destination_pieces) == 1 and destination_pieces[0] != player:
            captured_piece = self.points[to_point].pop()
            opponent_bar_index = 0 if captured_piece == 1 else 1
            self.bar[opponent_bar_index].append(captured_piece)
        
        # Place piece at destination
        self.points[to_point].append(piece)
        
        return True
    
    def is_all_pieces_in_home(self, player):
        """Check if all player's pieces are in their home board."""
        # Check if any pieces on bar
        player_bar_index = 0 if player == 1 else 1
        if self.bar[player_bar_index]:
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
            for piece in self.points[i]:
                if piece == player:
                    return False
        
        # Make sure player has pieces in home
        has_pieces = False
        for i in home_range:
            for piece in self.points[i]:
                if piece == player:
                    has_pieces = True
                    break
            if has_pieces:
                break
                
        return has_pieces
    
    def can_bear_off(self, point, player, dice_value=None):
        """Check if a player can bear off a piece from a specific point."""
        # Check if all pieces are in home
        if not self.is_all_pieces_in_home(player):
            return False
        
        # Check if the point has a piece of the player
        if not self.points[point] or self.points[point][0] != player:
            return False
        
        # If no dice value specified, just check if in home board
        if dice_value is None:
            return True
        
        # Calculate distance to off-board
        if player == 1:
            distance = 23 - point + 1
            higher_points_range = range(point + 1, 24)
        else:
            distance = point + 1
            higher_points_range = range(0, point)
        
        # Exact roll
        if distance == dice_value:
            return True
        
        # Higher roll, but need to check if no pieces on higher points
        if distance < dice_value:
            for i in higher_points_range:
                for p in self.points[i]:
                    if p == player:
                        return False
            return True
        
        return False
    
    def bear_off_piece(self, point, player):
        """Bear off a piece from the board."""
        if not self.can_bear_off(point, player):
            return False
        
        # Remove piece from point and add to off_board
        if self.points[point] and self.points[point][0] == player:
            piece = self.points[point].pop()
            player_off_index = 0 if player == 1 else 1
            self.off_board[player_off_index].append(piece)
            return True
        
        return False
    
    def has_pieces_on_bar(self, player):
        """Check if a player has pieces on the bar."""
        player_bar_index = 0 if player == 1 else 1
        return len(self.bar[player_bar_index]) > 0
    
    def enter_from_bar(self, to_point, player):
        """Move a piece from the bar to a point on the board."""
        player_bar_index = 0 if player == 1 else 1
        
        # Check if player has pieces on bar
        if not self.bar[player_bar_index]:
            return False
        
        # Check if destination is valid
        if to_point < 0 or to_point >= 24:
            return False
            
        # Check if destination is not blocked
        destination_pieces = self.points[to_point]
        if destination_pieces and len(destination_pieces) >= 2 and destination_pieces[0] != player:
            return False
        
        # Handle capture
        if len(destination_pieces) == 1 and destination_pieces[0] != player:
            captured_piece = self.points[to_point].pop()
            opponent_bar_index = 0 if captured_piece == 1 else 1
            self.bar[opponent_bar_index].append(captured_piece)
        
        # Move piece from bar to point
        piece = self.bar[player_bar_index].pop()
        self.points[to_point].append(piece)
        
        return True
    
    def get_possible_moves(self, player, dice_values):
        """Get all possible moves for a player given dice values."""
        moves = []
        player_bar_index = 0 if player == 1 else 1
        
        # If player has pieces on bar, they must move those first
        if self.bar[player_bar_index]:
            for dice in dice_values:
                if player == 1:
                    entry_point = 24 - dice
                else:
                    entry_point = dice - 1
                
                if 0 <= entry_point < 24:
                    # Check if can enter from bar
                    destination_pieces = self.points[entry_point]
                    if not destination_pieces or len(destination_pieces) < 2 or destination_pieces[0] == player:
                        moves.append({
                            'from': 'bar',
                            'to': entry_point,
                            'dice': dice
                        })
            return moves
        # Check for bearing off
        if self.is_all_pieces_in_home(player):
            if player == 1:
                home_range = range(18, 24)
            else:
                home_range = range(0, 6)
            
            for point in home_range:
                for dice in dice_values:
                    if self.points[point] and self.points[point][0] == player:
                        if self.can_bear_off(point, player, dice):
                            moves.append({
                                'from': point,
                                'to': 'off',
                                'dice': dice
                            })
        # Regular moves
        for from_point in range(24):
            if self.points[from_point] and self.points[from_point][0] == player:
                for dice in dice_values:
                    if player == 1:
                        to_point = from_point + dice
                    else:
                        to_point = from_point - dice
                    
                    if 0 <= to_point < 24:
                        if self.can_move(from_point, to_point, player):
                            moves.append({
                                'from': from_point,
                                'to': to_point,
                                'dice': dice
                            })
        
        return moves
    
    def is_game_over(self):
        """Check if the game is over (all pieces of a player are off the board)."""
        return len(self.off_board[0]) == 15 or len(self.off_board[1]) == 15
    
    def get_winner(self):
        """Get the winner of the game."""
        if len(self.off_board[0]) == 15:
            return 1
        elif len(self.off_board[1]) == 15:
            return 2
        return None
    
    def count_pieces_for_player(self, player):
        """Count pieces for a player across the board."""
        player_bar_index = 0 if player == 1 else 1
        count = 0
        
        # Count pieces on board
        for point in self.points:
            for piece in point:
                if piece == player:
                    count += 1
        
        # Count pieces on bar
        count += len(self.bar[player_bar_index])
        
        # Count pieces off board
        count += len(self.off_board[player_bar_index])
        
        return count
    
    def get_board_state(self):
        """Get the complete state of the board."""
        return {
            'points': [point.copy() for point in self.points],
            'bar': [bar.copy() for bar in self.bar],
            'off_board': [off.copy() for off in self.off_board]
        }
    
    def copy(self):
        """Create a deep copy of the board."""
        new_board = Board()
        new_board.points = copy.deepcopy(self.points)
        new_board.bar = copy.deepcopy(self.bar)
        new_board.off_board = copy.deepcopy(self.off_board)
        return new_board