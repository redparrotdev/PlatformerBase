import pygame


class Camera:

    def __init__(self, size, focus):
        self.size = size
        self.offset = pygame.Vector2()
        self.focus = pygame.Vector2(focus) * -1
        self.viewport = pygame.Rect(self.offset, self.size)

    def set_scroll_method(self, method):
        self.method = method

    def update(self, dt):
        self.method.update(dt)
        self.viewport = pygame.Rect(self.offset, self.size)


class ScrollMethod:

    def __init__(self, camera):
        self.camera = camera

    def update(self, dt):
        pass


class CameraFollow(ScrollMethod):

    def __init__(self, camera, target):
        super().__init__(camera)
        self.target = target

    def update(self, dt):
        self.camera.offset += pygame.Vector2(self.target.rect.topleft) - self.camera.offset + self.camera.focus
