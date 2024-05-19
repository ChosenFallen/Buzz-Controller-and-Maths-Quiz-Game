import pygame

from buzzSystem import BuzzBrain
from Questions.curatedQuestion import CuratedQuestionSet, question_sets

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt: float = 0

player_pos = pygame.Vector2(screen.get_width() // 2, screen.get_height() // 2)

display_question = True

question_set = CuratedQuestionSet(question_sets["bodmas"])
buzz_brain = BuzzBrain(question_set)
buzz_brain.turn_on_all_lights()
ALL_CONTROLLERS = [0, 1, 2, 3]
valid_controllers = ALL_CONTROLLERS.copy()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    pygame.draw.circle(screen, "red", player_pos, 40)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    pygame.display.flip()

    dt = clock.tick(60) / 1000

    if display_question:
        display_question = False
        question_set.get_current_question_data().display_question()

    # Update the controllers
    buzz_brain.update()
    # buzz_brain.first_pressed_controller()
    # print(buzz_brain.first_pressed_controller())

    # TODO: Prevent the system from detecting a button press until it is released
    #       or potentially only show next question when no buttons are down and time has elapsed (maybe depends on game mode)

    index = buzz_brain.first_pressed_controller()
    if index is not None:
        # print(index)
        colour = buzz_brain.first_pressed_button(index)
        print(f"Controller {index} pressed {colour}")
        if question_set.get_current_question_data().check_answer(colour):
            print("Correct")
            if buzz_brain.question_set.load_next_question():
                buzz_brain.turn_on_all_lights()
                buzz_brain.reset_all_controllers()
                display_question = True

            else:
                running = False
        else:
            print("Wrong")
            buzz_brain.turn_off_index(index)
            buzz_brain.remove_controller(index)

    # Get the most recently pressed button
    # Update the lights?
    # Update the players question


buzz_brain.turn_off_all_lights()
# force update
buzz_brain.sendLightState()
pygame.quit()
