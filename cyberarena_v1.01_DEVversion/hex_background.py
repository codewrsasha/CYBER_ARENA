# hex_background.py
import pygame
import math
import random
import os
from fonts import FontManager

font_manager = FontManager()

class HexBackground:
    """Гексагональный фон в стиле киберпанк"""
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.hex_size = 40
        self.hexes = []
        self.glitch_lines = []
        
        # Цвета
        self.colors = [
            (20, 20, 30),      # темный
            (30, 20, 40),      # фиолетово-черный
            (40, 20, 50),      # темно-фиолетовый
            (10, 10, 20)       # почти черный
        ]
        
        self.neon_red = (255, 50, 50)
        self.neon_blue = (50, 50, 255)
        
        self.generate_hexes()
        self.glitch_timer = 0
        
    def generate_hexes(self):
        """Генерирует сетку гексагонов"""
        hex_width = self.hex_size * 2
        hex_height = math.sqrt(3) * self.hex_size
        
        cols = int(self.screen_width / (hex_width * 0.75)) + 2
        rows = int(self.screen_height / hex_height) + 2
        
        for row in range(rows):
            for col in range(cols):
                x = col * hex_width * 0.75
                y = row * hex_height
                
                # Смещение для четных рядов
                if row % 2 == 1:
                    x += hex_width * 0.375
                    
                # Случайный цвет из палитры
                color = random.choice(self.colors)
                
                self.hexes.append({
                    'x': x,
                    'y': y,
                    'color': color,
                    'pulse': random.uniform(0, 2 * math.pi)
                })
                
    def draw_hexagon(self, screen, x, y, size, color, width=1):
        """Рисует один гексагон"""
        points = []
        for i in range(6):
            angle = math.radians(60 * i - 30)
            px = x + size * math.cos(angle)
            py = y + size * math.sin(angle)
            points.append((px, py))
        pygame.draw.polygon(screen, color, points, width)
        
    def update(self):
        """Обновляет эффекты фона"""
        self.glitch_timer += 1
        
        # Случайные глитч-линии
        if random.random() < 0.02:  # 2% шанс каждый кадр
            self.glitch_lines.append({
                'x': random.randint(0, self.screen_width),
                'y': random.randint(0, self.screen_height),
                'width': random.randint(50, 200),
                'height': random.randint(1, 3),
                'life': 5
            })
            
        # Обновляем линии
        for line in self.glitch_lines[:]:
            line['life'] -= 1
            if line['life'] <= 0:
                self.glitch_lines.remove(line)
                
        # Пульсация гексагонов
        for hex_data in self.hexes:
            hex_data['pulse'] += 0.05
            if hex_data['pulse'] > 2 * math.pi:
                hex_data['pulse'] = 0
                
    def draw(self, screen):
        """Рисует фон"""
        screen.fill((5, 5, 10))  # базовый черный
        
        # Рисуем гексагоны
        for hex_data in self.hexes:
            # Пульсирующая яркость
            pulse = (math.sin(hex_data['pulse']) + 1) / 2
            color = tuple(min(255, int(c + pulse * 20)) for c in hex_data['color'])
            self.draw_hexagon(screen, hex_data['x'], hex_data['y'], 
                            self.hex_size, color, 1)
            
        # Рисуем глитч-линии
        for line in self.glitch_lines:
            alpha = int(255 * (line['life'] / 5))
            color = (255, 50, 50, alpha)
            rect = pygame.Rect(line['x'], line['y'], line['width'], line['height'])
            pygame.draw.rect(screen, self.neon_red, rect)
            
        # Добавляем случайные "битые пиксели"
        if random.random() < 0.05:
            for _ in range(random.randint(1, 5)):
                x = random.randint(0, self.screen_width)
                y = random.randint(0, self.screen_height)
                pygame.draw.rect(screen, self.neon_red, (x, y, 2, 2))


