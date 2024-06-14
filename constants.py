from enum import Enum, auto

ALL_COLOURS = ["yellow", "green", "orange", "blue", "red"]
ANSWER_COLOURS = ["yellow", "green", "orange", "blue"]
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720


class Colours(Enum):
    Red = auto()
    Yellow = auto()
    Green = auto()
    Orange = auto()
    Blue = auto()


class GameType(Enum):
    ONE_QUESTION = auto()
    IDV_QUESTION = auto()


class GAMESTATE(Enum):
    # SETUP = auto()
    MAIN_MENU = auto()
    SETTINGS_MENU = auto()
    CONTROLLERS_SETTINGS_MENU = auto()
    MAIN_GAME = auto()


class Tags(Enum):
    EQUATION = "equation"


class DIFFICULTY(Enum):
    EASY = auto()
    MEDIUM = auto()
    HARD = auto()

# class CursorType(Enum):
#     NORMAL = auto()
#     HAND = auto()
