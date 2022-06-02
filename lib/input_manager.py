import pygame


class Input:
    
    __keys = None
    __prev_keys = None

    @staticmethod
    def initialize():
        Input.__keys = pygame.key.get_pressed()
        Input.__prev_keys = Input.__keys

    @staticmethod
    def update():
        Input.__prev_keys = Input.__keys
        Input.__keys = pygame.key.get_pressed()

    @staticmethod
    def is_key_pressed(key):
        return not Input.__prev_keys[key] and Input.__keys[key]

    @staticmethod
    def is_key_down(key):
        return Input.__keys[key]
