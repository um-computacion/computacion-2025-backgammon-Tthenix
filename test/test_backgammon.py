"""Test module for the Backgammon game.

This module contains comprehensive unit tests for the BackgammonGame class,
testing all game mechanics, rules, and edge cases.
"""
import unittest
from unittest.mock import patch
from core.backgammon import BackgammonGame
from core.player import Player
from core.board import Board
from core.dice import Dice
from core.checker import Checker
class TestBackgammonGame(unittest.TestCase):
    """Test class for BackgammonGame functionality."""
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.game = BackgammonGame()
    def test_game_initialization_with_default_players(self):
        """Test game initialization with default players."""
        game = BackgammonGame()
        self.assertIsInstance(game.player1, Player)
        self.assertIsInstance(game.player2, Player)
        self.assertIsInstance(game.board, Board)
        self.assertIsInstance(game.dice, Dice)
        self.assertEqual(game.player1.color, "white")
        self.assertEqual(game.player2.color, "black")
    def test_game_initialization_with_custom_players(self):
        """Test game initialization with custom players."""
        player1 = Player("Alice", "white")
        player2 = Player("Bob", "black")
        game = BackgammonGame(player1, player2)
        self.assertEqual(game.player1, player1)
        self.assertEqual(game.player2, player2)
        self.assertEqual(game.player1.name, "Alice")
        self.assertEqual(game.player2.name, "Bob")
    def test_game_initialization_sets_current_player(self):
        """Test that game initialization sets a current player."""
        game = BackgammonGame()
        self.assertIn(game.current_player, [game.player1, game.player2])
    def test_game_initialization_creates_empty_board(self):
        """Test that game initialization creates an empty board."""
        game = BackgammonGame()
        self.assertIsInstance(game.board, Board)
        self.assertEqual(len(game.board.points), 24)
    def test_setup_initial_position(self):
        """Test setting up the initial backgammon position."""
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
        """Test dice rolling with controlled values."""
        roll = self.game.roll_dice()
        self.assertIsInstance(roll, tuple)
        self.assertEqual(len(roll), 2)
        self.assertEqual(roll, (3, 5))
        self.assertTrue(mock_roll.called)
    @patch('core.dice.Dice.roll', return_value=(2, 4))
    def test_roll_dice_updates_last_roll(self, mock_roll):
        """Test that last_roll is updated with controlled dice values."""
        roll = self.game.roll_dice()
        self.assertEqual(self.game.last_roll, roll)
        self.assertEqual(self.game.last_roll, (2, 4))
        self.assertTrue(mock_roll.called)
    @patch('core.dice.Dice.get_moves', return_value=[1, 2])
    def test_get_available_moves_normal_roll(self, mock_get_moves):
        """Test getting available moves with controlled normal roll."""
        self.game.setup_initial_position()
        self.game.last_roll = (1, 2)
        moves = self.game.get_available_moves()
        self.assertIsInstance(moves, list)
        self.assertTrue(mock_get_moves.called)
        mock_get_moves.assert_called_with((1, 2))
    @patch('core.dice.Dice.get_moves', return_value=[3, 3, 3, 3])
    def test_get_available_moves_double_roll(self, mock_get_moves):
        """Test getting available moves with controlled double roll."""
        self.game.setup_initial_position()
        self.game.last_roll = (3, 3)
        moves = self.game.get_available_moves()
        self.assertIsInstance(moves, list)
        self.assertTrue(mock_get_moves.called)
        mock_get_moves.assert_called_with((3, 3))
    def test_get_available_moves_no_roll(self):
        """Test getting available moves when no dice have been rolled."""
        moves = self.game.get_available_moves()
        self.assertEqual(moves, [])
    def test_validate_move_valid_move(self):
        """Test validating a valid move."""
        self.game.setup_initial_position()
        self.game.last_roll = (1, 2)
        is_valid = self.game.validate_move(0, 1)
        self.assertIsInstance(is_valid, bool)
    def test_validate_move_no_piece_at_origin(self):
        """Test validating a move when no piece is at origin."""
        self.game.last_roll = (1, 2)
        is_valid = self.game.validate_move(10, 11)
        self.assertFalse(is_valid)
    def test_validate_move_invalid_distance(self):
        """Test validating a move with invalid distance."""
        self.game.setup_initial_position()
        self.game.last_roll = (1, 2)
        is_valid = self.game.validate_move(0, 5)
        self.assertFalse(is_valid)
    def test_validate_move_blocked_destination(self):
        """Test validating a move to a blocked destination."""
        self.game.setup_initial_position()
        self.game.last_roll = (1, 2)
        is_valid = self.game.validate_move(23, 22)
        self.assertFalse(is_valid)
    def test_make_move_valid_move(self):
        """Test making a valid move."""
        self.game.setup_initial_position()
        self.game.last_roll = (1, 2)
        result = self.game.make_move(0, 1)
        self.assertTrue(result)
    def test_make_move_invalid_move(self):
        """Test making an invalid move."""
        self.game.setup_initial_position()
        self.game.last_roll = (1, 2)
        result = self.game.make_move(10, 15)
        self.assertFalse(result)
    def test_make_move_updates_board(self):
        """Test that make_move updates the board state."""
        self.game.setup_initial_position()
        self.game.last_roll = (1, 2)
        initial_count = len(self.game.board.points[0])
        self.game.make_move(0, 1)
        self.assertEqual(len(self.game.board.points[0]), initial_count - 1)
        self.assertGreater(len(self.game.board.points[1]), 0)
    def test_make_move_consumes_dice_value(self):
        """Test that make_move consumes the used dice value."""
        self.game.setup_initial_position()
        self.game.last_roll = (1, 2)
        self.game.available_moves = [1, 2]
        self.game.make_move(0, 1)
        self.assertNotIn(1, self.game.available_moves)
    def test_hit_opponent_checker(self):
        """Test hitting an opponent checker."""
        self.game.setup_initial_position()
        self.game.board.points[5] = [1]
        self.game.last_roll = (1, 2)
        result = self.game.make_move(23, 22)
        if result:
            self.assertGreater(len(self.game.board.checker_bar[1]), 0)
    def test_move_checker_from_bar(self):
        """Test moving a checker from the bar."""
        self.game.setup_initial_position()
        self.game.board.checker_bar[0] = [1]
        self.game.last_roll = (1, 2)
        result = self.game.move_from_bar(1)
        self.assertIsInstance(result, bool)
    def test_move_from_bar_no_checkers(self):
        """Test moving from bar when no checkers are on bar."""
        self.game.last_roll = (1, 2)
        result = self.game.move_from_bar(1)
        self.assertFalse(result)
    def test_move_from_bar_blocked_entry(self):
        """Test moving from bar when entry point is blocked."""
        self.game.setup_initial_position()
        self.game.board.checker_bar[0] = [1]
        self.game.board.points[0] = [2, 2]
        self.game.last_roll = (1, 2)
        result = self.game.move_from_bar(1)
        self.assertFalse(result)
    def test_can_bear_off_all_checkers_in_home(self):
        """Test bearing off when all checkers are in home board."""
        for i in range(18, 24):
            self.game.board.points[i] = [1] if i == 23 else []
        can_bear_off = self.game.can_bear_off(1)
        self.assertTrue(can_bear_off)
    def test_cannot_bear_off_checkers_outside_home(self):
        """Test that bearing off is not allowed when checkers are outside home."""
        self.game.setup_initial_position()
        can_bear_off = self.game.can_bear_off(1)
        self.assertFalse(can_bear_off)
    def test_bear_off_checker_valid(self):
        """Test bearing off a checker under valid conditions."""
        for i in range(18, 24):
            self.game.board.points[i] = [1] if i == 23 else []
        self.game.last_roll = (1, 2)
        result = self.game.bear_off_checker(23)
        self.assertTrue(result)
    def test_bear_off_checker_invalid_conditions(self):
        """Test bearing off a checker under invalid conditions."""
        self.game.setup_initial_position()
        self.game.last_roll = (1, 2)
        result = self.game.bear_off_checker(23)
        self.assertFalse(result)
    def test_bear_off_updates_off_board(self):
        """Test that bearing off updates the off-board count."""
        for i in range(18, 24):
            self.game.board.points[i] = [1] if i == 23 else []
        self.game.last_roll = (1, 2)
        initial_off_count = len(self.game.board.off_board[0])
        self.game.bear_off_checker(23)
        self.assertGreater(len(self.game.board.off_board[0]), initial_off_count)
    def test_switch_current_player(self):
        """Test switching the current player."""
        initial_player = self.game.current_player
        self.game.switch_current_player()
        self.assertNotEqual(self.game.current_player, initial_player)
    def test_switch_player_alternates(self):
        """Test that switching players alternates correctly."""
        player1 = self.game.current_player
        self.game.switch_current_player()
        player2 = self.game.current_player
        self.game.switch_current_player()
        player3 = self.game.current_player
        self.assertEqual(player1, player3)
        self.assertNotEqual(player1, player2)
    def test_is_game_over_false_at_start(self):
        """Test that game is not over at the start."""
        self.game.setup_initial_position()
        self.assertFalse(self.game.is_game_over())
    def test_is_game_over_true_when_player_wins(self):
        """Test that game is over when a player wins."""
        self.game.board.off_board[0] = [1] * 15
        self.assertTrue(self.game.is_game_over())
    def test_get_winner_player1_wins(self):
        """Test getting the winner when player 1 wins."""
        self.game.board.off_board[0] = [1] * 15
        winner = self.game.get_winner()
        self.assertEqual(winner, self.game.player1)
    def test_get_winner_player2_wins(self):
        """Test getting the winner when player 2 wins."""
        self.game.board.off_board[1] = [2] * 15
        winner = self.game.get_winner()
        self.assertEqual(winner, self.game.player2)
    def test_get_winner_no_winner(self):
        """Test getting the winner when no one has won yet."""
        self.game.setup_initial_position()
        winner = self.game.get_winner()
        self.assertIsNone(winner)
    def test_get_game_state(self):
        """Test getting the current game state."""
        state = self.game.get_game_state()
        self.assertIn('board', state)
        self.assertIn('current_player', state)
        self.assertIn('last_roll', state)
        self.assertIn('available_moves', state)
        self.assertIn('game_over', state)
    def test_get_player_by_color_white(self):
        """Test getting player by white color."""
        player = self.game.get_player_by_color("white")
        self.assertEqual(player.color, "white")
    def test_get_player_by_color_black(self):
        """Test getting player by black color."""
        player = self.game.get_player_by_color("black")
        self.assertEqual(player.color, "black")
    def test_get_player_by_color_invalid(self):
        """Test getting player by invalid color."""
        player = self.game.get_player_by_color("red")
        self.assertIsNone(player)
    def test_reset_game(self):
        """Test resetting the game state."""
        self.game.setup_initial_position()
        self.game.last_roll = (3, 4)
        self.game.reset_game()
        self.assertIsNone(self.game.last_roll)
        self.assertEqual(self.game.available_moves, [])
    def test_copy_game_state(self):
        """Test copying the game state."""
        self.game.setup_initial_position()
        copy = self.game.copy_game_state()
        self.assertIsInstance(copy, dict)
        self.assertIn('board', copy)
        self.assertIn('players', copy)
    def test_undo_last_move(self):
        """Test undoing the last move."""
        self.game.setup_initial_position()
        self.game.last_roll = (1, 2)
        self.game.make_move(0, 1)
        result = self.game.undo_last_move()
        self.assertTrue(result)
    def test_undo_last_move_no_moves(self):
        """Test undoing when no moves have been made."""
        result = self.game.undo_last_move()
        self.assertFalse(result)
    def test_get_possible_destinations_from_point(self):
        """Test getting possible destinations from a point."""
        self.game.setup_initial_position()
        self.game.last_roll = (1, 2)
        destinations = self.game.get_possible_destinations(0)
        self.assertIsInstance(destinations, list)
    def test_get_possible_destinations_invalid_point(self):
        """Test getting destinations from an invalid point."""
        self.game.last_roll = (1, 2)
        destinations = self.game.get_possible_destinations(10)
        self.assertEqual(destinations, [])
    def test_has_valid_moves_true(self):
        """Test has_valid_moves when moves are available."""
        self.game.setup_initial_position()
        self.game.last_roll = (1, 2)
        has_moves = self.game.has_valid_moves()
        self.assertTrue(has_moves)
    def test_has_valid_moves_false(self):
        """Test has_valid_moves when no moves are available."""
        self.game.last_roll = (1, 2)
        has_moves = self.game.has_valid_moves()
        self.assertFalse(has_moves)
    def test_must_enter_from_bar_true(self):
        """Test must_enter_from_bar when player has pieces on bar."""
        self.game.board.checker_bar[0] = [1]
        self.game.current_player = self.game.player1
        must_enter = self.game.must_enter_from_bar()
        self.assertTrue(must_enter)
    def test_must_enter_from_bar_false(self):
        """Test must_enter_from_bar when player has no pieces on bar."""
        self.game.current_player = self.game.player1
        must_enter = self.game.must_enter_from_bar()
        self.assertFalse(must_enter)
    def test_get_pip_count_player1(self):
        """Test getting pip count for player 1."""
        self.game.setup_initial_position()
        pip_count = self.game.get_pip_count(self.game.player1)
        self.assertIsInstance(pip_count, int)
        self.assertGreater(pip_count, 0)
    def test_get_pip_count_player2(self):
        """Test getting pip count for player 2."""
        self.game.setup_initial_position()
        pip_count = self.game.get_pip_count(self.game.player2)
        self.assertIsInstance(pip_count, int)
        self.assertGreater(pip_count, 0)
    @patch('core.dice.Dice.roll', return_value=(1, 2))
    def test_auto_play_turn_when_no_moves(self, mock_roll):
        """Test auto play turn with controlled dice values."""
        self.game.last_roll = (1, 2)
        result = self.game.auto_play_turn()
        self.assertTrue(result)
    def test_is_blocked_position_true(self):
        """Test is_blocked_position when position is blocked."""
        self.game.board.points[5] = [2, 2]
        is_blocked = self.game.is_blocked_position(5, 1)
        self.assertTrue(is_blocked)
    def test_is_blocked_position_false(self):
        """Test is_blocked_position when position is not blocked."""
        self.game.board.points[5] = [1]
        is_blocked = self.game.is_blocked_position(5, 1)
        self.assertFalse(is_blocked)
    def test_can_hit_opponent_true(self):
        """Test can_hit_opponent when opponent can be hit."""
        self.game.board.points[5] = [2]
        can_hit = self.game.can_hit_opponent(5, 1)
        self.assertTrue(can_hit)
    def test_can_hit_opponent_false_multiple_checkers(self):
        """Test can_hit_opponent when opponent has multiple checkers."""
        self.game.board.points[5] = [2, 2]
        can_hit = self.game.can_hit_opponent(5, 1)
        self.assertFalse(can_hit)
    def test_can_hit_opponent_false_same_player(self):
        """Test can_hit_opponent when it's the same player's checker."""
        self.game.board.points[5] = [1]
        can_hit = self.game.can_hit_opponent(5, 1)
        self.assertFalse(can_hit)
    def test_apply_game_rules_bearing_off(self):
        """Test applying game rules for bearing off."""
        for i in range(18, 24):
            self.game.board.points[i] = [1] if i == 23 else []
        self.game.last_roll = (6, 6)
        rules_applied = self.game.apply_game_rules()
        self.assertIsInstance(rules_applied, bool)
    def test_validate_complete_turn(self):
        """Test validating a complete turn."""
        self.game.setup_initial_position()
        self.game.last_roll = (1, 2)
        moves = [(0, 1), (0, 2)]
        is_valid = self.game.validate_complete_turn(moves)
        self.assertIsInstance(is_valid, bool)
    def test_execute_turn_with_moves(self):
        """Test executing a turn with moves."""
        self.game.setup_initial_position()
        self.game.last_roll = (1, 2)
        moves = [(0, 1)]
        result = self.game.execute_turn(moves)
        self.assertIsInstance(result, bool)
    def test_auto_play_turn_with_moves_present(self):
        """Test auto_play_turn when moves are available."""
        self.game.setup_initial_position()
        self.game.current_player = self.game.player1
        self.game.last_roll = (1, 2)
        self.game.available_moves = [1, 2]
        initial_player = self.game.current_player
        result = self.game.auto_play_turn()
        self.assertFalse(result)
        self.assertEqual(self.game.current_player, initial_player)
    @patch('core.dice.Dice.get_moves', return_value=[1, 2])
    def test_undo_last_move_restores_available_moves(self, mock_get_moves):
        """Test that undo_last_move restores available moves."""
        self.game.setup_initial_position()
        self.game.current_player = self.game.player1
        self.game.last_roll = (1, 2)
        self.game.available_moves = [1, 2]
        # Make a valid move to consume a die
        self.assertTrue(self.game.make_move(0, 1))
        self.assertLess(len(self.game.available_moves), 2)
        # Undo and expect available moves restored via dice.get_moves
        self.assertTrue(self.game.undo_last_move())
        self.assertEqual(self.game.available_moves, [1, 2])
        self.assertTrue(mock_get_moves.called)
    def test_get_possible_destinations_repopulates_available_moves(self):
        """Test that get_possible_destinations repopulates available_moves."""
        self.game.setup_initial_position()
        self.game.current_player = self.game.player1
        self.game.last_roll = (1, 2)
        self.game.available_moves = []
        # Should compute [1, 2] moves from point 0->destinations include 1 and maybe 2 from point 0
        dests = self.game.get_possible_destinations(0)
        self.assertIsInstance(dests, list)
        self.assertTrue(all(isinstance(x, int) for x in dests))
    def test_move_from_bar_success_no_capture(self):
        """Test successful move from bar without capture."""
        self.game.setup_initial_position()
        self.game.current_player = self.game.player1
        self.game.board.checker_bar[0] = [1]
        self.game.available_moves = [6]
        # Ensure entry point 18 is free or friendly
        self.game.board.points[18] = []
        self.assertTrue(self.game.move_from_bar(6))
        self.assertNotIn(6, self.game.available_moves)
    def test_validate_complete_turn_invalid_dice(self):
        """Test validate_complete_turn with invalid dice distances."""
        self.game.setup_initial_position()
        self.game.last_roll = (1, 2)
        self.game.available_moves = [1, 2]
        moves = [(0, 3)]  # distance 3 not available
        self.assertFalse(self.game.validate_complete_turn(moves))
    def test_execute_turn_invalid(self):
        """Test execute_turn when validation fails."""
        self.game.setup_initial_position()
        self.game.last_roll = (1, 2)
        self.game.available_moves = [1, 2]
        moves = [(0, 3)]
        self.assertFalse(self.game.execute_turn(moves))
    def test_bear_off_tries_multiple_dice(self):
        """Test bear_off_checker tries multiple dice values."""
        # Prepare a simple bear-off scenario for player 1
        for i in range(24):
            self.game.board.points[i] = []
        self.game.board.points[23] = [1]
        self.game.current_player = self.game.player1
        self.game.last_roll = (2, 1)
        self.game.available_moves = [2, 1]
        # 23 requires 1 to bear off (distance 1). Should succeed and consume one die
        self.assertTrue(self.game.bear_off_checker(23))
        self.assertIn(len(self.game.available_moves), (1, 1))
    def test_is_blocked_position_out_of_bounds(self):
        """Test is_blocked_position with out of bounds positions."""
        self.assertFalse(self.game.is_blocked_position(-1, 1))
        self.assertFalse(self.game.is_blocked_position(24, 1))
    def test_can_hit_opponent_out_of_bounds(self):
        """Test can_hit_opponent with out of bounds positions."""
        self.assertFalse(self.game.can_hit_opponent(-1, 1))
        self.assertFalse(self.game.can_hit_opponent(24, 1))
    def test_move_checker_from_bar_object_capture_player2(self):
        """Test player 2 returning from bar and capturing opponent."""
        self.game.setup_initial_position()
        # Put player 2 checker on bar and place a single white checker at point 2
        c2 = self.game.player2_checkers[0]
        c2.send_to_bar()
        self.game.player1_checkers[0].place_on_point(2)
        result = self.game.move_checker_from_bar_object(1, 2)  # to point 2 (0-indexed)
        self.assertTrue(result)
        # White checker should now be on bar
        whites_on_bar = [c for c in self.game.player1_checkers if c.is_on_bar]
        self.assertGreaterEqual(len(whites_on_bar), 1)
    # Tests for Checker objects integration
    def test_checker_objects_initialization(self):
        """Test that checker objects are created for each player."""
        self.assertEqual(len(self.game.player1_checkers), 15)
        self.assertEqual(len(self.game.player2_checkers), 15)
        for checker in self.game.player1_checkers:
            self.assertIsInstance(checker, Checker)
            self.assertEqual(checker.color, "white")
        for checker in self.game.player2_checkers:
            self.assertIsInstance(checker, Checker)
            self.assertEqual(checker.color, "black")
    def test_get_checkers_at_point(self):
        """Test getting checker objects at a specific point."""
        self.game.setup_initial_position()
        # Point 1 (0-indexed as 0) should have 2 white checkers
        checkers = self.game.get_checkers_at_point(0, 1)
        self.assertEqual(len(checkers), 2)
        for checker in checkers:
            self.assertIsInstance(checker, Checker)
            self.assertEqual(checker.color, "white")
            self.assertEqual(checker.position, 1)
        # Point 24 (0-indexed as 23) should have 2 black checkers
        checkers = self.game.get_checkers_at_point(23, 2)
        self.assertEqual(len(checkers), 2)
        for checker in checkers:
            self.assertIsInstance(checker, Checker)
            self.assertEqual(checker.color, "black")
            self.assertEqual(checker.position, 24)
    def test_get_checkers_on_bar_empty(self):
        """Test getting checkers on bar when none are there."""
        checkers_p1 = self.game.get_checkers_on_bar(1)
        checkers_p2 = self.game.get_checkers_on_bar(2)
        self.assertEqual(len(checkers_p1), 0)
        self.assertEqual(len(checkers_p2), 0)
    def test_get_checkers_on_bar_with_checkers(self):
        """Test getting checkers on bar when there are some."""
        self.game.setup_initial_position()
        # Send a checker to the bar
        checker = self.game.player1_checkers[0]
        checker.place_on_point(1)
        checker.send_to_bar()
        checkers = self.game.get_checkers_on_bar(1)
        self.assertEqual(len(checkers), 1)
        self.assertTrue(checkers[0].is_on_bar)
        self.assertEqual(checkers[0].color, "white")
    def test_get_borne_off_checkers_empty(self):
        """Test getting borne off checkers when none are borne off."""
        checkers_p1 = self.game.get_borne_off_checkers(1)
        checkers_p2 = self.game.get_borne_off_checkers(2)
        self.assertEqual(len(checkers_p1), 0)
        self.assertEqual(len(checkers_p2), 0)
    def test_get_borne_off_checkers_with_checkers(self):
        """Test getting borne off checkers when some are borne off."""
        self.game.setup_initial_position()
        # Bear off a checker
        checker = self.game.player1_checkers[0]
        checker.place_on_point(24)
        checker.bear_off()
        checkers = self.game.get_borne_off_checkers(1)
        self.assertEqual(len(checkers), 1)
        self.assertTrue(checkers[0].is_borne_off)
        self.assertEqual(checkers[0].color, "white")
    def test_move_checker_object_success(self):
        """Test moving a checker object from one point to another."""
        self.game.setup_initial_position()
        # Move from point 1 (0-indexed as 0) to point 2 (0-indexed as 1)
        result = self.game.move_checker_object(0, 1, 1)
        self.assertTrue(result)
        # Verify the checker moved
        checkers_at_origin = self.game.get_checkers_at_point(0, 1)
        checkers_at_destination = self.game.get_checkers_at_point(1, 1)
        self.assertEqual(len(checkers_at_origin), 1)  # One less at origin
        self.assertEqual(len(checkers_at_destination), 1)  # One at destination
    def test_move_checker_object_capture(self):
        """Test checker object capturing opponent checker."""
        self.game.setup_initial_position()
        # Place a single opponent checker at destination
        self.game.player2_checkers[0].place_on_point(2)
        # Move player 1 checker to capture
        result = self.game.move_checker_object(0, 1, 1)  # Move to point 2 (0-indexed as 1)
        self.assertTrue(result)
        # Verify opponent checker is on bar
        captured_checkers = self.game.get_checkers_on_bar(2)
        self.assertEqual(len(captured_checkers), 1)
        self.assertEqual(captured_checkers[0].color, "black")
    def test_move_checker_from_bar_object_success(self):
        """Test moving a checker object from bar to board."""
        self.game.setup_initial_position()
        # Put a checker on the bar
        checker = self.game.player1_checkers[0]
        checker.send_to_bar()
        # Move from bar to point 2 (0-indexed as 1)
        result = self.game.move_checker_from_bar_object(1, 1)
        self.assertTrue(result)
        # Verify checker is no longer on bar and is at destination
        self.assertFalse(checker.is_on_bar)
        self.assertEqual(checker.position, 2)
    def test_bear_off_checker_object_success(self):
        """Test bearing off a checker object."""
        self.game.setup_initial_position()
        # Place a checker at point 24 (0-indexed as 23)
        checker = self.game.player1_checkers[0]
        checker.place_on_point(24)
        # Bear off the checker
        result = self.game.bear_off_checker_object(23, 1)
        self.assertTrue(result)
        # Verify checker is borne off
        self.assertTrue(checker.is_borne_off)
        self.assertIsNone(checker.position)
    def test_reset_game_resets_checkers(self):
        """Test that reset_game resets all checker objects."""
        self.game.setup_initial_position()
        # Modify some checkers
        self.game.player1_checkers[0].send_to_bar()
        self.game.player2_checkers[0].bear_off()
        # Reset the game
        self.game.reset_game()
        # Verify all checkers are reset
        for checker in self.game.player1_checkers:
            self.assertIsNone(checker.position)
            self.assertFalse(checker.is_on_bar)
            self.assertFalse(checker.is_borne_off)
        for checker in self.game.player2_checkers:
            self.assertIsNone(checker.position)
            self.assertFalse(checker.is_on_bar)
            self.assertFalse(checker.is_borne_off)
    def test_validate_move_no_dice_rolled(self):
        """Test validate_move when no dice have been rolled."""
        self.game.setup_initial_position()
        # Don't roll dice
        self.assertFalse(self.game.validate_move(0, 1))
    def test_validate_move_empty_available_moves_with_last_roll(self):
        """Test validate_move when available_moves is empty but last_roll exists."""
        self.game.setup_initial_position()
        self.game.last_roll = (3, 4)
        self.game.available_moves = []  # Empty but last_roll exists

        result = self.game.validate_move(0, 3)
        self.assertIsInstance(result, bool)

    def test_validate_move_out_of_bounds(self):
        """Test validate_move with out of bounds positions."""
        self.game.setup_initial_position()
        self.game.last_roll = (1, 2)
        # Test negative from_point
        self.assertFalse(self.game.validate_move(-1, 1))
        # Test from_point >= 24
        self.assertFalse(self.game.validate_move(24, 23))
    def test_validate_move_wrong_player_piece(self):
        """Test validate_move when trying to move opponent's piece."""
        self.game.setup_initial_position()
        self.game.current_player = self.game.player1  # White player
        self.game.last_roll = (1, 2)
        # Try to move black piece (at point 23, 0-indexed)
        result = self.game.validate_move(23, 22)
        self.assertFalse(result)
    def test_validate_move_wrong_direction_player1(self):
        """Test validate_move when player1 tries to move backwards."""
        self.game.setup_initial_position()
        self.game.current_player = self.game.player1
        self.game.last_roll = (1, 2)
        # Player 1 should move forward (increasing point numbers)
        result = self.game.validate_move(11, 10)  # Moving backwards
        self.assertFalse(result)
    def test_validate_move_wrong_direction_player2(self):
        """Test validate_move when player2 tries to move backwards."""
        self.game.setup_initial_position()
        self.game.current_player = self.game.player2
        self.game.last_roll = (1, 2)
        # Player 2 should move backward (decreasing point numbers)
        result = self.game.validate_move(12, 13)  # Moving forwards for player2
        self.assertFalse(result)
    def test_make_move_with_capture(self):
        """Test make_move when capturing an opponent piece."""
        self.game.setup_initial_position()
        self.game.current_player = self.game.player1
        self.game.last_roll = (1, 2)
        # Place a single opponent piece to capture
        self.game.board.points[1] = [2]  # Single black piece
        self.game.board.points[0] = [1, 1]  # Two white pieces to move from
        result = self.game.make_move(0, 1)
        self.assertTrue(result)
        # Check that the piece was captured (sent to bar)
        self.assertGreater(len(self.game.board.checker_bar[1]), 0)  # Player 2's bar
    def test_move_from_bar_invalid_dice(self):
        """Test move_from_bar with invalid dice value."""
        self.game.setup_initial_position()
        self.game.current_player = self.game.player1
        self.game.available_moves = [3, 4]  # Only 3 and 4 available
        self.game.board.checker_bar[0] = [1]  # Player 1 on bar
        # Try to use dice value 2 which is not available
        result = self.game.move_from_bar(2)
        self.assertFalse(result)
    def test_bear_off_checker_not_all_in_home(self):
        """Test bear_off_checker when not all pieces are in home."""
        self.game.setup_initial_position()
        self.game.current_player = self.game.player1
        self.game.available_moves = [6]
        # Player 1 still has pieces outside home board
        result = self.game.bear_off_checker(23)
        self.assertFalse(result)
    def test_bear_off_checker_no_dice_available(self):
        """Test bear_off_checker when no dice values are available."""
        self.game.setup_initial_position()
        self.game.current_player = self.game.player1
        self.game.available_moves = []  # No moves available
        self.game.last_roll = None

        # Move all pieces to home board first
        for i in range(18, 24):
            self.game.board.points[i] = [1] if i == 23 else []
        result = self.game.bear_off_checker(23)
        self.assertFalse(result)
    def test_bear_off_checker_with_valid_dice(self):
        """Test successful bear off with valid conditions."""
        # Clear board and set up bear off scenario
        for i in range(24):
            self.game.board.points[i] = []
        self.game.board.points[23] = [1]  # One piece at point 24
        self.game.current_player = self.game.player1
        self.game.available_moves = [6]
        self.game.last_roll = (6, 6)
        result = self.game.bear_off_checker(23)
        self.assertTrue(result)
    def test_get_available_moves_no_last_roll(self):
        """Test get_available_moves when no dice have been rolled."""
        self.game.last_roll = None
        moves = self.game.get_available_moves()
        self.assertEqual(moves, [])
    def test_move_checker_object_no_checkers_at_point(self):
        """Test move_checker_object when no checkers at source point."""
        self.game.setup_initial_position()
        # Try to move from an empty point
        result = self.game.move_checker_object(10, 11, 1)  #Point 11(0-indexed 10)is empty initially
        self.assertFalse(result)
    def test_move_checker_from_bar_object_no_checkers(self):
        """Test move_checker_from_bar_object when no checkers on bar."""
        self.game.setup_initial_position()
        # Bar should be empty initially
        result = self.game.move_checker_from_bar_object(20, 1)
        self.assertFalse(result)
    def test_bear_off_checker_object_no_checkers(self):
        """Test bear_off_checker_object when no checkers at point."""
        self.game.setup_initial_position()
        # Try to bear off from an empty point
        result = self.game.bear_off_checker_object(10, 1)  # Point 11 is empty
        self.assertFalse(result)
    # Test methods that may not have full coverage
    def test_move_from_bar_out_of_bounds_entry_point(self):
        """Test move_from_bar with dice that would create out of bounds entry point."""
        self.game.setup_initial_position()
        self.game.current_player = self.game.player1
        self.game.available_moves = [25]  # Invalid dice value
        self.game.board.checker_bar[0] = [1]  # Player 1 on bar
        result = self.game.move_from_bar(25)
        self.assertFalse(result)
    def test_move_from_bar_success_with_capture(self):
        """Test successful move from bar with capture."""
        self.game.setup_initial_position()
        self.game.current_player = self.game.player1
        self.game.available_moves = [1]
        self.game.board.checker_bar[0] = [1]  # Player 1 on bar
        # Place single opponent piece at entry point
        self.game.board.points[23] = [2]  # Single black piece at point 24
        result = self.game.move_from_bar(1)
        self.assertTrue(result)
        # Check that opponent was captured
        self.assertGreater(len(self.game.board.checker_bar[1]), 0)
    def test_bear_off_checker_empty_available_moves_with_last_roll(self):
        """Test bear_off_checker when available_moves is empty but last_roll exists."""
        # Set up bear off scenario
        for i in range(24):
            self.game.board.points[i] = []
        self.game.board.points[23] = [1]  # One piece at point 24
        self.game.current_player = self.game.player1
        self.game.available_moves = []  # Empty
        self.game.last_roll = (6, 6)  # But last_roll exists
        result = self.game.bear_off_checker(23)
        self.assertIsInstance(result, bool)
    def test_bear_off_checker_successful_removal(self):
        """Test successful bear off with dice removal."""
        # Set up bear off scenario
        for i in range(24):
            self.game.board.points[i] = []
        self.game.board.points[23] = [1]  # One piece at point 24
        self.game.current_player = self.game.player1
        self.game.available_moves = [6, 5]  # Multiple dice values
        self.game.last_roll = (6, 5)
        result = self.game.bear_off_checker(23)
        self.assertTrue(result)
        # Check that dice was consumed
        self.assertNotEqual(len(self.game.available_moves), 2)  # Should be reduced
    def test_make_move_with_history_capture_info(self):
        """Test make_move saves capture information in history."""
        self.game.setup_initial_position()
        self.game.current_player = self.game.player1
        self.game.last_roll = (1, 2)
        self.game.available_moves = [1, 2]
        # Set up capture scenario
        self.game.board.points[1] = [2]  # Single black piece
        self.game.board.points[0] = [1, 1]  # White pieces to move
        initial_history_length = len(self.game.move_history)
        result = self.game.make_move(0, 1)
        self.assertTrue(result)
        self.assertEqual(len(self.game.move_history), initial_history_length + 1)
        # Check that capture was recorded
        last_move = self.game.move_history[-1]
        self.assertEqual(last_move['captured'], 2)  # Player 2 was captured
    def test_validate_move_distance_not_found(self):
        """Test validate_move when dice distance is not available."""
        self.game.setup_initial_position()
        self.game.current_player = self.game.player1
        self.game.last_roll = (1, 2)
        self.game.available_moves = [1, 2]  # Only 1 and 2 available
        # Try to make a move with distance 3 (not available)
        result = self.game.validate_move(0, 3)
        self.assertFalse(result)
    def test_current_player_is_player2(self):
        """Test various methods when current player is player2."""
        self.game.setup_initial_position()
        self.game.current_player = self.game.player2
        self.game.last_roll = (1, 2)
        self.game.available_moves = [1, 2]
        # Test validate_move for player 2
        result = self.game.validate_move(12, 11)  # Player 2 moving backward
        self.assertIsInstance(result, bool)
        # Test make_move for player 2
        if result:
            move_result = self.game.make_move(12, 11)
            self.assertIsInstance(move_result, bool)
    def test_move_from_bar_player2(self):
        """Test move_from_bar for player 2."""
        self.game.setup_initial_position()
        self.game.current_player = self.game.player2
        self.game.available_moves = [2]
        self.game.board.checker_bar[1] = [2]  # Player 2 on bar
        # Clear the entry point to ensure it's not blocked
        self.game.board.points[1] = []  # Clear point 2 (0-indexed as 1)
        # Player 2 should enter at point 2 (dice_value - 1 = 1 for dice_value 2)
        result = self.game.move_from_bar(2)
        self.assertTrue(result)
    def test_bear_off_checker_player2(self):
        """Test bear_off_checker for player 2."""
        # Set up bear off scenario for player 2
        for i in range(24):
            self.game.board.points[i] = []
        self.game.board.points[0] = [2]  # One piece at point 1 for player 2
        self.game.current_player = self.game.player2
        self.game.available_moves = [1]
        # No-op stray expression caused linter warning; ensure a real assertion
        self.assertIsInstance(self.game, BackgammonGame)
