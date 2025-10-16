import copy
from random import randint

from src.domain.board import ObstructionBoard
from src.domain.board_exceptions import BoardException, GameOverException
from src.domain.symbol_types import SymbolTypes

NO_ELEMENTS = 0
FIRST_MOVE = 0

ROW_INDEX = 0
COLUMN_INDEX = 1

NO_WINNING_MOVES = 0


class Difficulty:
    def __init__(self, board: ObstructionBoard):
        self._board = board

    def computer_move(self):
        raise NotImplemented


class DifficultyEasy(Difficulty):
    def computer_move(self):
        """
        Function that returns a valid computer for the easy difficulty
        :return: (row, column) tuple for the computer move
        """
        while True:
            try:
                row = randint(0, self._board.rows - 1)
                column = randint(0, self._board.columns - 1)
                self._board.check_move_validity(row, column)
                return row, column
            except BoardException:
                continue


class DifficultyMedium(Difficulty):
    def computer_move(self):
        """
        Function that returns a valid computer for the medium difficulty
        :return: (row, column) tuple for the computer move
        """
        list_of_all_possible_moves, list_of_all_winning_moves = self._board.generate_all_possible_moves(
            SymbolTypes.COMPUTER_SYMBOL)

        # Check if there exists a winning move
        if len(list_of_all_winning_moves) != NO_ELEMENTS:
            return list_of_all_winning_moves[FIRST_MOVE]

        # Make the best move otherwise
        if len(list_of_all_possible_moves) != NO_ELEMENTS:
            best_moves = [list_of_all_possible_moves[FIRST_MOVE]]
        else:
            best_moves = [list_of_all_winning_moves[FIRST_MOVE]]
        best_move_score = float('inf')

        for computer_move in list_of_all_possible_moves:
            current_board = copy.deepcopy(self._board)
            current_board.place_symbol(computer_move[ROW_INDEX], computer_move[COLUMN_INDEX],
                                       SymbolTypes.COMPUTER_SYMBOL)

            list_of_all_remaining_player_moves, list_of_all_player_winning_moves = current_board.generate_all_possible_moves(
                SymbolTypes.PLAYER_SYMBOL)

            if len(list_of_all_player_winning_moves) == NO_WINNING_MOVES:
                player_move_score = len(list_of_all_remaining_player_moves)

                if player_move_score < best_move_score:
                    best_move_score = player_move_score
                    best_moves = [computer_move]
                if player_move_score == best_move_score:
                    best_moves.append(computer_move)

        random_best_move = randint(0, len(best_moves) - 1)
        return best_moves[random_best_move][ROW_INDEX], best_moves[random_best_move][COLUMN_INDEX]


class DifficultyHard(DifficultyMedium):
     pass
