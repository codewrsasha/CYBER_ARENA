# fonts.py
import pygame
import os

class FontManager:
    def __init__(self):
        self.fonts = {}
        self.cyrillic_font = None
        self.latin_font = None
        
        # Загружаем шрифты
        self.load_fonts()
        
    def load_fonts(self):
        """Загружает шрифты из папки assets/fonts"""
        fonts_folder = os.path.join("assets", "fonts")
        
        # Проверяем существование папки
        if not os.path.exists(fonts_folder):
            os.makedirs(fonts_folder)
            print(f"Создана папка {fonts_folder}. Поместите туда файлы HackedCyr.ttf и HACKED.ttf")
            return
            
        # Загружаем кириллический шрифт
        cyrillic_path = os.path.join(fonts_folder, "HackedCyr.ttf")
        if os.path.exists(cyrillic_path):
            self.cyrillic_font = cyrillic_path
            print("Кириллический шрифт загружен")
        else:
            print(f"Файл {cyrillic_path} не найден. Используется системный шрифт")
            
        # Загружаем латинский шрифт
        latin_path = os.path.join(fonts_folder, "HACKED.ttf")
        if os.path.exists(latin_path):
            self.latin_font = latin_path
            print("Латинский шрифт загружен")
        else:
            print(f"Файл {latin_path} не найден. Используется системный шрифт")
            
    def get_font(self, size, use_cyrillic=True):
        """
        Возвращает шрифт нужного размера
        use_cyrillic=True - для русского текста
        use_cyrillic=False - для английского текста
        """
        font_path = self.cyrillic_font if use_cyrillic else self.latin_font
        
        # Создаем ключ для кэша
        cache_key = f"{font_path}_{size}_{use_cyrillic}"
        
        # Проверяем, есть ли уже такой шрифт в кэше
        if cache_key in self.fonts:
            return self.fonts[cache_key]
            
        # Загружаем шрифт
        if font_path and os.path.exists(font_path):
            try:
                font = pygame.font.Font(font_path, size)
                self.fonts[cache_key] = font
                return font
            except Exception as e:
                print(f"Ошибка загрузки шрифта {font_path}: {e}")
                
        # Если шрифт не загрузился, используем системный
        return pygame.font.Font(None, size)