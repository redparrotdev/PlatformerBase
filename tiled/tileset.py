import os
import pygame
from bs4 import BeautifulSoup as bs
from lib import Animation


class Tileset:

    def __init__(self, node: bs, map_folder):
        self.gid = int(node["firstgid"])
        self.name = node.get("name", "")
        self.tile_width = int(node["tilewidth"])
        self.tile_height = int(node["tileheight"])
        self.tilecount = int(node["tilecount"])
        self.columns = int(node["columns"])
        self.is_grid = node.find("grid") is not None

        self.tiles = {}

        if self.is_grid:
            self.__load_grid(node, map_folder)
        else:
            self.__load_default(node, map_folder)

        self.__load_props_and_anims(node)

    def get_tile(self, tile_id):
        return self.tiles.get(tile_id)

    def __load_default(self, node: bs, map_folder):
        image = node.find("image")
        sheet_path = os.path.join(map_folder, image["source"])
        sheet = pygame.image.load(sheet_path)

        for i in range(self.tilecount):
            keys = ("image", "type", "animated", "properties", "animation")
            tile_data = dict.fromkeys(keys)

            row = i // self.columns
            col = i % self.columns

            x = col * self.tile_width
            y = row * self.tile_height

            tile_rect = pygame.Rect(x, y, self.tile_width, self.tile_height)
            image = sheet.subsurface(tile_rect)

            tile_data[keys[0]] = image
            self.tiles[i] = tile_data

    def __load_grid(self, node: bs, map_folder):
        for tile in node.find_all("tile"):
            keys = ("image", "type", "animated", "properties", "animation")
            tile_data = dict.fromkeys(keys)

            tile_id = int(tile["id"])
            image = tile.find("image")
            sprite_path = os.path.join(map_folder, image["source"])
            sprite = pygame.image.load(sprite_path)

            tile_data[keys[0]] = sprite
            self.tiles[tile_id] = tile_data

    def __load_props_and_anims(self, node: bs):
        for tile in node.find_all("tile"):
            tile_id = int(tile["id"])
            self.tiles[tile_id]["type"] = tile.get("type")
            self.tiles[tile_id]["animated"] = False

            props_node = tile.find("properties")
            properties = {}

            if props_node is not None:
                properties = self.__get_properties(props_node)

            animation_node = tile.find("animation")
            animation = None

            if animation_node is not None:
                self.tiles[tile_id]["animated"] = True
                animation = self.__get__animation(animation_node)

            self.tiles[tile_id]["properties"] = properties
            self.tiles[tile_id]["animation"] = animation


    def __get_properties(self, node: bs):
        properties = {}

        for prop in node.find_all("property"):
            name = prop["name"]
            prop_type = prop.get("type", "")
            value = prop["value"]

            properties[name] = {
                "type": prop_type,
                "value": value
            }

        return properties

    def __get__animation(self, node: bs):
        frames = []
        duration = 0

        for frame in node.find_all("frame"):
            tile_id = int(frame["tileid"])
            frame_time = int(frame["duration"])

            frames.append(self.tiles[tile_id]["image"])
            duration += frame_time

        return Animation(frames, duration / 1000)
