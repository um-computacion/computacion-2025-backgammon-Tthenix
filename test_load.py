#!/usr/bin/env python3
"""
Test script for load game functionality.
"""

from core.backgammon import BackgammonGame
from core.file_persistence import FileGamePersistence
from core.game_persistence import GamePersistenceService


def test_load_functionality():
    """Test the load game functionality."""
    print("=== Testing Load Game Functionality ===")

    # Create a test game and make some moves
    game = BackgammonGame()
    game.setup_initial_position()

    # Roll dice to create some game state
    game.roll_dice()
    print(f"Initial dice roll: {game.__last_roll__}")
    print(f"Current player: {game.__current_player__.__name__}")

    # Create persistence service
    file_persistence = FileGamePersistence()
    persistence_service = GamePersistenceService(file_persistence)

    # Save the game
    print("\nSaving game...")
    save_success = persistence_service.save_game(game)
    print(f"Save result: {save_success}")

    # Create a new game instance (simulating restart)
    new_game = BackgammonGame()
    new_game.setup_initial_position()
    print(f"New game current player: {new_game.__current_player__.__name__}")
    print(f"New game last roll: {new_game.__last_roll__}")

    # Load the saved game
    print("\nLoading game...")
    loaded_game = persistence_service.load_game()

    if loaded_game:
        print("Load successful!")
        print(f"Loaded game current player: {loaded_game.__current_player__.__name__}")
        print(f"Loaded game last roll: {loaded_game.__last_roll__}")
        print(f"Loaded game available moves: {loaded_game.__available_moves__}")

        # Verify the loaded game has the same state
        if (
            loaded_game.__current_player__.__name__ == game.__current_player__.__name__
            and loaded_game.__last_roll__ == game.__last_roll__
        ):
            print("Game state restored correctly!")
        else:
            print("Game state mismatch!")
    else:
        print("Load failed!")

    # Clean up
    persistence_service.delete_game()
    print("\nTest completed!")


if __name__ == "__main__":
    test_load_functionality()
