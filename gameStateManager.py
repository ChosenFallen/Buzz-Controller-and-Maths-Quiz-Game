from enum import Enum, auto

import pygame

from baseGameState import BaseGameState
from buzzSystem import BuzzBrain
from menu import ControllerSettingsMenu, MainMenu, MainSettingsMenu
from settingsManager import SettingsManager


class GAMESTATE(Enum):
    # SETUP = auto()
    MAIN_MENU = auto()
    SETTINGS_MENU = auto()
    CONTROLLERS_SETTINGS_MENU = auto()
    MAIN_GAME = auto()
    QUIT = auto()


class GameStateManager:
    state: BaseGameState

    def __init__(self, state: GAMESTATE, settings_manager: SettingsManager) -> None:
        self.state_name: GAMESTATE = state
        self.settings_manager = settings_manager
        self.set_state(state)

    def set_state(self, state: GAMESTATE) -> None:
        self.state_name = state
        match state:
            case GAMESTATE.MAIN_MENU:
                self.state = MainMenu(self.settings_manager, self)

            case GAMESTATE.SETTINGS_MENU:
                self.state = MainSettingsMenu(self.settings_manager, self)

            case GAMESTATE.CONTROLLERS_SETTINGS_MENU:
                self.state = ControllerSettingsMenu(self.settings_manager, self)

            case GAMESTATE.MAIN_GAME:
                self.state = BuzzBrain(self.settings_manager, self)

            case GAMESTATE.QUIT:
                self.quit()

            case _:
                raise NotImplementedError()

    def change_state(self, state_name: GAMESTATE) -> None:
        if self.state_name != state_name:
            self.state.kill()
            pygame.display.update()
            self.set_state(state_name)

    def quit(self) -> None:
        self.state.kill()
        pygame.quit()
        exit()

    def update(self) -> None:
        self.state.update()
