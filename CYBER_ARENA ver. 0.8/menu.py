# menu.py
import pygame
import sys
from settings import Settings
from ui import Button, CyberText
from matrix_effect import MatrixEffect

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        
        # Инициализация матричного эффекта
        self.matrix_effect = MatrixEffect(self.settings.screen_width, 
                                          self.settings.screen_height)
        
        # Шрифты для заголовков
        self.title_font = pygame.font.Font(None, 150)
        self.subtitle_font = pygame.font.Font(None, 80)
        
        # Цвета
        self.bg_color = (0, 0, 0)
        self.title_color = (0, 255, 0)
        
    def draw_background(self):
        """Рисует фон с матричным эффектом"""
        self.screen.fill(self.bg_color)
        self.matrix_effect.update()
        self.matrix_effect.draw(self.screen)
        
    def draw_title(self):
        """Рисует анимированный заголовок"""
        # Эффект пульсации для заголовка
        pulse = (pygame.time.get_ticks() % 1000) / 1000
        alpha = int(150 + pulse * 105)
        
        # Основной заголовок
        title_text = "CYBER ARENA"
        title_surface = self.title_font.render(title_text, True, self.title_color)
        title_surface.set_alpha(alpha)
        title_rect = title_surface.get_rect(center=(self.settings.screen_width // 2, 150))
        self.screen.blit(title_surface, title_rect)
        
        # Эффект глитча
        if pygame.time.get_ticks() % 3000 < 100:
            glitch_offset = 3
            glitch_surface = self.title_font.render(title_text, True, (0, 255, 255))
            glitch_surface.set_alpha(100)
            self.screen.blit(glitch_surface, 
                           (title_rect.x + glitch_offset, title_rect.y))
            
        # Подзаголовок
        subtitle_text = ">>> ВИРУСНАЯ АТАКА <<<"
        subtitle_surface = self.subtitle_font.render(subtitle_text, True, (0, 200, 0))
        subtitle_rect = subtitle_surface.get_rect(center=(self.settings.screen_width // 2, 280))
        self.screen.blit(subtitle_surface, subtitle_rect)
        
    def main_menu(self):
        while True:
            self.clock.tick(self.settings.FPS)
            self.draw_background()
            self.draw_title()
            
            # Кнопки меню
            play_button = Button(self.settings.screen_width // 2, 400, 
                                "> ИНИЦИАЛИЗАЦИЯ <", 60,
                                (0, 200, 0), (0, 255, 255))
            settings_button = Button(self.settings.screen_width // 2, 550,
                                   "> НАСТРОЙКИ <", 60,
                                   (0, 200, 0), (0, 255, 255))
            exit_button = Button(self.settings.screen_width // 2, 700,
                               "> ВЫХОД <", 60,
                               (0, 200, 0), (0, 255, 255))
            
            # Обработка событий
            mouse_pos = pygame.mouse.get_pos()
            
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
                        
            # Обновление кнопок
            play_button.update(mouse_pos)
            settings_button.update(mouse_pos)
            exit_button.update(mouse_pos)
            
            # Отрисовка кнопок
            play_button.draw(self.screen)
            settings_button.draw(self.screen)
            exit_button.draw(self.screen)
            
            pygame.display.flip()
            
    def settings_menu(self):
        from sound_manager import SoundManager
        
        # Временно отключаем эффект для настроек
        self.matrix_effect.clear()
        
        while True:
            self.clock.tick(self.settings.FPS)
            self.draw_background()
            
            # Заголовок
            title = CyberText("НАСТРОЙКИ СИСТЕМЫ", 80, (0, 255, 0))
            title_rect = title.get_rect(center=(self.settings.screen_width // 2, 120))
            title.draw(self.screen, title_rect.topleft)
            
            # Параметры разрешения
            resolutions = [(1024, 768), (1280, 720), (1920, 1080)]
            current_res = f"{self.settings.screen_width} x {self.settings.screen_height}"
            
            res_text = CyberText(f"РАЗРЕШЕНИЕ: {current_res}", 40, (0, 200, 0))
            res_rect = res_text.get_rect(center=(self.settings.screen_width // 2, 240))
            res_text.draw(self.screen, res_rect.topleft)
            
            # Кнопки разрешения
            prev_res = Button(self.settings.screen_width // 2 - 230, 240, "<", 40,
                             (0, 200, 0), (0, 255, 255))
            next_res = Button(self.settings.screen_width // 2 + 230, 240, ">", 40,
                             (0, 200, 0), (0, 255, 255))
            
            # Настройки громкости
            music_vol_text = CyberText(f"МУЗЫКА: {int(self.settings.music_volume * 100)}%", 
                                       40, (0, 200, 0))
            music_vol_rect = music_vol_text.get_rect(center=(self.settings.screen_width // 2, 360))
            music_vol_text.draw(self.screen, music_vol_rect.topleft)
            
            music_down = Button(self.settings.screen_width // 2 - 140, 360, "-", 60,
                               (0, 200, 0), (0, 255, 255))
            music_up = Button(self.settings.screen_width // 2 + 140, 360, "+", 60,
                             (0, 200, 0), (0, 255, 255))
            
            sfx_vol_text = CyberText(f"ЭФФЕКТЫ: {int(self.settings.sound_volume * 100)}%", 
                                     40, (0, 200, 0))
            sfx_vol_rect = sfx_vol_text.get_rect(center=(self.settings.screen_width // 2, 460))
            sfx_vol_text.draw(self.screen, sfx_vol_rect.topleft)
            
            sfx_down = Button(self.settings.screen_width // 2 - 140, 460, "-", 60,
                             (0, 200, 0), (0, 255, 255))
            sfx_up = Button(self.settings.screen_width // 2 + 140, 460, "+", 60,
                           (0, 200, 0), (0, 255, 255))
            
            back_button = Button(self.settings.screen_width // 2, 640,
                               "> НАЗАД <", 60,
                               (0, 200, 0), (0, 255, 255))
            
            # Обработка событий
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(event.pos):
                        self.settings.save_settings()
                        return
                    elif prev_res.is_clicked(event.pos):
                        current_index = 0
                        for i, res in enumerate(resolutions):
                            if res[0] == self.settings.screen_width and res[1] == self.settings.screen_height:
                                current_index = i
                                break
                        new_index = (current_index - 1) % len(resolutions)
                        self.settings.current["screen_width"] = resolutions[new_index][0]
                        self.settings.current["screen_height"] = resolutions[new_index][1]
                    elif next_res.is_clicked(event.pos):
                        current_index = 0
                        for i, res in enumerate(resolutions):
                            if res[0] == self.settings.screen_width and res[1] == self.settings.screen_height:
                                current_index = i
                                break
                        new_index = (current_index + 1) % len(resolutions)
                        self.settings.current["screen_width"] = resolutions[new_index][0]
                        self.settings.current["screen_height"] = resolutions[new_index][1]
                    elif music_down.is_clicked(event.pos):
                        self.settings.current["music_volume"] = max(0, self.settings.music_volume - 0.1)
                    elif music_up.is_clicked(event.pos):
                        self.settings.current["music_volume"] = min(1, self.settings.music_volume + 0.1)
                    elif sfx_down.is_clicked(event.pos):
                        self.settings.current["sound_volume"] = max(0, self.settings.sound_volume - 0.1)
                    elif sfx_up.is_clicked(event.pos):
                        self.settings.current["sound_volume"] = min(1, self.settings.sound_volume + 0.1)
            
            # Обновление кнопок
            prev_res.update(mouse_pos)
            next_res.update(mouse_pos)
            music_down.update(mouse_pos)
            music_up.update(mouse_pos)
            sfx_down.update(mouse_pos)
            sfx_up.update(mouse_pos)
            back_button.update(mouse_pos)
            
            # Отрисовка кнопок
            prev_res.draw(self.screen)
            next_res.draw(self.screen)
            music_down.draw(self.screen)
            music_up.draw(self.screen)
            sfx_down.draw(self.screen)
            sfx_up.draw(self.screen)
            back_button.draw(self.screen)
            
            pygame.display.flip()