# main.py
import pygame
import sys
import os
from settings import Settings
from menu import Menu
from game import Game

class CyberArena:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        pygame.display.set_caption(self.settings.GAME_TITLE)
        
        # Проверка наличия папок для ассетов
        self.check_asset_folders()
        
        # Инициализация меню
        self.menu = Menu(self.screen)
        self.clock = pygame.time.Clock()
        
    def check_asset_folders(self):
        """Создает необходимые папки, если их нет"""
        folders = [
            "assets",
            "assets/images",
            "assets/images/viruses",
            "assets/fonts"
        ]
        
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"Создана папка: {folder}")
        
    def run(self):
        while True:
            # Показываем главное меню
            choice = self.menu.main_menu()
            
            if choice == "play":
                # Запускаем игру
                game = Game(self.screen)
                game.run()
            elif choice == "settings":
                self.menu.settings_menu()
                # Обновляем размер экрана после изменения настроек
                self.screen = pygame.display.set_mode((self.settings.screen_width,
                                                       self.settings.screen_height))
                self.menu.screen = self.screen
                
if __name__ == "__main__":
    game = CyberArena()
    game.run()
    pygame.quit()
    sys.exit()