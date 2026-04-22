# statistics.py
import json
import os

class Statistics:
    def __init__(self):
        self.stats_file = "statistics.json"
        self.stats = self.load_stats()
        
    def load_stats(self):
        """Загружает статистику из файла"""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except:
                return self.get_default_stats()
        else:
            return self.get_default_stats()
            
    def get_default_stats(self):
        """Возвращает статистику по умолчанию"""
        return {
            "max_wave": 0,
            "max_score": 0,
            "max_kills_per_session": 0,
            "total_kills": 0,
            "kills_trojan": 0,
            "kills_worm": 0,
            "kills_ransomware": 0,
            "damage_standard": 0,
            "damage_rapid": 0,
            "damage_shotgun": 0,
            "damage_laser": 0
        }
        
    def save_stats(self):
        """Сохраняет статистику в файл"""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.stats, f, indent=4)
            print("Статистика сохранена")
        except Exception as e:
            print(f"Ошибка сохранения статистики: {e}")
            
    def update_session_stats(self, wave, score, kills, kills_by_type, damage_by_weapon):
        """Обновляет статистику после игровой сессии"""
        # Максимальная волна
        if wave > self.stats["max_wave"]:
            self.stats["max_wave"] = wave
            
        # Максимальное количество очков
        if score > self.stats["max_score"]:
            self.stats["max_score"] = score
            
        # Максимальное количество убийств за сессию
        if kills > self.stats["max_kills_per_session"]:
            self.stats["max_kills_per_session"] = kills
            
        # Общее количество убийств
        self.stats["total_kills"] += kills
        
        # Убийства по типам
        self.stats["kills_trojan"] += kills_by_type.get("trojan", 0)
        self.stats["kills_worm"] += kills_by_type.get("worm", 0)
        self.stats["kills_ransomware"] += kills_by_type.get("ransomware", 0)
        
        # Урон по оружию
        self.stats["damage_standard"] += damage_by_weapon.get("standard", 0)
        self.stats["damage_rapid"] += damage_by_weapon.get("rapid", 0)
        self.stats["damage_shotgun"] += damage_by_weapon.get("shotgun", 0)
        self.stats["damage_laser"] += damage_by_weapon.get("laser", 0)
        
        self.save_stats()
        
    def reset_stats(self):
        """Сбрасывает всю статистику"""
        self.stats = self.get_default_stats()
        self.save_stats()
        
    def get_stats(self):
        """Возвращает текущую статистику"""
        return self.stats

# Глобальный экземпляр статистики
statistics = Statistics()