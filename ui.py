import pygame


class Title(pygame.sprite.Sprite):
    def __init__(self, groups, font, text: str, pos: tuple[float, float]) -> None:
        super().__init__(groups)

        self.image = font.render(text, True, "black")
        self.rect = self.image.get_frect(center=pos)  # type: ignore

        # self.image = import_image("questions", "images", "ampere_maxwell_law@2x")


class Button(pygame.sprite.Sprite):
    def __init__(
        self, groups, pos, text, font, function, size: tuple[float, float] = (300, 100)
    ) -> None:
        super().__init__(groups)

        self.pos = pos
        self.function = function
        self.text = text
        self.font = font
        self.size = size

        self.normal_surf = self.create_normal_surf()
        # self.normal_surf = self.create_clicked_surf()
        self.hover_surf = self.create_hover_surf()
        self.clicked_surf = self.create_clicked_surf()

        self.do_function: bool = False
        self.hover = False

        self.image = self.normal_surf
        self.rect: pygame.FRect = self.image.get_frect(center=pos)  # type: ignore
        self.normal_rect: pygame.FRect = self.normal_surf.get_frect(center=pos)

    def create_normal_surf(self) -> pygame.Surface:
        surf = pygame.Surface(
            self.size, flags=pygame.SRCALPHA, depth=32
        ).convert_alpha()
        text_rect = surf.get_frect(topleft=(0, 0))
        pygame.draw.rect(
            surface=surf,
            color="white",
            rect=text_rect,
            width=0,
            border_radius=10,
        )
        text_render = self.font.render(self.text, True, "black")
        x_scale = (self.size[0] * 0.8) / text_render.get_width()
        if x_scale < 1:
            text_render = pygame.transform.scale_by(text_render, x_scale)
        surf.blit(
            text_render,
            text_render.get_frect(center=(self.size[0] / 2, self.size[1] / 2)),
        )
        pygame.draw.rect(
            surface=surf,
            color="black",
            rect=text_rect,
            width=5,
            border_radius=10,
        )
        return surf

    def create_hover_surf(self) -> pygame.Surface:
        # sourcery skip: class-extract-method
        surf = pygame.Surface(
            self.size, flags=pygame.SRCALPHA, depth=32
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
        x_scale = (self.size[0] * 0.8) / text_render.get_width()
        if x_scale < 1:
            text_render = pygame.transform.scale_by(text_render, x_scale)
        surf.blit(
            text_render,
            text_render.get_frect(center=(self.size[0] / 2, self.size[1] / 2)),
        )
        pygame.draw.rect(
            surface=surf,
            color="white",
            rect=text_rect,
            width=5,
            border_radius=10,
        )
        return surf

    def create_clicked_surf(self) -> pygame.Surface:

        return pygame.transform.smoothscale_by(self.create_hover_surf(), 0.8)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.isOver(mouse_pos):
            # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            self.hover = True
            if pygame.mouse.get_pressed()[0]:
                self.image = self.clicked_surf
                self.do_function = True
            else:
                self.image = self.hover_surf
                if self.do_function:
                    self.do_function = False
                    self.function()
        else:
            self.hover = False
            self.image = self.normal_surf
            self.do_function = False
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
        return self.normal_rect.collidepoint(pos)


class BackButton(pygame.sprite.Sprite):
    def __init__(
        self, groups, pos, function, size: tuple[float, float] = (300, 100)
    ) -> None:
        super().__init__(groups)

        self.pos = pos
        self.function = function
        self.size = size

        self.normal_surf = self.create_normal_surf()
        # self.normal_surf = self.create_clicked_surf()
        self.hover_surf = self.create_hover_surf()
        self.clicked_surf = self.create_clicked_surf()

        self.hover = False

        self.do_function: bool = False

        self.image = self.normal_surf
        self.rect: pygame.FRect = self.image.get_frect(center=pos)  # type: ignore
        self.normal_rect: pygame.FRect = self.normal_surf.get_frect(center=pos)

    def create_normal_surf(self) -> pygame.Surface:
        # surf = pygame.Surface(
        #     self.size, flags=pygame.SRCALPHA, depth=32
        # ).convert_alpha()
        # text_render =
        # surf.blit(text_render, text_render.get_frect(center=(self.size[0]/2, self.size[1]/2)))
        surf = pygame.Surface(
            self.size, flags=pygame.SRCALPHA, depth=32
        ).convert_alpha()
        pygame.draw.polygon(
            surface=surf,
            color="black",
            points=[
                (0, self.size[1] / 2),
                (self.size[0], 0),
                (self.size[0], self.size[1]),
            ],  # type: ignore
        )
        return surf

    def create_hover_surf(self) -> pygame.Surface:
        surf = pygame.Surface(
            self.size, flags=pygame.SRCALPHA, depth=32
        ).convert_alpha()
        pygame.draw.polygon(
            surface=surf,
            color="white",
            points=[
                (0, self.size[1] / 2),
                (self.size[0], 0),
                (self.size[0], self.size[1]),
            ],  # type: ignore
        )
        return surf

    def create_clicked_surf(self) -> pygame.Surface:
        surf = pygame.Surface(
            self.size, flags=pygame.SRCALPHA, depth=32
        ).convert_alpha()
        pygame.draw.polygon(
            surface=surf,
            color="white",
            points=[
                (self.size[0] * 0.2, self.size[1] / 2),
                (self.size[0] * 0.8, self.size[1] * 0.2),
                (self.size[0] * 0.8, self.size[1] * 0.8),
            ],  # type: ignore
        )
        return surf

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.isOver(mouse_pos):
            self.hover = True
            if pygame.mouse.get_pressed()[0]:
                self.image = self.clicked_surf
                self.do_function = True
            else:
                self.image = self.hover_surf
                if self.do_function:
                    self.do_function = False
                    self.function()
        else:
            self.hover = False
            self.image = self.normal_surf
            self.do_function = False
        self.rect = self.image.get_frect(center=self.pos)  # type: ignore

    def isOver(self, pos):
        return self.normal_rect.collidepoint(pos)
