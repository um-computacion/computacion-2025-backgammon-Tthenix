"""
Test module for game persistence functionality.
"""

import unittest
from unittest.mock import Mock, patch
import redis

from core.game_persistence import (
    GamePersistenceInterface,
    RedisGamePersistence,
    GamePersistenceService,
)
from core.backgammon import BackgammonGame


class MockPersistence(GamePersistenceInterface):
    """Mock implementation of GamePersistenceInterface for testing."""

    def __init__(self):
        self.saved_games = {}
        self.should_fail_save = False
        self.should_fail_load = False
        self.should_fail_delete = False

    def save_game(self, game_id, game_state):
        """Mock save game implementation."""
        if self.should_fail_save:
            return False
        self.saved_games[game_id] = game_state
        return True

    def load_game(self, game_id):
        """Mock load game implementation."""
        if self.should_fail_load:
            return None
        return self.saved_games.get(game_id)

    def delete_game(self, game_id):
        """Mock delete game implementation."""
        if self.should_fail_delete:
            return False
        if game_id in self.saved_games:
            del self.saved_games[game_id]
            return True
        return False


class TestGamePersistenceInterface(unittest.TestCase):
    """Test cases for GamePersistenceInterface."""

    def test_interface_is_abstract(self):
        """Test that GamePersistenceInterface is abstract."""
        with self.assertRaises(TypeError):
            GamePersistenceInterface()  # pylint: disable=abstract-class-instantiated


