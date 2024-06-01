from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from gameStateManager import GameStateManager
    from settingsManager import SettingsManager


# class GAMESTATE(Enum):
#     # SETUP = auto()
#     MAIN_MENU = auto()
#     SETTINGS_MENU = auto()
#     CONTROLLERS_SETTINGS_MENU = auto()
#     MAIN_GAME = auto()
#     QUIT = auto()


class BaseGameState(ABC):
    def __init__(
        self,
        settings_manager: "SettingsManager",
        game_state_manager: "GameStateManager",
    ) -> None:
        self.settings_manager = settings_manager
        self.game_state_manager = game_state_manager
        # self.redirect: None | GAMESTATE = None
        self.state_group = pygame.sprite.Group()  # type: ignore
        super().__init__()

    @abstractmethod
    def update(self) -> None:
        pass

    def kill(self) -> None:
        for sprite in self.state_group:
            sprite.kill()
