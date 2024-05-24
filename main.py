from os.path import join

import pygame

from buzzSystem import BuzzBrain, GameType  # NoControllerBuzzBrain
from menu import ControllerSettingsMenu, MainMenu, MainSettingsMenu
from questions.curatedQuestion import CuratedQuestionSet, question_sets
from settings import *
from settings import GameState
from support import BaseState, import_image, import_svg


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Maths Quiz")
        self.main_title_font = pygame.font.Font(
            join("fonts", "Game Of Squids.ttf"), 125
        )
        self.sub_title_font = pygame.font.Font(join("fonts", "CT ProLamina.ttf"), 125)
        self.button_font = pygame.font.Font(join("fonts", "CT ProLamina.ttf"), 100)
        # self.arrow_font = pygame.font.Font(join("fonts", "Arrows.ttf"), 150)

        # display_question = True

        self.all_sprites = pygame.sprite.Group()  # type: ignore
        self.buttons_group = pygame.sprite.Group()  # type: ignore
        # self.redirect_group = pygame.sprite.Group()  # type: ignore

        # Do we need?
        # self.menu_group = pygame.sprite.Group()  # type: ignore

        # self.question_set = CuratedQuestionSet(
        #     question_sets["bodmas"], [] #, self.all_sprites
        # )
        # self.brain = BuzzBrain(
        #     self.question_set, num_of_controllers=4, game_type=GameType.ONE_QUESTION
        # )
        # buzz_brain = NoControllerBuzzBrain(question_set)
        # self.test_surf = import_image("questions", "images", "ampere_maxwell_law@2x")
        self.state: BaseState
        self.set_gamemode(GameState.MAIN_MENU)
        # self.test_surf.set_colorkey("white")
        # buzz_brain.setup(game_type=GameType.ONE_QUESTION)

    def set_gamemode(self, mode: GameState) -> None:
        self.gamemode = mode
        match mode:
            case GameState.MAIN_MENU:
                self.state = MainMenu(
                    self.all_sprites,
                    self.buttons_group,
                    self.main_title_font,
                    self.button_font,
                )

            case GameState.SETTINGS_MENU:
                self.state = MainSettingsMenu(
                    self.all_sprites,
                    self.buttons_group,
                    self.sub_title_font,
                    self.button_font,
                )

            case GameState.CONTROLLERS_SETTINGS_MENU:
                self.state = ControllerSettingsMenu(
                    self.all_sprites,
                    self.buttons_group,
                    self.sub_title_font,
                    self.button_font,
                )

            case GameState.MAIN_GAME:
                self.state = BuzzBrain()

            case GameState.QUIT:
                self.quit()

            case _:
                raise NotImplementedError()

    def change_gamemode(self, mode: GameState) -> None:
        if self.gamemode != mode:
            self.state.kill()
            pygame.display.update()
            self.set_gamemode(mode)

    def run(self) -> None:
        while True:

            if self.state.redirect is not None:
                self.change_gamemode(self.state.redirect)

            self.display_surface.fill("darkgray")

            # self.display_surface.blit(self.test_surf, (200, 200))
            self.all_sprites.update()
            self.state.update()
            self.all_sprites.draw(self.display_surface)

            hover = any(sprite.hover for sprite in self.buttons_group)
            if hover:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            pygame.display.update()

            # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def quit(self) -> None:
        self.state.kill()
        pygame.quit()
        exit()


if __name__ == "__main__":
    game = Game()
    game.run()
