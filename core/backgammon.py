from .player import Player
from .board import Board
from .dice import Dice
from .checker import Checker
class BackgammonGame:
    """Main Backgammon game class."""
    
    def __init__(self, player1=None, player2=None):
        """Initialize a new backgammon game."""
        if player1 is None:
            self.player1 = Player("Player 1", "white")
        else:
            self.player1 = player1
            
        if player2 is None:
            self.player2 = Player("Player 2", "black")
        else:
            self.player2 = player2
            
        self.board = Board()
        self.dice = Dice()
        self.current_player = self.player1
        self.last_roll = None
        self.available_moves = []
        self.move_history = []
        
        # Initialize checker objects for each player
        self.player1_checkers = [Checker("white") for _ in range(15)]
        self.player2_checkers = [Checker("black") for _ in range(15)]
    
    def setup_initial_position(self):
        """Set up the initial board position using Checker objects."""
        self.board.setup_initial_position()
        
        # Reset all checkers
        for checker in self.player1_checkers:
            checker.reset()
        for checker in self.player2_checkers:
            checker.reset()
            
        # Place player 1 checkers in their initial positions
        checker_index = 0
        # Point 1 (0-indexed as 0): 2 checkers
        for i in range(2):
            self.player1_checkers[checker_index].place_on_point(1)
            checker_index += 1
        # Point 12 (0-indexed as 11): 5 checkers  
        for i in range(5):
            self.player1_checkers[checker_index].place_on_point(12)
            checker_index += 1
        # Point 17 (0-indexed as 16): 3 checkers
        for i in range(3):
            self.player1_checkers[checker_index].place_on_point(17)
            checker_index += 1
        # Point 19 (0-indexed as 18): 5 checkers
        for i in range(5):
            self.player1_checkers[checker_index].place_on_point(19)
            checker_index += 1
            
        # Place player 2 checkers in their initial positions  
        checker_index = 0
        # Point 24 (0-indexed as 23): 2 checkers
        for i in range(2):
            self.player2_checkers[checker_index].place_on_point(24)
            checker_index += 1
        # Point 13 (0-indexed as 12): 5 checkers
        for i in range(5):
            self.player2_checkers[checker_index].place_on_point(13)
            checker_index += 1
        # Point 8 (0-indexed as 7): 3 checkers
        for i in range(3):
            self.player2_checkers[checker_index].place_on_point(8)
            checker_index += 1
        # Point 6 (0-indexed as 5): 5 checkers
        for i in range(5):
            self.player2_checkers[checker_index].place_on_point(6)
            checker_index += 1
    
    def get_checkers_at_point(self, point, player_num):
        """Get all checker objects at a specific point for a player."""
        checkers = []
        if player_num == 1:
            for checker in self.player1_checkers:
                if checker.position == point + 1:  # Convert 0-based to 1-based
                    checkers.append(checker)
        else:
            for checker in self.player2_checkers:
                if checker.position == point + 1:  # Convert 0-based to 1-based
                    checkers.append(checker)
        return checkers
    
    def get_checkers_on_bar(self, player_num):
        """Get all checker objects on the bar for a player."""
        checkers = []
        if player_num == 1:
            for checker in self.player1_checkers:
                if checker.is_on_bar:
                    checkers.append(checker)
        else:
            for checker in self.player2_checkers:
                if checker.is_on_bar:
                    checkers.append(checker)
        return checkers
    
    def get_borne_off_checkers(self, player_num):
        """Get all checker objects that have been borne off for a player."""
        checkers = []
        if player_num == 1:
            for checker in self.player1_checkers:
                if checker.is_borne_off:
                    checkers.append(checker)
        else:
            for checker in self.player2_checkers:
                if checker.is_borne_off:
                    checkers.append(checker)
        return checkers
    
    def move_checker_object(self, from_point, to_point, player_num):
        """Move a checker object from one point to another."""
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
        """Move a checker object from the bar to a point."""
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
        """Bear off a checker object from a point."""
        checkers_at_point = self.get_checkers_at_point(point, player_num)
        if not checkers_at_point:
            return False
        
        checker = checkers_at_point[0]  # Bear off the first checker
        checker.bear_off()
        return True
    
    def roll_dice(self):
        """Roll dice and update game state."""
        roll = self.dice.roll()
        self.last_roll = roll
        self.available_moves = self.dice.get_moves(roll)
        return roll
    
    def get_available_moves(self):
        """Get available moves based on last dice roll."""
        if self.last_roll is None:
            return []
        return self.dice.get_moves(self.last_roll)
    
    def validate_move(self, from_point, to_point):
        """Validate if a move is legal."""
        # Check if dice have been rolled
        if self.last_roll is None:
            return False
        
        # Update available moves if they are empty
        if len(self.available_moves) == 0 and self.last_roll is not None:
            self.available_moves = self.dice.get_moves(self.last_roll)
            
        if len(self.available_moves) == 0:
            return False
            
        # Get current player number
        if self.current_player == self.player1:
            player_num = 1
        else:
            player_num = 2
        
        # Check if there's a piece at the origin
        if from_point < 0 or from_point >= 24:
            return False
        if len(self.board.points[from_point]) == 0:
            return False
        if self.board.points[from_point][0] != player_num:
            return False
        
        # Calculate movement distance
        distance = abs(to_point - from_point)
        
        # Check if this distance is available
        found_distance = False
        for move in self.available_moves:
            if move == distance:
                found_distance = True
                break
        if not found_distance:
            return False
        
        # Check movement direction
        if player_num == 1 and to_point <= from_point:
            return False
        if player_num == 2 and to_point >= from_point:
            return False
        
        # Use board method to check if movement is valid
        return self.board.can_move(from_point, to_point, player_num)
    
    def make_move(self, from_point, to_point):
        """Execute a move on the board."""
        if not self.validate_move(from_point, to_point):
            return False
        
        if self.current_player == self.player1:
            player_num = 1
        else:
            player_num = 2
            
        distance = abs(to_point - from_point)
        
        # Save previous state for history
        old_board = self.board.copy()
        move_info = {
            'from': from_point,
            'to': to_point,
            'player': player_num,
            'captured': None,
            'board_state': old_board
        }
        
        # Check if there's a capture
        if len(self.board.points[to_point]) > 0:
            if len(self.board.points[to_point]) == 1:
                if self.board.points[to_point][0] != player_num:
                    move_info['captured'] = self.board.points[to_point][0]
        
        # Execute movement
        success = self.board.move_piece(from_point, to_point, player_num)
        
        if success:
            # Remove used dice value
            for i in range(len(self.available_moves)):
                if self.available_moves[i] == distance:
                    self.available_moves.pop(i)
                    break
            self.move_history.append(move_info)
        
        return success
    
    def move_from_bar(self, dice_value):
        """Move a checker from the bar to the board."""
        # Check if the dice value is available
        found_dice = False
        for move in self.available_moves:
            if move == dice_value:
                found_dice = True
                break
        if not found_dice:
            return False
            
        if self.current_player == self.player1:
            player_num = 1
            player_bar_index = 0
        else:
            player_num = 2
            player_bar_index = 1
        
        # Check if player has checkers on bar
        if len(self.board.bar[player_bar_index]) == 0:
            return False
        
        # Calculate entry point
        if player_num == 1:
            entry_point = 24 - dice_value
        else:
            entry_point = dice_value - 1
        
        # Validate entry point
        if entry_point < 0 or entry_point >= 24:
            return False
        
        # Save move for history
        old_board = self.board.copy()
        move_info = {
            'from': 'bar',
            'to': entry_point,
            'player': player_num,
            'captured': None,
            'board_state': old_board
        }
        
        # Execute movement
        success = self.board.enter_from_bar(entry_point, player_num)
        
        if success:
            # Remove used dice value
            for i in range(len(self.available_moves)):
                if self.available_moves[i] == dice_value:
                    self.available_moves.pop(i)
                    break
            self.move_history.append(move_info)
        
        return success
    
    def can_bear_off(self, player_num):
        """Check if a player can bear off checkers."""
        return self.board.is_all_pieces_in_home(player_num)
    
    def bear_off_checker(self, point):
        """Bear off a checker from the board."""
        if self.current_player == self.player1:
            player_num = 1
        else:
            player_num = 2
        
        if not self.can_bear_off(player_num):
            return False
        
        # Update available moves if they are empty
        if len(self.available_moves) == 0 and self.last_roll is not None:
            self.available_moves = self.dice.get_moves(self.last_roll)
            
        # Check if there are valid dice values
        if len(self.available_moves) == 0:
            return False
        
        # Try each available dice value
        for i in range(len(self.available_moves)):
            dice_value = self.available_moves[i]
            if self.board.can_bear_off(point, player_num, dice_value):
                # Save move for history
                old_board = self.board.copy()
                move_info = {
                    'from': point,
                    'to': 'off',
                    'player': player_num,
                    'captured': None,
                    'board_state': old_board
                }
                
                success = self.board.bear_off_piece(point, player_num)
                if success:
                    self.available_moves.pop(i)
                    self.move_history.append(move_info)
                    return True
        
        return False
    
    def switch_current_player(self):
        """Switch to the other player."""
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
    
    def is_game_over(self):
        """Check if the game is over."""
        return self.board.is_game_over()
    
    def get_winner(self):
        """Get the winner of the game."""
        winner_num = self.board.get_winner()
        if winner_num == 1:
            return self.player1
        elif winner_num == 2:
            return self.player2
        return None
    
    def get_game_state(self):
        """Get the current game state."""
        state = {}
        state['board'] = self.board.get_board_state()
        state['current_player'] = self.current_player
        state['last_roll'] = self.last_roll
        state['available_moves'] = []
        for move in self.available_moves:
            state['available_moves'].append(move)
        state['game_over'] = self.is_game_over()
        return state
    
    def get_player_by_color(self, color):
        """Get player by color."""
        if self.player1.color == color:
            return self.player1
        elif self.player2.color == color:
            return self.player2
        return None
    
    def reset_game(self):
        """Reset the game to initial state."""
        self.board = Board()
        self.current_player = self.player1
        self.last_roll = None
        self.available_moves = []
        self.move_history = []
        self.player1.reset()
        self.player2.reset()
        
        # Reset all checker objects
        for checker in self.player1_checkers:
            checker.reset()
        for checker in self.player2_checkers:
            checker.reset()
    
    def copy_game_state(self):
        """Create a copy of the current game state."""
        state = {}
        state['board'] = self.board.copy()
        state['players'] = {}
        state['players']['player1'] = Player(self.player1.name, self.player1.color)
        state['players']['player2'] = Player(self.player2.name, self.player2.color)
        state['current_player'] = self.current_player
        state['last_roll'] = self.last_roll
        state['available_moves'] = []
        for move in self.available_moves:
            state['available_moves'].append(move)
        state['move_history'] = []
        for move in self.move_history:
            state['move_history'].append(move)
        return state
    
    def undo_last_move(self):
        """Undo the last move."""
        if len(self.move_history) == 0:
            return False
        
        last_move = self.move_history.pop()
        self.board = last_move['board_state']
        
        # Restore available moves
        if self.last_roll is not None:
            self.available_moves = self.dice.get_moves(self.last_roll)
        
        return True
    
    def get_possible_destinations(self, from_point):
        """Get possible destinations from a given point."""
        # Update available moves if they are empty
        if len(self.available_moves) == 0 and self.last_roll is not None:
            self.available_moves = self.dice.get_moves(self.last_roll)
            
        if len(self.available_moves) == 0:
            return []
        
        if self.current_player == self.player1:
            player_num = 1
        else:
            player_num = 2
        
        # Check if there's a piece at the origin
        if from_point < 0 or from_point >= 24:
            return []
        if len(self.board.points[from_point]) == 0:
            return []
        if self.board.points[from_point][0] != player_num:
            return []
        
        destinations = []
        for move_dist in self.available_moves:
            if player_num == 1:
                to_point = from_point + move_dist
            else:
                to_point = from_point - move_dist
            
            if to_point >= 0 and to_point < 24:
                if self.board.can_move(from_point, to_point, player_num):
                    destinations.append(to_point)
        
        return destinations
    
    def has_valid_moves(self):
        """Check if current player has valid moves."""
        # Update available moves if they are empty
        if len(self.available_moves) == 0 and self.last_roll is not None:
            self.available_moves = self.dice.get_moves(self.last_roll)
            
        if len(self.available_moves) == 0:
            return False
        
        if self.current_player == self.player1:
            player_num = 1
        else:
            player_num = 2
        
        # Check if player must enter from bar first
        if self.must_enter_from_bar():
            for dice_value in self.available_moves:
                if player_num == 1:
                    entry_point = 24 - dice_value
                else:
                    entry_point = dice_value - 1
                
                if entry_point >= 0 and entry_point < 24:
                    if len(self.board.points[entry_point]) == 0:
                        return True
                    elif len(self.board.points[entry_point]) < 2:
                        return True
                    elif self.board.points[entry_point][0] == player_num:
                        return True
            return False
        
        # Check regular moves
        for point in range(24):
            destinations = self.get_possible_destinations(point)
            if len(destinations) > 0:
                return True
        
        # Check bearing off
        if self.can_bear_off(player_num):
            if player_num == 1:
                home_points = [18, 19, 20, 21, 22, 23]
            else:
                home_points = [0, 1, 2, 3, 4, 5]
                
            for point in home_points:
                if len(self.board.points[point]) > 0:
                    if self.board.points[point][0] == player_num:
                        for dice_value in self.available_moves:
                            if self.board.can_bear_off(point, player_num, dice_value):
                                return True
        
        return False
    
    def must_enter_from_bar(self):
        """Check if current player must enter checkers from bar."""
        if self.current_player == self.player1:
            player_num = 1
        else:
            player_num = 2
        return self.board.has_pieces_on_bar(player_num)
    
    def get_pip_count(self, player):
        """Calculate pip count for a player."""
        if player == self.player1:
            player_num = 1
        else:
            player_num = 2
            
        pip_count = 0
        
        # Count pips for pieces on board
        for point_idx in range(24):
            point = self.board.points[point_idx]
            for piece in point:
                if piece == player_num:
                    if player_num == 1:
                        pip_count = pip_count + (24 - point_idx)
                    else:
                        pip_count = pip_count + (point_idx + 1)
        
        # Count pips for pieces on bar
        if player_num == 1:
            player_bar_index = 0
            bar_pieces = len(self.board.bar[player_bar_index])
            pip_count = pip_count + (bar_pieces * 25)
        else:
            player_bar_index = 1
            bar_pieces = len(self.board.bar[player_bar_index])
            pip_count = pip_count + (bar_pieces * 24)
        
        return pip_count
    
    def auto_play_turn(self):
        """Automatically play a turn."""
        if not self.has_valid_moves():
            self.switch_current_player()
            return True
        return False
    
    def is_blocked_position(self, point, player_num):
        """Check if a position is blocked by opponent."""
        if point < 0 or point >= 24:
            return False
        
        pieces = self.board.points[point]
        if len(pieces) >= 2 and pieces[0] != player_num:
            return True
        return False
    
    def can_hit_opponent(self, point, player_num):
        """Check if player can hit opponent at given point."""
        if point < 0 or point >= 24:
            return False
        
        pieces = self.board.points[point]
        if len(pieces) == 1 and pieces[0] != player_num:
            return True
        return False
    
    def apply_game_rules(self):
        """Apply game rules."""
        return True
    
    def validate_complete_turn(self, moves):
        """Validate a complete turn with multiple moves."""
        # Create a temporary board to test moves
        temp_board = self.board.copy()
        temp_moves = []
        for move in self.available_moves:
            temp_moves.append(move)
        
        if self.current_player == self.player1:
            player_num = 1
        else:
            player_num = 2
        
        for move in moves:
            from_point = move[0]
            to_point = move[1]
            distance = abs(to_point - from_point)
            
            found_distance = False
            for i in range(len(temp_moves)):
                if temp_moves[i] == distance:
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
        """Execute a complete turn with multiple moves."""
        if not self.validate_complete_turn(moves):
            return False
        
        for move in moves:
            from_point = move[0]
            to_point = move[1]
            if not self.make_move(from_point, to_point):
                return False
        
        return True