class LanguageSwitch:
    """Стилизованный переключатель языка в стиле киберпанк"""
    def __init__(self, x, y, width=120, height=40):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_en = True  # True = EN, False = RU
        
        # Цвета (исправлены для лучшей видимости)
        self.bg_color = (10, 10, 15)  # Темный фон
        self.active_color = (0, 255, 0)  # Ярко-зеленый для активного
        self.inactive_color = (255, 50, 50)  # Красный для неактивного
        self.border_color = (0, 255, 255)  # Голубая рамка
        self.text_color_active = (0, 0, 0)  # Черный текст на зеленом фоне
        self.text_color_inactive = (255, 255, 255)  # Белый текст на красном фоне
        
        # Позиция ползунка
        self.slider_width = width // 2 - 4
        self.slider_x = x + 2 if self.is_en else x + width // 2 + 2
        
        # Шрифты
        self.font = font_manager.get_font(24, False)  # Увеличил размер шрифта
        
        # Анимация
        self.animation_progress = 0
        self.target_slider_x = self.slider_x
        
    def update(self, mouse_pos):
        """Обновляет состояние переключателя"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hovered = rect.collidepoint(mouse_pos)
        
    def update_animation(self):
        """Плавная анимация переключения"""
        if abs(self.slider_x - self.target_slider_x) > 1:
            self.slider_x += (self.target_slider_x - self.slider_x) * 0.2
            
    def set_language(self, is_en):
        """Устанавливает язык и запускает анимацию"""
        if self.is_en != is_en:
            self.is_en = is_en
            self.target_slider_x = self.x + 2 if self.is_en else self.x + self.width // 2 + 2
            
    def is_clicked(self, mouse_pos):
        """Проверяет клик по переключателю"""
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        if rect.collidepoint(mouse_pos):
            self.set_language(not self.is_en)
            return True
        return False
        
    def draw(self, screen):
        """Рисует переключатель"""
        self.update_animation()
        
        # Фон переключателя
        bg_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.bg_color, bg_rect)
        pygame.draw.rect(screen, self.border_color, bg_rect, 2)
        
        # Ползунок с улучшенной видимостью
        slider_rect = pygame.Rect(int(self.slider_x), self.y + 2, 
                                  self.slider_width, self.height - 4)
        slider_color = self.active_color if self.is_en else self.inactive_color
        pygame.draw.rect(screen, slider_color, slider_rect)
        
        # Добавляем свечение для ползунка
        glow_rect = slider_rect.inflate(4, 4)
        glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(glow_surf, (*slider_color, 50), glow_surf.get_rect(), 2)
        screen.blit(glow_surf, glow_rect)
        
        # Текст EN (с черным текстом на зеленом фоне для активного)
        if self.is_en:
            # Активный EN - зеленый фон, черный текст
            en_color = self.text_color_active
            # Рисуем фон для текста
            en_bg_rect = pygame.Rect(self.x + 2, self.y + 2, self.width // 2 - 4, self.height - 4)
            pygame.draw.rect(screen, self.active_color, en_bg_rect)
        else:
            # Неактивный EN - красный фон, белый текст
            en_color = self.text_color_inactive
            en_bg_rect = pygame.Rect(self.x + 2, self.y + 2, self.width // 2 - 4, self.height - 4)
            pygame.draw.rect(screen, self.inactive_color, en_bg_rect)
            
        en_text = self.font.render("EN", True, en_color)
        en_rect = en_text.get_rect(center=(self.x + self.width // 4, self.y + self.height // 2))
        screen.blit(en_text, en_rect)
        
        # Текст RU
        if not self.is_en:
            # Активный RU - зеленый фон, черный текст
            ru_color = self.text_color_active
            ru_bg_rect = pygame.Rect(self.x + self.width // 2 + 2, self.y + 2, self.width // 2 - 4, self.height - 4)
            pygame.draw.rect(screen, self.active_color, ru_bg_rect)
        else:
            # Неактивный RU - красный фон, белый текст
            ru_color = self.text_color_inactive
            ru_bg_rect = pygame.Rect(self.x + self.width // 2 + 2, self.y + 2, self.width // 2 - 4, self.height - 4)
            pygame.draw.rect(screen, self.inactive_color, ru_bg_rect)
            
        ru_text = self.font.render("RU", True, ru_color)
        ru_rect = ru_text.get_rect(center=(self.x + self.width * 3 // 4, self.y + self.height // 2))
        screen.blit(ru_text, ru_rect)
        
        # Эффект глитча при переключении
        if self.animation_progress > 0:
            glitch_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            pygame.draw.rect(screen, (255, 255, 255), glitch_rect, 1)
            
    def get_current_lang(self):
        """Возвращает текущий язык"""
        return "en" if self.is_en else "ru"


class GlitchText:
    """Текст с глитч-эффектом и поддержкой локализации"""
    def __init__(self, text_key, x, y, size=50, color=(255, 50, 50), use_cyrillic=None):
        self.text_key = text_key
        self.x = x
        self.y = y
        self.size = size
        self.base_color = color
        self.hover_color = (50, 50, 255)
        self.current_color = self.base_color
        self.glitch_intensity = 0
        self.hovered = False
        
        # Определяем нужно ли использовать кириллицу
        if use_cyrillic is None:
            from localization import localization
            self.use_cyrillic = localization.current_lang == "ru"
        else:
            self.use_cyrillic = use_cyrillic
        
        # Используем наш киберпанк шрифт
        self.font = font_manager.get_font(size, self.use_cyrillic)
        
    def update_text(self):
        """Обновляет текст при смене языка"""
        from localization import localization
        self.use_cyrillic = localization.current_lang == "ru"
        self.font = font_manager.get_font(self.size, self.use_cyrillic)
        
    def get_current_text(self):
        """Возвращает актуальный текст для текущего языка"""
        from localization import localization
        return localization.get_text(self.text_key)
        
    def update(self, mouse_pos):
        """Обновляет состояние и глитч-эффект"""
        self.update_text()
        rect = self.get_rect()
        self.hovered = rect.collidepoint(mouse_pos)
        
        if self.hovered:
            self.current_color = self.hover_color
            self.glitch_intensity = random.randint(1, 3)
        else:
            self.current_color = self.base_color
            self.glitch_intensity = 0
            
    def get_rect(self):
        """Возвращает прямоугольник текста"""
        text = self.get_current_text()
        text_surface = self.font.render(text, True, self.current_color)
        return text_surface.get_rect(center=(self.x, self.y))
        
    def draw(self, screen):
        """Рисует текст с глитч-эффектом"""
        text = self.get_current_text()
        rect = self.get_rect()
        
        # Основной текст
        text_surface = self.font.render(text, True, self.current_color)
        screen.blit(text_surface, rect)
        
        # Глитч-эффект
        if self.glitch_intensity > 0:
            for i in range(self.glitch_intensity):
                offset_x = random.randint(-3, 3)
                offset_y = random.randint(-1, 1)
                glitch_color = (255, 0, 0) if random.random() > 0.5 else (0, 0, 255)
                glitch_surface = self.font.render(text, True, glitch_color)
                glitch_surface.set_alpha(100)
                screen.blit(glitch_surface, (rect.x + offset_x, rect.y + offset_y))
                
        # Эффект "короткого замыкания" при наведении
        if self.hovered and random.random() < 0.3:
            flash = pygame.Surface((rect.width + 20, rect.height + 10))
            flash.fill((255, 255, 255))
            flash.set_alpha(100)
            screen.blit(flash, (rect.x - 10, rect.y - 5))
            
    def is_clicked(self, mouse_pos):
        return self.get_rect().collidepoint(mouse_pos)