"""
Additional Pygame UI tests focused on:
- Dice rendering: two vs four when doubles are rolled
- Automatic turn switch when no moves remain
"""

from unittest.mock import MagicMock, patch

from test.base_pygame_test import (  # pylint: disable=import-error,no-name-in-module
    BasePygameTest,
)


class TestPygameUIDiceAndTurn(BasePygameTest):
    """Dice rendering and auto turn switch tests."""

    def setUp(self) -> None:  # pylint: disable=invalid-name
        """Configura el entorno de pruebas con patches para pygame."""
        # Patch real drawing calls inside the renderer modules to avoid real Surface requirement
        self.__patch_draw_rect__ = patch(
            "pygame_ui.renderers.dice_renderer.pygame.draw.rect", MagicMock()
        )
        self.__patch_draw_circle__ = patch(
            "pygame_ui.renderers.dice_renderer.pygame.draw.circle", MagicMock()
        )
        self.__patch_draw_rect__.start()
        self.__patch_draw_circle__.start()

        with patch("pygame.display.set_mode"), patch("pygame.init"):
            self._init_board_and_game()

    def tearDown(self) -> None:  # pylint: disable=invalid-name
        """Limpia los patches de pygame después de cada prueba."""
        # Stop drawing patches
        self.__patch_draw_rect__.stop()
        self.__patch_draw_circle__.stop()

    def test_draw_dice_two_and_four_on_doubles(self) -> None:
        """Verify four dice on doubles and two dice otherwise."""
        # Prepare mocked screen surface
        self.__board__.screen = MagicMock()

        # Patch draw_die_face to count calls
        with patch.object(
            self.__board__.__dice_renderer__,
            "draw_die_face",
            wraps=self.__board__.__dice_renderer__.draw_die_face,
        ) as draw_face:
            # Non-doubles case
            self.__board__.set_dice_values(2, 5)
            self.__board__.draw_dice()
            # There must be 2 calls
            self.assertEqual(draw_face.call_count, 2)

        with patch.object(
            self.__board__.__dice_renderer__,
            "draw_die_face",
            wraps=self.__board__.__dice_renderer__.draw_die_face,
        ) as draw_face:
            # Doubles case
            self.__board__.set_dice_values(3, 3)
            self.__board__.draw_dice()
            # There must be 4 calls
            self.assertEqual(draw_face.call_count, 4)

    def test_auto_turn_switch_after_moves_exhausted(self) -> None:
        """When no moves remain, it should automatically switch turns."""
        # Configure turn and dice available to a single move of 1
        self.__game__.__current_player__ = self.__game__.__player1__
        self.__game__.__last_roll__ = (1, 1)
        self.__game__.__available_moves__ = [1]

        # From point 0 (white) to 1 should be valid in initial position
        from_point = 0
        to_point = 1

        # Ensure the move is valid before executing
        if self.__game__.validate_move(from_point, to_point):
            # Execute via UI to trigger auto turn switch logic
            moved = self.__board__.__interaction__.execute_checker_move(
                from_point, to_point
            )
            self.assertTrue(moved)
            # When moves are exhausted, UI must clear roll and switch player
            self.assertIsNone(self.__game__.__last_roll__)
            self.assertEqual(self.__game__.__available_moves__, [])
            self.assertEqual(
                self.__game__.__current_player__, self.__game__.__player2__
            )
