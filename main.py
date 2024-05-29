from os.path import join

import pygame

from baseGameState import BaseGameState
from buzzSystem import BuzzBrain, GameType  # NoControllerBuzzBrain
from constants import *
from gameStateManager import GAMESTATE, GameStateManager
from menu import ControllerSettingsMenu, MainMenu, MainSettingsMenu
from questions.baseQuestion import BaseQuestionSet
from questions.curatedQuestion import CuratedQuestionSet, question_sets
from settingsManager import SettingsManager
from utilities import import_image, import_svg


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Maths Quiz")
        # self.arrow_font = pygame.font.Font(join("fonts", "Arrows.ttf"), 150)

        # display_question = True

        self.all_sprites = pygame.sprite.Group()  # type: ignore
        self.button_group = pygame.sprite.Group()  # type: ignore
        # self.redirect_group = pygame.sprite.Group()  # type: ignore

        self.settings_manager = SettingsManager(
            num_of_controllers=4,
            game_type=GameType.IDV_QUESTION,
            question_set=BaseQuestionSet(),
            button_group=self.button_group,
            all_sprites=self.all_sprites,
            main_title_font=pygame.font.Font(join("fonts", "Game Of Squids.ttf"), 125),
            button_font=pygame.font.Font(join("fonts", "CT ProLamina.ttf"), 100),
            sub_title_font=pygame.font.Font(join("fonts", "CT ProLamina.ttf"), 125),
        )

        self.game_state_manager = GameStateManager(
            state=GAMESTATE.MAIN_MENU,
            settings_manager=self.settings_manager,
        )

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
        # self.state: BaseGameState
        # self.set_gamemode(GAMESTATE.MAIN_MENU)
        # self.test_surf.set_colorkey("white")
        # buzz_brain.setup(game_type=GameType.ONE_QUESTION)

    # def change_controller_settings(self, *, gametype: GameType | None = None) -> None:
    #     if gametype is not None:
    #         self.gametype = gametype

    # def set_gamemode(self, mode: GAMESTATE) -> None:
    #     self.gamemode = mode
    #     match mode:
    #         case GAMESTATE.MAIN_MENU:
    #             self.state = MainMenu(
    #                 self.all_sprites,
    #                 self.button_group,
    #                 self.main_title_font,
    #                 self.button_font,
    #             )

    #         case GAMESTATE.SETTINGS_MENU:
    #             self.state = MainSettingsMenu(
    #                 self.all_sprites,
    #                 self.button_group,
    #                 self.sub_title_font,
    #                 self.button_font,
    #             )

    #         case GAMESTATE.CONTROLLERS_SETTINGS_MENU:
    #             self.state = ControllerSettingsMenu(
    #                 self.all_sprites,
    #                 self.button_group,
    #                 self.sub_title_font,
    #                 self.button_font,
    #                 self.change_controller_settings,
    #             )

    #         case GAMESTATE.MAIN_GAME:
    #             self.state = BuzzBrain()

    #         case GAMESTATE.QUIT:
    #             self.quit()

    #         case _:
    #             raise NotImplementedError()

    # def change_gamemode(self, mode: GAMESTATE) -> None:
    #     if self.gamemode != mode:
    #         self.state.kill()
    #         pygame.display.update()
    #         self.set_gamemode(mode)

    def run(self) -> None:
        while True:

            # if self.state.redirect is not None:
            #     self.change_gamemode(self.state.redirect)

            self.display_surface.fill("darkgray")

            # self.display_surface.blit(self.test_surf, (200, 200))
            self.all_sprites.update()
            self.game_state_manager.update()
            self.all_sprites.draw(self.display_surface)

            hover = any(sprite.hover for sprite in self.button_group)
            if hover:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_state_manager.quit()

            pygame.display.update()

            # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # def quit(self) -> None:
    #     self.state.kill()
    #     pygame.quit()
    #     exit()


if __name__ == "__main__":
    game = Game()
    game.run()
