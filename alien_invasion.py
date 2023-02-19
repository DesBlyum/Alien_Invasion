import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""
    def __init__(self):
        """Иницилизирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        """self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height"""

        pygame.display.set_caption("Инопланетное вторжение (Охотник на прешельцев!)")

        # назначение цвета фона.
        self.bg_color = (self.settings.bg_color)

        # передача рессурсов(предоставления доступа) в класс Ship объекта screen
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self.check_events() #отслеживание нажатие клавиш и событий мыши
            self.ship.update()
            self._update_bullets() #обновление позиции снарядов и уничтожение старых снарядов
            self._update_screen() #при каждом проходе цикла перерисовываеться экран

    def check_events(self):
        """Обрабатывает нажатие клавиш и события мыши"""
        for evant in pygame.event.get():
            if evant.type == pygame.QUIT:
                sys.exit()
            elif evant.type == pygame.KEYDOWN:
                self._check_keydown_evants(evant)
            elif evant.type == pygame.KEYUP:
                self._check_keyup_evants(evant)

    def _check_keydown_evants(self, evant):
        """Реагирует на нажатие клавиш"""
        if evant.key == pygame.K_RIGHT:
            # переместить корабль вправо пока нажата клафища
            self.ship.moving_right = True
        elif evant.key == pygame.K_LEFT:
            # переместить корабль влево пока нажата клафища
            self.ship.moving_left = True
        elif evant.key == pygame.K_ESCAPE:
            sys.exit()
        elif evant.key == pygame.K_SPACE:
            self._fire_bullet()
        elif evant.key == pygame.K_UP:
            # переместить корабль вверх
            self.ship.moving_up = True
        elif evant.key == pygame.K_DOWN:
            # переместить корабль вниз
            self.ship.moving_down = True

    def _check_keyup_evants(self, evant):
        """Реагирует на отпускание клавиш"""
        if evant.key == pygame.K_RIGHT:
            # клавища вправо - отжали, более не перемещаем корабль
            self.ship.moving_right = False
        elif evant.key == pygame.K_LEFT:
            # клавища влево - отжали, более не перемещаем корабль
            self.ship.moving_left = False
        elif evant.key == pygame.K_UP:
            # клавища вверх - отжали, более не перемещаем корабль
            self.ship.moving_up = False
        elif evant.key == pygame.K_DOWN:
            # клавища вниз - отжали, более не перемещаем корабль
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновление позиции снарядов и уничтожение старых снарядов."""
        # Обновление позиций снарядов.
        self.bullets.update()

        # Удаление снарядов, вышедших за край экрана
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets)) # проверка обнуления кол-ва снарядов на экране

    def _update_screen(self):
        """Обновляет изображение на экране и отображает новый экран"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
