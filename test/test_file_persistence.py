"""
Test module for file persistence functionality.
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch

from core.file_persistence import FileGamePersistence


class TestFileGamePersistence(unittest.TestCase):
    """Test cases for FileGamePersistence class."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.persistence = FileGamePersistence(self.temp_dir)

    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up any test files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_init_creates_directory(self):
        """Test that initialization creates the save directory."""
        new_dir = os.path.join(self.temp_dir, "new_save_dir")
        FileGamePersistence(new_dir)  # pylint: disable=unused-variable
        self.assertTrue(os.path.exists(new_dir))
        os.rmdir(new_dir)

    def test_save_game_success(self):
        """Test successful game save."""
        game_state = {"board": {"points": []}, "current_player": "Player 1"}
        result = self.persistence.save_game("test_game", game_state)
        self.assertTrue(result)

        # Verify file was created
        file_path = os.path.join(self.temp_dir, "test_game.json")
        self.assertTrue(os.path.exists(file_path))

        # Verify file content
        with open(file_path, "r", encoding="utf-8") as f:
            saved_data = json.load(f)
        self.assertEqual(saved_data, game_state)

    def test_save_game_file_error(self):
        """Test save game with file system error."""
        with patch("builtins.open", side_effect=OSError("Permission denied")):
            game_state = {"board": {"points": []}}
            result = self.persistence.save_game("test_game", game_state)
            self.assertFalse(result)

    def test_save_game_json_error(self):
        """Test save game with JSON serialization error."""

        # Create an object that can't be JSON serialized
        class UnserializableObject:  # pylint: disable=too-few-public-methods
            """Test class for JSON serialization testing."""

            def __str__(self):
                return "unserializable"

        game_state = {"invalid": UnserializableObject()}
        result = self.persistence.save_game("test_game", game_state)
        # The file persistence uses default=str, so it should succeed
        self.assertTrue(result)

    def test_load_game_success(self):
        """Test successful game load."""
        game_state = {"board": {"points": []}, "current_player": "Player 1"}

        # Save a game first
        self.persistence.save_game("test_game", game_state)

        # Load it back
        loaded_state = self.persistence.load_game("test_game")
        self.assertEqual(loaded_state, game_state)

    def test_load_game_not_found(self):
        """Test loading non-existent game."""
        result = self.persistence.load_game("nonexistent_game")
        self.assertIsNone(result)

    def test_load_game_file_error(self):
        """Test load game with file system error."""
        with patch("builtins.open", side_effect=OSError("Permission denied")):
            result = self.persistence.load_game("test_game")
            self.assertIsNone(result)

    def test_load_game_json_error(self):
        """Test load game with JSON parsing error."""
        # Create a file with invalid JSON
        file_path = os.path.join(self.temp_dir, "invalid_game.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("invalid json content")

        result = self.persistence.load_game("invalid_game")
        self.assertIsNone(result)

    def test_delete_game_success(self):
        """Test successful game deletion."""
        game_state = {"board": {"points": []}}

        # Save a game first
        self.persistence.save_game("test_game", game_state)

        # Delete it
        result = self.persistence.delete_game("test_game")
        self.assertTrue(result)

        # Verify file was deleted
        file_path = os.path.join(self.temp_dir, "test_game.json")
        self.assertFalse(os.path.exists(file_path))

    def test_delete_game_not_found(self):
        """Test deleting non-existent game."""
        result = self.persistence.delete_game("nonexistent_game")
        self.assertFalse(result)

    def test_delete_game_error(self):
        """Test delete game with file system error."""
        with patch("os.remove", side_effect=OSError("Permission denied")):
            result = self.persistence.delete_game("test_game")
            self.assertFalse(result)

    def test_multiple_games(self):
        """Test saving and loading multiple games."""
        game1 = {"board": {"points": []}, "player": "Player 1"}
        game2 = {"board": {"points": []}, "player": "Player 2"}

        # Save both games
        self.assertTrue(self.persistence.save_game("game1", game1))
        self.assertTrue(self.persistence.save_game("game2", game2))

        # Load both games
        loaded1 = self.persistence.load_game("game1")
        loaded2 = self.persistence.load_game("game2")

        self.assertEqual(loaded1, game1)
        self.assertEqual(loaded2, game2)

        # Delete one game
        self.assertTrue(self.persistence.delete_game("game1"))
        self.assertIsNone(self.persistence.load_game("game1"))
        self.assertEqual(self.persistence.load_game("game2"), game2)


if __name__ == "__main__":
    unittest.main()
