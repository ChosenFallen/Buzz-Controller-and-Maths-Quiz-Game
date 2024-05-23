from copy import copy
from os.path import join

from ui import Button, Title, BackButton
from settings import *
from settings import GameState
from support import BaseState, import_image


class MainMenu(BaseState):
    def __init__(self, all_sprites, buttons_group, title_font, button_font) -> None:
        super().__init__()
        # type: ignore

        # self.display_surface = pygame.display.get_surface()
        self.title = Title(
            [all_sprites, self.state_group],
            title_font,
            "Maths Quiz",
            (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4),
        )

        # button_font2 = pygame.font.Font(join("fonts", "recharge bd.otf"), 50)
        self.start_button = Button(
            [all_sprites, buttons_group, self.state_group],
            (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 2),
            "Start",
            button_font,
            self.start,
        )
        self.settings_button = Button(
            [all_sprites, buttons_group, self.state_group],
            (3 * (WINDOW_WIDTH / 4), WINDOW_HEIGHT / 2),
            "Settings",
            button_font,
            self.settings,
        )
        # self.start_button = Button(all_sprites, "blue", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 100, 50, button_font, "Start")

    def settings(self):
        self.redirect = GameState.SETTINGS_MENU

    def start(self):
        self.redirect = GameState.MAIN_GAME

    def update(self) -> None:
        pass

    # def kill(self) -> None:
    #     for sprite in self.menu_group:
    #         sprite.kill()

    # def update(self) -> None:
    #     self.display_surface.blit(self.title.image, self.title.rect)


class SettingsMenu(BaseState):
    def __init__(
        self, all_sprites, buttons_group, title_font, button_font, arrow_font
    ) -> None:
        super().__init__()
        # print(arrow_font)
        # self.menu_group = pygame.sprite.Group()  # type: ignore

        self.title = Title(
            groups=[all_sprites, self.state_group],
            font=title_font,
            text="Settings",
            pos=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4),
        )
        self.go_back_button = BackButton(
            groups=[all_sprites, buttons_group, self.state_group],
            pos=(WINDOW_WIDTH / 16, WINDOW_HEIGHT / 8),
            function=self.go_back,
            size=(50, 50),
        )
        # self.start_button = Button(
        #     [all_sprites, buttons_group, self.menu_group],
        #     (WINDOW_WIDTH / 4, WINDOW_HEIGHT / 2),
        #     "Start",
        #     button_font,
        #     self.start,
        # )
        # self.settings_button = Button(
        #     [all_sprites, buttons_group, self.menu_group],
        #     (3 * (WINDOW_WIDTH / 4), WINDOW_HEIGHT / 2),
        #     "Settings",
        #     button_font,
        #     self.settings,
        # )

    def go_back(self):
        self.redirect = GameState.MAIN_MENU

    def update(self) -> None:
        pass

    # def kill(self) -> None:
    #     pass

