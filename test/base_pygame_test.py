"""
Clase base para tests de pygame UI.
Contiene métodos comunes de inicialización para evitar duplicación.
"""

from unittest import TestCase
from pygame_ui.pygame_ui import BackgammonBoard
from core.backgammon import BackgammonGame


class BasePygameTest(TestCase):
    """Clase base con lógica compartida para tests de pygame UI."""

    def __init__(self, *args, **kwargs):
        """Initialize test with board and game attributes."""
        super().__init__(*args, **kwargs)
        self.__board__: "BackgammonBoard" = None
        self.__game__: "BackgammonGame" = None

    def _init_board_and_game(self) -> None:
        """Crear tablero y juego inicializados y reflejarlos en el tablero."""

        self.__board__ = BackgammonBoard()
        self.__game__ = BackgammonGame()
        self.__game__.setup_initial_position()
        self.__board__.set_game(self.__game__)
        self.__board__.update_from_game()
