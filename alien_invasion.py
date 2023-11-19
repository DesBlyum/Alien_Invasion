import sys
import pygame

#from time time import sleep
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats

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

        # Создание экземпляра для хранения игровой статистики.
        self.stats = GameStats(self)

        # назначение цвета фона.
        self.bg_color = (self.settings.bg_color)

        # передача рессурсов(предоставления доступа) в класс Ship объекта screen
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            self.check_events() #отслеживание нажатие клавиш и событий мыши

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets() #обновление позиции снарядов и уничтожение старых снарядов
                self._update_aliens()  # обновление позиции каждого пришельца

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

        # Проверка попадений в пришельцев.
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Обработка коллизии снарядов с пришельцами"""
        # Удаление снарядов и пришельцев, участвующих в коллизии
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """Проверяет достиг ли флот края экрана с последующим обновлением позиций всех пришельцев во флоте"""
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # проверить, добрались ли пришельцы до нижнего края
        self._check_aliens_bottom()

    def _update_screen(self):
        """Обновляет изображение на экране и отображает новый экран"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # Отображение последнего прорисованного экрана.
        pygame.display.flip()

    def _create_fleet(self):
        """Создание флота вторжения"""
        # Создание пришельца и вычисление количества пришельцев в ряду.
        # Интервал м/у соседникми пришельцами равен ширине пришельца.

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        availanle_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = availanle_space_x // (2 * alien_width)

        """Определение кол-ва рядов, помещяющихся на экране."""
        ship_height = self.ship.rect.height
        availanle_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = availanle_space_y // (2 * alien_height)

        # Создание флота вторжения
        for row_number in range(number_rows):
            # Создание первого ряда пришельцев.
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создание прищельца и размещение его в ряду."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем"""
        if self.stats.ship_left > 0:
            # Уменьшение ships_left
            self.stats.ship_left -= 1

            # Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение коробля в центре
            self._create_fleet()
            self.ship.center_ship()

            # Пауза
            #sleep(0.5)
        else:
            self.stats.game_active = False
            # Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()
            print("Конец игры!")


    def _check_aliens_bottom(self):
        """Проверяет добрались ли пришельцы до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # происходит то же, что и при столкновении с кораблем
                self._ship_hit()
                break

if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
