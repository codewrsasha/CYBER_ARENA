# main.py 
import pygame
import sys
import os
from settings import Settings
from menu import Menu
from game import Game
from localization import localization
from tutorial import Tutorial
from statistics_menu import StatisticsMenu

class CyberArena:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.settings = Settings()
        
        # Применяем сохраненные настройки окна
        self.screen = self.settings.apply_settings()
        
        pygame.display.set_caption(self.settings.GAME_TITLE)
        
        # Проверка наличия папок
        self.check_asset_folders()
        self.check_player_sprites()
        
        # Инициализация меню с передачей настроек
        self.menu = Menu(self.screen, self.settings)
        self.clock = pygame.time.Clock()
        
        # Применяем сохраненную громкость
        from sound_manager import SoundManager
        self.temp_sound = SoundManager()
        self.temp_sound.set_music_volume(self.settings.music_volume)
        self.temp_sound.set_sfx_volume(self.settings.sound_volume)
        
        print(f"Текущий язык: {localization.current_lang}")
        print(f"Разрешение экрана: {self.settings.screen_width}x{self.settings.screen_height}")
        print(f"Полноэкранный режим: {self.settings.fullscreen}")
        print(f"Громкость музыки: {self.settings.music_volume}")
        print(f"Громкость эффектов: {self.settings.sound_volume}")

    def restart_game(self):
        """Перезапускает игру с новыми настройками"""
        # Сохраняем настройки перед перезапуском
        self.settings.save_settings()
        
        # Создаем новое окно с новыми настройками
        self.screen = self.settings.apply_settings()
        pygame.display.set_caption(self.settings.GAME_TITLE)
        
        # Обновляем меню с новым экраном
        self.menu.screen = self.screen
        self.menu.hex_bg.screen_width = self.settings.screen_width
        self.menu.hex_bg.screen_height = self.settings.screen_height
        self.menu.hex_bg.hexes.clear()
        self.menu.hex_bg.generate_hexes()
        
        print(f"Настройки применены: {self.settings.screen_width}x{self.settings.screen_height}, "
              f"Fullscreen: {self.settings.fullscreen}")
        
    def check_asset_folders(self):
        """Создает необходимые папки, если их нет"""
        folders = [
            "assets",
            "assets/images",
            "assets/images/viruses",
            "assets/sounds",
            "assets/fonts"
        ]
        
        for folder in folders:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"Создана папка: {folder}")
                
    def check_player_sprites(self):
        """Проверяет наличие спрайтов игрока"""
        required_sprites = [
            "player_front.png",
            "player_back.png", 
            "player_left.png",
            "player_right.png"
        ]
        
        missing_sprites = []
        for sprite in required_sprites:
            sprite_path = os.path.join("assets", "images", sprite)
            if not os.path.exists(sprite_path):
                missing_sprites.append(sprite)
                
        if missing_sprites:
            print("ВНИМАНИЕ: Отсутствуют следующие спрайты игрока:")
            for sprite in missing_sprites:
                print(f"  - {sprite}")
        else:
            print("Все спрайты игрока загружены")
        
    def run(self):
        while True:
            choice = self.menu.main_menu()
            
            if choice == "play":
                game_instance = Game(self.screen, self.settings)
                game_instance.run_game()
                self.menu = Menu(self.screen, self.settings)
            elif choice == "tutorial":
                tutorial = Tutorial(self.screen, self.settings)
                tutorial.show()
            elif choice == "statistics":
                stats_menu = StatisticsMenu(self.screen, self.settings)
                stats_menu.show()
            elif choice == "settings":
                self.menu.settings_menu()
                self.screen = pygame.display.set_mode((self.settings.screen_width,
                                                    self.settings.screen_height))
                pygame.display.set_caption(self.settings.GAME_TITLE)
                self.menu.screen = self.screen
                self.menu.settings = self.settings
                self.menu.hex_bg.screen_width = self.settings.screen_width
                self.menu.hex_bg.screen_height = self.settings.screen_height
                self.menu.hex_bg.hexes.clear()
                self.menu.hex_bg.generate_hexes()
                
if __name__ == "__main__":
    game = CyberArena()
    game.run()
    pygame.quit()
    sys.exit()