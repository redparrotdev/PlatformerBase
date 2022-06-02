import os
import pygame


class Assets:

    __assets_folder = os.path.join(os.getcwd(), "assets")

    __storage = {}

    @staticmethod
    def set_assets_folder(folder_path):
        Assets.__assets_folder = folder_path

    @staticmethod
    def __get_path(asset_name):
        return os.path.join(Assets.__assets_folder, asset_name)

    @staticmethod
    def load_image(name, asset_name):
        asset_path = Assets.__get_path(asset_name)
        image = pygame.image.load(asset_path)

        Assets.__storage[name] = image

    @staticmethod
    def load_sound(name, asset_name):
        asset_path = Assets.__get_path(asset_name)
        sound = pygame.mixer.Sound(asset_path)

        Assets.__storage[name] = sound

    @staticmethod
    def load_animation(name, asset_name, row, count, size, col=0, resize=None):
        frames = []
        size = pygame.Vector2(size)
        y = row * size.y

        asset_path = Assets.__get_path(asset_name)
        sheet = pygame.image.load(asset_path)

        for i in range(count):
            i += col
            x = i * size.x

            frame_rect = pygame.Rect((x, y), size)
            image = sheet.subsurface(frame_rect)

            if resize is not None:
                if type(resize) != tuple:
                    w = image.get_width() * resize
                    h = image.get_height() * resize
                    resize = (w, h)

                image = pygame.transform.scale(image, resize)

            frames.append(image)

        Assets.__storage[name] = frames

    @staticmethod
    def get(asset_name):
        return Assets.__storage.get(asset_name)
