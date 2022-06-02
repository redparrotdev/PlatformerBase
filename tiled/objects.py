import os
from turtle import position
import pygame
from bs4 import BeautifulSoup as bs
from .tile import Tile, AnimatedTile
from lib import Animation

class ObjectGroup:

    def __init__(self, map, node: bs, tilesets):
        self.id = int(node["id"])
        self.name = node.get("name", "")

        self.objects = {}
        self.__objects_by_name = {}
        self.__renderable = []  # utility list of renderable object like TileObject and TextObject
        
        for obj in node.find_all("object"):
            o = None

            if obj.find("point") is not None:
                o = Point(map, obj)
            elif obj.find("ellipse") is not None:
                o = Ellipse(map, obj)
            elif obj.find("text") is not None:
                o = Text(map, obj)
                self.__renderable.append(o)
            elif obj.get("gid") is not None:
                o = TileObject(map, obj, tilesets)
                self.__renderable.append(o)
            else:
                o = Rectangle(map, obj)

            self.objects[o.id] = o

    def get_object(self, object_id):
        return self.objects.get(object_id)

    def filter_by_type(self, object_type):
        filtered = []
        for o in self.objects.values():
            if o.object_type == object_type:
                filtered.append(o)
        
        return filtered

    # Only for visual elements
    def update(self, dt):
        for element in self.__renderable:
            element.update(dt)

    def render(self, win, offset):
        for element in self.__renderable:
            element.render(win, offset)


class BaseObject:

    def __init__(self, map, node: bs):
        self.map = map
        self.id = int(node["id"])
        self.name = node.get("name", "")
        self.object_type = node.get("type")

        x = float(node["x"])
        y = float(node["y"])

        w = float(node.get("width", 0))
        h = float(node.get("height", 0))

        self.position = pygame.Vector2(x, y)
        self.size = pygame.Vector2(w, h)
        self.rect = pygame.Rect(self.position, self.size)

        self.properties = self.__get_properties(node.find("properties"))

    def __get_properties(self, node: bs):
        properties = {}

        if node is None:
            return properties

        for prop in node.find_all("property"):
            name = prop["name"]
            prop_type = prop.get("type", "")
            value = prop["value"]

            properties[name] = {
                "type": prop_type,
                "value": value
            }

        return properties

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

    def collide_rect(self, rect: pygame.Rect):
        pass

    def collide_point(self, point: pygame.Vector2):
        pass

    def collide_sprite(self, sprite: pygame.sprite.Sprite):
        pass


class Rectangle(BaseObject):
    ''' Basic map reactangle area '''
    
    def collide_rect(self, rect: pygame.Rect):
        return self.rect.colliderect(rect)

    def collide_point(self, point: pygame.Vector2):
        return self.rect.collidepoint(point.x, point.y)

    def collide_sprite(self, sprite: pygame.sprite.Sprite):
        return self.rect.colliderect(sprite.rect)


class Point(BaseObject):
    ''' Point is same as MapRect, except widht and height is equals to 0'''
    def collide_rect(self, rect: pygame.Rect):
        return rect.collidepoint(self.position.x, self.position.y)

    def collide_point(self, point: pygame.Vector2):
        return self.position == point

    def collide_sprite(self, sprite: pygame.sprite.Sprite):
        return sprite.rect.collidepoint(self.position.x, self.position.y) 


class Ellipse(BaseObject):
    ''' ellipse is same as MapRect, bur have another collision detection functionality'''
    # TODO Add ellipse collision behavior
    pass


class VisualObject(BaseObject):

    def update(self, dt):
        pass
    
    def render(self, win, offset):
        pass

class TileObject(VisualObject):
    ''' Object that contain renderable tile'''
    
    def __init__(self, map, node: bs, tilesets):
        super().__init__(map, node)

        gid = int(node["gid"])

        tileset = None
        # bad type of search xD
        for ts in tilesets:
            if ts.gid <= gid:
                tileset = ts
                break

        tile_id = gid - tileset.gid
        tile_data = tileset.get_tile(tile_id)

        if self.size != pygame.Vector2(tile_data["image"].get_size()):
            tile_data["image"] = pygame.transform.scale(tile_data["image"], self.size)
            if tile_data["animated"]:
                animation = tile_data["animation"]
                frames = []
                for f in animation.frames:
                    scaled_frame = pygame.transform.scale(f, self.size)
                    frames.append(scaled_frame)

                scaled_animation = Animation(frames, animation.duration, animation.repeat)

                tile_data["animation"] = scaled_animation
                

        tile = None

        if tile_data["animated"]:
            tile = AnimatedTile(
                map, self.position,
                tile_data["animation"],
                tile_data["type"],
                tile_data["properties"]
            )
        else:
            tile = Tile(
                map, self.position,
                tile_data["image"],
                tile_data["type"],
                tile_data["properties"]
            )

        self.tile = tile

        self.tile.rect.bottomleft = self.position

    def update(self, dt):
        self.tile.update(dt)

    def render(self, win, offset):
        self.tile.render(win, offset)

    def collide_rect(self, rect: pygame.Rect):
        return self.tile.rect.colliderect(rect)

    def collide_point(self, point: pygame.Vector2):
        return self.tile.rect.collidepoint(point.x, point.y)

    def collide_sprite(self, sprite: pygame.sprite.Sprite):
        return pygame.sprite.collide_rect(self.tile, sprite)


class Text(VisualObject):
    ''' Similar to TileObject, but contains tile with text image'''
    
    def __init__(self, map, node: bs):
        super().__init__(map, node)

        text_node = node.find("text")

        self.text = text_node.text
        self.font_family = text_node.get("fontfamily", "MS Sans Serif")
        self.font_size = int(text_node.get("pixelsize", 16))
        self.wrap = bool(text_node["wrap"])
        self.color = pygame.Color(text_node.get("color", "#000000"))

        font = pygame.font.SysFont(self.font_family, self.font_size)
        self.image = font.render(self.text, True, self.color)
        # TO DO Make text wrapping when it is too large for rectangle

    def render(self, win, offset):
        win.blit(self.image, self.position - offset)

    def collide_rect(self, rect: pygame.Rect):
        return self.rect.colliderect(rect)

    def collide_point(self, point: pygame.Vector2):
        return self.rect.collidepoint(point.x, point.y)

    def collide_sprite(self, sprite: pygame.sprite.Sprite):
        return self.rect.colliderect(sprite.rect)
