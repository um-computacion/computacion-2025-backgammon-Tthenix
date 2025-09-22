#!/usr/bin/env python3
"""Main entry point for the Backgammon game.

This module provides a simple command-line interface to demonstrate
the Backgammon game functionality.
"""

from core.backgammon import BackgammonGame
from core.player import Player


def main():
    """Run a simple demonstration of the Backgammon game."""
    print("Welcome to Backgammon!")
    print("=" * 40)
    # Create players
    player1 = Player("Player 1", "white")
    player2 = Player("Player 2", "black")
    # Create and initialize game
    game = BackgammonGame(player1, player2)
    game.setup_initial_position()
    print(f"Game initialized with {player1.name} (white) and {player2.name} (black)")
    print(f"Current player: {game.current_player.name}")
    roll = game.roll_dice()
    print(f"Dice roll: {roll}")
    print(f"Available moves: {game.get_available_moves()}")
    # Show game state
    print(f"Game over: {game.is_game_over()}")
    print("Game demonstration completed!")


if __name__ == "__main__":
    main()
