from enum import Enum


class SymbolTypes(Enum):
    PLAYER_SYMBOL = 'O'
    COMPUTER_SYMBOL = 'X'
    BLOCKED_SYMBOL = '#'
    EMPTY_SYMBOL = ' '