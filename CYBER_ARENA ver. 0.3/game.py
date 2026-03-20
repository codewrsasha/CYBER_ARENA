# game.py
import pygame
import sys
import random
from settings import Settings
from player import Player
from enemy import Enemy, EnemySpawner
from camera import Camera
from ui import CyberText
from bullet import Bullet, LaserBeam  # Добавляем импорт пуль

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.running = True
        
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
        self.bullets = pygame.sprite.Group()  # Группа для пуль
        
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
        
        # Шрифты
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # Смена оружия для тестирования
                elif event.key == pygame.K_1:
                    self.player.weapon_type = "bullet"
                elif event.key == pygame.K_2:
                    self.player.weapon_type = "spread"
                elif event.key == pygame.K_3:
                    self.player.weapon_type = "laser"
                    
            # Обработка стрельбы
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
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
                pass
        
        # Проверка коллизий
        self.check_collisions()
        
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
                if self.player.take_damage(enemy.damage):
                    self.game_over()
                    
        # Проверка попаданий пуль во врагов
        for bullet in self.bullets:
            if isinstance(bullet, LaserBeam):
                # Для лазера специальная проверка
                hit_enemies = []
                for enemy in self.enemies:
                    if bullet.check_collision(enemy.rect):
                        hit_enemies.append(enemy)
                        
                for enemy in hit_enemies:
                    if enemy.take_damage(self.player.bullet_damage):
                        self.score += 10
                        enemy.kill()
            else:
                # Для обычных пуль
                hit_enemies = pygame.sprite.spritecollide(bullet, self.enemies, False)
                for enemy in hit_enemies:
                    if enemy.take_damage(self.player.bullet_damage):
                        self.score += 10
                        enemy.kill()
                    bullet.kill()  # Пуля исчезает при попадании
                
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
            
        # Применяем камеру к фону
        camera_offset = self.camera.apply(pygame.Rect(0, 0, 0, 0))
        self.screen.blit(arena_surface, camera_offset)
        
    def draw_hud(self):
        """Рисует интерфейс с новыми шрифтами"""
        # Статистика с кириллицей
        wave_text = CyberText(f"ВОЛНА: {self.wave}", 36, self.settings.CYBER_GREEN, 
                            use_cyrillic=True)
        wave_text.draw(self.screen, (10, 10))

        score_text = CyberText(f"ОЧКИ: {self.score}", 36, self.settings.CYBER_BLUE,
                            use_cyrillic=True)
        score_text.draw(self.screen, (10, 50))

        # Здоровье игрока
        health_text = CyberText(f"СИСТЕМЫ: {self.player.health}/{self.player.max_health}",
                                36, self.settings.CYBER_PINK, use_cyrillic=True)
        health_text.draw(self.screen, (10, 90))

        # Счетчик врагов
        enemy_text = CyberText(f"ВИРУСЫ: {len(self.enemies)}", 36,
                            self.settings.NEON_RED, use_cyrillic=True)
        enemy_text.draw(self.screen, (10, 130))
        
        # Отображение текущего оружия
        if hasattr(self.player, 'weapon_type'):
            weapon_names = {
                "bullet": "СТАНДАРТНЫЙ БЛАСТЕР",
                "spread": "ВЕЕРНЫЙ РАЗРЯД", 
                "laser": "ПЛАЗМЕННЫЙ ЛАЗЕР"
            }
            weapon_colors = {
                "bullet": self.settings.CYBER_BLUE,
                "spread": self.settings.CYBER_PURPLE,
                "laser": (255, 100, 100)
            }
            
            weapon_name = weapon_names.get(self.player.weapon_type, "БЛАСТЕР")
            weapon_color = weapon_colors.get(self.player.weapon_type, self.settings.CYBER_BLUE)
            
            weapon_text = CyberText(f"ОРУЖИЕ: {weapon_name}", 24, weapon_color,
                                    use_cyrillic=True)
            weapon_text.draw(self.screen, 
                        (self.settings.screen_width - 350, 
                            self.settings.screen_height - 50))
        
    def game_over(self):
        """Конец игры"""
        # Затемнение экрана
        overlay = pygame.Surface((self.settings.screen_width, 
                                  self.settings.screen_height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Текст Game Over
        game_over_text = CyberText("СИСТЕМА СКОМПРОМЕТИРОВАНА", 74, 
                                   self.settings.NEON_RED, glow=True)
        text_rect = game_over_text.get_rect(center=(self.settings.screen_width // 2,
                                                    self.settings.screen_height // 2))
        game_over_text.draw(self.screen, text_rect.topleft)
        
        # Счет
        score_text = CyberText(f"ВИРУСОВ УНИЧТОЖЕНО: {self.score}", 36,
                               self.settings.CYBER_BLUE)
        score_rect = score_text.get_rect(center=(self.settings.screen_width // 2,
                                                 self.settings.screen_height // 2 + 80))
        score_text.draw(self.screen, score_rect.topleft)
        
        pygame.display.flip()
        pygame.time.wait(3000)
        self.running = False
        
    def run(self):
        while self.running:
            self.clock.tick(self.settings.FPS)
            self.handle_events()
            self.update()
            
            # Отрисовка
            self.screen.fill(self.settings.CYBER_BLACK)
            
            # Рисуем фон
            self.draw_background()
            
            # Рисуем игрока и врагов
            for sprite in self.all_sprites:
                self.screen.blit(sprite.image, self.camera.apply(sprite))
                
            for enemy in self.enemies:
                self.screen.blit(enemy.image, self.camera.apply(enemy))
                enemy.draw_health_bar(self.screen, self.camera)
                
            # Отрисовка пуль
            for bullet in self.bullets:
                if isinstance(bullet, LaserBeam):
                    # Лазер рисуется по-особому
                    bullet.draw(self.screen, self.camera)
                else:
                    # Обычные пули
                    self.screen.blit(bullet.image, self.camera.apply(bullet))
                    if hasattr(bullet, 'draw_effect'):
                        bullet.draw_effect(self.screen, self.camera)
                    
            # Рисуем границу арены
            self.draw_arena_border()
            
            # Рисуем HUD
            self.draw_hud()
            
            pygame.display.flip()