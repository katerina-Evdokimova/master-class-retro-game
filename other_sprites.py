import pygame
from data_manager import data_manager
from parameters import params


class Sprite(pygame.sprite.Sprite):
    pass


class Particle(pygame.sprite.Sprite):
    """
    Класс пуль
    """

    def __init__(self, x: int, y: int, all_sprites, particle_group):
        """Конструктор

        Args:
            x int: коррдината размещения корабля
            y int: коррдината размещения корабля
        """
        super().__init__(all_sprites, particle_group)
        self.frames = data_manager.particle['frames']
        self.columns = data_manager.particle['columns']
        self.rows = data_manager.particle['rows']
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.pos = [x, y]

        # скорость движения пуль
        self.v = 5

        self.r = params.SIZE_SPRITES + 20
        self.time = 0

    def update(self) -> None:
        self.time += 1
        self.pos[1] -= self.v + params.get_boost()

        if self.pos[1] < 0:
            self.kill()

        self.rect = self.image.get_rect().move(
            self.pos[0], self.pos[1]
        )

        if self.time >= 30 and self.cur_frame < self.rows - 1:
            self.cur_frame += 1
            self.image = self.frames[self.cur_frame]
            self.time = 0


class ShipEnemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, all_sprites, enemy_group):
        """Конструктор

        Args:
            x int: коррдината размещения корабля
            y int: коррдината размещения корабля
        """
        super().__init__(all_sprites, enemy_group)
        self.frames = data_manager.ship_enemy['frames']
        self.columns = data_manager.ship_enemy['columns']
        self.rows = data_manager.ship_enemy['rows']
        self.cur_frame = self.columns - 1
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.pos = [x, y]
        # скорость движение врагов
        self.v = 1

    def update(self, particle_group):
        # self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        # self.image = self.frames[self.cur_frame]
        self.pos[1] += self.v + params.get_boost()
        self.rect = self.image.get_rect().move(
            self.pos[0], self.pos[1]
        )

        if self.pos[1] > params.get_height():
            self.kill()

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
