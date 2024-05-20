from enum import Enum, auto

import pygame

from buzzSystem import BuzzBrain, GameType  # NoControllerBuzzBrain
from questions.curatedQuestion import CuratedQuestionSet, question_sets
from support import import_image, import_svg
from settings import *
from menu import Menu


class GameMode(Enum):
    SETUP = auto()
    MENU = auto()
    MAIN_GAME = auto()


# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     screen.fill("darkgray")

#     # pygame.draw.circle(screen, "red", player_pos, 40)

#     # keys = pygame.key.get_pressed()

#     # if keys[pygame.K_w]:
#     #     player_pos.y -= 300 * dt
#     # if keys[pygame.K_s]:
#     #     player_pos.y += 300 * dt
#     # if keys[pygame.K_a]:
#     #     player_pos.x -= 300 * dt
#     # if keys[pygame.K_d]:
#     #     player_pos.x += 300 * dt

#     # pygame.display.flip()

#     dt = clock.tick(60) / 1000


#     # Get buzz brain to display question
#     # if display_question:
#     #     display_question = False
#     #     question_set.get_current_question_data().display_question()


#     # Update the controllers
#     running = buzz_brain.update()
#     # buzz_brain.first_pressed_controller()
#     # print(buzz_brain.first_pressed_controller())

#     # TODO: Prevent the system from detecting a button press until it is released
#     #       or potentially only show next question when no buttons are down and time has elapsed (maybe depends on game mode)


#     # TODO: Do all this in the update of the buzz_brain
#     # index = buzz_brain.first_pressed_controller()
#     # if index is not None:
#     #     # print(index)
#     #     colour = buzz_brain.first_pressed_button(index)
#     #     print(f"Controller {index} pressed {colour}")
#     #     if question_set.get_current_question_data().check_answer(colour):
#     #         print("Correct")
#     #         if buzz_brain.question_set.load_next_question():
#     #             buzz_brain.turn_on_all_lights()
#     #             buzz_brain.reset_all_controllers()
#     #             display_question = True

#     #         else:
#     #             running = False
#     #     else:
#     #         print("Wrong")
#     #         buzz_brain.turn_off_index(index)
#     #         buzz_brain.remove_controller(index)

#     # Get the most recently pressed button
#     # Update the lights?
#     # Update the players question


# buzz_brain.quit()
# # buzz_brain.turn_off_all_lights()
# # # force update
# # buzz_brain.sendLightState()
# pygame.quit()


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Maths Quiz")

        # display_question = True

        self.all_sprites = pygame.sprite.Group()  # type: ignore

        # self.question_set = CuratedQuestionSet(
        #     question_sets["bodmas"], [] #, self.all_sprites
        # )
        # self.brain = BuzzBrain(
        #     self.question_set, num_of_controllers=4, game_type=GameType.ONE_QUESTION
        # )
        # buzz_brain = NoControllerBuzzBrain(question_set)
        # self.test_surf = import_image("questions", "images", "ampere_maxwell_law@2x")
        
        self.menu = Menu(self.all_sprites)
        # self.test_surf.set_colorkey("white")
        # buzz_brain.setup(game_type=GameType.ONE_QUESTION)

    def run(self) -> None:
        while True:

            self.display_surface.fill("darkgray")

            # self.display_surface.blit(self.test_surf, (200, 200))
            self.all_sprites.update()
            self.all_sprites.draw(self.display_surface)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit()

            pygame.display.update()

    def exit(self) -> None:
        # if self.brain:
        #     self.brain.quit()
        pygame.quit()
        exit()


if __name__ == "__main__":
    game = Game()
    game.run()
