# worm_bullet.py
import pygame
import math
import os

class WormBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, damage, speed=8):
        super().__init__()
        
        # Загружаем спрайт плазменного шара
        self.load_sprite()
        
        # Создаем rect для столкновений
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Направление стрельбы к игроку
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
        self.lifetime = 180  # 3 секунды жизни (при 60 FPS)
        
    def load_sprite(self):
        """Загружает спрайт плазменного шара"""
        image_path = os.path.join("assets", "images", "plasm.png")
        
        try:
            original_image = pygame.image.load(image_path).convert_alpha()
            # Масштабируем до 32x32
            self.image = pygame.transform.scale(original_image, (32, 32))
        except FileNotFoundError:
            print(f"Внимание: файл {image_path} не найден. Используется заглушка - красный шар.")
            # Создаем простую заглушку - красный круг
            self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
            # Рисуем красный круг
            pygame.draw.circle(self.image, (255, 0, 0), (16, 16), 14)
            # Добавляем обводку белым цветом
            pygame.draw.circle(self.image, (255, 255, 255), (16, 16), 14, 2)
            
    def update(self):
        # Движение пули
        self.rect.x += self.vx
        self.rect.y += self.vy
        
        # Уменьшаем время жизни
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()