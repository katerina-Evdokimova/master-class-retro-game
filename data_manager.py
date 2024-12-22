import os
import sys
import pygame


class DataManager:
    def __init__(self):
        pass

    def load_image(self, name, alpha=False):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()

        image = pygame.image.load(fullname)

        # if alpha:
        #     image = image.convert_alpha()
        # else:
        #     image = image.convert()

        return image


data_manager = DataManager()
