# camera.py
import pygame
from settings import Settings

class Camera:
    def __init__(self, width, height):
        self.settings = Settings()
        self.camera_rect = pygame.Rect(0, 0, 
                                      self.settings.screen_width, 
                                      self.settings.screen_height)
        self.world_width = width
        self.world_height = height
        
    def apply(self, entity):
        """Применяет смещение камеры к позиции объекта"""
        if isinstance(entity, pygame.Rect):
            return entity.move(self.camera_rect.x, self.camera_rect.y)
        else:
            return entity.rect.move(self.camera_rect.x, self.camera_rect.y)
    
    def update(self, target):
        """Обновляет позицию камеры следуя за целью"""
        x = -target.rect.centerx + self.settings.screen_width // 2
        y = -target.rect.centery + self.settings.screen_height // 2
        
        # Ограничиваем камеру границами мира
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.world_width - self.settings.screen_width), x)
        y = max(-(self.world_height - self.settings.screen_height), y)
        
        self.camera_rect.x = x
        self.camera_rect.y = y