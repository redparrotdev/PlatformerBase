import pygame
from lib import Handler, Assets


class CollectCoinHandler(Handler):

    def __init__(self, level):
        self.level = level

    def invoke(self, collectable):
        sound_asset = collectable.get("sound_asset")
        sound = Assets.get(sound_asset)

        value = collectable.get("value")

        sound.play()

        collectable.kill()


class TpToPointHandler(Handler):

    def __init__(self, player):
        self.player = player
    
    def invoke(self, trigger):
        point = trigger.get("point")

        self.player.rect.center = point.position
        self.player.position = pygame.Vector2(self.player.rect.topleft)
