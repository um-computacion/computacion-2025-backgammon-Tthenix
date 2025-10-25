"""
Tests for pygame_ui.py main functions.

This module tests the main pygame_ui.py functions including event handling,
game mechanics, and UI rendering.
"""

import unittest
from unittest.mock import patch, Mock
from test.base_pygame_test import (  # pylint: disable=import-error,no-name-in-module
    BasePygameTest,
)
import pygame  # pylint: disable=import-error
from pygame_ui.pygame_ui import (
    _handle_event,
    _handle_keydown,
    _handle_roll_dice,
    _handle_reset_game,
    _handle_mouse_click,
    _handle_roll_button_click,
    _draw_win_message,
    main,
)


class TestPygameUIMain(BasePygameTest):
    """Test cases for pygame_ui.py main functions."""

    def setUp(self):  # pylint: disable=invalid-name
        """Set up test fixtures.

        Returns:
            None
        """
        with patch("pygame.display.set_mode"), patch("pygame.init"):
            self._init_board_and_game()

    def test_handle_event_quit(self):
        """Test handling quit event returns False.

        Returns:
            None
        """
        event = Mock()
        event.type = pygame.QUIT  # pylint: disable=no-member

        result = _handle_event(event, self.__game__, self.__board__)
        self.assertFalse(result)

    def test_handle_event_game_over_escape(self):
        """Test handling escape key when game is over.

        Returns:
            None
        """
        # Mock game over state
        self.__game__.is_game_over = Mock(return_value=True)

        event = Mock()
        event.type = pygame.KEYDOWN  # pylint: disable=no-member
        event.key = pygame.K_ESCAPE  # pylint: disable=no-member

        result = _handle_event(event, self.__game__, self.__board__)
        self.assertFalse(result)

    def test_handle_event_game_over_reset(self):
        """Test handling reset key when game is over.

        Returns:
            None
        """
        # Mock game over state
        self.__game__.is_game_over = Mock(return_value=True)

        event = Mock()
        event.type = pygame.KEYDOWN  # pylint: disable=no-member
        event.key = pygame.K_r  # pylint: disable=no-member

        result = _handle_event(event, self.__game__, self.__board__)
        self.assertTrue(result)

    def test_handle_event_keydown(self):
        """Test handling keydown events.

        Returns:
            None
        """
        self.__game__.is_game_over = Mock(return_value=False)

        event = Mock()
        event.type = pygame.KEYDOWN  # pylint: disable=no-member
        event.key = pygame.K_SPACE  # pylint: disable=no-member

        with patch("pygame_ui.pygame_ui._handle_keydown") as mock_handle:
            mock_handle.return_value = True
            result = _handle_event(event, self.__game__, self.__board__)
            self.assertTrue(result)
            mock_handle.assert_called_once_with(event, self.__game__, self.__board__)

    def test_handle_event_mouse_click(self):
        """Test handling mouse click events.

        Returns:
            None
        """
        self.__game__.is_game_over = Mock(return_value=False)

        # Mock roll button
        self.__board__.roll_button = Mock()
        self.__board__.roll_button.handle_event.return_value = False

        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN  # pylint: disable=no-member
        event.pos = (100, 200)

        with patch("pygame_ui.pygame_ui._handle_mouse_click") as mock_handle:
            result = _handle_event(event, self.__game__, self.__board__)
            self.assertTrue(result)
            mock_handle.assert_called_once_with(event, self.__board__)

    def test_handle_event_roll_button(self):
        """Test handling roll button events.

        Returns:
            None
        """
        self.__game__.is_game_over = Mock(return_value=False)

        # Mock roll button
        self.__board__.roll_button = Mock()
        self.__board__.roll_button.handle_event.return_value = True

        event = Mock()
        event.type = pygame.MOUSEBUTTONDOWN  # pylint: disable=no-member
        event.pos = (100, 200)  # Add pos attribute

        with patch("pygame_ui.pygame_ui._handle_roll_button_click") as mock_handle:
            result = _handle_event(event, self.__game__, self.__board__)
            self.assertTrue(result)
            mock_handle.assert_called_once_with(self.__game__, self.__board__)

    def test_handle_keydown_escape(self):
        """Test handling escape key.

        Returns:
            None
        """
        event = Mock()
        event.key = pygame.K_ESCAPE  # pylint: disable=no-member

        result = _handle_keydown(event, self.__game__, self.__board__)
        self.assertFalse(result)

    def test_handle_keydown_space(self):
        """Test handling space key for rolling dice.

        Returns:
            None
        """
        event = Mock()
        event.key = pygame.K_SPACE  # pylint: disable=no-member

        with patch("pygame_ui.pygame_ui._handle_roll_dice") as mock_roll:
            result = _handle_keydown(event, self.__game__, self.__board__)
            self.assertTrue(result)
            mock_roll.assert_called_once_with(self.__game__, self.__board__)

    def test_handle_keydown_reset(self):
        """Test handling reset key.

        Returns:
            None
        """
        event = Mock()
        event.key = pygame.K_r  # pylint: disable=no-member

        with patch("pygame_ui.pygame_ui._handle_reset_game") as mock_reset:
            result = _handle_keydown(event, self.__game__, self.__board__)
            self.assertTrue(result)
            mock_reset.assert_called_once_with(self.__game__, self.__board__)

    def test_handle_roll_dice_no_roll(self):
        """Test rolling dice when no previous roll.

        Returns:
            None
        """
        self.__game__.__last_roll__ = None
        self.__game__.__available_moves__ = []
        self.__game__.roll_dice = Mock()
        self.__game__.has_valid_moves = Mock(return_value=True)
        self.__board__.update_from_game = Mock()

        _handle_roll_dice(self.__game__, self.__board__)

        self.__game__.roll_dice.assert_called_once()
        self.__board__.update_from_game.assert_called_once()

    def test_handle_roll_dice_no_valid_moves(self):
        """Test rolling dice when no valid moves available.

        Returns:
            None
        """
        self.__game__.__last_roll__ = None
        self.__game__.__available_moves__ = []
        self.__game__.roll_dice = Mock()
        self.__game__.has_valid_moves = Mock(return_value=False)
        self.__game__.switch_current_player = Mock()
        self.__board__.update_from_game = Mock()

        _handle_roll_dice(self.__game__, self.__board__)

        self.__game__.roll_dice.assert_called_once()
        self.__game__.switch_current_player.assert_called_once()
        self.assertEqual(self.__game__.__last_roll__, None)
        self.assertEqual(self.__game__.__available_moves__, [])
        self.__board__.update_from_game.assert_called_once()

    def test_handle_reset_game(self):
        """Test resetting the game.

        Returns:
            None
        """
        self.__game__.reset_game = Mock()
        self.__game__.setup_initial_position = Mock()
        self.__board__.update_from_game = Mock()

        _handle_reset_game(self.__game__, self.__board__)

        self.__game__.reset_game.assert_called_once()
        self.__game__.setup_initial_position.assert_called_once()
        self.__board__.update_from_game.assert_called_once()

    def test_handle_mouse_click(self):
        """Test handling mouse click.

        Returns:
            None
        """
        event = Mock()
        event.pos = (150, 250)
        self.__board__.handle_board_click = Mock()

        _handle_mouse_click(event, self.__board__)

        self.__board__.handle_board_click.assert_called_once_with(150, 250)

    def test_handle_roll_button_click_no_roll(self):
        """Test roll button click when no previous roll.

        Returns:
            None
        """
        self.__game__.__last_roll__ = None
        self.__game__.__available_moves__ = []
        self.__game__.roll_dice = Mock()
        self.__game__.has_valid_moves = Mock(return_value=True)
        self.__board__.update_from_game = Mock()

        _handle_roll_button_click(self.__game__, self.__board__)

        self.__game__.roll_dice.assert_called_once()
        self.__board__.update_from_game.assert_called_once()

    def test_handle_roll_button_click_no_valid_moves(self):
        """Test roll button click when no valid moves.

        Returns:
            None
        """
        self.__game__.__last_roll__ = None
        self.__game__.__available_moves__ = []
        self.__game__.roll_dice = Mock()
        self.__game__.has_valid_moves = Mock(return_value=False)
        self.__game__.switch_current_player = Mock()
        self.__board__.update_from_game = Mock()

        _handle_roll_button_click(self.__game__, self.__board__)

        self.__game__.roll_dice.assert_called_once()
        self.__game__.switch_current_player.assert_called_once()
        self.assertEqual(self.__game__.__last_roll__, None)
        self.assertEqual(self.__game__.__available_moves__, [])
        self.__board__.update_from_game.assert_called_once()

    def test_draw_win_message_no_game_over(self):
        """Test draw win message when game is not over.

        Returns:
            None
        """
        self.__game__.is_game_over = Mock(return_value=False)
        screen = Mock()

        _draw_win_message(screen, self.__game__)

        # Should return early, no drawing calls
        screen.blit.assert_not_called()

    def test_draw_win_message_no_winner(self):
        """Test draw win message when no winner.

        Returns:
            None
        """
        self.__game__.is_game_over = Mock(return_value=True)
        self.__game__.get_winner = Mock(return_value=None)
        screen = Mock()

        _draw_win_message(screen, self.__game__)

        # Should return early, no drawing calls
        screen.blit.assert_not_called()

    def test_draw_win_message_with_winner(self):
        """Test draw win message with winner.

        Returns:
            None
        """
        self.__game__.is_game_over = Mock(return_value=True)
        winner = Mock()
        winner.__name__ = "Player 1"
        self.__game__.get_winner = Mock(return_value=winner)

        screen = Mock()
        screen.get_width.return_value = 800
        screen.get_height.return_value = 600

        with patch("pygame.Surface") as mock_surface, patch(
            "pygame.font.Font"
        ) as mock_font:

            mock_surface_instance = Mock()
            mock_surface.return_value = mock_surface_instance

            mock_font_instance = Mock()
            mock_font_instance.render.return_value = Mock()
            mock_font.return_value = mock_font_instance

            _draw_win_message(screen, self.__game__)

            # Should create overlay and draw text
            mock_surface.assert_called()
            screen.blit.assert_called()

    def test_main_function(self):
        """Test main function execution.

        Returns:
            None
        """
        with patch("pygame_ui.pygame_ui.BackgammonBoard") as mock_board_class, patch(
            "pygame_ui.pygame_ui.BackgammonGame"
        ) as mock_game_class, patch("pygame.time.Clock") as mock_clock_class, patch(
            "pygame.event.get"
        ) as mock_event_get, patch(
            "pygame.display.flip"
        ), patch(
            "pygame.quit"
        ) as mock_quit:

            # Setup mocks
            mock_board = Mock()
            mock_board_class.return_value = mock_board
            mock_board.__screen__ = Mock()
            mock_board.__screen__.fill = Mock()
            mock_board.__screen__.get_width.return_value = 800
            mock_board.__screen__.get_height.return_value = 600
            mock_board.draw_board = Mock()
            mock_board.set_game = Mock()
            mock_board.update_from_game = Mock()

            mock_game = Mock()
            mock_game_class.return_value = mock_game
            mock_game.setup_initial_position = Mock()
            mock_game.is_game_over.return_value = False

            mock_clock = Mock()
            mock_clock_class.return_value = mock_clock
            mock_clock.tick = Mock()

            # Mock event loop - first event is quit
            quit_event = Mock()
            quit_event.type = pygame.QUIT  # pylint: disable=no-member
            mock_event_get.return_value = [quit_event]

            # Mock _handle_event to return False for quit
            with patch("pygame_ui.pygame_ui._handle_event") as mock_handle:
                mock_handle.return_value = False

                main()

                # Verify initialization
                mock_game.setup_initial_position.assert_called_once()
                mock_board.set_game.assert_called_once_with(mock_game)
                mock_board.update_from_game.assert_called_once()

                # Verify event handling
                mock_handle.assert_called_once()

                # Verify cleanup
                mock_quit.assert_called_once()

    def test_main_function_with_multiple_events(self):
        """Test main function with multiple events in one frame.

        Returns:
            None
        """
        with patch("pygame_ui.pygame_ui.BackgammonBoard") as mock_board_class, patch(
            "pygame_ui.pygame_ui.BackgammonGame"
        ) as mock_game_class, patch("pygame.time.Clock") as mock_clock_class, patch(
            "pygame.event.get"
        ) as mock_event_get, patch(
            "pygame.display.flip"
        ), patch(
            "pygame.quit"
        ):

            # Setup mocks
            mock_board = Mock()
            mock_board_class.return_value = mock_board
            mock_board.__screen__ = Mock()
            mock_board.__screen__.fill = Mock()
            mock_board.__screen__.get_width.return_value = 800
            mock_board.__screen__.get_height.return_value = 600
            mock_board.draw_board = Mock()
            mock_board.set_game = Mock()
            mock_board.update_from_game = Mock()

            mock_game = Mock()
            mock_game_class.return_value = mock_game
            mock_game.setup_initial_position = Mock()
            mock_game.is_game_over.return_value = False

            mock_clock = Mock()
            mock_clock_class.return_value = mock_clock
            mock_clock.tick = Mock()

            # Mock multiple events - first frame has multiple events, second has quit
            space_event = Mock()
            space_event.type = pygame.KEYDOWN  # pylint: disable=no-member
            space_event.key = pygame.K_SPACE  # pylint: disable=no-member

            quit_event = Mock()
            quit_event.type = pygame.QUIT  # pylint: disable=no-member

            mock_event_get.side_effect = [
                [space_event, quit_event],  # First frame
                [quit_event],  # Second frame
            ]

            with patch("pygame_ui.pygame_ui._handle_event") as mock_handle:
                # First call returns True (continue), second returns False (quit)
                mock_handle.side_effect = [True, False]

                main()

                # Should handle multiple events in first frame
                self.assertEqual(mock_handle.call_count, 2)


if __name__ == "__main__":
    unittest.main()
