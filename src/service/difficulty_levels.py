from enum import Enum

from src.service.computer_move import DifficultyEasy, DifficultyMedium, DifficultyHard


class DifficultyLevels(Enum):
    EASY = DifficultyEasy
    MEDIUM = DifficultyMedium
    HARD = DifficultyHard
