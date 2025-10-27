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
