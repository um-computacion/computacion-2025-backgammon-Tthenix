"""
File-based Game Persistence Module

This module provides a simple file-based persistence implementation
as a fallback when Redis is not available.
"""

import json
import os
from typing import Dict, Any, Optional

from .game_persistence import GamePersistenceInterface


class FileGamePersistence(GamePersistenceInterface):
    """File-based implementation of game persistence."""

    def __init__(self, save_dir: str = "saved_games") -> None:
        """
        Initialize file-based persistence.

        Args:
            save_dir: Directory to save game files

        Returns:
            None
        """
        self.__save_dir__ = save_dir
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

    def save_game(self, game_id: str, game_state: Dict[str, Any]) -> bool:
        """
        Save a game state to a file.

        Args:
            game_id: Unique identifier for the game
            game_state: Dictionary containing the game state

        Returns:
            True if save was successful, False otherwise
        """
        try:
            file_path = os.path.join(self.__save_dir__, f"{game_id}.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(game_state, f, indent=2, default=str)
            return True
        except (OSError, IOError, TypeError):
            return False

    def load_game(self, game_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a game state from a file.

        Args:
            game_id: Unique identifier for the game

        Returns:
            Dictionary containing the game state, or None if not found
        """
        try:
            file_path = os.path.join(self.__save_dir__, f"{game_id}.json")
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            return None
        except (OSError, IOError, ValueError):
            return None

    def delete_game(self, game_id: str) -> bool:
        """
        Delete a saved game file.

        Args:
            game_id: Unique identifier for the game

        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            file_path = os.path.join(self.__save_dir__, f"{game_id}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except OSError:
            return False
