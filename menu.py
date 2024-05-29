from typing import TYPE_CHECKING

from baseGameState import BaseGameState
from constants import *
from ui import BackButton, Button, Title

if TYPE_CHECKING:
    from gameStateManager import GameStateManager
    from settingsManager import SettingsManager


class MainMenu(BaseGameState):
    def __init__(
        self, settings_manager: "SettingsManager", game_state_manager: "GameStateManager"
    ) -> None:

        # all_sprites, buttons_group, title_font, button_font) -> None:
        super().__init__(settings_manager, game_state_manager)

        # self.display_surface = pygame.display.get_surface()
        self.title = Title(
            [self.settings_manager.all_sprites, self.state_group],
            self.settings_manager.main_title_font,
            "Maths Quiz",
            (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4),
        )

        # button_font2 = pygame.font.Font(join("fonts", "recharge bd.otf"), 50)
        self.start_button = Button(
            [
                self.settings_manager.all_sprites,
                self.settings_manager.button_group,
                self.state_group,
            ],
            (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 2),
            "Start",
            self.settings_manager.button_font,
            function=lambda: self.game_state_manager.change_state(
                GAMESTATE.MAIN_GAME
            ),
        )
        
        self.settings_button = Button(
            [
                self.settings_manager.all_sprites,
                self.settings_manager.button_group,
                self.state_group,
            ],
            (3 * (WINDOW_WIDTH / 4), WINDOW_HEIGHT / 2),
            "Settings",
            self.settings_manager.button_font,
            function=lambda: self.game_state_manager.change_state(
                GAMESTATE.SETTINGS_MENU
            ),
        )
        # self.start_button = Button(all_sprites, "blue", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 100, 50, button_font, "Start")

    # def settings(self):
    #     self.redirect = GAMESTATE.SETTINGS_MENU

    # def start(self):
    #     self.redirect = GAMESTATE.MAIN_GAME

    def update(self) -> None:
        pass

    # def kill(self) -> None:
    #     for sprite in self.menu_group:
    #         sprite.kill()

    # def update(self) -> None:
    #     self.display_surface.blit(self.title.image, self.title.rect)


class MainSettingsMenu(BaseGameState):
    def __init__(
        self, settings_manager: "SettingsManager", game_state_manager: "GameStateManager"
    ) -> None:
        super().__init__(settings_manager, game_state_manager)

        self.title = Title(
            groups=[self.settings_manager.all_sprites, self.state_group],
            font=self.settings_manager.sub_title_font,
            text="Settings",
            pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4),
        )
        self.go_back_button = BackButton(
            groups=[
                self.settings_manager.all_sprites,
                self.settings_manager.button_group,
                self.state_group,
            ],
            pos=(WINDOW_WIDTH / 16, WINDOW_HEIGHT / 8),
            function=lambda: self.game_state_manager.change_state(
                GAMESTATE.MAIN_MENU
            ),
            size=(50, 50),
        )
        self.start_button = Button(
            [
                self.settings_manager.all_sprites,
                self.settings_manager.button_group,
                self.state_group,
            ],
            (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 2),
            "Controllers",
            self.settings_manager.button_font,
            lambda: self.game_state_manager.change_state(
                GAMESTATE.CONTROLLERS_SETTINGS_MENU
            ),
        )
        # self.settings_button = Button(
        #     [all_sprites, buttons_group, self.state_group],
        #     (3 * (WINDOW_WIDTH / 4), WINDOW_HEIGHT / 2),
        #     "Settings",
        #     button_font,
        #     self.settings,
        # )

    # def go_back(self):

    # def go_to_controllers_settings(self):

    def update(self) -> None:
        pass

    # def kill(self) -> None:
    #     pass


class ControllerSettingsMenu(BaseGameState):
    def __init__(
        self, settings_manager: "SettingsManager", game_state_manager: "GameStateManager"
    ) -> None:
        super().__init__(settings_manager, game_state_manager)

        self.title = Title(
            groups=[self.settings_manager.all_sprites, self.state_group],
            font=self.settings_manager.sub_title_font,
            text="Controller Settings",
            pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4),
        )
        self.go_back_button = BackButton(
            groups=[
                self.settings_manager.all_sprites,
                self.settings_manager.button_group,
                self.state_group,
            ],
            pos=(WINDOW_WIDTH / 16, WINDOW_HEIGHT / 8),
            function=lambda: self.game_state_manager.change_state(
                GAMESTATE.SETTINGS_MENU
            ),
            size=(50, 50),
        )

    def update(self) -> None:
        pass

