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
    def __init__(self, x, y, text, size=36, color=None, hover_color=None):
        self.settings = Settings()
        self.text = text
        self.size = size
        self.normal_color = color or self.settings.CYBER_GREEN
        self.hover_color = hover_color or self.settings.CYBER_BLUE
        self.current_color = self.normal_color
        
        # Определяем, нужна ли кириллица
        self.use_cyrillic = self.has_cyrillic(text)
        
        # Получаем шрифт
        self.font = font_manager.get_font(size, self.use_cyrillic)
        
        self.text_surface = self.font.render(text, True, self.current_color)
        self.rect = self.text_surface.get_rect(center=(x, y))
        self.hovered = False
        
        # Эффект пульсации
        self.pulse_time = 0
        
    def has_cyrillic(self, text):
        """Проверяет, есть ли в тексте русские буквы"""
        cyrillic_range = range(0x0400, 0x0500)
        for char in text:
            if ord(char) in cyrillic_range:
                return True
        return False
        
    def update(self, mouse_pos):
        """Обновляет состояние кнопки"""
        was_hovered = self.hovered
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if self.hovered:
            self.current_color = self.hover_color
            self.pulse_time += 1
        else:
            self.current_color = self.normal_color
            self.pulse_time = 0
            
    def draw(self, screen):
        # Эффект свечения при наведении
        if self.hovered:
            # Создаем эффект пульсации
            pulse = (pygame.time.get_ticks() % 500) / 500
            alpha = int(100 + pulse * 100)
            
            # Рисуем тень/свечение
            for offset in range(2, 6, 2):
                glow_surf = self.font.render(self.text, True, self.current_color)
                glow_surf.set_alpha(50 - offset * 10)
                screen.blit(glow_surf, (self.rect.x - offset, self.rect.y - offset))
        
        # Основной текст
        text_surface = self.font.render(self.text, True, self.current_color)
        
        # Добавляем эффект мерцания при наведении
        if self.hovered:
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                text_surface = self.font.render(self.text, True, (255, 255, 255))
        
        screen.blit(text_surface, self.rect)
        
        # Рисуем рамку при наведении с эффектом неона
        if self.hovered:
            border_rect = self.rect.inflate(20, 10)
            # Рисуем несколько слоев для неон-эффекта
            for i in range(3):
                width = 2 + i
                alpha = 100 - i * 30
                border_color = (*self.current_color, alpha)
                # Для рамки используем отдельную поверхность
                pygame.draw.rect(screen, self.current_color, border_rect, width)
            
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)