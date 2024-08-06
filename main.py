import pygame
import random
from image import load_image
from OtherSprites import Sprite, EnemyShips, Particle
from  gloabal_parametrs import param



def draw_score(screen):
    font = pygame.font.Font(None, 50)
    text = font.render(f"SCORE: {param.get_score()}", True, (100, 255, 10))
    text_x = width - text.get_width()
    text_y = 0

    screen.blit(text, (text_x, text_y))


class Ship(Sprite):
    columns = 4
    rows = 1
    image = load_image('ship.png')

    def __init__(self, x: int, y: int):
        """Конструктор

        Args:
            x int: коррдината размещения корабля
            y int: коррдината размещения корабля
        """
        super().__init__(all_sprites, ship_group)
        self.frames = [] # список со всеми, нарезанными спрайтами
        self.cut_sheet(Ship.image, Ship.columns, Ship.rows)

        self.cur_frame = 0 # номер первого спрайта
        self.image = self.frames[self.cur_frame] # присваивание картинки
        self.rect = self.rect.move(x, y) # размещение на экране

        # координаты спрайта
        self.x = x
        self.y = y

        # скорость корабля
        self.v = 100

        self.time = pygame.time.get_ticks()

        # ФЛАГИ
        self.flag = {pygame.K_LEFT: False, pygame.K_RIGHT: False, pygame.K_UP: False, pygame.K_DOWN: False}
 
    def is_live(self):
        """Проверка на кол-во жизней

        Returns:
            bool: True - корабль потерпел крушение, False - еще жив
        """
        return self.cur_frame == Ship.columns - 1
 
    def update(self, *args):
        FPS = param.FPS

        # Проверка на столкновение нашего корабля и корабля противника
        sprite = pygame.sprite.spritecollideany(self, enemy_group)
        if sprite:
            # если произошло столкновение, то отнимаем жизнь и 5 очков
            self.cur_frame += 1
            if self.cur_frame < Ship.columns - 1:
                self.image = self.frames[self.cur_frame] # меняем картинку спрайта на более побитую
                param.set_score(-5)
            else:
                self.kill() # если закончились жизни, корабль погибает
                param.set_score(-param.get_score()) # счет равен 0
            sprite.kill()
        
        
        # ЗДЕСЬ ПИШЕМ ЛОГИКУ ДВИЖЕНИЯ КОРАБЛЯ
        
        # ЗДЕСЬ ЛОГИКУ ПОЯВЛЕНИЯ ПУЛЬ

            
        
            


def main():
    running = True
    times = pygame.time.get_ticks()
    while running: 
        if ship.is_live():
            return True
        # внутри игрового цикла ещё один цикл
        # приема и обработки сообщений
        screen.blit(bg, (0, 0)) # отображение фона на экране
        
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
        enemy_group.update(particle_group)
        ship_group.update()
        particle_group.update()
        draw_score(screen)
		# обновление экрана
        pygame.display.flip()
        time.tick(param.FPS)

        if len(enemy_group.sprites()) <= N // 2 or abs(times - pygame.time.get_ticks()) >= 3000:
            for x, y in [(random.randrange(1, width), -25) for _ in range(N)]:
                EnemyShips(x, y, all_sprites, enemy_group)
            times = pygame.time.get_ticks()
    


if __name__ == '__main__':
    running = True
    
    # цикл для вечной игры
    while running:
        pygame.init()

        param.set_score(-param.get_score())
        N = 5
        time = pygame.time.Clock()
        all_sprites = pygame.sprite.Group()
        enemy_group = pygame.sprite.Group()
        particle_group = pygame.sprite.Group()
        ship_group = pygame.sprite.Group()

        

        size = width, height = 500, 600
        bg = pygame.transform.scale(load_image('bg.jpg'), size)
        screen = pygame.display.set_mode(size)

        for x, y in [(random.randrange(1, width), -25) for _ in range(N)]:
            EnemyShips(x, y, all_sprites, enemy_group)

        ship = Ship(width // 2, height - param.SIZE_SPRITES)
        running = main()
    