import os
import pygame
from bs4 import BeautifulSoup as bs


class ImageLayer(pygame.sprite.Sprite):

    def __init__(self, map, node: bs):
        super().__init__()
        self.map = map
        self.id = int(node["id"])
        self.name = node.get("name", "")
        x = float(node.get("offsetx", 0))
        y = float(node.get("offsety", 0))
        self.position = pygame.Vector2(x, y)
        
        image_node = node.find("image")
        image_path = os.path.join(map.map_folder, image_node["source"])
        self.image = pygame.image.load(image_path)

        self.size = pygame.Vector2(self.image.get_size())

        self.rect = self.image.get_rect(topleft=self.position)

    def render(self, win, offset):
        win.blit(self.image, self.position - offset)
