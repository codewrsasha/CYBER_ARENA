# settings.py
import pygame
import json
import os
import sys

class Settings:
    def __init__(self):
        self.settings_file = "settings.json"
        
        # Все доступные разрешения (всегда доступны)
        self.all_resolutions = [
            (1280, 720),
            (1600, 900),
            (1920, 1080),
            (2560, 1440)
        ]
        
        # Загружаем сохраненные настройки
        self.load_settings()
        
        # Проверяем, что разрешение из настроек есть в списке
        self.validate_resolution()
        
        # Игровые константы
        self.ARENA_WIDTH = 3000
        self.ARENA_HEIGHT = 3000
        self.FPS = 60
        self.GAME_TITLE = "CYBER ARENA: VIRUS ATTACK"
        
        # Цвета в стиле Cyberpunk
        self.CYBER_BLACK = (10, 10, 15)
        self.CYBER_PURPLE = (140, 0, 255)
        self.CYBER_BLUE = (0, 255, 255)
        self.CYBER_PINK = (255, 0, 140)
        self.CYBER_GREEN = (0, 255, 140)
        self.CYBER_YELLOW = (255, 255, 100)
        self.NEON_RED = (255, 50, 50)
        self.CYBER_RED = (255, 50, 50)
        self.NEON_GREEN = (0, 255, 0)
        
    def load_settings(self):
        """Загружает настройки из файла"""
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    
                # Загружаем настройки
                self.current = {
                    "screen_width": loaded_settings.get("screen_width", 1280),
                    "screen_height": loaded_settings.get("screen_height", 720),
                    "fullscreen": loaded_settings.get("fullscreen", False),
                    "sound_volume": loaded_settings.get("sound_volume", 0.7),
                    "music_volume": loaded_settings.get("music_volume", 0.5)
                }
                print(f"Загружены настройки: {self.current}")
                
            except Exception as e:
                print(f"Ошибка загрузки настроек: {e}")
                self.current = self.get_default_settings()
        else:
            print("Файл настроек не найден, используются настройки по умолчанию")
            self.current = self.get_default_settings()
            
    def get_default_settings(self):
        """Возвращает настройки по умолчанию"""
        return {
            "screen_width": 1280,
            "screen_height": 720,
            "fullscreen": False,
            "sound_volume": 0.7,
            "music_volume": 0.5
        }
            
    def validate_resolution(self):
        """Проверяет, что разрешение из настроек есть в списке"""
        current_res = (self.current["screen_width"], self.current["screen_height"])
        
        # Если текущего разрешения нет в списке, устанавливаем 1280x720
        if current_res not in self.all_resolutions:
            print(f"Разрешение {current_res[0]}x{current_res[1]} не в списке, устанавливаем 1280x720")
            self.current["screen_width"] = 1280
            self.current["screen_height"] = 720
            
    def save_settings(self):
        """Сохраняет настройки в файл"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.current, f, indent=4)
            print(f"Настройки сохранены: {self.current}")
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
            
    def apply_settings(self):
        """Применяет настройки (создает новое окно)"""
        flags = pygame.FULLSCREEN if self.current["fullscreen"] else 0
        try:
            return pygame.display.set_mode((self.current["screen_width"],
                                            self.current["screen_height"]), flags)
        except pygame.error as e:
            print(f"Ошибка применения разрешения {self.current['screen_width']}x{self.current['screen_height']}: {e}")
            # Если не получилось, пробуем 1280x720
            self.current["screen_width"] = 1280
            self.current["screen_height"] = 720
            return pygame.display.set_mode((1280, 720), flags)
    
    def get_available_resolutions(self):
        """Возвращает список всех доступных разрешений"""
        return self.all_resolutions
            
    @property
    def screen_width(self):
        return self.current["screen_width"]
    
    @property
    def screen_height(self):
        return self.current["screen_height"]
    
    @property
    def fullscreen(self):
        return self.current["fullscreen"]
    
    @property
    def sound_volume(self):
        return self.current.get("sound_volume", 0.7)
    
    @property
    def music_volume(self):
        return self.current.get("music_volume", 0.5)