"""
Additional Pygame UI tests focused on:
- Dice rendering: two vs four when doubles are rolled
- Automatic turn switch when no moves remain
"""

from unittest.mock import MagicMock, patch

from test.base_pygame_test import (
    BasePygameTest,
)


class TestPygameUIDiceAndTurn(BasePygameTest):
    """Dice rendering and auto turn switch tests."""

    def setUp(self) -> None:
        """Configura el entorno de pruebas con patches para pygame."""
        # Patch real drawing calls inside the UI module to avoid real Surface requirement
        self._patch_draw_rect = patch(
            "pygame_ui.pygame_ui.pygame.draw.rect", MagicMock()
        )
        self._patch_draw_circle = patch(
            "pygame_ui.pygame_ui.pygame.draw.circle", MagicMock()
        )
        self._patch_draw_rect.start()
        self._patch_draw_circle.start()

        with patch("pygame.display.set_mode"), patch("pygame.init"):
            self._init_board_and_game()

    def tearDown(self) -> None:
        """Limpia los patches de pygame después de cada prueba."""
        # Stop drawing patches
        self._patch_draw_rect.stop()
        self._patch_draw_circle.stop()

    def test_draw_dice_two_and_four_on_doubles(self) -> None:
        """Verify four dice on doubles and two dice otherwise."""
        # Prepare mocked screen surface
        self.board.screen = MagicMock()

        # Patch draw_die_face to count calls
        with patch.object(
            self.board, "draw_die_face", wraps=self.board.draw_die_face
        ) as draw_face:
            # Non-doubles case
            self.board.set_dice_values(2, 5)
            self.board.draw_dice()
            # There must be 2 calls
            self.assertEqual(draw_face.call_count, 2)

        with patch.object(
            self.board, "draw_die_face", wraps=self.board.draw_die_face
        ) as draw_face:
            # Doubles case
            self.board.set_dice_values(3, 3)
            self.board.draw_dice()
            # There must be 4 calls
            self.assertEqual(draw_face.call_count, 4)

    def test_auto_turn_switch_after_moves_exhausted(self) -> None:
        """When no moves remain, it should automatically switch turns."""
        # Configure turn and dice available to a single move of 1
        self.game.current_player = self.game.player1
        self.game.last_roll = (1, 1)
        self.game.available_moves = [1]

        # From point 0 (white) to 1 should be valid in initial position
        from_point = 0
        to_point = 1

        # Ensure the move is valid before executing
        if self.game.validate_move(from_point, to_point):
            # Execute via UI to trigger auto turn switch logic
            moved = self.board.execute_checker_move(from_point, to_point)
            self.assertTrue(moved)
            # When moves are exhausted, UI must clear roll and switch player
            self.assertIsNone(self.game.last_roll)
            self.assertEqual(self.game.available_moves, [])
            self.assertEqual(self.game.current_player, self.game.player2)
