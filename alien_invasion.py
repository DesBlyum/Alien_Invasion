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
            # Отсеживание событий клавиатуры и мыши.
            for evant in pygame.event.get():
                if evant.type == pygame.QUIT:
                    sys.exit()
            # при каждом проходе цикла перерисовываеться экран
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()

            # Отображение последнего прорисованного экрана.
            pygame.display.flip()

if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
