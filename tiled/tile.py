import os
import pygame
from lib import Animation, Animator


class Tile(pygame.sprite.Sprite):
    
    def __init__(self, map, pos, image, tile_type=None, properties={}):
        super().__init__()
        self.map = map
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.tile_type = tile_type
        self.properties = properties

    def get(self, key):
        ''' Get object property. this method return various types'''
        if key not in self.properties:
            return None

        prop = self.properties[key]

        t = prop["type"]
        value = prop["value"]

        if t == "int":
            value = int(value)
        elif t == "float":
            value = float(value)
        elif t == "bool":
            value = True if value == "true" else False
        elif t == "color":
            value = pygame.Color(value) if value != "" else pygame.Color("#000000")
        elif t == "file":
            value = os.path.join(self.map.map_folder, value)
        elif t == "object":
            value = self.map.find_object(int(value))
        # If noone, its str property

        return value

    def render(self, win, offset):
        win.blit(self.image, self.rect.topleft - offset)


class AnimatedTile(Tile):
    
    def __init__(self, map, pos, animation, tile_type=None, properties={}):
        super().__init__(map, pos, animation.frames[0], tile_type, properties)
        
        self.animator = Animator()
        self.animator.add("idle", animation)
        self.animator.play("idle")

    def update(self, dt):
        self.animator.update(dt)

    def render(self, win, offset):
        self.image = self.animator.get_frame()
        
        super().render(win, offset)
