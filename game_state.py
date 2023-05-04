from enum import Enum

class GameState(Enum):
    def __int__(self):
        self.NOT_STARTED = 0
        self.ROUND_ACTIVE = 1
        self.ROUND_DONE = 2
        self.GAME_OVER = 3
