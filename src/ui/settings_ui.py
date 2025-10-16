MINIMUM_SIZE = 6
MAXIMUM_SIZE = 8

COLUMN_INDEX = 0
ROW_INDEX = 1

REQUIRED_BOARD_INPUT_SIZE = 2

MAXIMUM_ALLOWED_DIFFERENCE_BETWEEN_COLUMNS_AND_ROWS = 1

ODD_NUMBER_OF_ROWS = 7
ODD_NUMBER_OF_COLUMNS = 7


class SettingsUI:

    def ask_for_settings(self):
        while True:
            try:
                board_rows, board_columns = self.request_board_size()
                break
            except ValueError:
                print("ERROR! Invalid input format")

        self.print_difficulty_menu()
        while True:
            try:
                difficulty = self.choose_difficulty()
                break
            except ValueError:
                print("ERROR! Difficulty not recognized")

        while True:
            try:
                user_plays_first = self.want_to_play_first()
                break
            except ValueError:
                print("ERROR! Option not recognized")

        return board_rows, board_columns, difficulty, user_plays_first

    @staticmethod
    def request_board_size():
        board_size = input("Enter the grid size of the board (ex: 6x6): ")
        board_size = board_size.strip()
        board_size = "".join(board_size.split(" ")).split('x')

        if len(board_size) != REQUIRED_BOARD_INPUT_SIZE:
            raise ValueError

        columns = int(board_size[COLUMN_INDEX])
        rows = int(board_size[ROW_INDEX])

        if not (MINIMUM_SIZE <= columns <= MAXIMUM_SIZE) or not (
                MINIMUM_SIZE <= rows <= MAXIMUM_SIZE) or rows > columns or columns - rows > MAXIMUM_ALLOWED_DIFFERENCE_BETWEEN_COLUMNS_AND_ROWS or (
                rows == ODD_NUMBER_OF_ROWS and columns == ODD_NUMBER_OF_COLUMNS):
            raise ValueError

        return rows, columns

    @staticmethod
    def print_difficulty_menu():
        print("Choose a difficulty:")
        print(" [1] Easy")
        print(" [2] Medium")
        print(" [3] Hard (minmax)")

    @staticmethod
    def choose_difficulty():
        user_choice = int(input(">>> "))
        return user_choice

    @staticmethod
    def want_to_play_first():
        print("Do you want to play first? (Yes/No)")
        option = input(">>> ")
        if option.lower() in "yes":
            return True
        elif option.lower() in "no":
            return False
        else:
            raise ValueError
