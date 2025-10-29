"""
Backgammon Pygame UI Module

This module provides the main entry point for the pygame UI.
It coordinates the game loop and event handling.
"""

import pygame  # pylint: disable=import-error
from core.backgammon import BackgammonGame
from core.game_persistence import RedisGamePersistence, GamePersistenceService
from core.file_persistence import FileGamePersistence
from pygame_ui.backgammon_board import BackgammonBoard


def _handle_event(event, game, board, persistence_service) -> bool:
    """
    Handle a pygame event.

    Args:
        event: Pygame event
        game: BackgammonGame instance
        board: BackgammonBoard instance
        persistence_service: GamePersistenceService instance

    Returns:
        True to continue running, False to quit
    """
    if event.type == pygame.QUIT:  # pylint: disable=no-member
        return False

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
    if board.__roll_button__.handle_event(event):
        _handle_roll_button_click(game, board)
    if board.handle_save_button_click(event):
        _handle_save_button_click(game, board, persistence_service)
    if board.handle_load_button_click(event):
        _handle_load_button_click(game, board, persistence_service)
    return True


def _handle_keydown(event, game, board) -> bool:
    """Handle keydown events.

    Args:
        event: Pygame event
        game: BackgammonGame instance
        board: BackgammonBoard instance

    Returns:
        True to continue running, False to quit
    """
    if event.key == pygame.K_ESCAPE:  # pylint: disable=no-member
        return False
    if event.key == pygame.K_SPACE:  # pylint: disable=no-member
        _handle_roll_dice(game, board)
    if event.key == pygame.K_r:  # pylint: disable=no-member
        _handle_reset_game(game, board)
    return True


def _handle_roll_dice(game, board) -> None:
    """Handle rolling dice.

    Args:
        game: BackgammonGame instance
        board: BackgammonBoard instance

    Returns:
        None
    """
    if game.__last_roll__ is None or not game.__available_moves__:
        game.roll_dice()
        if not game.has_valid_moves():
            # Clear dice state and switch player when no valid moves
            game.__last_roll__ = None
            game.__available_moves__ = []
            game.switch_current_player()
        board.update_from_game()


def _handle_reset_game(game, board) -> None:
    """Handle game reset.

    Args:
        game: BackgammonGame instance
        board: BackgammonBoard instance

    Returns:
        None
    """
    game.reset_game()
    game.setup_initial_position()
    board.update_from_game()


def _handle_mouse_click(event, board) -> None:
    """Handle mouse click events.

    Args:
        event: Pygame event
        board: BackgammonBoard instance

    Returns:
        None
    """
    mouse_x, mouse_y = event.pos
    board.handle_board_click(mouse_x, mouse_y)


def _handle_roll_button_click(game, board) -> None:
    """Handle roll button click.

    Args:
        game: BackgammonGame instance
        board: BackgammonBoard instance

    Returns:
        None
    """
    if game.__last_roll__ is None or not game.__available_moves__:
        game.roll_dice()
        if not game.has_valid_moves():
            # Clear dice state and switch player when no valid moves
            game.__last_roll__ = None
            game.__available_moves__ = []
            game.switch_current_player()
        board.update_from_game()


def _handle_save_button_click(game, board, persistence_service) -> None:
    """Handle save button click.

    Args:
        game: BackgammonGame instance
        board: BackgammonBoard instance
        persistence_service: GamePersistenceService instance

    Returns:
        None
    """
    # Check if dice have been rolled but no moves made yet
    if game.__last_roll__ is not None and game.__available_moves__:
        board.show_save_message("No puedes guardar después de tirar dados")
        return

    try:
        success = persistence_service.save_game(game)
        if success:
            board.show_save_message("¡Juego guardado exitosamente!")
        else:
            board.show_save_message("Error al guardar el juego")
    except (OSError, IOError, ValueError) as e:
        board.show_save_message(f"Error al guardar: {str(e)[:30]}")


def _handle_load_button_click(game, board, persistence_service) -> None:
    """Handle load button click.

    Args:
        game: BackgammonGame instance
        board: BackgammonBoard instance
        persistence_service: GamePersistenceService instance

    Returns:
        None
    """
    try:
        loaded_game = persistence_service.load_game()
        if loaded_game:
            # Replace current game with loaded game
            game.__board__ = loaded_game.__board__
            game.__current_player__ = loaded_game.__current_player__
            game.__last_roll__ = loaded_game.__last_roll__
            game.__available_moves__ = loaded_game.__available_moves__
            game.__move_history__ = loaded_game.__move_history__

            # Update the board display
            board.update_from_game()
            board.show_save_message("¡Juego cargado exitosamente!")
        else:
            board.show_save_message("No hay juego guardado")
    except (OSError, IOError, ValueError) as e:
        board.show_save_message(f"Error al cargar: {str(e)[:30]}")


def _draw_win_message(screen, game) -> None:
    """
    Draw win message when the game ends.

    Args:
        screen: Pygame screen surface
        game: BackgammonGame instance

    Returns:
        None
    """
    if not game.is_game_over():
        return

    winner = game.get_winner()
    if winner is None:
        return

    overlay = pygame.Surface((screen.get_width(), screen.get_height()))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    font_large = pygame.font.Font(None, 72)
    font_medium = pygame.font.Font(None, 36)

    win_text = f"¡{winner.__name__} WINS!"
    win_surface = font_large.render(win_text, True, (255, 215, 0))  # Dorado
    win_rect = win_surface.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2 - 50)
    )
    screen.blit(win_surface, win_rect)

    instruction_text = "Press R to restart or ESC to exit"
    instruction_surface = font_medium.render(instruction_text, True, (255, 255, 255))
    instruction_rect = instruction_surface.get_rect(
        center=(screen.get_width() // 2, screen.get_height() // 2 + 20)
    )
    screen.blit(instruction_surface, instruction_rect)


def main() -> None:
    """Main function to run the backgammon board display.

    Returns:
        None
    """
    board = BackgammonBoard()
    clock = pygame.time.Clock()
    running = True

    # Create game instance
    game = BackgammonGame()
    game.setup_initial_position()

    # Initialize persistence service
    try:
        redis_persistence = RedisGamePersistence()
        # Test connection using the proper method
        if redis_persistence.test_connection():
            persistence_service = GamePersistenceService(redis_persistence)
            print("Redis connection successful")
        else:
            raise ConnectionError("Redis connection failed")
    except (ConnectionError, TimeoutError, OSError) as e:
        # Fallback to file-based persistence if Redis is not available
        print(f"Redis not available: {e}")
        print("Using file-based persistence instead")
        file_persistence = FileGamePersistence()
        persistence_service = GamePersistenceService(file_persistence)

    # Set the game instance in the board
    board.set_game(game)

    # Update board from game state
    board.update_from_game()

    while running:
        for event in pygame.event.get():
            if not _handle_event(event, game, board, persistence_service):
                running = False

        # Update save message timer
        board.update_save_message_timer()

        # Clear screen with a neutral background
        board.__screen__.fill((50, 50, 50))  # Dark gray background

        # Draw the board
        board.draw_board()

        # draw win message
        _draw_win_message(board.__screen__, game)

        # Update display
        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

    pygame.quit()  # pylint: disable=no-member


if __name__ == "__main__":
    main()
