# sound_manager.py
import pygame
import os

class SoundManager:
    def __init__(self, settings=None):
        pygame.mixer.init()
        
        # Получаем настройки
        if settings is None:
            from settings import Settings
            self.settings = Settings()
        else:
            self.settings = settings
        
        # Громкость из настроек
        self.music_volume = self.settings.music_volume
        self.sfx_volume = self.settings.sound_volume
        
        # Загрузка звуков
        self.sounds = {}
        self.music = None
        self.current_music = None
        
        self.load_sounds()
        
        # Применяем громкость
        self.set_music_volume(self.music_volume)
        self.set_sfx_volume(self.sfx_volume)
        
    def load_sounds(self):
        """Загружает все звуковые файлы"""
        sounds_folder = os.path.join("assets", "sounds")
        
        if not os.path.exists(sounds_folder):
            os.makedirs(sounds_folder)
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
                    # Сразу применяем громкость
                    self.sounds[sound_name].set_volume(self.sfx_volume)
                    print(f"Загружен звук: {sound_name}")
                except pygame.error as e:
                    print(f"Ошибка загрузки звука {file_path}: {e}")
            else:
                print(f"Файл {file_path} не найден")
                
        # Загружаем музыку
        music_extensions = ['.ogg', '.mp3', '.wav']
        for ext in music_extensions:
            music_path = os.path.join(sounds_folder, f"soundtrack{ext}")
            if os.path.exists(music_path):
                try:
                    pygame.mixer.music.load(music_path)
                    pygame.mixer.music.set_volume(self.music_volume)
                    print(f"Загружена фоновая музыка: soundtrack{ext}")
                    break
                except pygame.error as e:
                    print(f"Ошибка загрузки музыки soundtrack{ext}: {e}")
            
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