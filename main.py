from os.path import join

import pygame

from buzzSystem import GameType
from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from gameStateManager import GAMESTATE, GameStateManager
from questions.baseQuestion import BaseQuestionSet
from settingsManager import SettingsManager
from utilities import load_font


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Maths Quiz")

        self.all_sprites = pygame.sprite.Group()  # type: ignore
        self.button_group = pygame.sprite.Group()  # type: ignore

        self.settings_manager = SettingsManager(
            num_of_controllers=4,
            game_type=GameType.IDV_QUESTION,
            question_set=BaseQuestionSet(),
            button_group=self.button_group,
            all_sprites=self.all_sprites,
            main_title_font=load_font("Game Of Squids.ttf", 125),
            button_font=load_font("CT ProLamina.ttf", 100),
            sub_title_font=load_font("CT ProLamina.ttf", 125),
        )

        self.game_state_manager = GameStateManager(
            state=GAMESTATE.MAIN_MENU,
            settings_manager=self.settings_manager,
        )

    def run(self) -> None:
        while True:

            self.display_surface.fill("darkgray")

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


if __name__ == "__main__":
    game = Game()
    game.run()
