from typing import TYPE_CHECKING

import pygame

from buzzSystem import BuzzBrain
from constants import *
from menu import ControllerSettingsMenu, MainMenu, MainSettingsMenu

# from settingsManager import SettingsManager

if TYPE_CHECKING:
    from baseGameState import BaseGameState
    from settingsManager import SettingsManager



class GameStateManager:
    state: "BaseGameState"
    state_mapping: dict[GAMESTATE, type[BaseGameState]] = {
        GAMESTATE.MAIN_MENU: MainMenu,
        GAMESTATE.SETTINGS_MENU: MainSettingsMenu,
        GAMESTATE.CONTROLLERS_SETTINGS_MENU: ControllerSettingsMenu,
        GAMESTATE.MAIN_GAME: BuzzBrain,
    }

    def __init__(self, state: GAMESTATE, settings_manager: "SettingsManager") -> None:
        self.state_name: GAMESTATE = state
        self.settings_manager = settings_manager
        self.set_state(state)

    def set_state(self, state: GAMESTATE) -> None:
        self.state_name = state
        if state in self.state_mapping:
            self.state = self.state_mapping[state](self.settings_manager, self)
        else:
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
        # print(self.state_name)
