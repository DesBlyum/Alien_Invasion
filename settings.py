class Settings():
    """Класс для хранения всех настроек игры Инопланетное вторжение."""

    def __init__(self):
        """Инициализируем статические настройки игры"""
        # параметры экрана
        self.screen_width = 1080
        self.screen_height = 800
        self.bg_color = (100, 230, 230) #self.bg_color = (0, 0, 0)
        # настройки корабля
        self.ship_limit = 3
        self.ship_speed = 1
        # параметры снаряда
        self.bullet_speed = 1.5
        self.bullet_width = 8
        self.bullet_height = 30
        self.bullet_color = (255, 0, 0)
        self.bullet_allowed = 3
        # настройки пришельцев
        self.alien_speed = 0.5
        self.fleet_drop_speed = 10
        self.fleet_direction = 0.3 # +1 обозначает движение вправо; a -1 - влево

        #Темп ускорения игры
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализация динамических настроек"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1.0

        self.fleet_direction = 1 # 1 - движение вправо, -1 влево

    def increase_speed(self):
        #Увеличиваем настройки скорости
        self.ship_speed_factor *=self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
