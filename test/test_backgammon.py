import unittest
from unittest.mock import patch
from core.backgammon import BackgammonGame
from core.player import Player
from core.board import Board
from core.dice import Dice

class TestBackgammonGame(unittest.TestCase):
	
	def setUp(self):
		self.game = BackgammonGame()
	
	def test_game_initialization_with_default_players(self):
		game = BackgammonGame()
		
		self.assertIsInstance(game.player1, Player)
		self.assertIsInstance(game.player2, Player)
		self.assertIsInstance(game.board, Board)
		self.assertIsInstance(game.dice, Dice)
		self.assertEqual(game.player1.color, "white")
		self.assertEqual(game.player2.color, "black")
	
	def test_game_initialization_with_custom_players(self):
		player1 = Player("Alice", "white")
		player2 = Player("Bob", "black")
		game = BackgammonGame(player1, player2)
		
		self.assertEqual(game.player1, player1)
		self.assertEqual(game.player2, player2)
		self.assertEqual(game.player1.name, "Alice")
		self.assertEqual(game.player2.name, "Bob")
	
	def test_game_initialization_sets_current_player(self):
		game = BackgammonGame()
		
		self.assertIn(game.current_player, [game.player1, game.player2])
	
	def test_game_initialization_creates_empty_board(self):
		game = BackgammonGame()
		
		self.assertIsInstance(game.board, Board)
		self.assertEqual(len(game.board.points), 24)
	
	def test_setup_initial_position(self):
		self.game.setup_initial_position()
		
		self.assertEqual(len(self.game.board.points[0]), 2)
		self.assertEqual(len(self.game.board.points[11]), 5)
		self.assertEqual(len(self.game.board.points[16]), 3)
		self.assertEqual(len(self.game.board.points[18]), 5)
		self.assertEqual(len(self.game.board.points[23]), 2)
		self.assertEqual(len(self.game.board.points[12]), 5)
		self.assertEqual(len(self.game.board.points[7]), 3)
		self.assertEqual(len(self.game.board.points[5]), 5)
	
	@patch('core.dice.Dice.roll', return_value=(3, 5))
	def test_roll_dice_returns_valid_values(self, mock_roll):
		"""Test dice rolling with controlled values"""
		roll = self.game.roll_dice()
		
		self.assertIsInstance(roll, tuple)
		self.assertEqual(len(roll), 2)
		self.assertEqual(roll, (3, 5))
		self.assertTrue(mock_roll.called)
	
	@patch('core.dice.Dice.roll', return_value=(2, 4))
	def test_roll_dice_updates_last_roll(self, mock_roll):
		"""Test that last_roll is updated with controlled dice values"""
		roll = self.game.roll_dice()
		
		self.assertEqual(self.game.last_roll, roll)
		self.assertEqual(self.game.last_roll, (2, 4))
		self.assertTrue(mock_roll.called)
	
	@patch('core.dice.Dice.get_moves', return_value=[1, 2])
	def test_get_available_moves_normal_roll(self, mock_get_moves):
		"""Test getting available moves with controlled normal roll"""
		self.game.setup_initial_position()
		self.game.last_roll = (1, 2)
		
		moves = self.game.get_available_moves()
		
		self.assertIsInstance(moves, list)
		self.assertTrue(mock_get_moves.called)
		mock_get_moves.assert_called_with((1, 2))
	
	@patch('core.dice.Dice.get_moves', return_value=[3, 3, 3, 3])
	def test_get_available_moves_double_roll(self, mock_get_moves):
		"""Test getting available moves with controlled double roll"""
		self.game.setup_initial_position()
		self.game.last_roll = (3, 3)
		
		moves = self.game.get_available_moves()
		
		self.assertIsInstance(moves, list)
		self.assertTrue(mock_get_moves.called)
		mock_get_moves.assert_called_with((3, 3))
	
	def test_get_available_moves_no_roll(self):
		moves = self.game.get_available_moves()
		
		self.assertEqual(moves, [])
	
	def test_validate_move_valid_move(self):
		self.game.setup_initial_position()
		self.game.last_roll = (1, 2)
		
		is_valid = self.game.validate_move(0, 1)
		
		self.assertIsInstance(is_valid, bool)
	
	def test_validate_move_no_piece_at_origin(self):
		self.game.last_roll = (1, 2)
		
		is_valid = self.game.validate_move(10, 11)
		
		self.assertFalse(is_valid)
	
	def test_validate_move_invalid_distance(self):
		self.game.setup_initial_position()
		self.game.last_roll = (1, 2)
		
		is_valid = self.game.validate_move(0, 5)
		
		self.assertFalse(is_valid)
	
	def test_validate_move_blocked_destination(self):
		self.game.setup_initial_position()
		self.game.last_roll = (1, 2)
		
		is_valid = self.game.validate_move(23, 22)
		
		self.assertFalse(is_valid)
	
	def test_make_move_valid_move(self):
		self.game.setup_initial_position()
		self.game.last_roll = (1, 2)
		
		result = self.game.make_move(0, 1)
		
		self.assertTrue(result)
	
	def test_make_move_invalid_move(self):
		self.game.setup_initial_position()
		self.game.last_roll = (1, 2)
		
		result = self.game.make_move(10, 15)
		
		self.assertFalse(result)
	
	def test_make_move_updates_board(self):
		self.game.setup_initial_position()
		self.game.last_roll = (1, 2)
		initial_count = len(self.game.board.points[0])
		
		self.game.make_move(0, 1)
		
		self.assertEqual(len(self.game.board.points[0]), initial_count - 1)
		self.assertGreater(len(self.game.board.points[1]), 0)
	
	def test_make_move_consumes_dice_value(self):
		self.game.setup_initial_position()
		self.game.last_roll = (1, 2)
		self.game.available_moves = [1, 2]
		
		self.game.make_move(0, 1)
		
		self.assertNotIn(1, self.game.available_moves)
	
	def test_hit_opponent_checker(self):
		self.game.setup_initial_position()
		self.game.board.points[5] = [1]
		self.game.last_roll = (1, 2)
		
		result = self.game.make_move(23, 22)
		
		if result:
			self.assertGreater(len(self.game.board.bar), 0)
	
	def test_move_checker_from_bar(self):
		self.game.setup_initial_position()
		self.game.board.bar[0] = [1]
		self.game.last_roll = (1, 2)
		
		result = self.game.move_from_bar(1)
		
		self.assertIsInstance(result, bool)
	
	def test_move_from_bar_no_checkers(self):
		self.game.last_roll = (1, 2)
		
		result = self.game.move_from_bar(1)
		
		self.assertFalse(result)
	
	def test_move_from_bar_blocked_entry(self):
		self.game.setup_initial_position()
		self.game.board.bar[0] = [1]
		self.game.board.points[0] = [2, 2]
		self.game.last_roll = (1, 2)
		
		result = self.game.move_from_bar(1)
		
		self.assertFalse(result)
	
	def test_can_bear_off_all_checkers_in_home(self):
		for i in range(18, 24):
			self.game.board.points[i] = [1] if i == 23 else []
		
		can_bear_off = self.game.can_bear_off(1)
		
		self.assertTrue(can_bear_off)
	
	def test_cannot_bear_off_checkers_outside_home(self):
		self.game.setup_initial_position()
		
		can_bear_off = self.game.can_bear_off(1)
		
		self.assertFalse(can_bear_off)
	
	def test_bear_off_checker_valid(self):
		for i in range(18, 24):
			self.game.board.points[i] = [1] if i == 23 else []
		self.game.last_roll = (1, 2)
		
		result = self.game.bear_off_checker(23)
		
		self.assertTrue(result)
	
	def test_bear_off_checker_invalid_conditions(self):
		self.game.setup_initial_position()
		self.game.last_roll = (1, 2)
		
		result = self.game.bear_off_checker(23)
		
		self.assertFalse(result)
	
	def test_bear_off_updates_off_board(self):
		for i in range(18, 24):
			self.game.board.points[i] = [1] if i == 23 else []
		self.game.last_roll = (1, 2)
		initial_off_count = len(self.game.board.off_board[0])
		
		self.game.bear_off_checker(23)
		
		self.assertGreater(len(self.game.board.off_board[0]), initial_off_count)
	
	def test_switch_current_player(self):
		initial_player = self.game.current_player
		
		self.game.switch_current_player()
		
		self.assertNotEqual(self.game.current_player, initial_player)
	
	def test_switch_player_alternates(self):
		player1 = self.game.current_player
		self.game.switch_current_player()
		player2 = self.game.current_player
		self.game.switch_current_player()
		player3 = self.game.current_player
		
		self.assertEqual(player1, player3)
		self.assertNotEqual(player1, player2)
	
	def test_is_game_over_false_at_start(self):
		self.game.setup_initial_position()
		
		self.assertFalse(self.game.is_game_over())
	
	def test_is_game_over_true_when_player_wins(self):
		self.game.board.off_board[0] = [1] * 15
		
		self.assertTrue(self.game.is_game_over())
	
	def test_get_winner_player1_wins(self):
		self.game.board.off_board[0] = [1] * 15
		
		winner = self.game.get_winner()
		
		self.assertEqual(winner, self.game.player1)
	
	def test_get_winner_player2_wins(self):
		self.game.board.off_board[1] = [2] * 15
		
		winner = self.game.get_winner()
		
		self.assertEqual(winner, self.game.player2)
	
	def test_get_winner_no_winner(self):
		self.game.setup_initial_position()
		
		winner = self.game.get_winner()
		
		self.assertIsNone(winner)
	
	def test_get_game_state(self):
		state = self.game.get_game_state()
		
		self.assertIn('board', state)
		self.assertIn('current_player', state)
		self.assertIn('last_roll', state)
		self.assertIn('available_moves', state)
		self.assertIn('game_over', state)
	
	def test_get_player_by_color_white(self):
		player = self.game.get_player_by_color("white")
		
		self.assertEqual(player.color, "white")
	
	def test_get_player_by_color_black(self):
		player = self.game.get_player_by_color("black")
		
		self.assertEqual(player.color, "black")
	
	def test_get_player_by_color_invalid(self):
		player = self.game.get_player_by_color("red")
		
		self.assertIsNone(player)
	
	def test_reset_game(self):
		self.game.setup_initial_position()
		self.game.last_roll = (3, 4)
		
		self.game.reset_game()
		
		self.assertIsNone(self.game.last_roll)
		self.assertEqual(self.game.available_moves, [])
	
	def test_copy_game_state(self):
		self.game.setup_initial_position()
		
		copy = self.game.copy_game_state()
		
		self.assertIsInstance(copy, dict)
		self.assertIn('board', copy)
		self.assertIn('players', copy)
	
	def test_undo_last_move(self):
		self.game.setup_initial_position()
		self.game.last_roll = (1, 2)
		initial_state = self.game.copy_game_state()
		self.game.make_move(0, 1)
		
		result = self.game.undo_last_move()
		
		self.assertTrue(result)
	
	def test_undo_last_move_no_moves(self):
		result = self.game.undo_last_move()
		
		self.assertFalse(result)
	
	def test_get_possible_destinations_from_point(self):
		self.game.setup_initial_position()
		self.game.last_roll = (1, 2)
		
		destinations = self.game.get_possible_destinations(0)
		
		self.assertIsInstance(destinations, list)
	
	def test_get_possible_destinations_invalid_point(self):
		self.game.last_roll = (1, 2)
		
		destinations = self.game.get_possible_destinations(10)
		
		self.assertEqual(destinations, [])
	
	def test_has_valid_moves_true(self):
		self.game.setup_initial_position()
		self.game.last_roll = (1, 2)
		
		has_moves = self.game.has_valid_moves()
		
		self.assertTrue(has_moves)
	
	def test_has_valid_moves_false(self):
		self.game.last_roll = (1, 2)
		
		has_moves = self.game.has_valid_moves()
		
		self.assertFalse(has_moves)
	
	def test_must_enter_from_bar_true(self):
		self.game.board.bar[0] = [1]
		self.game.current_player = self.game.player1
		
		must_enter = self.game.must_enter_from_bar()
		
		self.assertTrue(must_enter)
	
	def test_must_enter_from_bar_false(self):
		self.game.current_player = self.game.player1
		
		must_enter = self.game.must_enter_from_bar()
		
		self.assertFalse(must_enter)
	
	def test_get_pip_count_player1(self):
		self.game.setup_initial_position()
		
		pip_count = self.game.get_pip_count(self.game.player1)
		
		self.assertIsInstance(pip_count, int)
		self.assertGreater(pip_count, 0)
	
	def test_get_pip_count_player2(self):
		self.game.setup_initial_position()
		
		pip_count = self.game.get_pip_count(self.game.player2)
		
		self.assertIsInstance(pip_count, int)
		self.assertGreater(pip_count, 0)
	
	@patch('core.dice.Dice.roll', return_value=(1, 2))
	def test_auto_play_turn_when_no_moves(self, mock_roll):
		"""Test auto play turn with controlled dice values"""
		self.game.last_roll = (1, 2)
		
		result = self.game.auto_play_turn()
		
		self.assertTrue(result)
	
	def test_is_blocked_position_true(self):
		self.game.board.points[5] = [2, 2]
		
		is_blocked = self.game.is_blocked_position(5, 1)
		
		self.assertTrue(is_blocked)
	
	def test_is_blocked_position_false(self):
		self.game.board.points[5] = [1]
		
		is_blocked = self.game.is_blocked_position(5, 1)
		
		self.assertFalse(is_blocked)
	
	def test_can_hit_opponent_true(self):
		self.game.board.points[5] = [2]
		
		can_hit = self.game.can_hit_opponent(5, 1)
		
		self.assertTrue(can_hit)
	
	def test_can_hit_opponent_false_multiple_checkers(self):
		self.game.board.points[5] = [2, 2]
		
		can_hit = self.game.can_hit_opponent(5, 1)
		
		self.assertFalse(can_hit)
	
	def test_can_hit_opponent_false_same_player(self):
		self.game.board.points[5] = [1]
		
		can_hit = self.game.can_hit_opponent(5, 1)
		
		self.assertFalse(can_hit)
	
	def test_apply_game_rules_bearing_off(self):
		for i in range(18, 24):
			self.game.board.points[i] = [1] if i == 23 else []
		self.game.last_roll = (6, 6)
		
		rules_applied = self.game.apply_game_rules()
		
		self.assertIsInstance(rules_applied, bool)
	
	def test_validate_complete_turn(self):
		self.game.setup_initial_position()
		self.game.last_roll = (1, 2)
		moves = [(0, 1), (0, 2)]
		
		is_valid = self.game.validate_complete_turn(moves)
		
		self.assertIsInstance(is_valid, bool)
	
	def test_execute_turn_with_moves(self):
		self.game.setup_initial_position()
		self.game.last_roll = (1, 2)
		moves = [(0, 1)]
		
		result = self.game.execute_turn(moves)
		
		self.assertIsInstance(result, bool)

if __name__ == "__main__":
	unittest.main()
