# settings.py
import pygame
import json
import os

class Settings:
    def __init__(self):
        self.settings_file = "settings.json"
        self.default_settings = {
            "screen_width": 1024,
            "screen_height": 768,
            "fullscreen": False,
            "sound_volume": 0.7,
            "music_volume": 0.5
        }
        self.load_settings()
        
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

        # Настройки оружия
    WEAPON_TYPES = {
        "bullet": {
            "name": "СТАНДАРТНЫЙ БЛАСТЕР",
            "damage": 15,
            "speed": 12,
            "cooldown": 200,
            "color": (0, 255, 255)
        },
        "spread": {
            "name": "ВЕЕРНЫЙ РАЗРЯД",
            "damage": 10,
            "speed": 10,
            "cooldown": 300,
            "color": (255, 0, 255)
        },
        "laser": {
            "name": "ПЛАЗМЕННЫЙ ЛАЗЕР",
            "damage": 30,
            "speed": 20,
            "cooldown": 500,
            "color": (255, 100, 100)
        }
    }
        
    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r') as f:
                    self.current = json.load(f)
            except:
                self.current = self.default_settings.copy()
        else:
            self.current = self.default_settings.copy()
            
    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.current, f, indent=4)
            
    @property
    def screen_width(self):
        return self.current["screen_width"]
    
    @property
    def screen_height(self):
        return self.current["screen_height"]