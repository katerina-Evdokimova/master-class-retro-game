import pygame
import random
from data_manager import data_manager
from other_sprites import Sprite, ShipEnemy, Particle
from parameters import params


def draw_score(screen):
    font = pygame.font.Font(None, 50)
    text = font.render(f"SCORE: {params.get_score()}", True, (100, 255, 10))
    text_x = width - text.get_width()
    text_y = 0

    screen.blit(text, (text_x, text_y))


class Ship(Sprite):
    def __init__(self, x: int, y: int):
        """Конструктор

        Args:
            x int: коррдината размещения корабля
            y int: коррдината размещения корабля
        """
        super().__init__(all_sprites, ship_group)
        # список со всеми, нарезанными спрайтами
        self.frames = data_manager.ship['frames']
        self.columns = data_manager.ship['columns']
        self.rows = data_manager.ship['rows']
        self.cur_frame = 0  # номер первого спрайта
        self.image = self.frames[self.cur_frame]  # присваивание картинки
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)  # размещение на экране

        # координаты спрайта
        self.x = x
        self.y = y

        # скорость корабля
        self.v = 1

        self.time = 0

        # ФЛАГИ
        self.flag_up = False
        self.flag_down = False
        self.flag_left = False
        self.flag_right = False

    def is_live(self):
        """Проверка на кол-во жизней

        Returns:
            bool: True - корабль потерпел крушение, False - еще жив
        """
        return self.cur_frame == self.columns - 1

    def update(self, *args, v=0):
        self.v += v
        FPS = params.FPS
        self.time += 1

        # Проверка на столкновение нашего корабля и корабля противника
        sprite = pygame.sprite.spritecollideany(self, enemy_group)
        if sprite:
            # если произошло столкновение, то отнимаем жизнь и 5 очков
            self.cur_frame += 1
            if self.cur_frame < self.columns - 1:
                self.image = self.frames[self.cur_frame]  # меняем картинку спрайта на более побитую
                params.set_score(-5)
            else:
                self.kill()  # если закончились жизни, корабль погибает
                params.set_score(-params.get_score())  # счет равен 0
            sprite.kill()

        # ЗДЕСЬ ПИШЕМ ЛОГИКУ ДВИЖЕНИЯ КОРАБЛЯ
        if args and args[0].type == pygame.KEYDOWN:
            if args[0].key == pygame.K_RIGHT:
                self.flag_right = True
            elif args[0].key == pygame.K_LEFT:
                self.flag_left = True
            elif args[0].key == pygame.K_UP:
                self.flag_up = True
            elif args[0].key == pygame.K_DOWN:
                self.flag_down = True

        if args and args[0].type == pygame.KEYUP:
            if args[0].key == pygame.K_RIGHT:
                self.flag_right = False
            elif args[0].key == pygame.K_LEFT:
                self.flag_left = False
            elif args[0].key == pygame.K_UP:
                self.flag_up = False
            elif args[0].key == pygame.K_DOWN:
                self.flag_down = False

        if self.flag_left:
            self.x -= self.v
        if self.flag_down:
            self.y += self.v
        if self.flag_right:
            self.x += self.v
        if self.flag_up:
            self.y -= self.v

        if self.y < 0:
            self.y = 0
        elif self.y > height - self.rect.height:
            self.y = height - self.rect.height
        elif self.x < 0:
            self.x = 0
        elif self.x > width - self.rect.width:
            self.x = width - self.rect.width

        self.rect = self.image.get_rect().move(
            self.x, self.y
        )

        # ЗДЕСЬ ЛОГИКУ ПОЯВЛЕНИЯ ПУЛЬ
        if self.time >= 30:
            Particle(self.x, self.y - params.SIZE_SPRITES // 2, all_sprites, particle_group)
            self.time = 0


def main():
    running = True
    clock = pygame.time.Clock()
    time = 0
    while running:
        time += 1
        if ship.is_live():
            return True
        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        screen.blit(bg, (0, 0))  # отображение фона на экране

        for event in pygame.event.get():
            # при закрытии окна

            if event.type == pygame.QUIT:
                return False
            ship_group.update(event)

        # отрисовка и изменение свойств объектов
        enemy_group.draw(screen)
        particle_group.draw(screen)
        all_sprites.draw(screen)
        ship_group.draw(screen)

        # каждые 20 очков идет увеличение скорости
        v = 0
        if not (params.get_score() + 1) % 20:
            v = 0.1

        enemy_group.update(particle_group, v)
        ship_group.update(v=v)
        particle_group.update(v=v)
        draw_score(screen)

        # обновление экрана
        pygame.display.flip()
        clock.tick(params.FPS)

        if len(enemy_group.sprites()) <= N // 2 or time >= 180:
            for x, y in [(random.randrange(1, width), -25) for _ in range(N)]:
                ShipEnemy(x, y, all_sprites, enemy_group)
            time = 0


if __name__ == '__main__':
    # цикл для вечной игры
    pygame.init()

    params.set_score(-params.get_score())
    N = 5
    time = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    particle_group = pygame.sprite.Group()
    ship_group = pygame.sprite.Group()

    size = width, height = 500, 600
    screen = pygame.display.set_mode(size)
    bg = pygame.transform.scale(data_manager.background, size)

    for x, y in [(random.randrange(1, width), -25) for _ in range(N)]:
        ShipEnemy(x, y, all_sprites, enemy_group)

    ship = Ship(width // 2, height - params.SIZE_SPRITES)
    main()
