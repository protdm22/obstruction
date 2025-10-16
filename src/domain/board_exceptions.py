class BoardException(Exception):
    pass


class PositionUnavailableException(BoardException):
    pass


class PositionOutsideBoundsException(BoardException):
    pass


class GameOverException(Exception):
    pass