class TestRedisGamePersistence(unittest.TestCase):
    """Test cases for RedisGamePersistence class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_redis = Mock()
        self.mock_redis.ping.return_value = True
        self.mock_redis.set.return_value = True
        self.mock_redis.get.return_value = '{"test": "data"}'
        self.mock_redis.delete.return_value = 1

    @patch("core.game_persistence.redis.Redis")
    def test_init_default_params(self, mock_redis_class):
        """Test initialization with default parameters."""
        mock_redis_class.return_value = self.mock_redis
        persistence = RedisGamePersistence()

        mock_redis_class.assert_called_once_with(
            host="localhost", port=6379, db=0, decode_responses=True
        )
        self.assertEqual(persistence.__key_prefix__, "backgammon_game:")

    @patch("core.game_persistence.redis.Redis")
    def test_init_custom_params(self, mock_redis_class):
        """Test initialization with custom parameters."""
        mock_redis_class.return_value = self.mock_redis
        RedisGamePersistence(host="test", port=1234, db=5)  # pylint: disable=unused-variable

        mock_redis_class.assert_called_once_with(
            host="test", port=1234, db=5, decode_responses=True
        )

    @patch("core.game_persistence.redis.Redis")
    def test_redis_save_game_success(self, mock_redis_class):
        """Test successful game save."""
        mock_redis_class.return_value = self.mock_redis
        persistence = RedisGamePersistence()

        game_state = {"board": {"points": []}}
        result = persistence.save_game("test_game", game_state)

        self.assertTrue(result)
        self.mock_redis.set.assert_called_once()

    @patch("core.game_persistence.redis.Redis")
    def test_save_game_redis_error(self, mock_redis_class):
        """Test save game with Redis error."""
        mock_redis_class.return_value = self.mock_redis
        self.mock_redis.set.side_effect = redis.RedisError("Redis error")

        persistence = RedisGamePersistence()
        game_state = {"board": {"points": []}}

        # The method should catch the exception and return False
        result = persistence.save_game("test_game", game_state)

        self.assertFalse(result)

    @patch("core.game_persistence.redis.Redis")
    def test_redis_load_game_success(self, mock_redis_class):
        """Test successful game load."""
        mock_redis_class.return_value = self.mock_redis
        persistence = RedisGamePersistence()

        result = persistence.load_game("test_game")

        self.assertEqual(result, {"test": "data"})
        self.mock_redis.get.assert_called_once()

    @patch("core.game_persistence.redis.Redis")
    def test_load_game_not_found(self, mock_redis_class):
        """Test loading non-existent game."""
        mock_redis_class.return_value = self.mock_redis
        self.mock_redis.get.return_value = None

        persistence = RedisGamePersistence()
        result = persistence.load_game("nonexistent_game")

        self.assertIsNone(result)

    @patch("core.game_persistence.redis.Redis")
    def test_load_game_redis_error(self, mock_redis_class):
        """Test load game with Redis error."""
        mock_redis_class.return_value = self.mock_redis
        self.mock_redis.get.side_effect = redis.RedisError("Redis error")

        persistence = RedisGamePersistence()

        # The method should catch the exception and return None
        result = persistence.load_game("test_game")

        self.assertIsNone(result)

    @patch("core.game_persistence.redis.Redis")
    def test_redis_delete_game_success(self, mock_redis_class):
        """Test successful game deletion."""
        mock_redis_class.return_value = self.mock_redis
        persistence = RedisGamePersistence()

        result = persistence.delete_game("test_game")

        self.assertTrue(result)
        self.mock_redis.delete.assert_called_once()

    @patch("core.game_persistence.redis.Redis")
    def test_delete_game_redis_error(self, mock_redis_class):
        """Test delete game with Redis error."""
        mock_redis_class.return_value = self.mock_redis
        self.mock_redis.delete.side_effect = redis.RedisError("Redis error")

        persistence = RedisGamePersistence()

        # The method should catch the exception and return False
        result = persistence.delete_game("test_game")

        self.assertFalse(result)

    @patch("core.game_persistence.redis.Redis")
    def test_test_connection_success(self, mock_redis_class):
        """Test successful connection test."""
        mock_redis_class.return_value = self.mock_redis
        persistence = RedisGamePersistence()

        result = persistence.test_connection()

        self.assertTrue(result)
        self.mock_redis.ping.assert_called_once()

    @patch("core.game_persistence.redis.Redis")
    def test_test_connection_failure(self, mock_redis_class):
        """Test connection test failure."""
        mock_redis_class.return_value = self.mock_redis
        self.mock_redis.ping.side_effect = redis.RedisError("Connection failed")

        persistence = RedisGamePersistence()

        # The method should catch the exception and return False
        result = persistence.test_connection()

        self.assertFalse(result)


class TestGamePersistenceService(unittest.TestCase):
    """Test cases for GamePersistenceService class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_persistence = MockPersistence()
        self.service = GamePersistenceService(self.mock_persistence)
        self.game = BackgammonGame()
        self.game.setup_initial_position()

    def test_init(self):
        """Test service initialization."""
        self.assertEqual(self.service.__persistence__, self.mock_persistence)

    def test_service_save_game_success(self):
        """Test successful game save."""
        result = self.service.save_game(self.game, "test_game")

        self.assertTrue(result)
        self.assertTrue("test_game" in self.mock_persistence.saved_games)

    def test_save_game_persistence_failure(self):
        """Test save game with persistence failure."""
        self.mock_persistence.should_fail_save = True
        result = self.service.save_game(self.game, "test_game")

        self.assertFalse(result)

    def test_service_load_game_success(self):
        """Test successful game load."""
        # Save a game first
        self.service.save_game(self.game, "test_game")

        # Load it back
        loaded_game = self.service.load_game("test_game")

        self.assertIsInstance(loaded_game, BackgammonGame)
        self.assertEqual(loaded_game.__player1__.__name__, "Player 1")
        self.assertEqual(loaded_game.__player2__.__name__, "Player 2")

    def test_load_game_not_found(self):
        """Test loading non-existent game."""
        loaded_game = self.service.load_game("nonexistent_game")
        self.assertIsNone(loaded_game)

    def test_load_game_persistence_failure(self):
        """Test load game with persistence failure."""
        self.mock_persistence.should_fail_load = True
        loaded_game = self.service.load_game("test_game")

        self.assertIsNone(loaded_game)

    def test_service_delete_game_success(self):
        """Test successful game deletion."""
        # Save a game first
        self.service.save_game(self.game, "test_game")

        # Delete it
        result = self.service.delete_game("test_game")

        self.assertTrue(result)
        self.assertFalse("test_game" in self.mock_persistence.saved_games)

    def test_delete_game_not_found(self):
        """Test deleting non-existent game."""
        result = self.service.delete_game("nonexistent_game")
        self.assertFalse(result)

    def test_delete_game_persistence_failure(self):
        """Test delete game with persistence failure."""
        self.mock_persistence.should_fail_delete = True
        result = self.service.delete_game("test_game")

        self.assertFalse(result)

    def test_default_game_id(self):
        """Test using default game ID."""
        result = self.service.save_game(self.game)
        self.assertTrue(result)
        self.assertTrue("current" in self.mock_persistence.saved_games)

    def test_game_state_serialization(self):
        """Test that game state is properly serialized."""
        # Roll dice to create some state
        self.game.roll_dice()

        result = self.service.save_game(self.game, "test_game")
        self.assertTrue(result)

        saved_state = self.mock_persistence.saved_games["test_game"]
        self.assertIn("board", saved_state)
        self.assertIn("current_player", saved_state)
        self.assertIn("last_roll", saved_state)
        self.assertIn("available_moves", saved_state)


if __name__ == "__main__":
    unittest.main()
