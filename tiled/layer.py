import pygame
from bs4 import BeautifulSoup as bs
from .tile import Tile, AnimatedTile


class Layer:
    
    def __init__(self, map, node: bs, tilesets):
        self.id = int(node["id"])
        self.name = node.get("name", "")
        self.width = int(node.get("width", 0))
        self.height = int(node.get("height", 0))

        self.tiles = pygame.sprite.Group()

        data = [int(i) for i in node.find("data").text.split(",")]

        self.__load(map, data, tilesets)

    def __load(self, map, data, tilesets):
        for i, tile_id in enumerate(data):
            if tile_id == 0:
                continue

            tileset = None
            # bad type of search xD
            for ts in tilesets:
                if ts.gid <= tile_id:
                    tileset = ts
                    break

            tile_id = tile_id - tileset.gid
            tile_data = tileset.get_tile(tile_id)
            
            if tile_data is None:
                continue

            row = i // self.width
            col = i % self.width

            x = col * map.tile_width
            y = row * map.tile_height

            pos = pygame.Vector2(x, y)
            tile = None

            if tile_data["animated"]:
                tile = AnimatedTile(
                    map, pos,
                    tile_data["animation"],
                    tile_data["type"],
                    tile_data["properties"]
                )
            else:
                tile = Tile(
                    map, pos,
                    tile_data["image"],
                    tile_data["type"],
                    tile_data["properties"]
                )

            self.tiles.add(tile)

    def filter_by_type(self, tile_type):
        filtered = []
        for t in self.tiles:
            if t.tile_type == tile_type:
                filtered.append(t)
        
        return filtered

    def update(self, dt):
        self.tiles.update(dt)

    def render(self, win, offset):
        for t in self.tiles:
            t.render(win, offset)
