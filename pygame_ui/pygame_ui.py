"""
Backgammon Pygame UI Module

This module provides the main entry point for the pygame UI.
It coordinates the game loop and event handling.
"""

import pygame  # pylint: disable=import-error
from core.backgammon import BackgammonGame
from pygame_ui.backgammon_board import BackgammonBoard


def main() -> None:
    """Main function to run the backgammon board display."""
    board = BackgammonBoard()
    clock = pygame.time.Clock()
    running = True

    # Create game instance
    game = BackgammonGame()
    game.setup_initial_position()

    # Set the game instance in the board
    board.set_game(game)

    # Update board from game state
    board.update_from_game()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                running = False
            elif event.type == pygame.KEYDOWN:  # pylint: disable=no-member
                if event.key == pygame.K_ESCAPE:  # pylint: disable=no-member
                    running = False
                elif event.key == pygame.K_SPACE:  # pylint: disable=no-member
                    # Presiona espacio para tirar dados (si corresponde)
                    if game.last_roll is None or not game.available_moves:
                        game.roll_dice()
                        board.update_from_game()
                elif event.key == pygame.K_r:  # pylint: disable=no-member
                    # Press 'r' to reset game
                    game.reset_game()
                    game.setup_initial_position()
                    board.update_from_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
                # Handle mouse clicks on board
                mouse_x, mouse_y = event.pos
                board.handle_board_click(mouse_x, mouse_y)

            # Handle button clicks
            if board.roll_button.handle_event(event):
                # Tirar dados desde botón (si corresponde)
                if game.last_roll is None or not game.available_moves:
                    game.roll_dice()
                    board.update_from_game()

        # Clear screen with a neutral background
        board.screen.fill((50, 50, 50))  # Dark gray background

        # Draw the board
        board.draw_board()

        # Update display
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()  # pylint: disable=no-member


if __name__ == "__main__":
    main()
