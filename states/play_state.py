import pygame
from lib import State, StateStack, Input, Camera, CameraFollow
from objects.level import Level
from objects.player import Player


class PlayState(State):

    def __init__(self):
        self.player = Player()
        self.player.load_animations()

        self.level = Level(self.player)
        self.level.load("level1")

        win = pygame.display.get_surface()
        self.camera = Camera(
            win.get_size(),
            win.get_rect().center
        )
        follow = CameraFollow(self.camera, self.player)
        self.camera.set_scroll_method(follow)

    def __input(self):
        pass

    def update(self, dt):
        self.__input()

        self.level.update(dt)

        self.camera.update(dt)

    def render(self, win):
        self.level.render(win, self.camera)

