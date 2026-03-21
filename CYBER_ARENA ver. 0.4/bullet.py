# bullet.py
import pygame
import math
import os
from settings import Settings  # Добавляем импорт

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, damage, speed=10):
        super().__init__()
        
        # Загружаем спрайт пули
        self.load_sprite()
        
        # Создаем rect для столкновений
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Направление стрельбы (к курсору мыши)
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        if distance > 0:
            self.vx = dx / distance * speed
            self.vy = dy / distance * speed
        else:
            self.vx = 0
            self.vy = 0
            
        self.damage = damage
        self.speed = speed
        self.lifetime = 120  # Кадров жизни пули (2 секунды при 60 FPS)
        
    def load_sprite(self):
        """Загружает спрайт пули"""
        image_path = os.path.join("assets", "images", "effects", "bullet.png")
        
        try:
            original_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(original_image, (8, 8))
        except FileNotFoundError:
            # Создаем заглушку, если файл не найден
            self.image = pygame.Surface((8, 8))
            self.image.fill((0, 255, 255))  # Голубой цвет
            # Добавляем свечение
            pygame.draw.circle(self.image, (255, 255, 255), (4, 4), 2)
            
    def update(self):
        # Движение пули
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        # Уменьшаем время жизни
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
            
    def draw_effect(self, screen, camera):
        """Рисует эффект трассера"""
        if hasattr(self, 'rect'):
            # Рисуем свечение за пулей
            trail_pos = (self.rect.centerx - self.vx * 2, 
                        self.rect.centery - self.vy * 2)
            trail_rect = pygame.Rect(trail_pos[0] - 2, trail_pos[1] - 2, 4, 4)
            trail_rect = camera.apply(trail_rect)
            
            # Создаем эффект послесвечения
            glow = pygame.Surface((8, 8), pygame.SRCALPHA)
            pygame.draw.circle(glow, (0, 255, 255, 100), (4, 4), 4)
            screen.blit(glow, trail_rect)


class LaserBeam(pygame.sprite.Sprite):
    """Альтернативный тип оружия - лазер"""
    def __init__(self, start_x, start_y, end_x, end_y, damage):
        super().__init__()
        
        self.settings = Settings()  # Добавляем settings
        self.start = (start_x, start_y)
        self.end = (end_x, end_y)
        self.damage = damage
        self.lifetime = 10  # Короткая длительность
        
        # Создаем rect для столкновений (линия лазера)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.update_rect()
        
        # Создаем поверхность для отрисовки
        self.image = pygame.Surface((abs(end_x - start_x) + 20, 
                                     abs(end_y - start_y) + 20), pygame.SRCALPHA)
        
    def update_rect(self):
        """Обновляет rect для обнаружения столкновений"""
        # Создаем прямоугольник, содержащий линию лазера
        x1, y1 = self.start
        x2, y2 = self.end
        
        left = min(x1, x2)
        top = min(y1, y2)
        width = abs(x2 - x1) + 10
        height = abs(y2 - y1) + 10
        
        self.rect = pygame.Rect(left, top, width, height)
        
    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()
            
    def check_collision(self, enemy_rect):
        """Проверяет пересечение лазера с врагом"""
        # Проверяем, пересекается ли линия лазера с прямоугольником врага
        # Используем алгоритм для проверки пересечения отрезка и прямоугольника
        x1, y1 = self.start
        x2, y2 = self.end
        
        # Простая проверка - если rect врага пересекает bounding box лазера
        if self.rect.colliderect(enemy_rect):
            # Более точная проверка - расстояние от точки до линии
            # Но для простоты оставим так
            return True
        return False
            
    def draw(self, screen, camera):
        """Рисует лазер"""
        start_pos = camera.apply(pygame.Rect(self.start[0], self.start[1], 0, 0))
        end_pos = camera.apply(pygame.Rect(self.end[0], self.end[1], 0, 0))
        
        # Основной луч
        pygame.draw.line(screen, (255, 100, 100), 
                        (start_pos.x, start_pos.y), 
                        (end_pos.x, end_pos.y), 3)
        
        # Свечение
        for i in range(5):
            alpha = 100 - i * 20
            width = 5 + i * 2
            # Создаем поверхность с альфа-каналом для свечения
            glow_surf = pygame.Surface((screen.get_width(),  # Используем screen.get_width()
                                        screen.get_height()), pygame.SRCALPHA)
            pygame.draw.line(glow_surf, (255, 100, 100, alpha),  # RGB значения
                           (start_pos.x, start_pos.y), 
                           (end_pos.x, end_pos.y), width)
            screen.blit(glow_surf, (0, 0))