# ui.py
import pygame
from settings import Settings
from fonts import FontManager

# Создаем глобальный менеджер шрифтов
font_manager = FontManager()

class CyberText:
    def __init__(self, text, size, color, glow=False, use_cyrillic=True):
        self.settings = Settings()
        self.text = text
        self.size = size
        self.color = color
        self.glow = glow
        
        # Определяем, нужна ли кириллица (если есть русские буквы)
        self.use_cyrillic = use_cyrillic or self.has_cyrillic(text)
        
        # Получаем шрифт из менеджера
        self.font = font_manager.get_font(size, self.use_cyrillic)
        
        self.render()
        
    def has_cyrillic(self, text):
        """Проверяет, есть ли в тексте русские буквы"""
        cyrillic_range = range(0x0400, 0x0500)  # Диапазон кириллицы в Unicode
        for char in text:
            if ord(char) in cyrillic_range:
                return True
        return False
        
    def render(self):
        # Основной текст
        self.text_surface = self.font.render(self.text, True, self.color)
        
        # Эффект свечения
        if self.glow:
            self.glow_surface = self.font.render(self.text, True, self.settings.CYBER_BLUE)
            self.glow_surface.set_alpha(128)
            
    def draw(self, screen, pos):
        if self.glow:
            # Рисуем свечение
            for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
                screen.blit(self.glow_surface, 
                           (pos[0] + offset[0], pos[1] + offset[1]))
        screen.blit(self.text_surface, pos)
        
    def get_rect(self, **kwargs):
        return self.text_surface.get_rect(**kwargs)


class Button:
    def __init__(self, x, y, text, size=36, color=None, use_cyrillic=True):
        self.settings = Settings()
        self.text = text
        self.size = size
        self.color = color or self.settings.CYBER_PURPLE
        self.hover_color = self.settings.CYBER_BLUE
        
        # Определяем, нужна ли кириллица
        self.use_cyrillic = use_cyrillic or self.has_cyrillic(text)
        
        # Получаем шрифт
        self.font = font_manager.get_font(size, self.use_cyrillic)
        
        self.text_surface = self.font.render(text, True, self.color)
        self.rect = self.text_surface.get_rect(center=(x, y))
        self.hovered = False
        
    def has_cyrillic(self, text):
        """Проверяет, есть ли в тексте русские буквы"""
        cyrillic_range = range(0x0400, 0x0500)
        for char in text:
            if ord(char) in cyrillic_range:
                return True
        return False
        
    def draw(self, screen):
        color = self.hover_color if self.hovered else self.color
        text_surface = self.font.render(self.text, True, color)
        
        # Эффект пульсации при наведении
        if self.hovered:
            pulse = (pygame.time.get_ticks() % 1000) / 1000
            
        screen.blit(text_surface, self.rect)
        
        # Рисуем рамку при наведении
        if self.hovered:
            pygame.draw.rect(screen, color, self.rect.inflate(20, 10), 2)
            
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)