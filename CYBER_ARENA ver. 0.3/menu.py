# menu.py
import pygame
import sys
from settings import Settings
from ui import Button, CyberText

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        
        # Анимация
        self.time = 0
        
    def draw_background(self):
        """Рисует киберпанк фон с эффектом матрицы"""
        self.screen.fill(self.settings.CYBER_BLACK)
        
        # Рисуем линии как в матрице
        for i in range(0, self.settings.screen_width, 30):
            x = i + (self.time % 30)
            alpha = (pygame.time.get_ticks() // 100 + i) % 255
            color = (0, min(255, alpha // 2), 0)
            pygame.draw.line(self.screen, color, (x, 0), (x, self.settings.screen_height), 1)
            
        self.time += 1
        
    def main_menu(self):
        while True:
            self.clock.tick(self.settings.FPS)
            self.draw_background()
            
            # Заголовок (автоматически определит кириллицу)
            title = CyberText("CYBER ARENA", 74, self.settings.CYBER_BLUE, glow=True)
            title_rect = title.get_rect(center=(self.settings.screen_width // 2, 100))
            title.draw(self.screen, title_rect.topleft)
            
            # Подзаголовок с кириллицей
            subtitle = CyberText("ПРОТОКОЛ ВИРУС", 36, self.settings.CYBER_PINK, 
                                use_cyrillic=True)
            subtitle_rect = subtitle.get_rect(center=(self.settings.screen_width // 2, 170))
            subtitle.draw(self.screen, subtitle_rect.topleft)
            
            # Кнопки с автоматическим определением языка
            play_button = Button(self.settings.screen_width // 2, 300, 
                                "> ИНИЦИАЛИЗИРОВАТЬ <", 36)
            settings_button = Button(self.settings.screen_width // 2, 400,
                                   "> НАСТРОЙКИ <", 36)
            exit_button = Button(self.settings.screen_width // 2, 500,
                               "> ВЫХОД <", 36)
            
            # Обработка событий...
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.is_clicked(event.pos):
                        return "play"
                    elif settings_button.is_clicked(event.pos):
                        return "settings"
                    elif exit_button.is_clicked(event.pos):
                        pygame.quit()
                        sys.exit()
                        
            play_button.draw(self.screen)
            settings_button.draw(self.screen)
            exit_button.draw(self.screen)
            
            pygame.display.flip()
            
    def settings_menu(self):
        while True:
            self.clock.tick(self.settings.FPS)
            self.draw_background()
            
            # Заголовок
            title = CyberText("НАСТРОЙКИ СИСТЕМЫ", 50, self.settings.CYBER_GREEN)
            title_rect = title.get_rect(center=(self.settings.screen_width // 2, 80))
            title.draw(self.screen, title_rect.topleft)
            
            # Параметры разрешения
            resolutions = [(1024, 768), (1280, 720), (1920, 1080)]
            current_res = f"{self.settings.screen_width} x {self.settings.screen_height}"
            
            res_text = CyberText(f"РАЗРЕШЕНИЕ: {current_res}", 36, self.settings.CYBER_BLUE)
            res_rect = res_text.get_rect(center=(self.settings.screen_width // 2, 200))
            res_text.draw(self.screen, res_rect.topleft)
            
            # Текстовые кнопки
            prev_text = CyberText("<", 50, self.settings.CYBER_PURPLE)
            prev_rect = prev_text.get_rect(center=(self.settings.screen_width // 2 - 150, 280))
            
            next_text = CyberText(">", 50, self.settings.CYBER_PURPLE)
            next_rect = next_text.get_rect(center=(self.settings.screen_width // 2 + 150, 280))
            
            back_text = CyberText("> НАЗАД <", 50, self.settings.CYBER_PINK)
            back_rect = back_text.get_rect(center=(self.settings.screen_width // 2, 500))
            
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_rect.collidepoint(event.pos):
                        self.settings.save_settings()
                        return
                    elif prev_rect.collidepoint(event.pos):
                        current_index = 0
                        for i, res in enumerate(resolutions):
                            if res[0] == self.settings.screen_width and res[1] == self.settings.screen_height:
                                current_index = i
                                break
                        new_index = (current_index - 1) % len(resolutions)
                        self.settings.current["screen_width"] = resolutions[new_index][0]
                        self.settings.current["screen_height"] = resolutions[new_index][1]
                    elif next_rect.collidepoint(event.pos):
                        current_index = 0
                        for i, res in enumerate(resolutions):
                            if res[0] == self.settings.screen_width and res[1] == self.settings.screen_height:
                                current_index = i
                                break
                        new_index = (current_index + 1) % len(resolutions)
                        self.settings.current["screen_width"] = resolutions[new_index][0]
                        self.settings.current["screen_height"] = resolutions[new_index][1]
            
            # Отрисовка
            prev_text.draw(self.screen, prev_rect.topleft)
            next_text.draw(self.screen, next_rect.topleft)
            back_text.draw(self.screen, back_rect.topleft)
            
            pygame.display.flip()