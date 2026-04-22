# statistics_menu.py
import pygame
import sys
from hex_background import HexBackground, GlitchText
from localization import localization
from statistics import statistics

class StatisticsMenu:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        
        # Создаем фон
        self.stats_bg = HexBackground(settings.screen_width, settings.screen_height)
        
        # Шрифты
        self.font = pygame.font.Font(None, 28)
        
        # Цвета
        self.neon_red = (255, 50, 50)
        self.neon_cyan = (0, 255, 255)
        self.neon_green = (0, 255, 0)
        
    def update_background(self):
        """Обновляет фон для нового размера экрана"""
        self.stats_bg.screen_width = self.settings.screen_width
        self.stats_bg.screen_height = self.settings.screen_height
        self.stats_bg.hexes.clear()
        self.stats_bg.generate_hexes()
        
    def draw_statistics(self):
        """Рисует всю статистику"""
        stats = statistics.get_stats()
        
        # Заголовок
        title = GlitchText("statistics_title",
                          self.settings.screen_width // 2, 60, 50,
                          self.neon_cyan, True)
        title.draw(self.screen)
        
        # Основные параметры
        stats_y = 120
        stats_x = 80
        col2_x = self.settings.screen_width // 2 + 50
        
        # Левая колонка
        left_stats = [
            ("stat_max_wave", stats["max_wave"]),
            ("stat_max_score", stats["max_score"]),
            ("stat_max_kills", stats["max_kills_per_session"]),
            ("stat_total_kills", stats["total_kills"]),
        ]
        
        for i, (key, value) in enumerate(left_stats):
            text = GlitchText(key, stats_x + 150, stats_y + i * 40, 28,
                             self.neon_red, True)
            text.draw(self.screen)
            
            value_text = GlitchText(str(value), stats_x + 360, stats_y + i * 40, 28,
                                   self.neon_cyan, False)
            value_text.draw(self.screen)
            
        # Правая колонка - убийства по типам
        right_stats = [
            ("stat_kills_trojan", stats["kills_trojan"]),
            ("stat_kills_worm", stats["kills_worm"]),
            ("stat_kills_ransomware", stats["kills_ransomware"]),
        ]
        
        for i, (key, value) in enumerate(right_stats):
            text = GlitchText(key, col2_x + 120, stats_y + i * 40, 28,
                             self.neon_red, True)
            text.draw(self.screen)
            
            value_text = GlitchText(str(value), col2_x + 330, stats_y + i * 40, 28,
                                   self.neon_cyan, False)
            value_text.draw(self.screen)
            
        # Урон по оружию
        damage_y = 300
        damage_title = GlitchText("stat_damage_title",
                                 self.settings.screen_width // 2, damage_y, 32,
                                 self.neon_green, True)
        damage_title.draw(self.screen)
        
        damage_stats = [
            ("weapon_standard", stats["damage_standard"]),
            ("weapon_rapid", stats["damage_rapid"]),
            ("weapon_shotgun", stats["damage_shotgun"]),
            ("weapon_laser", stats["damage_laser"]),
        ]
        
        damage_x = self.settings.screen_width // 2 - 200
        for i, (key, value) in enumerate(damage_stats):
            text = GlitchText(key, damage_x, damage_y + 40 + i * 35, 24,
                             self.neon_cyan, True)
            text.draw(self.screen)
            
            value_text = GlitchText(str(value), damage_x + 250, damage_y + 40 + i * 35, 24,
                                   self.neon_green, False)
            value_text.draw(self.screen)
            
        # Кнопки
        reset_button = GlitchText("stat_reset",
                                 self.settings.screen_width // 2 - 100, 
                                 self.settings.screen_height - 80, 36,
                                 self.neon_red, True)
        
        back_button = GlitchText("back",
                                self.settings.screen_width // 2 + 100, 
                                self.settings.screen_height - 80, 36,
                                self.neon_cyan, True)
        
        return reset_button, back_button
        
    def show(self):
        """Показывает страницу статистики"""
        self.update_background()
        
        while True:
            self.stats_bg.update()
            self.stats_bg.draw(self.screen)
            
            reset_button, back_button = self.draw_statistics()
            
            mouse_pos = pygame.mouse.get_pos()
            reset_button.update(mouse_pos)
            back_button.update(mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if reset_button.is_clicked(event.pos):
                        # Подтверждение сброса
                        statistics.reset_stats()
                        return  # Возвращаемся в меню после сброса
                    elif back_button.is_clicked(event.pos):
                        return
                        
            reset_button.draw(self.screen)
            back_button.draw(self.screen)
            
            # Декоративная рамка
            border_rect = pygame.Rect(50, 30, 
                                     self.settings.screen_width - 100, 
                                     self.settings.screen_height - 60)
            pygame.draw.rect(self.screen, self.neon_red, border_rect, 2)
            pygame.draw.rect(self.screen, self.neon_cyan, border_rect.inflate(-4, -4), 1)
            
            pygame.display.flip()