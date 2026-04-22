# pause_menu.py
import pygame
import sys
from hex_background import HexBackground, GlitchText
from localization import localization

class PauseMenu:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        
        # Создаем фон для паузы
        self.pause_bg = HexBackground(settings.screen_width, settings.screen_height)
        
        # Затемнение экрана
        self.overlay = pygame.Surface((settings.screen_width, settings.screen_height))
        self.overlay.set_alpha(180)
        self.overlay.fill((0, 0, 0))
        
        # Цвета
        self.neon_red = (255, 50, 50)
        self.neon_cyan = (0, 255, 255)
        self.neon_green = (0, 255, 0)
        
    def update_background(self):
        """Обновляет фон для нового размера экрана"""
        self.pause_bg.screen_width = self.settings.screen_width
        self.pause_bg.screen_height = self.settings.screen_height
        self.pause_bg.hexes.clear()
        self.pause_bg.generate_hexes()
        self.overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        self.overlay.set_alpha(180)
        self.overlay.fill((0, 0, 0))
        
    def show(self):
        """Показывает меню паузы и возвращает выбор пользователя"""
        # Сохраняем текущий экран игры
        game_screen = self.screen.copy()
        
        # Обновляем фон если размер экрана изменился
        self.update_background()
        
        while True:
            # Рисуем фон (экран игры с затемнением)
            self.screen.blit(game_screen, (0, 0))
            self.screen.blit(self.overlay, (0, 0))
            
            # Рисуем эффект паузы
            self.pause_bg.update()
            self.pause_bg.draw(self.screen)
            
            # Заголовок "ПАУЗА"
            title_y = self.settings.screen_height // 2 - 150
            
            # Тень
            title_shadow = GlitchText("PAUSE", 
                                      self.settings.screen_width // 2 + 3, 
                                      title_y + 3, 80,
                                      (30, 30, 40), True)
            title_shadow.draw(self.screen)
            
            # Основной заголовок (с кириллицей или без)
            pause_text = "ПАУЗА" if localization.current_lang == "ru" else "PAUSE"
            title = GlitchText(pause_text,
                              self.settings.screen_width // 2, title_y, 80,
                              self.neon_cyan, True)
            title.update(pygame.mouse.get_pos())
            title.draw(self.screen)
            
            # Декоративная линия
            line_y = title_y + 70
            line_rect = pygame.Rect(self.settings.screen_width // 2 - 150, line_y, 300, 2)
            pygame.draw.rect(self.screen, self.neon_red, line_rect)
            
            # Кнопки меню паузы
            button_y = self.settings.screen_height // 2 - 30
            
            # Кнопка "Продолжить"
            continue_button = GlitchText("continue",
                                        self.settings.screen_width // 2, button_y, 45,
                                        self.neon_green, True)
            
            # Кнопка "Начать заново"
            restart_button = GlitchText("restart",
                                       self.settings.screen_width // 2, button_y + 80, 45,
                                       self.neon_cyan, True)
            
            # Кнопка "В главное меню"
            menu_button = GlitchText("main_menu",
                                    self.settings.screen_width // 2, button_y + 160, 45,
                                    self.neon_red, True)
            
            # Обработка событий
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "continue"  # Выход из паузы по ESC
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.is_clicked(event.pos):
                        return "continue"
                    elif restart_button.is_clicked(event.pos):
                        return "restart"
                    elif menu_button.is_clicked(event.pos):
                        return "main_menu"
            
            # Обновление кнопок
            continue_button.update(mouse_pos)
            restart_button.update(mouse_pos)
            menu_button.update(mouse_pos)
            
            # Отрисовка кнопок
            continue_button.draw(self.screen)
            restart_button.draw(self.screen)
            menu_button.draw(self.screen)
            
            # Декоративная рамка
            border_rect = pygame.Rect(50, 50, 
                                     self.settings.screen_width - 100, 
                                     self.settings.screen_height - 100)
            pygame.draw.rect(self.screen, self.neon_red, border_rect, 2)
            pygame.draw.rect(self.screen, self.neon_cyan, border_rect.inflate(-4, -4), 1)
            
            # Подсказка
            hint_text = GlitchText("esc_hint",
                                  self.settings.screen_width // 2, 
                                  self.settings.screen_height - 40, 20,
                                  self.neon_cyan, True)
            hint_text.update(mouse_pos)
            hint_text.draw(self.screen)
            
            pygame.display.flip()