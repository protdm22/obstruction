import unittest

from src.domain.board import ObstructionBoard
from src.domain.board_exceptions import PositionOutsideBoundsException, PositionUnavailableException, GameOverException
from src.domain.symbol_types import SymbolTypes
from src.service.computer_move import DifficultyEasy
from src.service.difficulty_levels import DifficultyLevels
from src.service.game_logic import GameLogic


class Tests(unittest.TestCase):
    # tests for board.py
    def test_board_check_move_validity(self):
        board = ObstructionBoard(6, 6)
        # Check free positions
        try:
            board.check_move_validity(2, 2)
            board.check_move_validity(5, 5)
        except PositionOutsideBoundsException:
            self.fail()
        except PositionUnavailableException:
            self.fail()

        # # Check positions outside board
        self.assertRaises(PositionOutsideBoundsException, lambda: board.check_move_validity(10, 10))
        self.assertRaises(PositionOutsideBoundsException, lambda: board.check_move_validity(-1, -1))

        # Check occupied positions
        board.place_symbol(2, 2, SymbolTypes.COMPUTER_SYMBOL)
        self.assertRaises(PositionUnavailableException, lambda: board.check_move_validity(2, 2))
        self.assertRaises(PositionUnavailableException, lambda: board.check_move_validity(1, 1))

    def test_board_check_game_status(self):
        board = ObstructionBoard(6, 6)
        # Check game not over
        try:
            board.check_game_status()
        except GameOverException:
            self.fail()

        # Check game over
        board.place_symbol(1, 1, SymbolTypes.COMPUTER_SYMBOL)
        board.place_symbol(1, 4, SymbolTypes.PLAYER_SYMBOL)
        board.place_symbol(4, 1, SymbolTypes.COMPUTER_SYMBOL)
        # When placing the last symbol GameOver is raised
        self.assertRaises(GameOverException, lambda: board.place_symbol(4, 4, SymbolTypes.PLAYER_SYMBOL))

    def test_board_place_symbol(self):
        board_rows = 6
        board_columns = 6

        board = ObstructionBoard(board_rows, board_columns)

        player_row_index = 2
        player_column_index = 2

        computer_row_index = 5
        computer_column_index = 5

        board.place_symbol(player_row_index, player_column_index, SymbolTypes.PLAYER_SYMBOL)
        board.place_symbol(computer_row_index, computer_column_index, SymbolTypes.COMPUTER_SYMBOL)

        for row in range(player_row_index - 1, player_row_index + 2):
            for column in range(player_column_index - 1, player_column_index + 2):
                if row == player_row_index and column == player_column_index:
                    self.assertEqual(board.board[row][column], SymbolTypes.PLAYER_SYMBOL)
                else:
                    self.assertEqual(board.board[row][column], SymbolTypes.BLOCKED_SYMBOL)

        for row in range(computer_row_index - 1, board_rows):
            for column in range(computer_column_index - 1, board_columns):
                if row == computer_row_index and column == computer_column_index:
                    self.assertEqual(board.board[row][column], SymbolTypes.COMPUTER_SYMBOL)
                else:
                    self.assertEqual(board.board[row][column], SymbolTypes.BLOCKED_SYMBOL)

    def test_board_generate_all_possible_moves(self):
        board = ObstructionBoard(6, 6)

        board.place_symbol(1, 1, SymbolTypes.COMPUTER_SYMBOL)
        board.place_symbol(1, 4, SymbolTypes.PLAYER_SYMBOL)
        board.place_symbol(4, 1, SymbolTypes.COMPUTER_SYMBOL)

        expected_remaining_moves = [(3, 3), (3, 4), (3, 5), (4, 3), (4, 5), (5, 3), (5, 4), (5, 5)]
        expected_winning_moves = [(4, 4)]

        actual_remaining_moves, actual_winning_moves = board.generate_all_possible_moves(SymbolTypes.COMPUTER_SYMBOL)

        self.assertEqual(actual_remaining_moves, expected_remaining_moves)
        self.assertEqual(actual_winning_moves, expected_winning_moves)

    # tests for computer_move.py
    def test_computer_move(self):
        board = ObstructionBoard(6, 6)
        board.place_symbol(1, 1, SymbolTypes.PLAYER_SYMBOL)
        board.place_symbol(4, 1, SymbolTypes.PLAYER_SYMBOL)

        # Test for easy difficulty
        game_logic_easy = GameLogic(board, DifficultyLevels.EASY)
        easy_move_row, easy_move_column = game_logic_easy.difficulty.computer_move()

        # Test for medium difficulty
        game_logic_medium = GameLogic(board, DifficultyLevels.MEDIUM)
        medium_move_row, medium_move_column = game_logic_medium.difficulty.computer_move()

        try:
            board.check_move_validity(easy_move_row, easy_move_column)
            board.check_move_validity(medium_move_row, medium_move_column)
        except PositionUnavailableException:
            self.fail()
        except PositionOutsideBoundsException:
            self.fail()

    # tests for game_logic.py
    def test_place_player_symbol(self):
        pass

    def test_place_computer_symbol(self):
        pass


if __name__ == "__main__":
    unittest.main()
