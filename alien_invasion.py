import sys
import pygame

from settings import Settings
from ship import Ship

class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""
    def __init__(self):
        """Иницилизирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Инопланетное вторжение (покаритель космоса - МАРКа)")

        # назначение цвета фона.
        self.bg_color = (self.settings.bg_color)

        # передача рессурсов(предоставления доступа) в класс Ship объекта screen
        self.ship = Ship(self)

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self.check_events() #отслеживание нажатие клавиш и событий мыши
            self.ship.update()
            self._update_screen() #при каждом проходе цикла перерисовываеться экран

    def check_events(self):
        """Обрабатывает нажатие клавиш и события мыши"""
        for evant in pygame.event.get():
            if evant.type == pygame.QUIT:
                sys.exit()
            elif evant.type == pygame.KEYDOWN:
                if evant.key == pygame.K_RIGHT:
                    #переместить корабль вправо пока нажата клафища
                    self.ship.moving_right = True
                elif evant.key == pygame.K_LEFT:
                    # переместить корабль вправо пока нажата клафища
                    self.ship.moving_left = True
            elif evant.type == pygame.KEYUP:
                if evant.key == pygame.K_RIGHT:
                    #клавища вправо - отжали, более не перемещаем корабль
                    self.ship.moving_right = False
                elif evant.key == pygame.K_LEFT:
                    #клавища вправо - отжали, более не перемещаем корабль
                    self.ship.moving_left = False

    def _update_screen(self):
        """Обновляет изображение на экране и отображает новый экран"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
