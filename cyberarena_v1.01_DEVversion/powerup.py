# powerup.py
import pygame
import math
import os
import random

class PowerUp(pygame.sprite.Sprite):
    """Базовый класс для всех бонусов"""
    def __init__(self, x, y, powerup_type, image_name):
        super().__init__()
        
        self.type = powerup_type
        self.x = x
        self.y = y
        
        # Загружаем изображение
        self.load_image(image_name)
        
        self.rect = self.image.get_rect(center=(x, y))
        
        # Эффект мерцания
        self.pulse_phase = random.uniform(0, 2 * math.pi)
        self.visible = True
        
        # Время жизни бонуса (30 секунд)
        self.lifetime = 1800
        self.spawn_time = pygame.time.get_ticks()
        
    def load_image(self, image_name):
        """Загружает изображение бонуса"""
        image_path = os.path.join("assets", "images", image_name)
        
        try:
            original_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(original_image, (64, 64))
        except FileNotFoundError:
            # Заглушка
            self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
            colors = {
                "health_small": (0, 255, 0),
                "health_big": (0, 255, 0),
                "damage_up": (255, 0, 0),
                "infinite_ammo": (0, 0, 255),
                "speed_boost": (255, 255, 0)
            }
            color = colors.get(self.type, (255, 255, 255))
            pygame.draw.circle(self.image, color, (32, 32), 30)
            pygame.draw.circle(self.image, (255, 255, 255), (32, 32), 30, 2)
            
    def update(self):
        """Обновляет эффект мерцания и проверяет время жизни"""
        self.pulse_phase += 0.1
        # Мерцание: видимость меняется
        self.visible = (math.sin(self.pulse_phase) > 0)
        
        # Проверяем время жизни
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime * 1000 // 60:
            self.kill()
        
    def draw(self, screen, camera):
        """Рисует бонус с эффектом мерцания"""
        if self.visible:
            screen.blit(self.image, camera.apply(self))


class HealthSmall(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, "health_small", "health_small.png")
        self.heal_amount = 20
        
    def apply(self, player):
        player.health = min(player.max_health, player.health + self.heal_amount)
        print(f"Подобран бонус: +{self.heal_amount} HP")  # Отладка
        return f"+{self.heal_amount} HP"


class HealthBig(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, "health_big", "health_big.png")
        self.heal_amount = 100
        
    def apply(self, player):
        player.health = min(player.max_health, player.health + self.heal_amount)
        print(f"Подобран бонус: +{self.heal_amount} HP")  # Отладка
        return f"+{self.heal_amount} HP"


class DamageUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, "damage_up", "damage_up.png")
        self.duration = 1800  # 30 секунд (60 FPS * 30)
        self.damage_multiplier = 2
        
    def apply(self, player):
        player.activate_damage_boost(self.duration, self.damage_multiplier)
        print("Подобран бонус: УРОН x2 на 30 секунд")  # Отладка
        return "DAMAGE x2 (30s)"


class InfiniteAmmo(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, "infinite_ammo", "infinite_ammo.png")
        self.duration = 1800
        
    def apply(self, player):
        player.activate_infinite_ammo(self.duration)
        print("Подобран бонус: БЕСКОНЕЧНЫЕ ПАТРОНЫ на 30 секунд")  # Отладка
        return "INFINITE AMMO (30s)"


class SpeedBoost(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y, "speed_boost", "speed_boost.png")
        self.duration = 1800
        self.speed_multiplier = 2
        
    def apply(self, player):
        player.activate_speed_boost(self.duration, self.speed_multiplier)
        print("Подобран бонус: СКОРОСТЬ x2 на 30 секунд")  # Отладка
        return "SPEED x2 (30s)"


class PowerUpSpawner:
    def __init__(self, max_powerups=5):
        self.max_powerups = max_powerups
        self.powerups = pygame.sprite.Group()
        
    def spawn_powerup(self, x, y, enemy_type):
        """Спавнит бонус при убийстве врага"""
        # Проверяем лимит бонусов на поле
        if len(self.powerups) >= self.max_powerups:
            print(f"Лимит бонусов ({self.max_powerups}) достигнут")  # Отладка
            return None
            
        # Генерируем случайное число от 0 до 100
        random_chance = random.random() * 100
        print(f"Шанс выпадения: {random_chance:.1f}%, тип врага: {enemy_type}")  # Отладка
        
        # Health Small (20% с любого врага)
        if random_chance < 20:
            print("Спавн: Health Small")  # Отладка
            powerup = HealthSmall(x, y)
            self.powerups.add(powerup)
            return powerup
            
        # Health Big (5% с любого врага) - следующий шанс 20-25%
        elif random_chance < 25:
            print("Спавн: Health Big")  # Отладка
            powerup = HealthBig(x, y)
            self.powerups.add(powerup)
            return powerup
            
        # Специфичные бонусы от типов врагов (5% шанс)
        if enemy_type == "ransomware" and random_chance < 30:  # 25-30%
            print("Спавн: Damage Up (от Ransomware)")  # Отладка
            powerup = DamageUp(x, y)
            self.powerups.add(powerup)
            return powerup
        elif enemy_type == "worm" and random_chance < 30:
            print("Спавн: Infinite Ammo (от Worm)")  # Отладка
            powerup = InfiniteAmmo(x, y)
            self.powerups.add(powerup)
            return powerup
        elif enemy_type == "trojan" and random_chance < 30:
            print("Спавн: Speed Boost (от Trojan)")  # Отладка
            powerup = SpeedBoost(x, y)
            self.powerups.add(powerup)
            return powerup
            
        print("Бонус не выпал")  # Отладка
        return None
        
    def update(self):
        self.powerups.update()
        
    def draw(self, screen, camera):
        for powerup in self.powerups:
            powerup.draw(screen, camera)
            
    def check_collisions(self, player):
        """Проверяет сбор бонусов игроком"""
        collected = []
        for powerup in self.powerups:
            if player.rect.colliderect(powerup.rect):
                print(f"Игрок собрал бонус: {powerup.type}")  # Отладка
                message = powerup.apply(player)
                collected.append(powerup)
                
        for powerup in collected:
            self.powerups.remove(powerup)
            
        return collected