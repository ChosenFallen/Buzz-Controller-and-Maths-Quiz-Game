from dataclasses import dataclass

import pygame

from buzzSystem import GameType
from questions.baseQuestion import BaseQuestionSet


@dataclass
class SettingsManager:
    num_of_controllers: int
    game_type: GameType
    question_set: BaseQuestionSet

    button_group: pygame.sprite.Group
    all_sprites: pygame.sprite.Group

    main_title_font: pygame.font.Font
    button_font: pygame.font.Font
    sub_title_font: pygame.font.Font
