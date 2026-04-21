# localization.py
import json
import os

class Localization:
    def __init__(self):
        self.language_file = "language.json"
        self.current_lang = "en"  # По умолчанию английский
        self.strings = {}
        
        # Загружаем сохраненный язык
        self.load_language_setting()
        
        # Загружаем строки для обоих языков
        self.load_strings()
        
    def load_language_setting(self):
        """Загружает сохраненный язык из файла"""
        if os.path.exists(self.language_file):
            try:
                with open(self.language_file, 'r') as f:
                    data = json.load(f)
                    self.current_lang = data.get("language", "en")
                    print(f"Загружен язык: {self.current_lang}")
            except:
                self.current_lang = "en"
        else:
            self.current_lang = "en"
            
    def save_language_setting(self):
        """Сохраняет текущий язык в файл"""
        with open(self.language_file, 'w') as f:
            json.dump({"language": self.current_lang}, f)
            
    def load_strings(self):
        """Загружает все текстовые строки"""
        self.strings = {
            "en": {
                # Меню
                "game_title": "CYBER ARENA",
                "subtitle": "=== VIRUS PROTOCOL ===",
                "play": "> INITIALIZATION <",
                "settings": "> SETTINGS <",
                "exit": "> EXIT <",
                "settings_title": "SYSTEM SETTINGS",
                "resolution": "RESOLUTION",
                "music": "MUSIC",
                "sfx": "SOUND EFFECTS",
                "back": "> BACK <",
                
                # HUD
                "wave": "WAVE",
                "points": "POINTS",
                "systems": "SYSTEMS",
                "viruses": "VIRUSES",
                "weapon": "WEAPON",
                "ammo": "AMMO",
                "damage": "DAMAGE",
                "reloading": "RELOADING...",
                "controls_hint": "1-4: CHANGE WEAPON | R: RELOAD",
                "game_over": "SYSTEM COMPROMISED",
                "viruses_destroyed": "VIRUSES DESTROYED",
                
                # Оружие
                "weapon_standard": "STANDARD BLASTER",
                "weapon_rapid": "RAPID BLASTER",
                "weapon_shotgun": "SPREAD SHOT",
                "weapon_laser": "PLASMA LASER",

                # Новые строки для настроек
                "settings_resolution": "RESOLUTION:",
                "settings_screen_type": "SCREEN TYPE:",
                "settings_window": "WINDOW",
                "settings_fullscreen": "FULLSCREEN",
                "settings_music": "MUSIC:",
                "settings_sfx": "SOUND EFFECTS:",
                "settings_apply": "> APPLY <",
                "settings_back": "> BACK <",
                "settings_restart_warning": "! SETTINGS APPLY REQUIRES GAME RESTART !",
                "settings_apply_warning": "! PRESS 'APPLY' TO SAVE SETTINGS ! THEN RESTART GAME !",

                # Типы экрана для настроек
                "screen_window": "WINDOW",
                "screen_fullscreen": "FULLSCREEN",
            },
            "ru": {
                # Меню
                "game_title": "CYBER ARENA",
                "subtitle": "=== ВИРУСНЫЙ ПРОТОКОЛ ===",
                "play": "> ИНИЦИАЛИЗАЦИЯ <",
                "settings": "> НАСТРОЙКИ <",
                "exit": "> ВЫХОД <",
                "settings_title": "НАСТРОЙКИ СИСТЕМЫ",
                "resolution": "РАЗРЕШЕНИЕ",
                "music": "МУЗЫКА",
                "sfx": "ЭФФЕКТЫ",
                "back": "> НАЗАД <",
                
                # HUD
                "wave": "ВОЛНА",
                "points": "ОЧКИ",
                "systems": "СИСТЕМЫ",
                "viruses": "ВИРУСЫ",
                "weapon": "ОРУЖИЕ",
                "ammo": "ПАТРОНЫ",
                "damage": "УРОН",
                "reloading": "ПЕРЕЗАРЯДКА...",
                "controls_hint": "1-4: СМЕНА ОРУЖИЯ | R: ПЕРЕЗАРЯДКА",
                "game_over": "СИСТЕМА СКОМПРОМЕТИРОВАНА",
                "viruses_destroyed": "ВИРУСОВ УНИЧТОЖЕНО",
                
                # Оружие
                "weapon_standard": "СТАНДАРТНЫЙ БЛАСТЕР",
                "weapon_rapid": "СКОРОСТНОЙ БЛАСТЕР",
                "weapon_shotgun": "ВЕЕРНЫЙ РАЗРЯД",
                "weapon_laser": "ПЛАЗМЕННЫЙ ЛАЗЕР",

                # Новые строки для настроек
                "settings_resolution": "РАЗРЕШЕНИЕ:",
                "settings_screen_type": "ТИП ЭКРАНА:",
                "settings_window": "В ОКНЕ",
                "settings_fullscreen": "ВО ВЕСЬ ЭКРАН",
                "settings_music": "МУЗЫКА:",
                "settings_sfx": "ЭФФЕКТЫ:",
                "settings_apply": "> ПРИМЕНИТЬ <",
                "settings_back": "> НАЗАД <",
                "settings_restart_warning": "! ПРИМЕНЕНИЕ НАСТРОЕК ТРЕБУЕТ ПЕРЕЗАПУСКА ИГРЫ !",
                "settings_apply_warning": "! НАЖМИТЕ 'ПРИМЕНИТЬ' ДЛЯ СОХРАНЕНИЯ НАСТРОЕК ! ПОСЛЕ ЧЕГО ПЕРЕЗАЙДИТЕ В ИГРУ !",

                # Типы экрана для настроек
                "screen_window": "В ОКНЕ",
                "screen_fullscreen": "ВО ВЕСЬ ЭКРАН",
            }
        }
        
    def get_text(self, key):
        """Возвращает текст для текущего языка"""
        if key in self.strings[self.current_lang]:
            return self.strings[self.current_lang][key]
        return key
        
    def set_language(self, lang):
        """Устанавливает язык"""
        if lang in ["en", "ru"]:
            self.current_lang = lang
            self.save_language_setting()
            return True
        return False
        
    def toggle_language(self):
        """Переключает язык между EN и RU"""
        if self.current_lang == "en":
            self.set_language("ru")
        else:
            self.set_language("en")
            
# Создаем глобальный экземпляр
localization = Localization()