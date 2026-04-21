# game.py
import pygame
import sys
import random
import math 
import os
from settings import Settings
from player import Player
from enemy import Enemy, EnemySpawner
from camera import Camera
from ui import CyberText
from bullet import Bullet, LaserBeam
from worm_bullet import WormBullet 
from sound_manager import SoundManager
from localization import localization
from powerup import PowerUpSpawner

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Загружаем фоновое изображение
        self.background = self.load_background()
        
        # Инициализация звуков
        self.sound_manager = SoundManager()
        
        # Устанавливаем громкость из настроек
        self.sound_manager.set_music_volume(self.settings.music_volume)
        self.sound_manager.set_sfx_volume(self.settings.sound_volume)
        
        # Запускаем фоновую музыку
        self.sound_manager.play_music()
        
        # Инициализация игровых объектов
        self.arena_rect = pygame.Rect(0, 0, 
                                     self.settings.ARENA_WIDTH, 
                                     self.settings.ARENA_HEIGHT)
        
        # Создание игрока в центре арены
        self.player = Player(self.settings.ARENA_WIDTH // 2,
                            self.settings.ARENA_HEIGHT // 2)
        
        # Группы спрайтов
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()  # Пули игрока
        self.enemy_bullets = pygame.sprite.Group()  # Пули врагов (новое)
        
        self.all_sprites.add(self.player)
        
        # Камера
        self.camera = Camera(self.settings.ARENA_WIDTH, self.settings.ARENA_HEIGHT)
        
        # Спавнер врагов
        self.enemy_spawner = EnemySpawner(self.settings.ARENA_WIDTH, 
                                         self.settings.ARENA_HEIGHT)
        
        # Игровые переменные
        self.score = 0
        self.game_time = 0
        self.wave = 1
        
        # Для стрельбы
        self.mouse_held = False

        # Система бонусов
        self.powerup_spawner = PowerUpSpawner(max_powerups=5)
        
        # Шрифты
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)

    def load_background(self):
        """Загружает фоновое изображение арены"""
        bg_path = os.path.join("assets", "images", "bg.png")
        
        try:
            # Загружаем изображение
            background = pygame.image.load(bg_path).convert()
            
            # Проверяем размер изображения
            if background.get_size() != (self.settings.ARENA_WIDTH, self.settings.ARENA_HEIGHT):
                print(f"ВНИМАНИЕ: Размер фона {background.get_size()} не соответствует размеру арены "
                      f"({self.settings.ARENA_WIDTH}x{self.settings.ARENA_HEIGHT})")
                # Масштабируем изображение под размер арены
                background = pygame.transform.scale(background, 
                                                   (self.settings.ARENA_WIDTH, 
                                                    self.settings.ARENA_HEIGHT))
                print("Изображение было масштабировано")
            else:
                print(f"Фоновое изображение загружено: {bg_path} ({self.settings.ARENA_WIDTH}x{self.settings.ARENA_HEIGHT})")
                
            return background
            
        except FileNotFoundError:
            print(f"Файл {bg_path} не найден! Используется процедурная генерация фона.")
            return None
        
        except pygame.error as e:
            print(f"Ошибка загрузки фона: {e}")
            return None
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # Смена оружия
                elif event.key == pygame.K_1:
                    self.player.switch_weapon("standard")
                elif event.key == pygame.K_2:
                    self.player.switch_weapon("rapid")
                elif event.key == pygame.K_3:
                    self.player.switch_weapon("shotgun")
                elif event.key == pygame.K_4:
                    self.player.switch_weapon("laser")
                elif event.key == pygame.K_r:  # Ручная перезарядка
                    self.player.start_reload()
                elif event.key == pygame.K_m:  # Музыка
                    if pygame.mixer.music.get_busy():
                        self.sound_manager.pause_music()
                    else:
                        self.sound_manager.unpause_music()
                        
            # Обработка стрельбы
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.mouse_held = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.mouse_held = False
                    
    def update(self):
        # Обновление объектов
        self.player.update()
        self.enemies.update()
        self.bullets.update()
        
        # Обновляем волну в спавнере
        self.enemy_spawner.set_wave(self.wave)  # Добавьте эту строкю
        
        # Обновление спавнера
        self.enemy_spawner.update(self.enemies, self.player)
        
        # Обработка стрельбы
        if self.mouse_held:
            mouse_pos = pygame.mouse.get_pos()
            
            # Конвертируем экранные координаты в мировые
            world_mouse_x = mouse_pos[0] - self.camera.camera_rect.x
            world_mouse_y = mouse_pos[1] - self.camera.camera_rect.y
            
            if self.player.shoot((world_mouse_x, world_mouse_y), self.bullets):
                self.sound_manager.play_shoot()  # Звук выстрела

        # Обновление стрельбы врагов
        self.update_enemy_shooting()
        
        # Обновление пуль врагов
        self.enemy_bullets.update()
        
        # Проверка коллизий
        self.check_collisions()

        # Обновляем бонусы
        self.powerup_spawner.update()
        
        # Обновление камеры
        self.camera.update(self.player)
        
        # Игровое время и волны
        self.game_time += 1
        if self.game_time % 1800 == 0:  # Каждые 30 секунд
            self.wave += 1
            
    def check_collisions(self):
        # Проверка столкновений врагов с игроком
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                if hasattr(enemy, 'attack_type') and enemy.attack_type == "melee":
                    if enemy.attack_player():
                        self.sound_manager.play_player_hit()
                        if self.player.health <= 0:
                            self.game_over()
        
        # Проверка попаданий пуль врагов в игрока
        for enemy_bullet in self.enemy_bullets:
            if self.player.rect.colliderect(enemy_bullet.rect):
                self.player.take_damage(enemy_bullet.damage)
                self.sound_manager.play_player_hit()
                enemy_bullet.kill()
                if self.player.health <= 0:
                    self.game_over()
        
        # Проверка попаданий пуль игрока во врагов
        for bullet in self.bullets:
            current_damage = self.player.weapon_data["damage"]
            
            if isinstance(bullet, LaserBeam):
                hit_enemies = []
                for enemy in self.enemies:
                    if hasattr(bullet, 'check_collision') and bullet.check_collision(enemy.rect):
                        hit_enemies.append(enemy)
                        
                for enemy in hit_enemies:
                    if enemy.take_damage(current_damage):
                        self.sound_manager.play_hit()
                        self.score += 10
                        # Спавним бонус на месте смерти врага
                        print(f"Враг {enemy.virus_type} убит! Попытка спавна бонуса...")
                        self.powerup_spawner.spawn_powerup(
                            enemy.rect.centerx, 
                            enemy.rect.centery,
                            enemy.virus_type
                        )
                        enemy.kill()
            else:
                hit_enemies = pygame.sprite.spritecollide(bullet, self.enemies, False)
                for enemy in hit_enemies:
                    if enemy.take_damage(current_damage):
                        self.sound_manager.play_hit()
                        self.score += 10
                        # Спавним бонус на месте смерти врага
                        print(f"Враг {enemy.virus_type} убит! Попытка спавна бонуса...")
                        self.powerup_spawner.spawn_powerup(
                            enemy.rect.centerx, 
                            enemy.rect.centery,
                            enemy.virus_type
                        )
                        enemy.kill()
                    bullet.kill()
                    
        # Проверка сбора бонусов
        self.powerup_spawner.check_collisions(self.player)

    def update_enemy_shooting(self):
        """Обновляет стрельбу врагов"""
        for enemy in self.enemies:
            if hasattr(enemy, 'attack_type') and enemy.attack_type == "ranged":
                # Проверяем кулдаун стрельбы
                if hasattr(enemy, 'shoot_cooldown') and enemy.shoot_cooldown == 0:
                    # Проверяем расстояние до игрока
                    dx = self.player.rect.centerx - enemy.rect.centerx
                    dy = self.player.rect.centery - enemy.rect.centery
                    distance = math.sqrt(dx ** 2 + dy ** 2)
                    
                    if distance <= enemy.shoot_range:
                        bullet = enemy.shoot_at_player()
                        if bullet:
                            self.enemy_bullets.add(bullet)
                            enemy.shoot_cooldown = enemy.shoot_delay
                
    def draw_arena_border(self):
        """Рисует границу арены в стиле киберпанк"""
        # Применяем камеру к границам арены
        border_rect = self.camera.apply(self.arena_rect)

        # Внешняя граница с неоновым эффектом
        colors = [self.settings.CYBER_BLUE, self.settings.CYBER_PURPLE,
                 self.settings.CYBER_PINK]

        for i, color in enumerate(colors):
            offset = i * 2
            rect = border_rect.inflate(offset * 2, offset * 2)
            pygame.draw.rect(self.screen, color, rect, 2)

        # Угловые элементы
        corner_size = 30
        corners = [
            (border_rect.left, border_rect.top),
            (border_rect.right - corner_size, border_rect.top),
            (border_rect.left, border_rect.bottom - corner_size),
            (border_rect.right - corner_size, border_rect.bottom - corner_size)
        ]

        for x, y in corners:
            pygame.draw.rect(self.screen, self.settings.CYBER_BLUE,
                           (x, y, corner_size, corner_size), 2)
                           
    def draw_background(self):
        """Рисует фон арены"""
        # Применяем камеру к фону
        camera_offset = self.camera.apply(pygame.Rect(0, 0, 0, 0))
        
        if self.background:
            # Рисуем загруженное изображение
            self.screen.blit(self.background, camera_offset)
        else:
            # Если изображение не загружено, используем процедурную генерацию
            self.draw_procedural_background(camera_offset)

    def draw_procedural_background(self, camera_offset):
        """Процедурная генерация фона (резервный вариант)"""
        # Создаем поверхность для арены
        arena_surface = pygame.Surface((self.settings.ARENA_WIDTH, 
                                       self.settings.ARENA_HEIGHT))
        arena_surface.fill((20, 20, 30))
        
        # Рисуем сетку
        grid_color = (40, 40, 60)
        for x in range(0, self.settings.ARENA_WIDTH, 50):
            pygame.draw.line(arena_surface, grid_color, (x, 0), 
                           (x, self.settings.ARENA_HEIGHT), 1)
        for y in range(0, self.settings.ARENA_HEIGHT, 50):
            pygame.draw.line(arena_surface, grid_color, (0, y), 
                           (self.settings.ARENA_WIDTH, y), 1)
            
        # Рисуем декоративные элементы
        font = pygame.font.Font(None, 36)
        for i in range(0, self.settings.ARENA_WIDTH, 200):
            for j in range(0, self.settings.ARENA_HEIGHT, 200):
                text = font.render("⚡", True, (60, 60, 80))
                arena_surface.blit(text, (i, j))
            
        self.screen.blit(arena_surface, camera_offset)
        
    def draw_hud(self):
        """Рисует интерфейс с поддержкой языка"""
        # Статистика
        wave_text = CyberText(f"{localization.get_text('wave')}: {self.wave}", 36, 
                            self.settings.CYBER_GREEN, use_cyrillic=True)
        wave_text.draw(self.screen, (10, 10))

        score_text = CyberText(f"{localization.get_text('points')}: {self.score}", 36, 
                            self.settings.CYBER_BLUE, use_cyrillic=True)
        score_text.draw(self.screen, (10, 50))

        health_text = CyberText(f"{localization.get_text('systems')}: {self.player.health}/{self.player.max_health}",
                                36, self.settings.CYBER_PINK, use_cyrillic=True)
        health_text.draw(self.screen, (10, 90))

        enemy_text = CyberText(f"{localization.get_text('viruses')}: {len(self.enemies)}", 36,
                            self.settings.NEON_RED, use_cyrillic=True)
        enemy_text.draw(self.screen, (10, 130))
        
        # Информация об оружии
        weapon_data = self.player.weapons[self.player.current_weapon]
        weapon_key = f"weapon_{self.player.current_weapon}"
        weapon_name = localization.get_text(weapon_key)
        weapon_color = weapon_data["color"]
        
        weapon_text = CyberText(f"{localization.get_text('weapon')}: {weapon_name}", 28, 
                            weapon_color, use_cyrillic=True)
        weapon_text.draw(self.screen, 
                        (self.settings.screen_width - 350, 
                        self.settings.screen_height - 80))
        
        # Патроны
        ammo_text = CyberText(f"{localization.get_text('ammo')}: {self.player.weapon_data['ammo']}/{weapon_data['max_ammo']}", 
                            24, weapon_color, use_cyrillic=True)
        ammo_text.draw(self.screen, 
                    (self.settings.screen_width - 350, 
                    self.settings.screen_height - 50))
        
        # Урон
        stats_text = CyberText(f"{localization.get_text('damage')}: {weapon_data['damage']}  |  {weapon_data['bullet_count']}x", 
                            20, self.settings.CYBER_BLUE, use_cyrillic=True)
        stats_text.draw(self.screen, 
                    (self.settings.screen_width - 350, 
                        self.settings.screen_height - 30))
        
        # Перезарядка
        if self.player.is_reloading:
            reload_hint = CyberText(localization.get_text("reloading"), 20, 
                                self.settings.CYBER_YELLOW, use_cyrillic=True)
            reload_hint.draw(self.screen, 
                            (self.settings.screen_width // 2 - 80, 
                            self.settings.screen_height - 50))
        
        # Подсказки
        hint_text = CyberText(localization.get_text("controls_hint"), 16, 
                            self.settings.CYBER_BLUE, use_cyrillic=True)
        hint_text.draw(self.screen, (10, self.settings.screen_height - 30))

        # Отображение активных эффектов (иконки)
        effect_y = 10
        effect_x = self.settings.screen_width - 250
        
        # Иконка Damage Up
        if self.player.damage_boost_active:
            try:
                damage_icon = pygame.image.load("assets/images/damage_up.png")
                damage_icon = pygame.transform.scale(damage_icon, (32, 32))
                self.screen.blit(damage_icon, (effect_x, effect_y))
                
                # Таймер
                timer_text = CyberText(f"{self.player.damage_boost_timer // 60}s", 16, 
                                      self.settings.CYBER_RED, use_cyrillic=True)
                timer_text.draw(self.screen, (effect_x + 35, effect_y + 8))
                effect_x -= 50
            except:
                pass
                
        # Иконка Infinite Ammo
        if self.player.infinite_ammo_active:
            try:
                ammo_icon = pygame.image.load("assets/images/infinite_ammo.png")
                ammo_icon = pygame.transform.scale(ammo_icon, (32, 32))
                self.screen.blit(ammo_icon, (effect_x, effect_y))
                
                timer_text = CyberText(f"{self.player.infinite_ammo_timer // 60}s", 16,
                                      self.settings.CYBER_BLUE, use_cyrillic=True)
                timer_text.draw(self.screen, (effect_x + 35, effect_y + 8))
                effect_x -= 50
            except:
                pass
                
        # Иконка Speed Boost
        if self.player.speed_boost_active:
            try:
                speed_icon = pygame.image.load("assets/images/speed_boost.png")
                speed_icon = pygame.transform.scale(speed_icon, (32, 32))
                self.screen.blit(speed_icon, (effect_x, effect_y))
                
                timer_text = CyberText(f"{self.player.speed_boost_timer // 60}s", 16,
                                      self.settings.CYBER_GREEN, use_cyrillic=True)
                timer_text.draw(self.screen, (effect_x + 35, effect_y + 8))
            except:
                pass

    def game_over(self):
        """Конец игры с локализацией"""
        overlay = pygame.Surface((self.settings.screen_width, 
                                self.settings.screen_height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = CyberText(localization.get_text("game_over"), 74, 
                                self.settings.NEON_RED, glow=True, use_cyrillic=True)
        text_rect = game_over_text.get_rect(center=(self.settings.screen_width // 2,
                                                    self.settings.screen_height // 2))
        game_over_text.draw(self.screen, text_rect.topleft)
        
        score_text = CyberText(f"{localization.get_text('viruses_destroyed')}: {self.score}", 36,
                            self.settings.CYBER_BLUE, use_cyrillic=True)
        score_rect = score_text.get_rect(center=(self.settings.screen_width // 2,
                                                self.settings.screen_height // 2 + 80))
        score_text.draw(self.screen, score_rect.topleft)
        
        pygame.display.flip()
        pygame.time.wait(3000)
        self.running = False
        
    def run_game(self):  # Переименовали с run на run_game
        while self.running:
            self.clock.tick(self.settings.FPS)
            self.handle_events()
            self.update()
            
            # Отрисовка
            self.screen.fill(self.settings.CYBER_BLACK)
            
            # Рисуем фон
            self.draw_background()
            
            # Рисуем игрока
            if self.player.visible:
                self.screen.blit(self.player.image, self.camera.apply(self.player))
                self.player.draw_ui(self.screen, self.camera)
            
            # Рисуем врагов
            for enemy in self.enemies:
                self.screen.blit(enemy.image, self.camera.apply(enemy))
                enemy.draw_health_bar(self.screen, self.camera)
                
            # Рисуем бонусы
            self.powerup_spawner.draw(self.screen, self.camera)
                
            # Отрисовка пуль
            for bullet in self.bullets:
                if isinstance(bullet, LaserBeam):
                    bullet.draw(self.screen, self.camera)
                else:
                    self.screen.blit(bullet.image, self.camera.apply(bullet))
                    
            for enemy_bullet in self.enemy_bullets:
                self.screen.blit(enemy_bullet.image, self.camera.apply(enemy_bullet))
                    
            # Рисуем границу арены
            self.draw_arena_border()
            
            # Рисуем HUD
            self.draw_hud()
            
            pygame.display.flip()