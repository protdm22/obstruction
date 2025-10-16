from src.domain.board_exceptions import BoardException, GameOverException
from src.service.game_logic import GameLogic

COLUMN_INDEX = 0
ROW_INDEX = 1

REQUIRED_POSITION_INPUT_LENGTH = 2


class GameUI:
    def __init__(self, game_logic: GameLogic, user_plays_first):
        self.__game_logic = game_logic
        self.__is_user_turn = user_plays_first

    def game_loop(self):
        while True:
            try:
                if self.__is_user_turn:
                    self.print_board()
                    # Read loop
                    while True:
                        try:
                            row, column = self.request_user_input()
                            self.__game_logic.place_player_symbol(row, column)
                            break
                        except BoardException:
                            print("POSITION INVALID! Please enter a valid position")
                        except ValueError:
                            print("INPUT ERROR! Please enter the position correctly (ex: B4)")
                else:
                    self.__game_logic.place_computer_symbol()
                self.__is_user_turn = not self.__is_user_turn

            except GameOverException:
                self.print_board()
                if self.__is_user_turn:
                    print("You won! 🎉🎉🎉")
                else:
                    print("You lost! 😭")
                break

    def print_board(self):
        print(str(self.__game_logic.get_board()))

    @staticmethod
    def request_user_input():
        user_input = input("Enter the next position: ")
        user_input = user_input.strip()
        user_input = "".join(user_input.split(" ")).upper()

        if len(user_input) != REQUIRED_POSITION_INPUT_LENGTH:
            raise ValueError

        row = user_input[ROW_INDEX]
        column = user_input[COLUMN_INDEX]

        if not (column.isalpha() and row.isdigit()):
            raise ValueError

        row = int(row) - 1
        column = ord(column) - ord('A')

        return row, column
