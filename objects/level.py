import pygame
from lib import Input, Timers
from tiled import Map
from tiled.tile import Tile, AnimatedTile
from objects import handlers


class Level:
    
    def __init__(self, player):
        self.player = player

        self.coin_collision_handler = handlers.CollectCoinHandler(self)
        self.tp_to_handler = handlers.TpToPointHandler(self.player)

    def load(self, level_name):
        self.spawn_point = pygame.Vector2()

        map = Map(f"assets/levels/{level_name}.tmx")
        self.tiles = map.get_layer("tiles")

        collectable_group = map.get_object_group("collectable")
        self.collectable_items = pygame.sprite.Group()
        if collectable_group is not None:
            for tile_obj in collectable_group.objects.values():
                self.collectable_items.add(tile_obj.tile)

        self.objects = map.get_object_group("objects")
        self.triggers = []
        if self.objects is not None:
            self.triggers = self.objects.filter_by_type("trigger")
            spawn_point_object = self.objects.filter_by_type("spawn_point")[0]
            self.spawn_point = pygame.Vector2() if spawn_point_object is None else spawn_point_object.position


        # move player to spawn point
        self.player.rect.center = self.spawn_point
        self.player.position = pygame.Vector2(self.player.rect.topleft)

    def __horisontal_collision(self):
        target = pygame.sprite.spritecollideany(self.player, self.tiles.tiles)

        if target is not None:
            if self.player.dx > 0:
                self.player.rect.right = target.rect.left
            elif self.player.dx < 0:
                self.player.rect.left = target.rect.right

            self.player.position.x = self.player.rect.x

    def __vertical_collision(self):
        target = pygame.sprite.spritecollideany(self.player, self.tiles.tiles)

        if target is not None:
            if self.player.velocity.y > 0:
                self.player.rect.bottom = target.rect.top
                self.player.on_ground = True
            elif self.player.velocity.y < 0:
                self.player.rect.top = target.rect.bottom

            self.player.velocity.y = 0
            self.player.position.y = self.player.rect.y

        if self.player.on_ground and self.player.state == "jump" or self.player.state == "fall":
            self.player.on_ground = False

    def __items_collision(self):
        targets = pygame.sprite.spritecollide(self.player, self.collectable_items, False)

        for t in targets:
            self.coin_collision_handler.invoke(t)

    def __triggers_collision(self):
        for t in self.triggers:
            if not t.collide_sprite(self.player):
                continue

            handler_name = t.get("handler")
            handler = None
            try:
                handler = self.__getattribute__(handler_name)
            except:
                pass

            if handler is None:
                continue

            handler.invoke(t)

    def __input(self):
        
        if Input.is_key_down(pygame.K_a):
            self.player.dx = -1
            self.player.facing_left = True
        elif Input.is_key_down(pygame.K_d):
            self.player.dx = 1
            self.player.facing_left = False
        else:
            self.player.dx = 0

        if Input.is_key_pressed(pygame.K_SPACE) and self.player.on_ground:
            self.player.jump()

    def update(self, dt):
        self.__input()

        self.player.move_x(dt)
        self.__horisontal_collision()
        self.player.move_y(dt)
        self.__vertical_collision()

        self.tiles.update(dt)
        self.objects.update(dt)
        self.collectable_items.update(dt)

        self.__items_collision()
        self.__triggers_collision()

        self.player.update(dt)

    def render(self, win, camera):
        self.tiles.render(win, camera.offset)
        
        self.objects.render(win, camera.offset)
        for item in self.collectable_items:
            item.render(win, camera.offset)

        self.player.render(win, camera.offset)