import pygame

from settings import *
from support import import_image


class Menu:
    def __init__(self, all_sprites) -> None:

        self.title = Title(all_sprites)
        # self.display_surface = pygame.display.get_surface()

    # def update(self) -> None:
    #     self.display_surface.blit(self.title.image, self.title.rect)


class Title(pygame.sprite.Sprite):
    def __init__(self, all_sprites) -> None:
        super().__init__(all_sprites)

        self.image = import_image("Questions", "Images", "ampere_maxwell_law@2x")
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3))  # type: ignore


class Button(pygame.sprite.Sprite):
    def __init__(self, all_sprites, pos, surf) -> None:
        super().__init__(all_sprites)

        self.image = surf
        self.rect = self.image.get_frect(center=pos)  # type: ignore
