from src.domain.board import ObstructionBoard
from src.domain.symbol_types import SymbolTypes
from src.service.difficulty_levels import DifficultyLevels


class GameLogic:
    def __init__(self, board: ObstructionBoard, difficulty: DifficultyLevels):
        self.__board = board
        self.__difficulty = difficulty.value(board)

    @property
    def difficulty(self):
        return self.__difficulty

    def get_board(self):
        return self.__board

    def place_player_symbol(self, row, column):
        """
        Places a player symbol on the board on the given row and column indexes
        :param row: the given row index
        :param column: the given column index
        :return: None
        """
        self.__board.place_symbol(row, column, SymbolTypes.PLAYER_SYMBOL)

    def place_computer_symbol(self):
        """
        Places a computer symbol on the board
        :return: None
        """
        row, column = self.__difficulty.computer_move()
        self.__board.place_symbol(row, column, SymbolTypes.COMPUTER_SYMBOL)