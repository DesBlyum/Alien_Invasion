import sys
import pygame

class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""
    def __init__(self):
        """Иницилизирует игру и создает игровые ресурсы."""
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Инопланетное вторжение")

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            # Отсеживание событий клавиатуры и мыши.
            for evant in pygame.event.get():
                if evant.type == pygame.QUIT:
                    sys.exit()
            #Отображение последнего прорисованного экрана.
            pygame.display.flip()

if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
