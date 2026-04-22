# menu.py 
import pygame
import sys
import random
from settings import Settings
from hex_background import HexBackground, GlitchText, LanguageSwitch
from fonts import FontManager
from localization import localization

font_manager = FontManager()

class Menu:
    def __init__(self, screen, settings=None):
        self.screen = screen
        self.settings = settings if settings else Settings()
        self.clock = pygame.time.Clock()
        
        # Инициализация гексагонального фона
        self.hex_bg = HexBackground(self.settings.screen_width, 
                                     self.settings.screen_height)
        
        # Используем наш киберпанк шрифт для заголовков
        self.title_font = font_manager.get_font(100, False)
        self.subtitle_font = font_manager.get_font(36, True)
        
        # Цвета
        self.neon_red = (255, 50, 50)
        self.neon_blue = (50, 50, 255)
        self.neon_cyan = (0, 255, 255)
        self.neon_green = (0, 255, 0)
        
        # Анимация
        self.glitch_timer = 0
        
    def draw_title(self):
        """Рисует анимированный заголовок с глитчем"""
        center_x = self.settings.screen_width // 2
        
        # Тень
        shadow = self.title_font.render("CYBER ARENA", True, (30, 30, 40))
        shadow_rect = shadow.get_rect(center=(center_x + 3, 103))
        self.screen.blit(shadow, shadow_rect)
        
        # Основной текст
        title = self.title_font.render("CYBER ARENA", True, self.neon_red)
        title_rect = title.get_rect(center=(center_x, 100))
        self.screen.blit(title, title_rect)
        
        # Эффект глитча для заголовка
        if random.random() < 0.05:
            for _ in range(3):
                offset_x = random.randint(-4, 4)
                offset_y = random.randint(-2, 2)
                glitch_color = (0, 255, 255) if random.random() > 0.5 else (255, 0, 255)
                glitch = self.title_font.render("CYBER ARENA", True, glitch_color)
                glitch.set_alpha(150)
                self.screen.blit(glitch, (title_rect.x + offset_x, title_rect.y + offset_y))
                
        # Подзаголовок (локализованный)
        subtitle = localization.get_text("subtitle")
        sub_surface = self.subtitle_font.render(subtitle, True, self.neon_cyan)
        sub_rect = sub_surface.get_rect(center=(center_x, 180))
        
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            self.screen.blit(sub_surface, sub_rect)
        else:
            sub_surface.set_alpha(100)
            self.screen.blit(sub_surface, sub_rect)
            sub_surface.set_alpha(255)
            
        # Декоративные линии
        line_y = 200
        line_color = self.neon_red
        for i in range(2):
            line_rect = pygame.Rect(center_x - 200, line_y + i * 2, 400, 2)
            pygame.draw.rect(self.screen, line_color, line_rect)
            
    def main_menu(self):
        # Создаем переключатель языка
        lang_switch = LanguageSwitch(self.settings.screen_width - 150, 
                                    self.settings.screen_height - 50, 130, 45)
        
        # Устанавливаем текущий язык
        lang_switch.is_en = (localization.current_lang == "en")
        lang_switch.target_slider_x = lang_switch.x + 2 if lang_switch.is_en else lang_switch.x + lang_switch.width // 2 + 2
        lang_switch.slider_x = lang_switch.target_slider_x
        
        while True:
            self.clock.tick(self.settings.FPS)
            
            # Обновление фона
            self.hex_bg.update()
            self.hex_bg.draw(self.screen)
            
            # Заголовок
            self.draw_title()
            
            # Кнопки меню (новый порядок)
            play_button = GlitchText("play", 
                                    self.settings.screen_width // 2, 260, 40,
                                    self.neon_red, True)
            
            tutorial_button = GlitchText("tutorial",
                                        self.settings.screen_width // 2, 320, 40,
                                        self.neon_cyan, True)
            
            statistics_button = GlitchText("statistics",
                                        self.settings.screen_width // 2, 380, 40,
                                        self.neon_green, True)
            
            settings_button = GlitchText("settings",
                                        self.settings.screen_width // 2, 440, 40,
                                        self.neon_red, True)
            
            exit_button = GlitchText("exit",
                                    self.settings.screen_width // 2, 500, 40,
                                    self.neon_red, True)
            
            # Обработка событий
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.is_clicked(event.pos):
                        return "play"
                    elif tutorial_button.is_clicked(event.pos):
                        return "tutorial"
                    elif statistics_button.is_clicked(event.pos):
                        return "statistics"
                    elif settings_button.is_clicked(event.pos):
                        return "settings"
                    elif exit_button.is_clicked(event.pos):
                        pygame.quit()
                        sys.exit()
                    elif lang_switch.is_clicked(event.pos):
                        new_lang = lang_switch.get_current_lang()
                        localization.set_language(new_lang)
                        lang_switch.is_en = (new_lang == "en")
                        lang_switch.target_slider_x = lang_switch.x + 2 if lang_switch.is_en else lang_switch.x + lang_switch.width // 2 + 2
                        
            # Обновление кнопок
            play_button.update(mouse_pos)
            tutorial_button.update(mouse_pos)
            statistics_button.update(mouse_pos)
            settings_button.update(mouse_pos)
            exit_button.update(mouse_pos)
            lang_switch.update(mouse_pos)
            
            # Отрисовка кнопок
            play_button.draw(self.screen)
            tutorial_button.draw(self.screen)
            statistics_button.draw(self.screen)
            settings_button.draw(self.screen)
            exit_button.draw(self.screen)
            lang_switch.draw(self.screen)
            
            # Добавляем "вирусы" на фон
            if random.random() < 0.1:
                virus_x = random.randint(0, self.settings.screen_width)
                virus_y = random.randint(0, self.settings.screen_height)
                pygame.draw.circle(self.screen, self.neon_red, (virus_x, virus_y), 2)
            
            pygame.display.flip()
            
    def settings_menu(self):
        """Новое меню настроек с полноэкранным режимом и локализацией"""
        import sys
        from localization import localization
        
        # Получаем ВСЕ доступные разрешения (без фильтрации)
        available_resolutions = self.settings.get_available_resolutions()
        
        # Выводим в консоль для отладки
        print(f"Доступные разрешения в меню: {available_resolutions}")
        
        # Индексы текущих настроек
        current_res_index = 0
        for i, res in enumerate(available_resolutions):
            if res[0] == self.settings.screen_width and res[1] == self.settings.screen_height:
                current_res_index = i
                break
                
        current_fullscreen = self.settings.fullscreen
        
        # Временные значения настроек
        temp_music_volume = self.settings.music_volume
        temp_sound_volume = self.settings.sound_volume
        temp_res_index = current_res_index
        temp_fullscreen = current_fullscreen
        
        # Флаг, были ли изменения
        has_changes = False
        
        # Сохраняем оригинальные настройки для отката
        original_settings = {
            "screen_width": self.settings.screen_width,
            "screen_height": self.settings.screen_height,
            "fullscreen": self.settings.fullscreen,
            "music_volume": self.settings.music_volume,
            "sound_volume": self.settings.sound_volume
        }
        
        while True:
            self.clock.tick(self.settings.FPS)
            
            # Обновление фона
            self.hex_bg.update()
            self.hex_bg.draw(self.screen)
            
            # Заголовок
            title = GlitchText("settings_title",
                            self.settings.screen_width // 2, 50, 50,
                            self.neon_cyan, True)
            title.update(pygame.mouse.get_pos())
            title.draw(self.screen)
            
            # Разрешение экрана
            res_y = 130
            current_res_text = f"{available_resolutions[temp_res_index][0]} x {available_resolutions[temp_res_index][1]}"
            
            res_label = GlitchText("settings_resolution",
                                self.settings.screen_width // 2 - 200, res_y, 32,
                                self.neon_red, True)
            
            prev_res = GlitchText("<",
                                self.settings.screen_width // 2 - 50, res_y, 40,
                                self.neon_red, False)
            
            res_text = GlitchText(current_res_text,
                                self.settings.screen_width // 2 + 70, res_y, 32,
                                self.neon_cyan, False)
            
            next_res = GlitchText(">",
                                self.settings.screen_width // 2 + 200, res_y, 40,
                                self.neon_red, False)
            
            # Тип экрана (окно/полный экран)
            screen_y = 210
            
            screen_label = GlitchText("settings_screen_type",
                                    self.settings.screen_width // 2 - 200, screen_y, 32,
                                    self.neon_red, True)
            
            # Кнопка "В окне"
            window_btn = GlitchText("settings_window",
                                self.settings.screen_width // 2 - 50, screen_y, 32,
                                self.neon_cyan if not temp_fullscreen else self.neon_red,
                                True)
            
            # Кнопка "Во весь экран"
            fullscreen_btn = GlitchText("settings_fullscreen",
                                    self.settings.screen_width // 2 + 100, screen_y, 32,
                                    self.neon_cyan if temp_fullscreen else self.neon_red,
                                    True)
            
            # Громкость музыки
            music_y = 290
            
            music_label = GlitchText("settings_music",
                                    self.settings.screen_width // 2 - 200, music_y, 32,
                                    self.neon_red, True)
            
            music_down = GlitchText("-",
                                self.settings.screen_width // 2 - 50, music_y, 40,
                                self.neon_red, False)
            
            music_text = GlitchText(f"{int(temp_music_volume * 100)}%",
                                self.settings.screen_width // 2 + 20, music_y, 32,
                                self.neon_cyan, False)
            
            music_up = GlitchText("+",
                                self.settings.screen_width // 2 + 100, music_y, 40,
                                self.neon_red, False)
            
            # Громкость эффектов
            sfx_y = 370
            
            sfx_label = GlitchText("settings_sfx",
                                self.settings.screen_width // 2 - 200, sfx_y, 32,
                                self.neon_red, True)
            
            sfx_down = GlitchText("-",
                                self.settings.screen_width // 2 - 50, sfx_y, 40,
                                self.neon_red, False)
            
            sfx_text = GlitchText(f"{int(temp_sound_volume * 100)}%",
                                self.settings.screen_width // 2 + 20, sfx_y, 32,
                                self.neon_cyan, False)
            
            sfx_up = GlitchText("+",
                            self.settings.screen_width // 2 + 100, sfx_y, 40,
                            self.neon_red, False)
            
            # Кнопки действий
            apply_button = GlitchText("settings_apply",
                                    self.settings.screen_width // 2 - 130, 470, 40,
                                    self.neon_green, True)
            
            back_button = GlitchText("settings_back",
                                    self.settings.screen_width // 2 + 130, 470, 40,
                                    self.neon_red, True)
            
            # Предупреждение о необходимости применить настройки
            if has_changes:
                warning = GlitchText("settings_apply_warning",
                                    self.settings.screen_width // 2, 530, 24,
                                    self.neon_cyan, True)
                warning.update(pygame.mouse.get_pos())
                warning.draw(self.screen)
            
            # Обработка событий
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Разрешение
                    if prev_res.is_clicked(event.pos):
                        temp_res_index = (temp_res_index - 1) % len(available_resolutions)
                        has_changes = True
                        print(f"Выбрано разрешение: {available_resolutions[temp_res_index]}")
                    elif next_res.is_clicked(event.pos):
                        temp_res_index = (temp_res_index + 1) % len(available_resolutions)
                        has_changes = True
                        print(f"Выбрано разрешение: {available_resolutions[temp_res_index]}")
                        
                    # Тип экрана
                    elif window_btn.is_clicked(event.pos) and temp_fullscreen:
                        temp_fullscreen = False
                        has_changes = True
                        print("Выбран оконный режим")
                    elif fullscreen_btn.is_clicked(event.pos) and not temp_fullscreen:
                        temp_fullscreen = True
                        has_changes = True
                        print("Выбран полноэкранный режим")
                        
                    # Громкость музыки
                    elif music_down.is_clicked(event.pos):
                        temp_music_volume = max(0, temp_music_volume - 0.1)
                        has_changes = True
                    elif music_up.is_clicked(event.pos):
                        temp_music_volume = min(1, temp_music_volume + 0.1)
                        has_changes = True
                        
                    # Громкость эффектов
                    elif sfx_down.is_clicked(event.pos):
                        temp_sound_volume = max(0, temp_sound_volume - 0.1)
                        has_changes = True
                    elif sfx_up.is_clicked(event.pos):
                        temp_sound_volume = min(1, temp_sound_volume + 0.1)
                        has_changes = True
                        
                    # Кнопка "Применить" - сохраняем и применяем настройки
                    elif apply_button.is_clicked(event.pos):
                        if has_changes:
                            # Сохраняем настройки
                            new_width = available_resolutions[temp_res_index][0]
                            new_height = available_resolutions[temp_res_index][1]
                            
                            print(f"Применяем настройки: {new_width}x{new_height}, Fullscreen: {temp_fullscreen}")
                            
                            self.settings.current["screen_width"] = new_width
                            self.settings.current["screen_height"] = new_height
                            self.settings.current["fullscreen"] = temp_fullscreen
                            self.settings.current["music_volume"] = temp_music_volume
                            self.settings.current["sound_volume"] = temp_sound_volume
                            
                            # Сохраняем в файл
                            self.settings.save_settings()
                            
                            # Применяем настройки окна
                            try:
                                self.screen = self.settings.apply_settings()
                                pygame.display.set_caption(self.settings.GAME_TITLE)
                                self.hex_bg.screen_width = self.settings.screen_width
                                self.hex_bg.screen_height = self.settings.screen_height
                                self.hex_bg.hexes.clear()
                                self.hex_bg.generate_hexes()
                                print(f"Настройки успешно применены")
                            except Exception as e:
                                print(f"Ошибка применения настроек: {e}")
                            
                            # Обновляем оригинальные настройки
                            original_settings.update(self.settings.current)
                            has_changes = False
                            
                    # Кнопка "Назад" - восстанавливаем оригинальные настройки и выходим
                    elif back_button.is_clicked(event.pos):
                        # Восстанавливаем оригинальные настройки если были изменения
                        if has_changes:
                            print("Отмена изменений, восстановление оригинальных настроек")
                            self.settings.current.update(original_settings)
                            self.settings.save_settings()
                            # Восстанавливаем окно
                            self.screen = self.settings.apply_settings()
                            pygame.display.set_caption(self.settings.GAME_TITLE)
                        return
            
            # Обновление кнопок
            prev_res.update(mouse_pos)
            next_res.update(mouse_pos)
            res_text.update(mouse_pos)
            window_btn.update(mouse_pos)
            fullscreen_btn.update(mouse_pos)
            music_down.update(mouse_pos)
            music_up.update(mouse_pos)
            music_text.update(mouse_pos)
            sfx_down.update(mouse_pos)
            sfx_up.update(mouse_pos)
            sfx_text.update(mouse_pos)
            apply_button.update(mouse_pos)
            back_button.update(mouse_pos)
            
            # Отрисовка кнопок
            res_label.draw(self.screen)
            prev_res.draw(self.screen)
            next_res.draw(self.screen)
            res_text.draw(self.screen)
            
            screen_label.draw(self.screen)
            window_btn.draw(self.screen)
            fullscreen_btn.draw(self.screen)
            
            music_label.draw(self.screen)
            music_down.draw(self.screen)
            music_up.draw(self.screen)
            music_text.draw(self.screen)
            
            sfx_label.draw(self.screen)
            sfx_down.draw(self.screen)
            sfx_up.draw(self.screen)
            sfx_text.draw(self.screen)
            
            apply_button.draw(self.screen)
            back_button.draw(self.screen)
            
            # Декоративная рамка
            border_rect = pygame.Rect(50, 30, 
                                    self.settings.screen_width - 100, 
                                    self.settings.screen_height - 60)
            pygame.draw.rect(self.screen, self.neon_red, border_rect, 2)
            pygame.draw.rect(self.screen, self.neon_cyan, border_rect.inflate(-4, -4), 1)
            
            pygame.display.flip()