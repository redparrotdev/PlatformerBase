import os
import pygame
from bs4 import BeautifulSoup as bs
from .tileset import Tileset
from .layer import Layer
from .objects import ObjectGroup
from .image_layer import ImageLayer


class Map:

    def __init__(self, map_path):
        self.map_folder = os.path.abspath(os.path.dirname(map_path))

        with open(map_path, "r", encoding="utf-8") as file:
            map_data = file.read()

        soup = bs(map_data, "xml")
        map = soup.find("map")
        
        self.width = int(map.get("width", 0))
        self.height = int(map.get("height", 0))
        self.tile_width = int(map["tilewidth"])
        self.tile_height = int(map["tileheight"])
        self.infinite = bool(map.get("infinite", 0))

        self.__tilesets = []
        for ts in map.find_all("tileset"):
            self.__tilesets.append(Tileset(ts, self.map_folder))
        self.__tilesets.reverse()

        self.__layers_by_name = {}
        self.__layers_by_id = {}
        for l in map.find_all("layer"):
            layer = Layer(self, l, self.__tilesets)
            self.__layers_by_id[layer.id] = layer
            if layer.name in self.__layers_by_name:
                raise ValueError(f"Layer with name {layer.name} is already exists!")
            self.__layers_by_name[layer.name] = layer

        self.__object_groups_by_name = {}
        self.__object_groups_by_id = {}
        for obj_group in map.find_all("objectgroup"):
            og = ObjectGroup(self, obj_group, self.__tilesets)
            self.__object_groups_by_id[og.id] = og
            if og.name is self.__object_groups_by_name:
                raise ValueError(f"ObjectGroup with name {og.name} is already exists!")
            self.__object_groups_by_name[og.name] = og

        self.__image_layers_by_name = {}
        self.__image_layers_by_id = {}
        for il_node in map.find_all("imagelayer"):
            il = ImageLayer(self, il_node)
            self.__image_layers_by_id[il.id] = il
            if il.name is self.__image_layers_by_name:
                raise ValueError(f"ImageLayer with name {il.name} is already exists!")
            self.__image_layers_by_name[il.name] = il

    def get_layer(self, identifier) -> Layer:
        if type(identifier) == int:
            return self.__layers_by_id.get(identifier)
        elif type(identifier) == str:
            return self.__layers_by_name.get(identifier)
        else:
            return None

    def get_object_group(self, identifier) -> ObjectGroup:
        if type(identifier) == int:
            return self.__object_groups_by_id.get(identifier)
        elif type(identifier) == str:
            return self.__object_groups_by_name.get(identifier)
        else:
            return None

    def find_object(self, id):
        for og in self.__object_groups_by_id.values():
            if id in og.objects:
                return og.get_object(id)

    def get_image_layer(self, identifier) -> ImageLayer:
        if type(identifier) == int:
            return self.__image_layers_by_id.get(identifier)
        elif type(identifier) == str:
            return self.__image_layers_by_name.get(identifier)
        else:
            return None

    def get_all_image_layers(self):
        return pygame.sprite.Group(self.__image_layers_by_id.values())
        
