"""
Rendering tests for pygame_ui.pygame_ui:
- Wood textures, triangles, center gap, bear-off
- Single checkers, stacks, bar, borne-off
- Dice faces 1..6, value updates, and full board drawing
- Selection highlights and points
"""

from unittest.mock import MagicMock, patch

import pygame

from .base_pygame_test import BasePygameTest  # pylint: disable=import-error


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


class TestPygameUIRendering(BasePygameTest):
    """General rendering tests for the UI."""

    def setUp(self) -> None:
        """Configura el entorno de pruebas con mocks para pygame."""
        _mock_pygame_graphics()

        # Deferred import after mocks
        with patch("pygame.display.set_mode"), patch("pygame.init"):
            self._init_board_and_game()

        # Patch drawing functions inside the concrete module to avoid real Surface use
        self._p_rect = patch("pygame_ui.pygame_ui.pygame.draw.rect", MagicMock())
        self._p_polygon = patch("pygame_ui.pygame_ui.pygame.draw.polygon", MagicMock())
        self._p_circle = patch("pygame_ui.pygame_ui.pygame.draw.circle", MagicMock())
        self._p_line = patch("pygame_ui.pygame_ui.pygame.draw.line", MagicMock())
        self._p_rect.start()
        self._p_polygon.start()
        self._p_circle.start()
        self._p_line.start()

        # Mocked screen
        self.board.screen = MagicMock()

    def tearDown(self) -> None:
        """Limpia los patches de pygame después de cada prueba."""
        # Stop patches
        self._p_rect.stop()
        self._p_polygon.stop()
        self._p_circle.stop()
        self._p_line.stop()

    def test_create_wood_texture_surface(self) -> None:
        """It should create a Surface and draw grain lines."""
        surf = self.board.create_wood_texture_surface(100, 50)
        self.assertIsNotNone(surf)

    def test_draw_triangular_point_variants(self) -> None:
        """Draws up and down triangles without errors."""
        self.board.draw_triangular_point(
            self.board.screen, 10, 10, 20, 30, (1, 2, 3), pointing_up=True
        )
        self.board.draw_triangular_point(
            self.board.screen, 10, 10, 20, 30, (1, 2, 3), pointing_up=False
        )

    def test_draw_center_gap_and_bear_off(self) -> None:
        """Draws center gap and bear-off, including labels."""
        self.board.draw_center_gap(self.board.screen)
        self.board.draw_bear_off_area(self.board.screen)

    def test_draw_checker_and_stack(self) -> None:
        """Draws a checker and a stack (normal/condensed)."""
        # Un checker blanco y uno negro
        self.board.draw_checker(self.board.screen, 50, 50, 1)
        self.board.draw_checker(self.board.screen, 80, 50, 2)

        # Pila pequeña
        self.board.draw_checkers_on_point(self.board.screen, 0, [1, 1, 1])
        # Pila grande (forzar condensado)
        self.board.draw_checkers_on_point(self.board.screen, 0, [1] * 8)

    def test_draw_bar_and_borne_off(self) -> None:
        """Draws bar and borne-off for both players."""
        self.board.draw_checkers_on_bar(self.board.screen, [1, 1], [2, 2, 2])
        self.board.draw_borne_off_checkers(self.board.screen, [1, 1, 1], [2, 2])

    def test_draw_die_face_all_values(self) -> None:
        """Draws all die faces (1..6)."""
        for value in range(1, 7):
            self.board.draw_die_face(self.board.screen, 10 * value, 20, value)

    def test_set_and_draw_dice(self) -> None:
        """Sets dice values and draws them (2 and doubles)."""
        self.board.set_dice_values(2, 5)
        self.board.draw_dice()
        self.board.set_dice_values(4, 4)
        self.board.draw_dice()

    def test_draw_points_and_selection(self) -> None:
        """Draws points and selection/possible destination highlights."""
        # Forzar selección y destinos válidos simulados
        self.board.selected_point = 0
        self.board.valid_destinations = [1, 2, 3]
        self.board.draw_points()
        self.board.draw_selection_highlights()

    def test_update_from_game_and_board(self) -> None:
        """Updates from game and draws the full board."""
        # Simular último tiro para mostrar dados
        self.game.last_roll = (3, 2)
        self.board.update_from_game()

        # Evitar dibujar botón real
        self.board.roll_button.draw = MagicMock()
        self.board.draw_board()
