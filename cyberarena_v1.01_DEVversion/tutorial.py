# tutorial.py

import pygame
import sys
from hex_background import HexBackground, GlitchText
from localization import localization
from player import Player
from bullet import Bullet, LaserBeam
from sound_manager import SoundManager
from fonts import FontManager

font_manager = FontManager()

class Tutorial:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        
        # Создаем фон
        self.tutorial_bg = HexBackground(settings.screen_width, settings.screen_height)
        
        # Создаем игрока для обучения
        self.player = Player(400, 300, game_speed=False)
        
        # Группы для пуль
        self.bullets = pygame.sprite.Group()
        
        # Для стрельбы
        self.mouse_held = False
        
        # Звуки
        self.sound_manager = SoundManager(settings)
        
        # Шрифт для текста
        self.font = font_manager.get_font(24, True)
        
        # Цвета
        self.neon_red = (255, 50, 50)
        self.neon_cyan = (0, 255, 255)
        self.neon_green = (0, 255, 0)
        
        # Размеры игровой области
        self.playground_rect = None
        
        # Флаги для отладки
        self.running = True
        
    def update_background(self):
        """Обновляет фон для нового размера экрана"""
        self.tutorial_bg.screen_width = self.settings.screen_width
        self.tutorial_bg.screen_height = self.settings.screen_height
        self.tutorial_bg.hexes.clear()
        self.tutorial_bg.generate_hexes()
        
    def is_mouse_in_playground(self, pos):
        """Проверяет, находится ли мышь в игровой области"""
        if self.playground_rect:
            return self.playground_rect.collidepoint(pos)
        return False
        
    def draw_controls(self):
        """Рисует левую панель с управлением"""
        panel_x = 50
        panel_y = 80
        panel_width = self.settings.screen_width // 2 - 70
        panel_height = self.settings.screen_height - 150
        
        # Рамка панели
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, (20, 20, 30), panel_rect)
        pygame.draw.rect(self.screen, self.neon_cyan, panel_rect, 2)
        
        # Заголовок
        title = GlitchText("tutorial_title", panel_width // 2  + 50, panel_y + 30, 36,
                        self.neon_green, True)
        title.draw(self.screen)
        
        # Правила управления
        controls_y = panel_y + 80
        
        if localization.current_lang == "ru":
            controls = [
                ("ДВИЖЕНИЕ:", "W/A/S/D  или  стрелки"),
                ("СТРЕЛЬБА:", "ЛКМ (В ИГРОВОЙ ОБЛАСТИ)"),
                ("СМЕНА ОРУЖИЯ:", "1, 2, 3, 4"),
                ("ПЕРЕЗАРЯДКА:", "R"),
                ("МУЗЫКА:", "M (ВКЛ/ВЫКЛ)"),
                ("ПАУЗА:", "ESC"),
            ]
        else:
            controls = [
                ("MOVEMENT:", "W/A/S/D  or  arrows"),
                ("SHOOT:", "LMB (IN GAME AREA)"),
                ("WEAPONS:", "1, 2, 3, 4"),
                ("RELOAD:", "R"),
                ("MUSIC:", "M (ON/OFF)"),
                ("PAUSE:", "ESC"),
            ]
        
        for i, (title_text, desc_text) in enumerate(controls):
            control_title = self.font.render(title_text, True, self.neon_red)
            self.screen.blit(control_title, (panel_x + 20, controls_y + i * 40))
            
            control_desc = self.font.render(desc_text, True, self.neon_cyan)
            self.screen.blit(control_desc, (panel_x + 200, controls_y + i * 40))
            
        # Кнопка назад
        back_button = GlitchText("back",
                                panel_x + panel_width // 2, 
                                panel_y + panel_height - 40, 40,
                                self.neon_red, True)
        
        return back_button
        
    def draw_playground(self):
        """Рисует правую панель с игровой областью"""
        panel_x = self.settings.screen_width // 2 + 20
        panel_y = 80
        panel_width = self.settings.screen_width // 2 - 70
        panel_height = self.settings.screen_height - 150
        
        # Рамка панели
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, (20, 20, 30), panel_rect)
        pygame.draw.rect(self.screen, self.neon_cyan, panel_rect, 2)
        
        # Внутренняя игровая область
        playground_width = panel_width - 40
        playground_height = panel_height - 100
        playground_x = panel_x + 20
        playground_y = panel_y + 40
        
        self.playground_rect = pygame.Rect(playground_x, playground_y, 
                                        playground_width, playground_height)
        
        # Заливка игровой области
        pygame.draw.rect(self.screen, (10, 10, 15), self.playground_rect)
        
        # Рисуем сетку
        grid_color = (40, 40, 60)
        for x in range(playground_x, playground_x + playground_width, 50):
            pygame.draw.line(self.screen, grid_color, (x, playground_y), 
                        (x, playground_y + playground_height))
        for y in range(playground_y, playground_y + playground_height, 50):
            pygame.draw.line(self.screen, grid_color, (playground_x, y), 
                        (playground_x + playground_width, y))
        
        # Рисуем игрока
        self.screen.blit(self.player.image, self.player.rect)
        
        # Рисуем пули (включая лазер)
        for bullet in self.bullets:
            if isinstance(bullet, LaserBeam):
                bullet.draw(self.screen, None)  # camera=None для туториала
            else:
                self.screen.blit(bullet.image, bullet.rect)
        
        # Информация о текущем оружии
        weapon_name_key = f"weapon_{self.player.current_weapon}"
        weapon_name = localization.get_text(weapon_name_key)
        weapon_color = self.player.weapon_data["color"]
        
        weapon_text = self.font.render(weapon_name, True, weapon_color)
        weapon_rect = weapon_text.get_rect(center=(panel_x + panel_width // 2, 
                                                panel_y + panel_height - 30))
        self.screen.blit(weapon_text, weapon_rect)
        
        # Патроны
        ammo_text = self.font.render(f"{localization.get_text('ammo')}: {self.player.weapon_data['ammo']}/{self.player.weapons[self.player.current_weapon]['max_ammo']}", 
                                    True, weapon_color)
        ammo_rect = ammo_text.get_rect(center=(panel_x + panel_width // 2, 
                                            playground_height + 100))
        self.screen.blit(ammo_text, ammo_rect)
        
        # Рамка игровой области (подсветка)
        pygame.draw.rect(self.screen, self.neon_green, self.playground_rect, 2)
            
    def show(self):
        """Показывает страницу обучения"""
        self.update_background()
        
        # Устанавливаем игрока в центр игровой области
        center_x = self.settings.screen_width // 2 + 50
        center_y = self.settings.screen_height // 2
        self.player.rect.x = center_x - self.player.rect.width // 2
        self.player.rect.y = center_y - self.player.rect.height // 2
        
        # Сбрасываем состояние
        self.mouse_held = False
        self.running = True
        
        # Главный цикл обучения
        while self.running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.player.switch_weapon("standard")
                    elif event.key == pygame.K_2:
                        self.player.switch_weapon("rapid")
                    elif event.key == pygame.K_3:
                        self.player.switch_weapon("shotgun")
                    elif event.key == pygame.K_4:
                        self.player.switch_weapon("laser")
                    elif event.key == pygame.K_r:
                        self.player.start_reload()
                    elif event.key == pygame.K_m:
                        # Включение/выключение музыки
                        if pygame.mixer.music.get_busy():
                            self.sound_manager.pause_music()
                            print("Музыка выключена")
                        else:
                            self.sound_manager.unpause_music()
                            print("Музыка включена")
                    elif event.key == pygame.K_ESCAPE:
                        return
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Проверяем, что клик в игровой области
                        if self.is_mouse_in_playground(event.pos):
                            self.mouse_held = True
                        else:
                            print("Клик вне игровой области - стрельба недоступна")
                        
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mouse_held = False
            
            # Обновление игрока
            self.player.update()
            
            # Ограничение движения
            if self.playground_rect:
                self.player.rect.x = max(self.playground_rect.left, 
                                        min(self.playground_rect.right - self.player.rect.width, 
                                            self.player.rect.x))
                self.player.rect.y = max(self.playground_rect.top, 
                                        min(self.playground_rect.bottom - self.player.rect.height, 
                                            self.player.rect.y))
            
            # Стрельба при зажатой ЛКМ (только если мышь в игровой области)
            if self.mouse_held:
                # Получаем позицию мыши в мировых координатах
                mouse_pos = pygame.mouse.get_pos()
                if self.is_mouse_in_playground(mouse_pos):
                    if self.player.shoot(mouse_pos, self.bullets):
                        self.sound_manager.play_shoot()
            
            # Обновление пуль
            self.bullets.update()
            
            # Удаление пуль за пределами
            for bullet in list(self.bullets):
                if self.playground_rect:
                    if (bullet.rect.x < self.playground_rect.left or 
                        bullet.rect.x > self.playground_rect.right or
                        bullet.rect.y < self.playground_rect.top or 
                        bullet.rect.y > self.playground_rect.bottom):
                        bullet.kill()
            
            # Отрисовка
            self.tutorial_bg.update()
            self.tutorial_bg.draw(self.screen)
            
            back_button = self.draw_controls()
            self.draw_playground()
            
            # Кнопка назад
            mouse_pos = pygame.mouse.get_pos()
            back_button.update(mouse_pos)
            
            # Проверка клика по кнопке назад
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.is_clicked(event.pos):
                        return
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            back_button.draw(self.screen)
            
            pygame.display.flip()
            pygame.time.Clock().tick(60)