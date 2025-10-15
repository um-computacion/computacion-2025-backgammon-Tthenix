"""
Clase base para tests de pygame UI.
Contiene métodos comunes de inicialización para evitar duplicación.
"""

from unittest import TestCase
from pygame_ui.pygame_ui import BackgammonBoard
from core.backgammon import BackgammonGame


class BasePygameTest(TestCase):
    """Clase base con lógica compartida para tests de pygame UI."""

    board: "BackgammonBoard"
    game: "BackgammonGame"

    def _init_board_and_game(self) -> None:
        """Crear tablero y juego inicializados y reflejarlos en el tablero."""

        self.board = BackgammonBoard()
        self.game = BackgammonGame()
        self.game.setup_initial_position()
        self.board.set_game(self.game)
        self.board.update_from_game()
