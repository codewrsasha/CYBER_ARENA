# matrix_effect.py
import pygame
import random

class MatrixSymbol:
    """Отдельный падающий символ"""
    def __init__(self, x, y, speed, char, color):
        self.x = x
        self.y = y
        self.speed = speed
        self.char = char
        self.color = color
        self.alpha = 255
        
    def update(self):
        self.y += self.speed
        # Затухание при приближении к краю
        if self.y > 600:
            self.alpha -= 5
        return self.y > 800 or self.alpha <= 0
        
    def draw(self, screen, font):
        text = font.render(self.char, True, self.color)
        text.set_alpha(self.alpha)
        screen.blit(text, (self.x, self.y))


class MatrixEffect:
    """Эффект падающих символов как в Матрице"""
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.symbols = []
        self.font_small = None
        self.font_medium = None
        self.init_fonts()
        
        # Набор символов для падения
        self.chars = [
            '0', '1', '(', ')', '[', ']', '{', '}', '<', '>',
            '+', '-', '*', '/', '=', '!', '?', '&', '%', '$',
            '#', '@', '^', '~', '|', '\\', '/', ';', ':', ',', '.'
        ]
        
        # Цвета для символов (оттенки зеленого)
        self.colors = [
            (0, 255, 0),      # ярко-зеленый
            (50, 255, 50),    # светло-зеленый
            (100, 255, 100),  # бледно-зеленый
            (0, 200, 0),      # темно-зеленый
            (0, 150, 0),      # очень темный
        ]
        
        self.spawn_timer = 0
        self.spawn_delay = 5  # кадров между спавном символов
        
    def init_fonts(self):
        """Инициализирует шрифты для символов"""
        try:
            # Пытаемся использовать системный моноширинный шрифт
            self.font_small = pygame.font.Font(None, 20)
            self.font_medium = pygame.font.Font(None, 28)
        except:
            self.font_small = pygame.font.SysFont('monospace', 20)
            self.font_medium = pygame.font.SysFont('monospace', 28)
            
    def update(self):
        """Обновляет все символы"""
        # Спавн новых символов
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_timer = 0
            self.spawn_symbol()
            
        # Обновляем существующие символы
        for symbol in self.symbols[:]:
            if symbol.update():
                self.symbols.remove(symbol)
                
    def spawn_symbol(self):
        """Создает новый падающий символ"""
        x = random.randint(0, self.screen_width)
        speed = random.uniform(1, 4)
        char = random.choice(self.chars)
        color = random.choice(self.colors)
        
        # Иногда используем больший шрифт
        font = self.font_medium if random.random() > 0.7 else self.font_small
        
        symbol = MatrixSymbol(x, -20, speed, char, color)
        symbol.font = font
        self.symbols.append(symbol)
        
    def draw(self, screen):
        """Рисует все символы"""
        for symbol in self.symbols:
            font = getattr(symbol, 'font', self.font_small)
            text = font.render(symbol.char, True, symbol.color)
            text.set_alpha(symbol.alpha)
            screen.blit(text, (symbol.x, symbol.y))
            
    def clear(self):
        """Очищает все символы"""
        self.symbols.clear()