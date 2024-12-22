import pygame
from data_manager import data_manager
from parameters import params


class Sprite(pygame.sprite.Sprite):
    def cut_sheet(self, sheet, columns, rows):
        """
 
        :param sheet:
        :param columns:
        :param rows:
        :return:
        """
        '0, 0 - координаты левого верхнего угла'
        'sheet.get_width() // columns, sheet.get_height() // rows - ширина и высота'
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)  # создаем прямоугольник
        # цикл для создания готовых фрэймов наших спрайтов,
        # те обрезаем каждую картинку и создаем из готовых изображений список для дальнейшего использования.
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)),
                                                          (params.SIZE_SPRITES, params.SIZE_SPRITES)))


class Particle(Sprite):
    """
    Класс пуль
    """
    columns = 1
    rows = 3
    image = data_manager.load_image('laser_bullets.png')

    def __init__(self, x: int, y: int, all_sprites, particle_group):
        """Конструктор

        Args:
            x int: коррдината размещения корабля
            y int: коррдината размещения корабля
        """
        super().__init__(all_sprites, particle_group)
        self.frames = []
        self.cut_sheet(Particle.image, Particle.columns, Particle.rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.pos = [x, y]
        self.start = pygame.time.get_ticks()

        # скорость движения пуль
        self.v = 90

        self.r = params.SIZE_SPRITES + 20
        self.time = pygame.time.get_ticks()

    def update(self) -> None:
        self.pos[1] -= self.v / params.FPS

        self.rect = self.image.get_rect().move(
            self.pos[0], self.pos[1]
        )

        # каждые 20 очков идет увеличение скорости
        if not (params.get_score() + 5) % 20:
            self.v += 1

        if abs(self.time - pygame.time.get_ticks()) >= 500 and self.cur_frame < Particle.rows - 1:
            self.cur_frame += 1
            self.image = self.frames[self.cur_frame]
            self.time = pygame.time.get_ticks()


class EnemyShips(pygame.sprite.Sprite):
    columns = 4
    rows = 1
    image = data_manager.load_image('ship_enemy.png')

    def __init__(self, x: int, y: int, all_sprites, enemy_group):
        """Конструктор

        Args:
            x int: коррдината размещения корабля
            y int: коррдината размещения корабля
        """
        super().__init__(all_sprites, enemy_group)
        self.frames = []
        self.cut_sheet(EnemyShips.image, EnemyShips.columns, EnemyShips.rows)
        self.cur_frame = EnemyShips.columns - 1
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.pos = [x, y]
        # скорость движение врагов
        self.v = 10

    def cut_sheet(self, sheet, columns, rows):
        """
 
        :param sheet:
        :param columns:
        :param rows:
        :return:
        """
        '0, 0 - координаты левого верхнего угла'
        'sheet.get_width() // columns, sheet.get_height() // rows - ширина и высота'
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)  # создаем прямоугольник
        # цикл для создания готовых фрэймов наших спрайтов,
        # те обрезаем каждую картинку и создаем из готовых изображений список для дальнейшего использования.
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)),
                                                          (params.SIZE_SPRITES, params.SIZE_SPRITES)))

    def update(self, particle_group):
        """
        обновление картинки
        :return:
        """
        # self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        # self.image = self.frames[self.cur_frame]
        self.pos[1] += self.v / params.FPS
        self.rect = self.image.get_rect().move(
            self.pos[0], self.pos[1]
        )

        # за каждые 20 очков пользователя, скорость кораблей увеличивается
        if not (params.get_score() + 1) % 20:
            self.v += 1

        sprite = pygame.sprite.spritecollideany(self, particle_group)
        if sprite:
            self.cur_frame -= 1
            if self.cur_frame:
                self.image = self.frames[self.cur_frame]
                params.set_score(1)
                sprite.kill()
            else:
                self.kill()
                params.set_score(5)
                sprite.kill()

    def cut_sheet(self, sheet, columns, rows):
        """
 
        :param sheet:
        :param columns:
        :param rows:
        :return:
        """
        '0, 0 - координаты левого верхнего угла'
        'sheet.get_width() // columns, sheet.get_height() // rows - ширина и высота'
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)  # создаем прямоугольник
        # цикл для создания готовых фрэймов наших спрайтов,
        # те обрезаем каждую картинку и создаем из готовых изображений список для дальнейшего использования.
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(pygame.transform.scale(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)),
                                                          (params.SIZE_SPRITES - 10, params.SIZE_SPRITES - 10)))
