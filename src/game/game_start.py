from src.domain.board import ObstructionBoard
from src.service.difficulty_levels import DifficultyLevels
from src.service.game_logic import GameLogic
from src.ui.gui import GameGUI
from src.ui.settings_gui import SettingsGUI
from src.ui.settings_ui import SettingsUI
from src.ui.ui import GameUI

DEFAULT_SIZE = 6

DIFFICULTY_EASY = 1
DIFFICULTY_MEDIUM = 2
DIFFICULTY_HARD = 3


class Game:
    def __init__(self):
        self.__board_rows = DEFAULT_SIZE
        self.__board_columns = DEFAULT_SIZE
        self.__difficulty = DifficultyLevels.EASY
        self.__user_plays_first = True
        self.__GUI = True

    def start_game(self):
        """
        Function that initializes the game with the user settings and starts the game loop
        :return: None
        """
        board = ObstructionBoard(self.__board_rows, self.__board_columns)
        game_logic = GameLogic(board, self.__difficulty)
        if self.__GUI:
            ui = GameGUI(game_logic, self.__user_plays_first)
        else:
            ui = GameUI(game_logic, self.__user_plays_first)
        ui.game_loop()

    def game_settings(self):
        """
        Function that sets the preferred settings of the user (board size, difficulty, who
        plays first)
        :return: None
        """

        settings_ui = SettingsGUI()
        self.__board_rows, self.__board_columns, difficulty, self.__user_plays_first = settings_ui.ask_for_settings()

        difficulty_dictionary = {
            DIFFICULTY_EASY: DifficultyLevels.EASY,
            DIFFICULTY_MEDIUM: DifficultyLevels.MEDIUM,
            DIFFICULTY_HARD: DifficultyLevels.HARD
        }

        self.__difficulty = difficulty_dictionary[difficulty]


if __name__ == "__main__":
    game = Game()
    game.game_settings()
    game.start_game()
