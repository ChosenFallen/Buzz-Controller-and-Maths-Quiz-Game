from os.path import join

import pygame

from settings import *
from support import import_image, BaseState


class Menu(BaseState):
    def __init__(self, all_sprites, buttons_group) -> None:

        # self.display_surface = pygame.display.get_surface()
        title_font = pygame.font.Font(join("fonts", "Game Of Squids.ttf"), 125)
        self.title = Title(all_sprites, title_font)

        button_font = pygame.font.Font(join("fonts", "GameCube.ttf"), 50)
        self.start_button = Button(
            [all_sprites, buttons_group],
            (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
            "Start",
            button_font,
            self.start,
        )
        # self.start_button = Button(all_sprites, "blue", WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 100, 50, button_font, "Start")

    def start(self):
        pass

    def update(self) -> None:
        pass
    
    def kill(self) -> None:
        pass

    # def update(self) -> None:
    #     self.display_surface.blit(self.title.image, self.title.rect)


class Title(pygame.sprite.Sprite):
    def __init__(self, all_sprites, font) -> None:
        super().__init__(all_sprites)

        self.image = font.render("Maths Quiz", True, "black")
        self.rect = self.image.get_frect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4))  # type: ignore

        # self.image = import_image("questions", "images", "ampere_maxwell_law@2x")


class Button(pygame.sprite.Sprite):
    def __init__(self, all_sprites, pos, text, font, function) -> None:
        super().__init__(all_sprites)

        self.pos = pos
        self.function = function
        self.text = text
        self.font = font

        self.normal_surf = self.create_normal_surf()
        self.hover_surf = self.create_hover_surf()
        self.clicked_surf = self.create_clicked_surf()

        self.hover = False

        self.image = self.normal_surf
        self.rect: pygame.FRect = self.image.get_frect(center=pos)  # type: ignore

    def create_hover_surf(self) -> pygame.Surface:
        # sourcery skip: class-extract-method
        surf = pygame.Surface(
            (300, 100), flags=pygame.SRCALPHA, depth=32
        ).convert_alpha()
        text_rect = surf.get_frect(topleft=(0, 0))
        pygame.draw.rect(
            surface=surf,
            color="black",
            rect=text_rect,
            width=0,
            border_radius=10,
        )
        text_render = self.font.render(self.text, True, "white")
        surf.blit(text_render, text_render.get_frect(center=(150, 50)))
        pygame.draw.rect(
            surface=surf,
            color="white",
            rect=text_rect,
            width=5,
            border_radius=10,
        )
        return surf

    def create_normal_surf(self) -> pygame.Surface:
        surf = pygame.Surface(
            (300, 100), flags=pygame.SRCALPHA, depth=32
        ).convert_alpha()
        text_rect = surf.get_frect(topleft=(0, 0))
        text_render = self.font.render(self.text, True, "black")
        surf.blit(text_render, text_render.get_frect(center=(150, 50)))
        pygame.draw.rect(
            surface=surf,
            color="black",
            rect=text_rect,
            width=5,
            border_radius=10,
        )
        return surf

    def create_clicked_surf(self) -> pygame.Surface:
        surf = pygame.Surface(
            (300, 100), flags=pygame.SRCALPHA, depth=32
        ).convert_alpha()
        text_rect = surf.get_frect(topleft=(0, 0))
        pygame.draw.rect(
            surface=surf,
            color="black",
            rect=text_rect,
            width=0,
            border_radius=10,
        )
        small_font = self.font
        small_font.point_size = int(self.font.point_size * 0.8)
        text_render = small_font.render(self.text, True, "white")
        surf.blit(text_render, text_render.get_frect(center=(150, 50)))
        pygame.draw.rect(
            surface=surf,
            color="white",
            rect=text_rect,
            width=10,
            border_radius=10,
        )
        return surf

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.isOver(mouse_pos):
            # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.hover = True
            if pygame.mouse.get_pressed()[0]:
                self.image = self.clicked_surf
            else:
                self.image = self.hover_surf
        else:
            self.hover = False
            self.image = self.normal_surf
        # self.image = self.hover_surf if self.isOver(mouse_pos) else self.normal_surf
        self.rect = self.image.get_frect(center=self.pos)  # type: ignore

    # def isOver(self, pos):
    #     # Pos is the mouse position or a tuple of (x, y) coordinates
    #     return (
    #         pos[0] > self.rect.left
    #         and pos[0] < self.rect.right
    #         and pos[1] > self.rect.top
    #         and pos[1] < self.rect.bottom
    #     )

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        return self.rect.collidepoint(pos)

    # def draw(self, display_surface) -> None:
    #     # super().draw(display_surface)


# class Button(pygame.sprite.Sprite):
#     def __init__(self, all_sprites, color, x, y, width, height, font, text=''):
#         super().__init__(all_sprites)
#         self.color = color
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = height
#         self.text = text
#         self.font = font

#     def draw(self, surf):
#         # Call this method to draw the button on the screen
#         pygame.draw.rect(surf, "black", (self.x-2, self.y-2, self.width+4, self.height+4), 0)

#         pygame.draw.rect(surf, self.color, (self.x, self.y, self.width, self.height), 0)

#         if self.text != '':
#             text = self.font.render(self.text, 1, (0, 0, 0))
#             surf.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

#     def isOver(self, pos):
#         # Pos is the mouse position or a tuple of (x, y) coordinates
#         return (
#             pos[0] > self.x
#             and pos[0] < self.x + self.width
#             and pos[1] > self.y
#             and pos[1] < self.y + self.height
#         )
