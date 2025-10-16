import copy
import string

from texttable import Texttable

from src.domain.board_exceptions import PositionUnavailableException, PositionOutsideBoundsException, BoardException, GameOverException
from src.domain.symbol_types import SymbolTypes


class ObstructionBoard:
    def __init__(self, rows: int, columns: int):
        self.__rows = rows
        self.__columns = columns
        self.__board = [[SymbolTypes.EMPTY_SYMBOL for _ in range(columns)] for _ in range(rows)]

    def __str__(self):
        drawn_board = Texttable()
        drawn_board.add_row('*' + string.ascii_uppercase[:self.__columns])
        for row in range(self.__rows):
            current_row = [cell.value for cell in self.__board[row]]
            drawn_board.add_row([str(row + 1)] + current_row)

        return drawn_board.draw()

    @property
    def rows(self):
        return self.__rows

    @property
    def columns(self):
        return self.__columns

    @property
    def board(self):
        return self.__board

    def check_move_validity(self, row, column):
        """
        Checks if a move can be made on the board at the given row and column indexes
        :param row: the given row index
        :param column: the given column index
        :return: True if move can be made, False otherwise
        """
        if row >= self.__rows or row < 0 or column >= self.__columns or column < 0:
            raise PositionOutsideBoundsException

        if self.__board[row][column] != SymbolTypes.EMPTY_SYMBOL:
            raise PositionUnavailableException

    def check_game_status(self):
        """
        Checks if the game is over. If so, raises a GameOver exception
        :return: None
        """
        for row in range(self.__rows):
            for column in range(self.__columns):
                if self.__board[row][column] == SymbolTypes.EMPTY_SYMBOL:
                    return None
        raise GameOverException()

    def place_symbol(self, row_index: int, column_index: int, symbol: SymbolTypes):
        """
        Places a symbol of the given type on the board on the given row and column indexes
        and also places block symbols on the orthogonally and diagonally adjacent cells
        :param row_index: the given row index
        :param column_index: the given column index
        :param symbol: the given symbol type
        :return: None
        """
        self.check_move_validity(row_index, column_index)

        for row in range(row_index - 1, row_index + 2):
            for column in range(column_index - 1, column_index + 2):
                try:
                    self.check_move_validity(row, column)
                    if row == row_index and column == column_index:
                        self.__board[row][column] = symbol
                    else:
                        self.__board[row][column] = SymbolTypes.BLOCKED_SYMBOL
                except BoardException:
                    continue

        self.check_game_status()

    def generate_all_possible_moves(self, symbol: SymbolTypes):
        """
        Generates all possible moves for the given symbol type
        :param symbol: the given symbol type
        :return: list of (row, column) tuples of all possible non-winning moves,
                 list of (row, column) tuples of all possible winning moves
        """
        list_of_possible_moves = []
        list_of_winning_moves = []
        for row in range(self.__rows):
            for column in range(self.__columns):
                current_board = ObstructionBoard(self.__rows, self.__columns)
                current_board.__board = copy.deepcopy(self.__board)
                try:
                    current_board.place_symbol(row, column, symbol)
                    list_of_possible_moves.append((row, column))
                except GameOverException:
                    list_of_winning_moves.append((row, column))
                except BoardException:
                    continue
        return list_of_possible_moves, list_of_winning_moves
