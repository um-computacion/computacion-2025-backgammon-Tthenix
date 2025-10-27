"""
Test module for Button class functionality.
"""

# pylint: disable=no-member
import unittest
from unittest.mock import Mock, patch
import pygame
from pygame_ui.button import Button


class TestButton(unittest.TestCase):
    """Test cases for Button class."""

    def setUp(self):
        """Set up test fixtures."""
        # pylint: disable=no-member
        pygame.init()
        self.button = Button(
            x=100,
            y=100,
            width=80,
            height=40,
            text="Test Button",
            color=(255, 0, 0),
            hover_color=(200, 0, 0),
            text_color=(255, 255, 255),
        )

    def tearDown(self):
        """Clean up test fixtures."""
        # pylint: disable=no-member
        pygame.quit()

    def test_init_default_params(self):
        """Test initialization with default parameters."""
        button = Button(0, 0, 50, 30, "Default")

        self.assertEqual(button.__color__, (139, 69, 19))
        self.assertEqual(button.__hover_color__, (160, 82, 45))
        self.assertEqual(button.__text_color__, (255, 255, 255))
        self.assertFalse(button.__is_hovered__)

    def test_init_custom_params(self):
        """Test initialization with custom parameters."""
        self.assertEqual(self.button.__text__, "Test Button")
        self.assertEqual(self.button.__color__, (255, 0, 0))
        self.assertEqual(self.button.__hover_color__, (200, 0, 0))
        self.assertEqual(self.button.__text_color__, (255, 255, 255))

    def test_rect_properties(self):
        """Test button rectangle properties."""
        self.assertEqual(self.button.__rect__.x, 100)
        self.assertEqual(self.button.__rect__.y, 100)
        self.assertEqual(self.button.__rect__.width, 80)
        self.assertEqual(self.button.__rect__.height, 40)

    @patch("pygame.draw.rect")
    @patch("pygame.font.Font")
    def test_draw_single_line_text(
        self, mock_font_class, mock_draw_rect
    ):  # pylint: disable=unused-argument
        """Test drawing button with single line text."""
        mock_font = Mock()
        mock_font_class.return_value = mock_font
        mock_surface = Mock()
        mock_text_surface = Mock()
        mock_text_rect = Mock()
        mock_text_surface.get_rect.return_value = mock_text_rect
        mock_font.render.return_value = mock_text_surface

        self.button.draw(mock_surface)
        # Verify font was created
        mock_font_class.assert_called_once_with(None, 28)

        # Verify text was rendered
        mock_font.render.assert_called_once_with("Test Button", True, (255, 255, 255))

        # Verify text rect was centered
        mock_text_surface.get_rect.assert_called_once_with(
            center=self.button.__rect__.center
        )

        # Verify text was blitted
        mock_surface.blit.assert_called_once_with(mock_text_surface, mock_text_rect)

        # Verify draw.rect was called for button background
        mock_draw_rect.assert_called()

    @patch("pygame.draw.rect")
    @patch("pygame.font.Font")
    def test_draw_multi_line_text(
        self, mock_font_class, mock_draw_rect
    ):  # pylint: disable=unused-argument
        """Test drawing button with multi-line text."""
        mock_font = Mock()
        mock_font_class.return_value = mock_font
        mock_font.get_height.return_value = 20
        mock_surface = Mock()
        mock_text_surface = Mock()
        mock_text_rect = Mock()
        mock_text_surface.get_rect.return_value = mock_text_rect
        mock_font.render.return_value = mock_text_surface

        # Create button with multi-line text
        multi_button = Button(0, 0, 50, 30, "Line1\nLine2")
        multi_button.draw(mock_surface)
        # Verify font was created
        mock_font_class.assert_called_once_with(None, 28)

        # Verify text was rendered for each line
        self.assertEqual(mock_font.render.call_count, 2)
        mock_font.render.assert_any_call("Line1", True, (255, 255, 255))
        mock_font.render.assert_any_call("Line2", True, (255, 255, 255))

        # Verify draw.rect was called for button background
        mock_draw_rect.assert_called()

    @patch("pygame.draw.rect")
    @patch("pygame.font.Font")
    def test_draw_empty_lines_ignored(
        self, mock_font_class, mock_draw_rect
    ):  # pylint: disable=unused-argument
        """Test that empty lines in multi-line text are ignored."""
        mock_font = Mock()
        mock_font_class.return_value = mock_font
        mock_font.get_height.return_value = 20
        mock_surface = Mock()
        mock_text_surface = Mock()
        mock_text_rect = Mock()
        mock_text_surface.get_rect.return_value = mock_text_rect
        mock_font.render.return_value = mock_text_surface

        # Create button with multi-line text including empty lines
        multi_button = Button(0, 0, 50, 30, "Line1\n\nLine2\n")
        multi_button.draw(mock_surface)
        # Verify only non-empty lines were rendered
        self.assertEqual(mock_font.render.call_count, 2)
        mock_font.render.assert_any_call("Line1", True, (255, 255, 255))
        mock_font.render.assert_any_call("Line2", True, (255, 255, 255))

        # Verify draw.rect was called for button background
        mock_draw_rect.assert_called()

    @patch("pygame.draw.rect")
    @patch("pygame.font.Font")
    def test_draw_font_error_handling(self, mock_font_class, mock_draw_rect):
        """Test handling of font errors during drawing."""
        # pylint: disable=no-member
        mock_font_class.side_effect = pygame.error("Font error")
        mock_surface = Mock()

        # Should not raise exception
        self.button.draw(mock_surface)
        # Verify draw.rect was still called (button background)
        self.assertTrue(mock_draw_rect.called)

    def test_handle_event_mouse_motion_hover(self):
        """Test mouse motion event handling for hover."""
        mock_event = Mock()
        mock_event.type = pygame.MOUSEMOTION
        mock_event.pos = (120, 120)  # Inside button

        result = self.button.handle_event(mock_event)

        self.assertFalse(result)
        self.assertTrue(self.button.__is_hovered__)

    def test_handle_event_mouse_motion_no_hover(self):
        """Test mouse motion event handling when not hovering."""
        mock_event = Mock()
        mock_event.type = pygame.MOUSEMOTION
        mock_event.pos = (50, 50)  # Outside button

        result = self.button.handle_event(mock_event)

        self.assertFalse(result)
        self.assertFalse(self.button.__is_hovered__)

    def test_handle_event_mouse_click_inside(self):
        """Test mouse click event handling when clicking inside button."""
        mock_event = Mock()
        mock_event.type = pygame.MOUSEBUTTONDOWN
        mock_event.button = 1
        mock_event.pos = (120, 120)  # Inside button

        result = self.button.handle_event(mock_event)

        self.assertTrue(result)

    def test_handle_event_mouse_click_outside(self):
        """Test mouse click event handling when clicking outside button."""
        mock_event = Mock()
        mock_event.type = pygame.MOUSEBUTTONDOWN
        mock_event.button = 1
        mock_event.pos = (50, 50)  # Outside button

        result = self.button.handle_event(mock_event)

        self.assertFalse(result)

    def test_handle_event_mouse_click_wrong_button(self):
        """Test mouse click event handling with wrong mouse button."""
        mock_event = Mock()
        mock_event.type = pygame.MOUSEBUTTONDOWN
        mock_event.button = 2  # Right click
        mock_event.pos = (120, 120)  # Inside button

        result = self.button.handle_event(mock_event)

        self.assertFalse(result)

    def test_handle_event_other_event_type(self):
        """Test handling of other event types."""
        mock_event = Mock()
        mock_event.type = pygame.KEYDOWN

        result = self.button.handle_event(mock_event)

        self.assertFalse(result)

    def test_hover_state_affects_drawing(self):
        """Test that hover state affects button appearance."""
        # Set hover state
        self.button.__is_hovered__ = True

        # Mock the drawing functions
        with patch("pygame.draw.rect") as mock_draw_rect, patch(
            "pygame.font.Font"
        ) as mock_font_class:  # pylint: disable=unused-variable

            mock_surface = Mock()
            self.button.draw(mock_surface)
            # Verify that hover color is used
            calls = mock_draw_rect.call_args_list
            # First call should be the button background with hover color
            self.assertEqual(calls[0][0][1], (200, 0, 0))

            # Verify font was created (even though we don't use the mock_font_class directly)
            mock_font_class.assert_called()

    def test_button_collision_detection(self):
        """Test button collision detection with different positions."""
        # Test positions inside button
        inside_positions = [
            (100, 100),  # Top-left corner
            (179, 100),  # Top-right corner (just inside)
            (100, 139),  # Bottom-left corner (just inside)
            (179, 139),  # Bottom-right corner (just inside)
            (140, 120),  # Center
        ]

        for pos in inside_positions:
            self.assertTrue(self.button.__rect__.collidepoint(pos))

        # Test positions outside button
        outside_positions = [
            (99, 100),  # Just left
            (180, 100),  # Just right
            (100, 99),  # Just above
            (100, 140),  # Just below
            (50, 50),  # Far away
        ]

        for pos in outside_positions:
            self.assertFalse(self.button.__rect__.collidepoint(pos))


if __name__ == "__main__":
    unittest.main()
