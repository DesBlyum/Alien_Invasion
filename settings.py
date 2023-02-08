class Settings():
    """Класс для хранения всех настроек игры Инопланетное вторжение."""

    def __init__(self):
        """Инициализируем настройки игры"""
        # параметры экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (100, 230, 230)
        #self.bg_color = (0, 0, 0)
        self.ship_speed = 1.5
        # параметры снаряда
        self.bullet_speed = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)