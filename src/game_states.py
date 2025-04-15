# game_states.py
from enum import Enum, auto

class GameState(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    INVENTORY = auto()
    GAME_OVER = auto()