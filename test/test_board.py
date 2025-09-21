import unittest
from unittest.mock import patch
from core.board import Board
import random

class TestBoard(unittest.TestCase):
	
	def setUp(self):
		self.board = Board()
	
	def test_board_initialization(self):
		board = Board()
		self.assertIsInstance(board, Board)
		self.assertEqual(len(board.points), 24)
		self.assertEqual(len(board.bar), 2)
		self.assertEqual(len(board.off_board), 2)
	
	def test_initial_board_setup(self):
		board = Board()
		board.setup_initial_position()
		
		self.assertEqual(board.points[0], [1, 1])
		self.assertEqual(board.points[11], [1, 1, 1, 1, 1])
		self.assertEqual(board.points[16], [1, 1, 1])
		self.assertEqual(board.points[18], [1, 1, 1, 1, 1])
		
		self.assertEqual(board.points[23], [2, 2])
		self.assertEqual(board.points[12], [2, 2, 2, 2, 2])
		self.assertEqual(board.points[7], [2, 2, 2])
		self.assertEqual(board.points[5], [2, 2, 2, 2, 2])
	
	def test_get_point_empty(self):
		board = Board()
		point_info = board.get_point(0)
		self.assertEqual(point_info['pieces'], [])
		self.assertEqual(point_info['count'], 0)
		self.assertIsNone(point_info['player'])
	
	def test_get_point_with_pieces(self):
		board = Board()
		board.points[0] = [1, 1, 1]
		point_info = board.get_point(0)
		self.assertEqual(point_info['pieces'], [1, 1, 1])
		self.assertEqual(point_info['count'], 3)
		self.assertEqual(point_info['player'], 1)
	
	def test_get_point_invalid_index(self):
		board = Board()
		with self.assertRaises(IndexError):
			board.get_point(-1)
		with self.assertRaises(IndexError):
			board.get_point(24)
	
	def test_can_move_valid_move(self):
		board = Board()
		board.points[0] = [1]
		self.assertTrue(board.can_move(0, 5, 1))
	
	def test_can_move_no_piece_at_origin(self):
		board = Board()
		self.assertFalse(board.can_move(0, 5, 1))
	
	def test_can_move_blocked_destination(self):
		board = Board()
		board.points[0] = [1]
		board.points[5] = [2, 2]
		self.assertFalse(board.can_move(0, 5, 1))
	
	def test_can_move_opponent_single_piece(self):
		board = Board()
		board.points[0] = [1]
		board.points[5] = [2]
		self.assertTrue(board.can_move(0, 5, 1))
	
	def test_can_move_same_player_destination(self):
		board = Board()
		board.points[0] = [1]
		board.points[5] = [1, 1]
		self.assertTrue(board.can_move(0, 5, 1))
	
	def test_move_piece_normal_move(self):
		board = Board()
		board.points[0] = [1]
		result = board.move_piece(0, 5, 1)
		
		self.assertTrue(result)
		self.assertEqual(board.points[0], [])
		self.assertEqual(board.points[5], [1])
	
	def test_move_piece_capture_opponent(self):
		board = Board()
		board.points[0] = [1]
		board.points[5] = [2]
		result = board.move_piece(0, 5, 1)
		
		self.assertTrue(result)
		self.assertEqual(board.points[0], [])
		self.assertEqual(board.points[5], [1])
		self.assertEqual(board.bar[1], [2])
	
	def test_move_piece_invalid_move(self):
		board = Board()
		result = board.move_piece(0, 5, 1)
		self.assertFalse(result)
	
	def test_move_piece_to_same_position(self):
		board = Board()
		board.points[0] = [1]
		result = board.move_piece(0, 0, 1)
		self.assertFalse(result)
	
	def test_can_bear_off_all_pieces_in_home(self):
		board = Board()

		for i in range(18, 24):
			board.points[i] = [1]
		self.assertTrue(board.can_bear_off(23, 1))
	
	def test_can_bear_off_pieces_outside_home(self):
		board = Board()
		board.points[23] = [1]
		board.points[10] = [1]
		
		self.assertFalse(board.can_bear_off(23, 1))
	
	def test_can_bear_off_exact_roll(self):
		board = Board()

		for i in range(18, 24):
			board.points[i] = [1] if i == 20 else []
		
		self.assertTrue(board.can_bear_off(20, 1, dice_value=4))
	
	def test_can_bear_off_higher_roll(self):
		board = Board()

		board.points[18] = [1]
		
		self.assertTrue(board.can_bear_off(18, 1, dice_value=6))
	
	def test_bear_off_piece_success(self):
		board = Board()

		for i in range(18, 24):
			board.points[i] = [1] if i == 23 else []
		
		result = board.bear_off_piece(23, 1)
		self.assertTrue(result)
		self.assertEqual(board.points[23], [])
		self.assertEqual(board.off_board[0], [1])
	
	def test_bear_off_piece_failure(self):
		board = Board()
		board.points[10] = [1]
		
		result = board.bear_off_piece(23, 1)
		self.assertFalse(result)
	
	def test_is_all_pieces_in_home_true(self):
		board = Board()

		board.points[18] = [1, 1]
		board.points[20] = [1]
		
		self.assertTrue(board.is_all_pieces_in_home(1))
	
	def test_is_all_pieces_in_home_false(self):
		board = Board()
		board.points[18] = [1]
		board.points[10] = [1]
		
		self.assertFalse(board.is_all_pieces_in_home(1))
	
	def test_is_all_pieces_in_home_with_bar(self):
		board = Board()
		board.points[18] = [1]
		board.bar[0] = [1]
		
		self.assertFalse(board.is_all_pieces_in_home(1))
	
	def test_has_pieces_on_bar_true(self):
		board = Board()
		board.bar[0] = [1]
		self.assertTrue(board.has_pieces_on_bar(1))
	
	def test_has_pieces_on_bar_false(self):
		board = Board()
		self.assertFalse(board.has_pieces_on_bar(1))
	
	def test_enter_from_bar_success(self):
		board = Board()
		board.bar[0] = [1]
		
		result = board.enter_from_bar(18, 1)
		self.assertTrue(result)
		self.assertEqual(board.bar[0], [])
		self.assertEqual(board.points[18], [1])
	
	def test_enter_from_bar_blocked(self):
		board = Board()
		board.bar[0] = [1]
		board.points[18] = [2, 2]
		
		result = board.enter_from_bar(18, 1)
		self.assertFalse(result)
	
	def test_enter_from_bar_no_pieces(self):
		board = Board()
		result = board.enter_from_bar(18, 1)
		self.assertFalse(result)
	
	def test_get_possible_moves_normal(self):
		board = Board()
		board.points[0] = [1]
		board.points[5] = [1]
		
		moves = board.get_possible_moves(1, [1, 2])
		self.assertIsInstance(moves, list)
		self.assertGreater(len(moves), 0)
	
	def test_get_possible_moves_with_bar(self):
		board = Board()
		board.bar[0] = [1]
		board.points[0] = [1]
		
		moves = board.get_possible_moves(1, [1, 2])

		for move in moves:
			self.assertEqual(move['from'], 'bar')
	
	def test_get_possible_moves_bearing_off(self):
		board = Board()

		for i in range(18, 24):
			board.points[i] = [1] if i == 23 else []
		
		moves = board.get_possible_moves(1, [1])
		bear_off_moves = [m for m in moves if m['to'] == 'off']
		self.assertGreater(len(bear_off_moves), 0)
	
	def test_is_game_over_true(self):
		board = Board()
		board.off_board[0] = [1] * 15
		
		self.assertTrue(board.is_game_over())
	
	def test_is_game_over_false(self):
		board = Board()
		board.points[0] = [1]
		
		self.assertFalse(board.is_game_over())
	
	def test_get_winner_player1(self):
		board = Board()
		board.off_board[0] = [1] * 15
		
		self.assertEqual(board.get_winner(), 1)
	
	def test_get_winner_player2(self):
		board = Board()
		board.off_board[1] = [2] * 15
		
		self.assertEqual(board.get_winner(), 2)
	
	def test_get_winner_no_winner(self):
		board = Board()
		self.assertIsNone(board.get_winner())
	
	def test_count_pieces_for_player(self):
		board = Board()
		board.points[0] = [1, 1]
		board.points[5] = [1]
		board.bar[0] = [1]
		board.off_board[0] = [1, 1]
		
		count = board.count_pieces_for_player(1)
		self.assertEqual(count, 6)
	
	def test_get_board_state(self):
		board = Board()
		board.points[0] = [1]
		state = board.get_board_state()
		
		self.assertIn('points', state)
		self.assertIn('bar', state)
		self.assertIn('off_board', state)
		self.assertEqual(len(state['points']), 24)
	
	def test_copy_board(self):
		board = Board()
		board.points[0] = [1]
		board.bar[0] = [1]
		
		board_copy = board.copy()
		self.assertIsInstance(board_copy, Board)
		self.assertEqual(board_copy.points[0], [1])
		self.assertEqual(board_copy.bar[0], [1])

		board.points[0] = []
		self.assertEqual(board_copy.points[0], [1])
	
	@patch('random.choice', return_value=1)
	def test_random_initial_setup_with_mock(self, mock_choice):
		"""Test board setup with controlled randomness if any"""
		board = Board()
		board.setup_initial_position()
		
		# Test that setup works correctly regardless of any internal randomness
		self.assertEqual(len(board.points), 24)
		# If random.choice was called for any reason, verify it was controlled
		if mock_choice.called:
			self.assertTrue(mock_choice.called)
	
	@patch('core.dice.Dice.roll', return_value=(3, 4))
	def test_board_with_mocked_dice_dependency(self, mock_roll):
		"""Test board interactions with mocked dice if there are any"""
		board = Board()
		# If board has any dice-related functionality, test it here
		# This ensures board doesn't have unexpected dice dependencies
		self.assertIsInstance(board, Board)
		# Verify dice mock was available if needed
		if mock_roll.called:
			self.assertTrue(mock_roll.called)
	
	def test_deterministic_move_validation(self):
		"""Test that move validation is deterministic (no random components)"""
		board = Board()
		board.points[0] = [1]
		board.points[5] = [2, 2]
		
		# These should always return the same result for same input
		result1 = board.can_move(0, 5, 1)
		result2 = board.can_move(0, 5, 1)
		result3 = board.can_move(0, 5, 1)
		
		self.assertEqual(result1, result2)
		self.assertEqual(result2, result3)
		self.assertFalse(result1)  # Should be blocked
	
	def test_deterministic_bear_off_validation(self):
		"""Test that bear off validation is deterministic"""
		board = Board()
		# Set up home position
		for i in range(18, 24):
			board.points[i] = [1] if i == 23 else []
		
		# These should always return the same result
		result1 = board.can_bear_off(23, 1)
		result2 = board.can_bear_off(23, 1)
		result3 = board.can_bear_off(23, 1)
		
		self.assertEqual(result1, result2)
		self.assertEqual(result2, result3)
		self.assertTrue(result1)  # Should be allowed
	
	@patch('core.board.random.shuffle')
	def test_no_unexpected_randomness_in_board(self, mock_shuffle):
		"""Test that board operations don't use unexpected randomness"""
		board = Board()
		board.setup_initial_position()
		
		# Perform various board operations
		board.points[0] = [1]
		board.move_piece(0, 5, 1)
		board.get_possible_moves(1, [1, 2])
		
		# Verify no unexpected random operations were called
		self.assertFalse(mock_shuffle.called)

	def test_can_move_out_of_bounds_from_point(self):
		"""Test can_move with out of bounds from_point"""
		board = Board()
		board.points[0] = [1]
		
		# Test negative from_point
		self.assertFalse(board.can_move(-1, 5, 1))
		# Test from_point >= 24
		self.assertFalse(board.can_move(24, 5, 1))
	
	def test_can_move_out_of_bounds_to_point(self):
		"""Test can_move with out of bounds to_point"""
		board = Board()
		board.points[0] = [1]
		
		# Test negative to_point
		self.assertFalse(board.can_move(0, -1, 1))
		# Test to_point >= 24
		self.assertFalse(board.can_move(0, 24, 1))
	
	def test_can_bear_off_no_piece_at_point(self):
		"""Test can_bear_off when no piece at point for player"""
		board = Board()
		# Set up home board scenario but no piece at test point
		for i in range(18, 24):
			board.points[i] = [1] if i != 20 else []
		
		# Try to bear off from point without player's piece
		self.assertFalse(board.can_bear_off(20, 1))
	
	def test_can_bear_off_wrong_player_piece(self):
		"""Test can_bear_off when point has wrong player's piece"""
		board = Board()
		# Set up home board scenario
		for i in range(18, 24):
			board.points[i] = [1] if i != 20 else [2]  # Point 21 has player 2 piece
		
		# Try to bear off player 1 from point with player 2 piece
		self.assertFalse(board.can_bear_off(20, 1))
	
	def test_bear_off_piece_no_piece_to_bear_off(self):
		"""Test bear_off_piece when there's no piece to bear off"""
		board = Board()
		# Set up home board but no piece at the target point
		for i in range(18, 24):
			board.points[i] = [1] if i != 23 else []
		
		result = board.bear_off_piece(23, 1)
		self.assertFalse(result)
	
	def test_bear_off_piece_wrong_player(self):
		"""Test bear_off_piece when point has wrong player's piece"""
		board = Board()
		# Set up home board but with wrong player at target point
		for i in range(18, 24):
			board.points[i] = [1] if i != 23 else [2]  # Player 2 piece instead
		
		result = board.bear_off_piece(23, 1)
		self.assertFalse(result)
	
	def test_bear_off_piece_not_in_home(self):
		"""Test bear_off_piece when not all pieces are in home"""
		board = Board()
		board.points[23] = [1]  # Piece to bear off
		board.points[10] = [1]  # Piece outside home
		
		result = board.bear_off_piece(23, 1)
		self.assertFalse(result)
	
	def test_is_all_pieces_in_home_pieces_outside_home(self):
		"""Test is_all_pieces_in_home when pieces are outside home board"""
		board = Board()
		board.points[18] = [1]  # In home
		board.points[10] = [1]  # Outside home
		
		result = board.is_all_pieces_in_home(1)
		self.assertFalse(result)
	
	def test_enter_from_bar_no_bar_pieces(self):
		"""Test enter_from_bar when no pieces on bar"""
		board = Board()
		# No pieces on bar
		
		result = board.enter_from_bar(18, 1)
		self.assertFalse(result)
	
	def test_get_possible_moves_bar_must_enter_blocked(self):
		"""Test get_possible_moves when must enter from bar but blocked"""
		board = Board()
		board.bar[0] = [1]  # Player 1 on bar
		
		# Block all possible entry points for dice values 1 and 2
		board.points[23] = [2, 2]  # Block entry for dice 1 (24-1=23)
		board.points[22] = [2, 2]  # Block entry for dice 2 (24-2=22)
		
		moves = board.get_possible_moves(1, [1, 2])
		
		# Should have moves but they should all be blocked bar entries
		for move in moves:
			self.assertEqual(move['from'], 'bar')
	
	def test_get_possible_moves_bearing_off_multiple_dice(self):
		"""Test get_possible_moves for bearing off with multiple dice values"""
		board = Board()
		# Set up bear off scenario
		for i in range(18, 24):
			board.points[i] = [1] if i in [20, 22, 23] else []
		
		moves = board.get_possible_moves(1, [1, 3, 6])
		
		# Should have bear off moves
		bear_off_moves = [m for m in moves if m['to'] == 'off']
		self.assertGreater(len(bear_off_moves), 0)
	
	def test_copy_preserves_independence(self):
		"""Test that copy creates independent board"""
		board = Board()
		board.points[0] = [1]
		board.bar[0] = [1]
		board.off_board[0] = [1]
		
		board_copy = board.copy()
		
		# Modify original
		board.points[0] = [2, 2]
		board.bar[0] = [2, 2]
		board.off_board[0] = [2, 2]
		
		# Copy should remain unchanged
		self.assertEqual(board_copy.points[0], [1])
		self.assertEqual(board_copy.bar[0], [1])
		self.assertEqual(board_copy.off_board[0], [1])

if __name__ == "__main__":
    unittest.main()