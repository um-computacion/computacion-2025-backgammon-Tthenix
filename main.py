"""
Main entry point for the Backgammon game.
Provides a simple demo of the game functionality.
"""

from core.backgammon import BackgammonGame
from core.player import Player


def main():
    """Main entry point to demonstrate the backgammon game."""
    print("🎲 Welcome to Backgammon! 🎲")
    print("=" * 40)
    
    # Create a new game with default players
    game = BackgammonGame()
    
    # Set up the initial position
    game.setup_initial_position()
    
    print(f"Game initialized with:")
    print(f"  {game.player1.name} ({game.player1.color})")
    print(f"  {game.player2.name} ({game.player2.color})")
    print(f"Current player: {game.current_player.name}")
    
    # Demo dice rolling
    print("\n🎲 Rolling dice...")
    roll = game.roll_dice()
    print(f"Rolled: {roll[0]} and {roll[1]}")
    print(f"Available moves: {game.get_available_moves()}")
    
    # Show game state
    print(f"\nGame over: {game.is_game_over()}")
    print(f"Winner: {game.get_winner() or 'None yet'}")
    
    # Demo pip count calculation
    pip_count_p1 = game.get_pip_count(game.player1)
    pip_count_p2 = game.get_pip_count(game.player2)
    print(f"\nPip counts:")
    print(f"  {game.player1.name}: {pip_count_p1}")
    print(f"  {game.player2.name}: {pip_count_p2}")
    
    print("\n✅ Demo completed successfully!")


if __name__ == "__main__":
    main()
