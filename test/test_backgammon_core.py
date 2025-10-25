"""Core tests for BackgammonGame functionality.

This module contains tests for the core BackgammonGame class including:
- Initialization and setup
- Basic game mechanics
- Move validation
- Game state management
"""

import unittest
from unittest.mock import patch
from core.backgammon import BackgammonGame
from core.player import Player
from core.board import Board
from core.dice import Dice


class TestBackgammonCore(unittest.TestCase):
    """Test class for core BackgammonGame functionality."""

    def setUp(self):
        """Set up test fixtures before each test method.

        Returns:
            None
        """
        self.__game__ = BackgammonGame()

    # ==================== INITIALIZATION TESTS ====================

    def test_game_initialization_with_default_players(self):
        """Test game initialization with default players.

        Returns:
            None
        """
        game = BackgammonGame()
        self.assertIsInstance(game.__player1__, Player)
        self.assertIsInstance(game.__player2__, Player)
        self.assertIsInstance(game.__board__, Board)
        self.assertIsInstance(game.__dice__, Dice)
        self.assertEqual(game.__player1__.__color__, "white")
        self.assertEqual(game.__player2__.__color__, "black")

    def test_game_initialization_with_custom_players(self):
        """Test game initialization with custom players.

        Returns:
            None
        """
        player1 = Player("Alice", "white")
        player2 = Player("Bob", "black")
        game = BackgammonGame(player1, player2)
        self.assertEqual(game.__player1__, player1)
        self.assertEqual(game.__player2__, player2)
        self.assertEqual(game.__player1__.__name__, "Alice")
        self.assertEqual(game.__player2__.__name__, "Bob")

    def test_game_initialization_sets_current_player(self):
        """Test that game initialization sets a current player.

        Returns:
            None
        """
        game = BackgammonGame()
        self.assertIn(game.__current_player__, [game.__player1__, game.__player2__])

    def test_game_initialization_creates_empty_board(self):
        """Test that game initialization creates an empty board.

        Returns:
            None
        """
        game = BackgammonGame()
        self.assertIsInstance(game.__board__, Board)
        self.assertEqual(len(game.__board__.__points__), 24)

    def test_setup_initial_position(self):
        """Test setting up the initial backgammon position.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.assertEqual(len(self.__game__.__board__.__points__[0]), 2)
        self.assertEqual(len(self.__game__.__board__.__points__[11]), 5)
        self.assertEqual(len(self.__game__.__board__.__points__[16]), 3)
        self.assertEqual(len(self.__game__.__board__.__points__[18]), 5)
        self.assertEqual(len(self.__game__.__board__.__points__[23]), 2)
        self.assertEqual(len(self.__game__.__board__.__points__[12]), 5)
        self.assertEqual(len(self.__game__.__board__.__points__[7]), 3)
        self.assertEqual(len(self.__game__.__board__.__points__[5]), 5)

    # ==================== DICE TESTS ====================

    @patch("core.dice.Dice.roll", return_value=(3, 5))
    def test_roll_dice_returns_valid_values(self, mock_roll):
        """Test dice rolling with controlled values.

        Args:
            mock_roll: Mock for dice roll method

        Returns:
            None
        """
        roll = self.__game__.roll_dice()
        self.assertIsInstance(roll, tuple)
        self.assertEqual(len(roll), 2)
        self.assertEqual(roll, (3, 5))
        self.assertTrue(mock_roll.called)

    @patch("core.dice.Dice.roll", return_value=(2, 4))
    def test_roll_dice_updates_last_roll(self, mock_roll):
        """Test that last_roll is updated with controlled dice values.

        Args:
            mock_roll: Mock for dice roll method

        Returns:
            None
        """
        roll = self.__game__.roll_dice()
        self.assertEqual(self.__game__.__last_roll__, roll)
        self.assertEqual(self.__game__.__last_roll__, (2, 4))
        self.assertTrue(mock_roll.called)

    @patch("core.dice.Dice.__get_moves__", return_value=[1, 2])
    def test_get_available_moves_normal_roll(self, mock_get_moves):
        """Test getting available moves with controlled normal roll.

        Args:
            mock_get_moves: Mock for dice get_moves method

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        moves = self.__game__.get_available_moves()
        self.assertIsInstance(moves, list)
        self.assertTrue(mock_get_moves.called)
        mock_get_moves.assert_called_with((1, 2))

    @patch("core.dice.Dice.__get_moves__", return_value=[3, 3, 3, 3])
    def test_get_available_moves_double_roll(self, mock_get_moves):
        """Test getting available moves with controlled double roll.

        Args:
            mock_get_moves: Mock for dice get_moves method

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (3, 3)
        moves = self.__game__.get_available_moves()
        self.assertIsInstance(moves, list)
        self.assertTrue(mock_get_moves.called)
        mock_get_moves.assert_called_with((3, 3))

    def test_get_available_moves_no_roll(self):
        """Test getting available moves when no dice have been rolled.

        Returns:
            None
        """
        moves = self.__game__.get_available_moves()
        self.assertEqual(moves, [])

    # ==================== MOVE VALIDATION TESTS ====================

    def test_validate_move_valid_move(self):
        """Test validating a valid move.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        is_valid = self.__game__.validate_move(0, 1)
        self.assertIsInstance(is_valid, bool)

    def test_validate_move_no_piece_at_origin(self):
        """Test validating a move when no piece is at origin.

        Returns:
            None
        """
        self.__game__.__last_roll__ = (1, 2)
        is_valid = self.__game__.validate_move(10, 11)
        self.assertFalse(is_valid)

    def test_validate_move_invalid_distance(self):
        """Test validating a move with invalid distance.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        is_valid = self.__game__.validate_move(0, 5)
        self.assertFalse(is_valid)

    def test_validate_move_blocked_destination(self):
        """Test validating a move to a blocked destination.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        is_valid = self.__game__.validate_move(23, 22)
        self.assertFalse(is_valid)

    def test_validate_move_out_of_bounds(self):
        """Test validate_move with out of bounds positions.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]

        result = self.__game__.validate_move(-1, 1)
        self.assertFalse(result)

        result = self.__game__.validate_move(0, 25)
        self.assertFalse(result)

    def test_validate_move_no_last_roll(self):
        """Test validate_move when no dice have been rolled.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = None

        result = self.__game__.validate_move(0, 1)
        self.assertFalse(result)

    def test_validate_move_no_available_moves(self):
        """Test validate_move when no moves are available.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        # Don't set __last_roll__ to prevent regeneration of available moves
        self.__game__.__available_moves__ = []

        result = self.__game__.validate_move(0, 1)
        self.assertFalse(result)

    def test_validate_move_wrong_player(self):
        """Test validate_move for wrong player.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__current_player__ = self.__game__.__player2__
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]

        # Try to move player 1's checker when it's player 2's turn
        result = self.__game__.validate_move(0, 1)
        self.assertFalse(result)

    def test_validate_move_distance_not_available(self):
        """Test validate_move with distance not in available moves.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]

        # Try to move distance 3 when only 1,2 are available
        result = self.__game__.validate_move(0, 3)
        self.assertFalse(result)

    def test_validate_move_blocked_destination_advanced(self):
        """Test validate_move to blocked destination with advanced scenario.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]

        # Mock board to have blocked destination (2+ opponent pieces)
        with patch.object(self.__game__.__board__, "can_move", return_value=False):
            result = self.__game__.validate_move(0, 1)
            self.assertFalse(result)

    # ==================== MOVE EXECUTION TESTS ====================

    def test_make_move_valid_move(self):
        """Test making a valid move.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        result = self.__game__.make_move(0, 1)
        self.assertTrue(result)

    def test_make_move_invalid_move(self):
        """Test making an invalid move.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        result = self.__game__.make_move(10, 15)
        self.assertFalse(result)

    def test_make_move_updates_board(self):
        """Test that make_move updates the board state.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        initial_count = len(self.__game__.__board__.__points__[0])
        self.__game__.make_move(0, 1)
        self.assertEqual(len(self.__game__.__board__.__points__[0]), initial_count - 1)
        self.assertGreater(len(self.__game__.__board__.__points__[1]), 0)

    def test_make_move_consumes_dice_value(self):
        """Test that make_move consumes the used dice value.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]
        self.__game__.make_move(0, 1)
        self.assertNotIn(1, self.__game__.__available_moves__)

    # ==================== GAME STATE TESTS ====================

    def test_switch_current_player(self):
        """Test switching the current player.

        Returns:
            None
        """
        initial_player = self.__game__.__current_player__
        self.__game__.switch_current_player()
        self.assertNotEqual(self.__game__.__current_player__, initial_player)

    def test_switch_player_alternates(self):
        """Test that switching players alternates correctly.

        Returns:
            None
        """
        player1 = self.__game__.__current_player__
        self.__game__.switch_current_player()
        player2 = self.__game__.__current_player__
        self.__game__.switch_current_player()
        player3 = self.__game__.__current_player__
        self.assertEqual(player1, player3)
        self.assertNotEqual(player1, player2)

    def test_is_game_over_false_at_start(self):
        """Test that game is not over at the start.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.assertFalse(self.__game__.is_game_over())

    def test_is_game_over_true_when_player_wins(self):
        """Test that game is over when a player wins.

        Returns:
            None
        """
        self.__game__.__board__.__off_board__[0] = [1] * 15
        self.assertTrue(self.__game__.is_game_over())

    def test_get_winner_player1_wins(self):
        """Test getting the winner when player 1 wins.

        Returns:
            None
        """
        self.__game__.__board__.__off_board__[0] = [1] * 15
        winner = self.__game__.get_winner()
        self.assertEqual(winner, self.__game__.__player1__)

    def test_get_winner_player2_wins(self):
        """Test getting the winner when player 2 wins.

        Returns:
            None
        """
        self.__game__.__board__.__off_board__[1] = [2] * 15
        winner = self.__game__.get_winner()
        self.assertEqual(winner, self.__game__.__player2__)

    def test_get_winner_no_winner(self):
        """Test getting the winner when no one has won yet.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        winner = self.__game__.get_winner()
        self.assertIsNone(winner)

    def test_get_game_state(self):
        """Test getting the current game state.

        Returns:
            None
        """
        state = self.__game__.get_game_state()
        self.assertIn("board", state)
        self.assertIn("current_player", state)
        self.assertIn("last_roll", state)
        self.assertIn("available_moves", state)
        self.assertIn("game_over", state)

    def test_get_player_by_color_white(self):
        """Test getting player by white color.

        Returns:
            None
        """
        player = self.__game__.get_player_by_color("white")
        self.assertEqual(player.__color__, "white")

    def test_get_player_by_color_black(self):
        """Test getting player by black color.

        Returns:
            None
        """
        player = self.__game__.get_player_by_color("black")
        self.assertEqual(player.__color__, "black")

    def test_get_player_by_color_invalid(self):
        """Test getting player by invalid color.

        Returns:
            None
        """
        player = self.__game__.get_player_by_color("red")
        self.assertIsNone(player)

    def test_reset_game(self):
        """Test resetting the game state.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (3, 4)
        self.__game__.reset_game()
        self.assertIsNone(self.__game__.__last_roll__)
        self.assertEqual(self.__game__.__available_moves__, [])

    def test_copy_game_state(self):
        """Test copying the game state.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        copy = self.__game__.copy_game_state()
        self.assertIsInstance(copy, dict)
        self.assertIn("board", copy)
        self.assertIn("players", copy)

    # ==================== HELPER METHOD TESTS ====================

    def test_has_valid_moves_no_roll(self):
        """Test has_valid_moves when no dice have been rolled.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = None

        result = self.__game__.has_valid_moves()
        self.assertFalse(result)

    def test_has_valid_moves_no_available_moves(self):
        """Test has_valid_moves when no moves are available.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        # Don't set __last_roll__ to prevent regeneration of available moves
        self.__game__.__available_moves__ = []

        result = self.__game__.has_valid_moves()
        self.assertFalse(result)

    def test_has_valid_moves_with_moves(self):
        """Test has_valid_moves when moves are available.

        Returns:
            None
        """
        self.__game__.setup_initial_position()
        self.__game__.__last_roll__ = (1, 2)
        self.__game__.__available_moves__ = [1, 2]

        result = self.__game__.has_valid_moves()
        self.assertTrue(result)

    def test_is_blocked_position_out_of_bounds(self):
        """Test is_blocked_position with out of bounds positions.

        Returns:
            None
        """
        self.__game__.setup_initial_position()

        result = self.__game__.is_blocked_position(-1, 1)
        self.assertFalse(result)

        result = self.__game__.is_blocked_position(24, 1)
        self.assertFalse(result)

    def test_can_hit_opponent_out_of_bounds(self):
        """Test can_hit_opponent with out of bounds positions.

        Returns:
            None
        """
        self.__game__.setup_initial_position()

        result = self.__game__.can_hit_opponent(-1, 1)
        self.assertFalse(result)

        result = self.__game__.can_hit_opponent(24, 1)
        self.assertFalse(result)

    def test_get_available_moves_no_last_roll(self):
        """Test get_available_moves when no dice have been rolled.

        Returns:
            None
        """
        self.__game__.__last_roll__ = None
        moves = self.__game__.get_available_moves()
        self.assertEqual(moves, [])


if __name__ == "__main__":
    unittest.main()
