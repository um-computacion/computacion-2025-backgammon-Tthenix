"""
Rendering tests for pygame_ui.pygame_ui:
- Wood textures, triangles, center gap, bear-off
- Single checkers, stacks, bar, borne-off
- Dice faces 1..6, value updates, and full board drawing
- Selection highlights and points
"""

from unittest.mock import MagicMock, patch

from test.base_pygame_test import (  # pylint: disable=import-error,no-name-in-module
    BasePygameTest,
)

import pygame
from pygame_ui.button import Button


def _mock_pygame_graphics() -> None:
    """Create basic mocks for pygame used in rendering."""
    with patch.dict(
        "sys.modules",
        {
            "pygame": MagicMock(),
            "pygame.font": MagicMock(),
            "pygame.display": MagicMock(),
            "pygame.draw": MagicMock(),
        },
    ):

        # Used submodules
        pygame.font = MagicMock()
        pygame.display = MagicMock()
        pygame.draw = MagicMock()

        # Drawing methods
        pygame.draw.rect = MagicMock()
        pygame.draw.polygon = MagicMock()
        pygame.draw.circle = MagicMock()
        pygame.draw.line = MagicMock()

        # Fonts
        mock_font_obj = MagicMock()
        mock_font_obj.render.return_value = MagicMock()
        pygame.font.Font.return_value = mock_font_obj

        # Event constants
        pygame.MOUSEMOTION = 4
        pygame.MOUSEBUTTONDOWN = 5

        # Exception types
        pygame.error = Exception

        # Rect constructor
        pygame.Rect = MagicMock(
            side_effect=lambda x, y, w, h: MagicMock(
                x=x,
                y=y,
                width=w,
                height=h,
                center=(x + w // 2, y + h // 2),
                collidepoint=lambda pos: x <= pos[0] <= x + w and y <= pos[1] <= y + h,
            )
        )


class TestPygameUIRendering(BasePygameTest):
    """General rendering tests for the UI."""

    def setUp(self) -> None:  # pylint: disable=invalid-name
        """Set up test environment with mocks for pygame.

        Returns:
            None
        """
        _mock_pygame_graphics()

        # Deferred import after mocks
        with patch("pygame.display.set_mode"), patch("pygame.init"):
            self._init_board_and_game()

        # Patch drawing functions inside the renderer modules to avoid real Surface use
        self._p_rect = patch(
            "pygame_ui.renderers.board_renderer.pygame.draw.rect", MagicMock()
        )
        self._p_polygon = patch(
            "pygame_ui.renderers.board_renderer.pygame.draw.polygon", MagicMock()
        )
        self._p_circle = patch(
            "pygame_ui.renderers.checker_renderer.pygame.draw.circle", MagicMock()
        )
        self._p_line = patch(
            "pygame_ui.renderers.board_renderer.pygame.draw.line", MagicMock()
        )
        self._p_rect.start()
        self._p_polygon.start()
        self._p_circle.start()
        self._p_line.start()

        # Mocked screen
        self.__board__.screen = MagicMock()

    def tearDown(self) -> None:  # pylint: disable=invalid-name
        """Clean up pygame patches after each test.

        Returns:
            None
        """
        # Stop patches
        self._p_rect.stop()
        self._p_polygon.stop()
        self._p_circle.stop()
        self._p_line.stop()

    def test_create_wood_texture_surface(self) -> None:
        """It should create a Surface and draw grain lines.

        Returns:
            None
        """
        surf = self.__board__.__board_renderer__.create_wood_texture_surface(100, 50)
        self.assertIsNotNone(surf)

    def test_draw_triangular_point_variants(self) -> None:
        """Draws up and down triangles without errors.

        Returns:
            None
        """
        self.__board__.__board_renderer__.draw_triangular_point(
            self.__board__.screen, 10, 10, 20, 30, (1, 2, 3), pointing_up=True
        )
        self.__board__.__board_renderer__.draw_triangular_point(
            self.__board__.screen, 10, 10, 20, 30, (1, 2, 3), pointing_up=False
        )

    def test_draw_center_gap_and_bear_off(self) -> None:
        """Draws center gap and bear-off, including labels.

        Returns:
            None
        """
        gap_x = self.__board__.play_area_x + self.__board__.half_width
        gap_y = self.__board__.play_area_y
        self.__board__.__board_renderer__.draw_center_gap(
            self.__board__.screen,
            gap_x,
            gap_y,
            self.__board__.__center_gap_width__,
            self.__board__.play_area_height,
        )
        self.__board__.__board_renderer__.draw_bear_off_area(
            self.__board__.screen,
            self.__board__.bear_off_x,
            self.__board__.bear_off_y,
            self.__board__.__bear_off_width__,
            self.__board__.board_height,
        )

    def test_draw_checker_and_stack(self) -> None:
        """Draws a checker and a stack (normal/condensed).

        Returns:
            None
        """
        # Un checker blanco y uno negro
        self.__board__.__checker_renderer__.draw_checker(
            self.__board__.screen, 50, 50, 1
        )
        self.__board__.__checker_renderer__.draw_checker(
            self.__board__.screen, 80, 50, 2
        )

        # Pila pequeña
        self.__board__.__checker_renderer__.draw_checkers_on_point(
            self.__board__.screen,
            0,
            [1, 1, 1],
            self.__board__.play_area_x,
            self.__board__.play_area_y,
            self.__board__.play_area_height,
            self.__board__.__point_width__,
            self.__board__.__point_height__,
            self.__board__.half_width,
            self.__board__.__center_gap_width__,
        )
        # Pila grande (forzar condensado)
        self.__board__.__checker_renderer__.draw_checkers_on_point(
            self.__board__.screen,
            0,
            [1] * 8,
            self.__board__.play_area_x,
            self.__board__.play_area_y,
            self.__board__.play_area_height,
            self.__board__.__point_width__,
            self.__board__.__point_height__,
            self.__board__.half_width,
            self.__board__.__center_gap_width__,
        )

    def test_draw_bar_and_borne_off(self) -> None:
        """Draws bar and borne-off for both players."""
        bar_center_x = (
            self.__board__.play_area_x
            + self.__board__.half_width
            + self.__board__.__center_gap_width__ // 2
        )
        self.__board__.__checker_renderer__.draw_checkers_on_bar(
            self.__board__.screen,
            [1, 1],
            [2, 2, 2],
            bar_center_x,
            self.__board__.play_area_y,
            self.__board__.play_area_height,
        )
        bear_off_center_x = (
            self.__board__.bear_off_x + self.__board__.__bear_off_width__ // 2
        )
        self.__board__.__checker_renderer__.draw_borne_off_checkers(
            self.__board__.screen,
            [1, 1, 1],
            [2, 2],
            bear_off_center_x,
            self.__board__.bear_off_y,
            self.__board__.board_height,
        )

    def test_draw_die_face_all_values(self) -> None:
        """Draws all die faces (1..6)."""
        for value in range(1, 7):
            self.__board__.__dice_renderer__.draw_die_face(
                self.__board__.screen, 10 * value, 20, value
            )

    def test_set_and_draw_dice(self) -> None:
        """Sets dice values and draws them (2 and doubles)."""
        self.__board__.set_dice_values(2, 5)
        self.__board__.draw_dice()
        self.__board__.set_dice_values(4, 4)
        self.__board__.draw_dice()

    def test_draw_points_and_selection(self) -> None:
        """Draws points and selection/possible destination highlights."""
        # Forzar selección y destinos válidos simulados en BoardInteraction
        self.__board__.__interaction__.__selected_point__ = 0
        self.__board__.__interaction__.__valid_destinations__ = [1, 2, 3]
        self.__board__.__board_renderer__.draw_points(
            self.__board__.screen,
            self.__board__.play_area_x,
            self.__board__.play_area_y,
            self.__board__.play_area_height,
            self.__board__.__point_width__,
            self.__board__.__point_height__,
            self.__board__.half_width,
            self.__board__.__center_gap_width__,
        )
        self.__board__.draw_selection_highlights()

    def test_update_from_game_and_board(self) -> None:
        """Updates from game and draws the full board."""
        # Simular último tiro para mostrar dados
        self.__game__.__last_roll__ = (3, 2)
        self.__board__.update_from_game()

        # Evitar dibujar botón real
        self.__board__.__roll_button__.draw = MagicMock()
        self.__board__.draw_board()

    # ==================== BUTTON COMPONENT TESTS ====================

    def test_button_initialization_default_colors(self) -> None:
        """Test button initialization with default colors.

        Returns:
            None
        """

        button = Button(10, 20, 100, 50, "Test Button")

        # Verify default colors
        self.assertEqual(button.__color__, (139, 69, 19))  # Brown
        self.assertEqual(button.__hover_color__, (160, 82, 45))  # Saddle brown
        self.assertEqual(button.__text_color__, (255, 255, 255))  # White
        self.assertFalse(button.__is_hovered__)
        self.assertEqual(button.__text__, "Test Button")

    def test_button_initialization_custom_colors(self) -> None:
        """Test button initialization with custom colors.

        Returns:
            None
        """

        custom_color = (255, 0, 0)
        custom_hover = (255, 100, 100)
        custom_text = (0, 0, 0)

        button = Button(
            10,
            20,
            100,
            50,
            "Custom Button",
            color=custom_color,
            hover_color=custom_hover,
            text_color=custom_text,
        )

        self.assertEqual(button.__color__, custom_color)
        self.assertEqual(button.__hover_color__, custom_hover)
        self.assertEqual(button.__text_color__, custom_text)

    def test_button_draw_normal_state(self) -> None:
        """Test button drawing in normal (non-hovered) state.

        Returns:
            None
        """

        button = Button(10, 20, 100, 50, "Test")
        button.__is_hovered__ = False

        # Mock surface
        mock_surface = MagicMock()

        # Test drawing
        button.draw(mock_surface)

        # Verify pygame.draw.rect was called for background
        pygame.draw.rect.assert_called()
        # Verify pygame.draw.rect was called for border
        self.assertEqual(pygame.draw.rect.call_count, 2)

    def test_button_draw_hovered_state(self) -> None:
        """Test button drawing in hovered state.

        Returns:
            None
        """

        button = Button(10, 20, 100, 50, "Test")
        button.__is_hovered__ = True

        # Mock surface
        mock_surface = MagicMock()

        # Test drawing
        button.draw(mock_surface)

        # Verify pygame.draw.rect was called
        pygame.draw.rect.assert_called()

    def test_button_draw_with_font_success(self) -> None:
        """Test button drawing with successful font rendering.

        Returns:
            None
        """

        button = Button(10, 20, 100, 50, "Test Button")

        # Mock surface
        mock_surface = MagicMock()

        # Mock font and text rendering
        mock_font = MagicMock()
        mock_text_surface = MagicMock()
        mock_text_rect = MagicMock()
        mock_text_surface.get_rect.return_value = mock_text_rect
        mock_font.render.return_value = mock_text_surface
        pygame.font.Font.return_value = mock_font

        # Test drawing
        button.draw(mock_surface)

        # Verify font was created and text was rendered
        pygame.font.Font.assert_called_with(None, 28)
        mock_font.render.assert_called_once_with("Test Button", True, (255, 255, 255))
        mock_surface.blit.assert_called_once_with(mock_text_surface, mock_text_rect)

    def test_button_draw_with_font_error(self) -> None:
        """Test button drawing when font rendering fails.

        Returns:
            None
        """

        button = Button(10, 20, 100, 50, "Test Button")

        # Mock surface
        mock_surface = MagicMock()

        # Mock font to raise pygame.error
        with patch("pygame.font.Font") as mock_font:
            mock_font.side_effect = pygame.error("Font loading failed")

            # Test drawing - should not raise exception but handle gracefully
            try:
                button.draw(mock_surface)
                # Test passes if no exception is raised
            except Exception as e:  # pylint: disable=broad-exception-caught
                self.fail(
                    f"Button.draw() should handle font errors gracefully, but raised: {e}"
                )

            # Verify that basic drawing operations were still called (rect drawing)
            self.assertGreater(len(mock_surface.method_calls), 0)

    def test_button_handle_mouse_motion_hover(self) -> None:
        """Test button handling mouse motion for hover detection.

        Returns:
            None
        """
        # Patch pygame constants and Rect for this test
        with patch("pygame.MOUSEMOTION", 4), patch("pygame.Rect") as mock_rect_class:

            # Set up the mock rect to simulate collision detection
            mock_rect = MagicMock()
            mock_rect.collidepoint.return_value = True  # Simulate mouse inside button
            mock_rect_class.return_value = mock_rect

            button = Button(10, 20, 100, 50, "Test")

            # Create mouse motion event with position inside button
            mock_event = MagicMock()
            mock_event.type = 4  # pygame.MOUSEMOTION
            mock_event.pos = (50, 40)  # Position inside button (10,20) to (110,70)

            # Test event handling
            result = button.handle_event(mock_event)

            # Verify hover state was set
            self.assertTrue(button.__is_hovered__)
            self.assertFalse(result)  # Mouse motion doesn't return True

    def test_button_handle_mouse_motion_no_hover(self) -> None:
        """Test button handling mouse motion when not hovering.

        Returns:
            None
        """
        # Patch pygame constants and Rect for this test
        with patch("pygame.MOUSEMOTION", 4), patch("pygame.Rect") as mock_rect_class:

            # Set up the mock rect to simulate collision detection
            mock_rect = MagicMock()
            mock_rect.collidepoint.return_value = False  # Simulate mouse outside button
            mock_rect_class.return_value = mock_rect

            button = Button(10, 20, 100, 50, "Test")

            # Create mouse motion event with position outside button
            mock_event = MagicMock()
            mock_event.type = 4  # pygame.MOUSEMOTION
            mock_event.pos = (200, 200)  # Position outside button

            # Test event handling
            result = button.handle_event(mock_event)

            # Verify hover state was not set
            self.assertFalse(button.__is_hovered__)
            self.assertFalse(result)

    def test_button_handle_mouse_click_left_button(self) -> None:
        """Test button handling left mouse button click.

        Returns:
            None
        """
        # Patch pygame constants and Rect for this test
        with patch("pygame.MOUSEBUTTONDOWN", 5), patch(
            "pygame.Rect"
        ) as mock_rect_class:

            # Set up the mock rect to simulate collision detection
            mock_rect = MagicMock()
            mock_rect.collidepoint.return_value = True  # Simulate mouse inside button
            mock_rect_class.return_value = mock_rect

            button = Button(10, 20, 100, 50, "Test")

            # Create mouse button down event with position inside button
            mock_event = MagicMock()
            mock_event.type = 5  # pygame.MOUSEBUTTONDOWN
            mock_event.button = 1  # Left button
            mock_event.pos = (50, 40)  # Position inside button

            # Test event handling
            result = button.handle_event(mock_event)

            # Verify button was clicked
            self.assertTrue(result)

    def test_button_handle_mouse_click_right_button(self) -> None:
        """Test button handling right mouse button click (should not trigger).

        Returns:
            None
        """
        # Patch pygame constants and Rect for this test
        with patch("pygame.MOUSEBUTTONDOWN", 5), patch(
            "pygame.Rect"
        ) as mock_rect_class:

            # Set up the mock rect to simulate collision detection
            mock_rect = MagicMock()
            mock_rect.collidepoint.return_value = True  # Simulate mouse inside button
            mock_rect_class.return_value = mock_rect

            button = Button(10, 20, 100, 50, "Test")

            # Create mouse button down event with right button
            mock_event = MagicMock()
            mock_event.type = 5  # pygame.MOUSEBUTTONDOWN
            mock_event.button = 3  # Right button
            mock_event.pos = (50, 40)  # Position inside button

            # Test event handling
            result = button.handle_event(mock_event)

            # Verify button was not clicked (only left button triggers)
            self.assertFalse(result)

    def test_button_handle_mouse_click_outside_button(self) -> None:
        """Test button handling mouse click outside button area.

        Returns:
            None
        """
        # Patch pygame constants and Rect for this test
        with patch("pygame.MOUSEBUTTONDOWN", 5), patch(
            "pygame.Rect"
        ) as mock_rect_class:

            # Set up the mock rect to simulate collision detection
            mock_rect = MagicMock()
            mock_rect.collidepoint.return_value = False  # Simulate mouse outside button
            mock_rect_class.return_value = mock_rect

            button = Button(10, 20, 100, 50, "Test")

            # Create mouse button down event with position outside button
            mock_event = MagicMock()
            mock_event.type = 5  # pygame.MOUSEBUTTONDOWN
            mock_event.button = 1  # Left button
            mock_event.pos = (200, 200)  # Position outside button

            # Test event handling
            result = button.handle_event(mock_event)

            # Verify button was not clicked
            self.assertFalse(result)

    def test_button_handle_unknown_event(self) -> None:
        """Test button handling unknown event type.

        Returns:
            None
        """

        button = Button(10, 20, 100, 50, "Test")

        # Create unknown event
        mock_event = MagicMock()
        mock_event.type = 999  # Unknown event type

        # Test event handling
        result = button.handle_event(mock_event)

        # Verify no action was taken
        self.assertFalse(result)

    def test_button_rect_properties(self) -> None:
        """Test button rectangle properties.

        Returns:
            None
        """

        button = Button(15, 25, 120, 60, "Test")

        # Verify rect properties
        self.assertEqual(button.__rect__.x, 15)
        self.assertEqual(button.__rect__.y, 25)
        self.assertEqual(button.__rect__.width, 120)
        self.assertEqual(button.__rect__.height, 60)
