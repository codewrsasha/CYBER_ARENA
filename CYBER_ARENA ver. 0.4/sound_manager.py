# sound_manager.py
import pygame
import os

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        
        # Громкость (0.0 - 1.0)
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        
        # Загрузка звуков
        self.sounds = {}
        self.music = None
        self.current_music = None
        
        self.load_sounds()
        
    def load_sounds(self):
        """Загружает все звуковые файлы"""
        sounds_folder = os.path.join("assets", "sounds_folder")
        
        # Проверяем существование папки
        if not os.path.exists(sounds_folder):
            os.makedirs(sounds_folder)
            print(f"Создана папка {sounds_folder}. Поместите туда звуковые файлы")
            return
            
        # Загружаем звуковые эффекты
        sound_files = {
            "shoot": "shoot.mp3",
            "hit": "hit.mp3", 
            "player_hit": "player_hit.mp3"
        }
        
        for sound_name, filename in sound_files.items():
            file_path = os.path.join(sounds_folder, filename)
            if os.path.exists(file_path):
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(file_path)
                    print(f"Загружен звук: {sound_name}")
                except:
                    print(f"Ошибка загрузки звука {file_path}")
            else:
                print(f"Файл {file_path} не найден")
                
        # Загружаем музыку
        music_path = os.path.join(sounds_folder, "soundtrack.ogg")
        if os.path.exists(music_path):
            pygame.mixer.music.load(music_path)
            print("Загружена фоновая музыка")
        else:
            print(f"Файл {music_path} не найден")
            
    def play_sound(self, sound_name):
        """Воспроизводит звуковой эффект"""
        if sound_name in self.sounds:
            self.sounds[sound_name].set_volume(self.sfx_volume)
            self.sounds[sound_name].play()
            
    def play_music(self, loop=True):
        """Воспроизводит фоновую музыку"""
        if pygame.mixer.music.get_busy():
            return
        pygame.mixer.music.set_volume(self.music_volume)
        if loop:
            pygame.mixer.music.play(-1)  # -1 = бесконечное повторение
        else:
            pygame.mixer.music.play()
            
    def stop_music(self):
        """Останавливает музыку"""
        pygame.mixer.music.stop()
        
    def pause_music(self):
        """Ставит музыку на паузу"""
        pygame.mixer.music.pause()
        
    def unpause_music(self):
        """Снимает музыку с паузы"""
        pygame.mixer.music.unpause()
        
    def set_music_volume(self, volume):
        """Устанавливает громкость музыки"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
        
    def set_sfx_volume(self, volume):
        """Устанавливает громкость звуковых эффектов"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
            
    def play_shoot(self):
        """Воспроизводит звук выстрела"""
        self.play_sound("shoot")
        
    def play_hit(self):
        """Воспроизводит звук попадания"""
        self.play_sound("hit")
        
    def play_player_hit(self):
        """Воспроизводит звук поражения игрока"""
        self.play_sound("player_hit")