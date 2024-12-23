import os
import sys
import pygame
from parameters import params


class DataManager:
    def __init__(self):
        self.ship = {
            'columns': 4,
            'rows': 1,
            'path': 'ship.png',
            'frames': []
        }

        self.ship_enemy = {
            'columns': 4,
            'rows': 1,
            'path': 'ship_enemy.png',
            'frames': []
        }

        self.particle = {
            'columns': 1,
            'rows': 3,
            'path': 'laser_bullets.png',
            'frames': []
        }

        self.background = self.load_image('background.png')
        self.ship['frames'] = self.cut_sheet(self.load_image(self.ship['path'], True),
                                             self.ship['columns'], self.ship['rows'])
        self.ship_enemy['frames'] = self.cut_sheet(self.load_image(self.ship_enemy['path'], True),
                                                   self.ship_enemy['columns'], self.ship_enemy['rows'])
        self.particle['frames'] = self.cut_sheet(self.load_image(self.particle['path'], True),
                                                 self.particle['columns'], self.particle['rows'])

    def load_image(self, name, alpha=False):
        fullname = os.path.join('data', name)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{fullname}' не найден")
            sys.exit()

        image = pygame.image.load(fullname)

        if alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()

        return image

    def cut_sheet(self, sheet, columns, rows):
        '0, 0 - координаты левого верхнего угла'
        'sheet.get_width() // columns, sheet.get_height() // rows - ширина и высота'
        # создаем прямоугольник
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        # цикл для создания готовых фрэймов наших спрайтов,
        # те обрезаем каждую картинку и создаем из готовых изображений список для дальнейшего использования.
        frames = []
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)),
                                                     (params.SIZE_SPRITES, params.SIZE_SPRITES)))
        return frames

pygame.init()
screen = pygame.display.set_mode((1, 1))
data_manager = DataManager()
