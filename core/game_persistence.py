"""
Game Persistence Module

This module provides game persistence functionality using Redis.
It follows SOLID principles with clear separation of concerns.
"""

import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

import redis  # pylint: disable=import-error

from .backgammon import BackgammonGame


class GamePersistenceInterface(ABC):
    """Abstract interface for game persistence operations."""

    @abstractmethod
    def save_game(self, game_id: str, game_state: Dict[str, Any]) -> bool:
        """
        Save a game state.

        Args:
            game_id: Unique identifier for the game
            game_state: Dictionary containing the game state

        Returns:
            True if save was successful, False otherwise
        """

    @abstractmethod
    def load_game(self, game_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a game state.

        Args:
            game_id: Unique identifier for the game

        Returns:
            Dictionary containing the game state, or None if not found
        """

    @abstractmethod
    def delete_game(self, game_id: str) -> bool:
        """
        Delete a saved game.

        Args:
            game_id: Unique identifier for the game

        Returns:
            True if deletion was successful, False otherwise
        """


class RedisGamePersistence(GamePersistenceInterface):
    """Redis implementation of game persistence."""

    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0) -> None:
        """
        Initialize Redis connection.

        Args:
            host: Redis server host
            port: Redis server port
            db: Redis database number

        Returns:
            None
        """
        self.__redis_client__ = redis.Redis(
            host=host, port=port, db=db, decode_responses=True
        )
        self.__key_prefix__ = "backgammon_game:"

    def save_game(self, game_id: str, game_state: Dict[str, Any]) -> bool:
        """
        Save a game state to Redis.

        Args:
            game_id: Unique identifier for the game
            game_state: Dictionary containing the game state

        Returns:
            True if save was successful, False otherwise
        """
        try:
            key = f"{self.__key_prefix__}{game_id}"
            serialized_state = json.dumps(game_state, default=str)
            self.__redis_client__.set(key, serialized_state)
            return True
        except redis.RedisError:
            return False

    def load_game(self, game_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a game state from Redis.

        Args:
            game_id: Unique identifier for the game

        Returns:
            Dictionary containing the game state, or None if not found
        """
        try:
            key = f"{self.__key_prefix__}{game_id}"
            serialized_state = self.__redis_client__.get(key)
            if serialized_state:
                return json.loads(serialized_state)
            return None
        except redis.RedisError:
            return None

    def delete_game(self, game_id: str) -> bool:
        """
        Delete a saved game from Redis.

        Args:
            game_id: Unique identifier for the game

        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            key = f"{self.__key_prefix__}{game_id}"
            result = self.__redis_client__.delete(key)
            return result > 0
        except redis.RedisError:
            return False

    def test_connection(self) -> bool:
        """
        Test if Redis connection is working.

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            self.__redis_client__.ping()
            return True
        except redis.RedisError:
            return False


class GamePersistenceService:
    """Service class that coordinates game persistence operations."""

    def __init__(self, persistence: GamePersistenceInterface) -> None:
        """
        Initialize the persistence service.

        Args:
            persistence: Implementation of GamePersistenceInterface

        Returns:
            None
        """
        self.__persistence__ = persistence

    def save_game(self, game: BackgammonGame, game_id: str = "current") -> bool:
        """
        Save a game to persistence.

        Args:
            game: BackgammonGame instance to save
            game_id: Unique identifier for the game

        Returns:
            True if save was successful, False otherwise
        """
        game_state = game.get_serializable_state()
        return self.__persistence__.save_game(game_id, game_state)

    def load_game(self, game_id: str = "current") -> Optional[BackgammonGame]:
        """
        Load a game from persistence.

        Args:
            game_id: Unique identifier for the game

        Returns:
            BackgammonGame instance, or None if not found
        """
        game_state = self.__persistence__.load_game(game_id)
        if game_state:
            # Create a new game instance and restore state
            from .player import Player

            player1 = Player(
                game_state["player1"]["name"], game_state["player1"]["color"]
            )
            player2 = Player(
                game_state["player2"]["name"], game_state["player2"]["color"]
            )
            game = BackgammonGame(player1, player2)
            game.restore_from_state(game_state)
            return game
        return None

    def delete_game(self, game_id: str = "current") -> bool:
        """
        Delete a saved game.

        Args:
            game_id: Unique identifier for the game

        Returns:
            True if deletion was successful, False otherwise
        """
        return self.__persistence__.delete_game(game_id)
