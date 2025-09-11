import unittest
from core.board import Board
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

if __name__ == "__main__":
    unittest.main()