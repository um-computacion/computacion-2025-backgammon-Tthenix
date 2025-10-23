"""
Backgammon Pygame UI Module

This module provides the main entry point for the pygame UI.
It coordinates the game loop and event handling.
"""

import pygame  # pylint: disable=import-error
from core.backgammon import BackgammonGame
from pygame_ui.backgammon_board import BackgammonBoard


def _handle_event(event, game, board) -> bool:
    """
    Handle a pygame event.

    Args:
        event: Pygame event
        game: BackgammonGame instance
        board: BackgammonBoard instance

    Returns:
        True to continue running, False to quit
    """
    if event.type == pygame.QUIT:  # pylint: disable=no-member
        return False

    # Si el juego ha terminado, solo permitir cerrar
    if game.is_game_over():
        if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
            if event.key == pygame.K_ESCAPE:  # pylint: disable=no-member
                return False
            if event.key == pygame.K_r:  # pylint: disable=no-member
                _handle_reset_game(game, board)
        return True

    if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
        return _handle_keydown(event, game, board)
    if event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
        _handle_mouse_click(event, board)
    if board.roll_button.handle_event(event):
        _handle_roll_button_click(game, board)
    return True


def _handle_keydown(event, game, board) -> bool:
    """Handle keydown events."""
    if event.key == pygame.K_ESCAPE:  # pylint: disable=no-member
        return False
    if event.key == pygame.K_SPACE:  # pylint: disable=no-member
        _handle_roll_dice(game, board)
    if event.key == pygame.K_r:  # pylint: disable=no-member
        _handle_reset_game(game, board)
    return True


def _handle_roll_dice(game, board) -> None:
    """Handle rolling dice."""
    if game.last_roll is None or not game.available_moves:
        game.roll_dice()
        if not game.has_valid_moves():
            game.switch_current_player()
        board.update_from_game()


def _handle_reset_game(game, board) -> None:
    """Handle game reset."""
    game.reset_game()
    game.setup_initial_position()
    board.update_from_game()


def _handle_mouse_click(event, board) -> None:
    """Handle mouse click events."""
    mouse_x, mouse_y = event.pos
    board.handle_board_click(mouse_x, mouse_y)


def _handle_roll_button_click(game, board) -> None:
    """Handle roll button click."""
    if game.last_roll is None or not game.available_moves:
        game.roll_dice()
        if not game.has_valid_moves():
            game.switch_current_player()
        board.update_from_game()


def _draw_win_message(screen, game) -> None:
    """
    Dibujar mensaje de victoria cuando el juego termine.

    Args:
        screen: Superficie de pygame
        game: Instancia de BackgammonGame
    """
    if not game.is_game_over():
        return

    winner = game.get_winner()
    if winner is None:
        return

    # Crear superficie semi-transparente para el fondo
    overlay = pygame.Surface((screen.get_width(), screen.get_height()))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Configurar fuente
    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 36)

    # Texto de victoria
    win_text = f"¡{winner.name} GANA!"
    win_surface = font_large.render(win_text, True, (255, 215, 0))  # Dorado
    win_rect = win_surface.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2 - 50)
    )
    screen.blit(win_surface, win_rect)

    # Texto de instrucciones
    instruction_text = "Presiona R para reiniciar o ESC para salir"
    instruction_surface = font_medium.render(instruction_text, True, (255, 255, 255))
    instruction_rect = instruction_surface.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2 + 20)
    )
    screen.blit(instruction_surface, instruction_rect)


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
            if not _handle_event(event, game, board):
                running = False

        # Clear screen with a neutral background
        board.screen.fill((50, 50, 50))  # Dark gray background

        # Draw the board
        board.draw_board()

        # Dibujar mensaje de victoria si el juego ha terminado
        _draw_win_message(board.screen, game)

        # Update display
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()  # pylint: disable=no-member


if __name__ == "__main__":
    main()
