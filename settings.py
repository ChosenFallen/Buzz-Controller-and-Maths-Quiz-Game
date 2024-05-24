from enum import Enum, auto

ALL_COLOURS = ["yellow", "green", "orange", "blue", "red"]
ANSWER_COLOURS = ["yellow", "green", "orange", "blue"]
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720


class GameState(Enum):
    # SETUP = auto()
    MAIN_MENU = auto()
    SETTINGS_MENU = auto()
    CONTROLLERS_SETTINGS_MENU = auto()
    MAIN_GAME = auto()
    QUIT = auto()


# class CursorType(Enum):
#     NORMAL = auto()
#     HAND = auto()
