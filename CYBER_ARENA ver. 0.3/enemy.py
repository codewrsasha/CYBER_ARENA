# enemy.py
import pygame
import random
import math
import os

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player, virus_type=None):  # Добавлен параметр virus_type
        super().__init__()
        
        self.player = player
        
        # Определяем тип вируса, если не указан
        if virus_type is None:
            self.virus_type = random.choice(["trojan", "worm", "ransomware"])
        else:
            self.virus_type = virus_type
            
        # Загружаем соответствующий спрайт
        self.load_sprite()
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Характеристики в зависимости от типа
        self.set_stats()
        
        self.pulse_phase = random.uniform(0, 2 * math.pi)
        
    def load_sprite(self):
        """Загружает спрайт в зависимости от типа вируса"""
        # Соответствие типов вирусов файлам изображений
        sprite_files = {
            "trojan": "enemy.png",  # Разные файлы для разных типов
            "worm": "green.png",
            "ransomware": "orange.png"
        }
        
        # Размеры для разных типов
        sizes = {
            "trojan": 32,
            "worm": 24,
            "ransomware": 48
        }
        
        size = sizes[self.virus_type]
        filename = sprite_files[self.virus_type]
        image_path = os.path.join("assets", "images", "viruses", filename)
        
        try:
            original_image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(original_image, (size, size))
        except FileNotFoundError:
            # Если файл не найден, создаем заглушку с цветом типа вируса
            print(f"Внимание: файл {image_path} не найден. Используется заглушка.")
            self.image = pygame.Surface((size, size))
            
            # Цвета для разных типов
            colors = {
                "trojan": (255, 0, 140),    # Розовый
                "worm": (0, 255, 140),      # Зеленый
                "ransomware": (255, 100, 0)  # Оранжевый
            }
            self.image.fill(colors[self.virus_type])
            
    def set_stats(self):
        """Устанавливает характеристики в зависимости от типа"""
        stats = {
            "trojan": {
                "speed": random.uniform(1.5, 2.5),
                "health": random.randint(30, 40),
                "damage": random.randint(8, 12)
            },
            "worm": {
                "speed": random.uniform(2.5, 3.5),
                "health": random.randint(15, 25),
                "damage": random.randint(5, 8)
            },
            "ransomware": {
                "speed": random.uniform(0.8, 1.5),
                "health": random.randint(50, 70),
                "damage": random.randint(15, 20)
            }
        }
        
        s = stats[self.virus_type]
        self.speed = s["speed"]
        self.health = s["health"]
        self.max_health = self.health
        self.damage = s["damage"]
        
    def update(self):
        # Движение к игроку
        dx = self.player.rect.centerx - self.rect.centerx
        dy = self.player.rect.centery - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        
        if distance > 0:
            dx = dx / distance * self.speed
            dy = dy / distance * self.speed
            
        self.rect.x += dx
        self.rect.y += dy
        
        # Пульсация
        self.pulse_phase += 0.1
        
    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0
    
    def draw_health_bar(self, screen, camera):
        if self.health < self.max_health:
            bar_width = 30
            bar_height = 4
            health_percent = self.health / self.max_health
            
            bar_x = self.rect.x + (self.rect.width - bar_width) // 2
            bar_y = self.rect.y - 8
            
            bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
            bar_rect = camera.apply(bar_rect)
            
            pygame.draw.rect(screen, (60, 60, 60), bar_rect)
            health_rect = pygame.Rect(bar_x, bar_y, 
                                     bar_width * health_percent, bar_height)
            health_rect = camera.apply(health_rect)
            
            # Цвет полоски здоровья в зависимости от типа
            colors = {
                "trojan": (255, 0, 140),
                "worm": (0, 255, 140),
                "ransomware": (255, 100, 0)
            }
            pygame.draw.rect(screen, colors[self.virus_type], health_rect)


class EnemySpawner:
    def __init__(self, arena_width, arena_height):
        self.arena_width = arena_width
        self.arena_height = arena_height
        self.spawn_timer = 0
        self.spawn_delay = 60  # кадров
        self.max_enemies = 20
        self.wave = 1
        
    def update(self, enemies, player):
        self.spawn_timer += 1
        
        if self.spawn_timer >= self.spawn_delay and len(enemies) < self.max_enemies:
            self.spawn_timer = 0
            self.spawn_enemy(enemies, player)
            
    def set_wave(self, wave):
        """Обновляет текущую волну"""
        self.wave = wave
        # Увеличиваем сложность с волной
        self.max_enemies = min(50, 20 + wave * 3)
        self.spawn_delay = max(30, 60 - wave * 2)
            
    def spawn_enemy(self, enemies, player):
        # Спавн за границами экрана
        margin = 100
        
        # Выбираем сторону для спавна
        side = random.choice(["top", "bottom", "left", "right"])
        
        if side == "top":
            x = random.randint(0, self.arena_width)
            y = -margin
        elif side == "bottom":
            x = random.randint(0, self.arena_width)
            y = self.arena_height + margin
        elif side == "left":
            x = -margin
            y = random.randint(0, self.arena_height)
        else:  # right
            x = self.arena_width + margin
            y = random.randint(0, self.arena_height)
            
        # Убеждаемся, что координаты в пределах арены
        x = max(-margin, min(self.arena_width + margin, x))
        y = max(-margin, min(self.arena_height + margin, y))
        
        # ВЫБОР ТИПА ВРАГА В ЗАВИСИМОСТИ ОТ ВОЛНЫ
        if self.wave >= 5:
            # На волнах 5+ все типы с равной вероятностью
            virus_type = random.choice(["trojan", "worm", "ransomware"])
        elif self.wave >= 3:
            # На волнах 3-4: trojan и worm, редко ransomware
            virus_type = random.choices(
                ["trojan", "worm", "ransomware"],
                weights=[45, 45, 10],  # проценты вероятности
                k=1
            )[0]
        elif self.wave >= 2:
            # На волне 2: trojan и worm
            virus_type = random.choice(["trojan", "worm"])
        else:
            # На волне 1: только trojan
            virus_type = "trojan"
        
        # Случайное изменение характеристик для разнообразия
        enemy = Enemy(x, y, player, virus_type)
        
        # Модифицируем врага в зависимости от волны
        if self.wave > 3:
            # Увеличиваем здоровье на поздних волнах
            enemy.health = int(enemy.health * (1 + (self.wave - 3) * 0.2))
            enemy.max_health = enemy.health
            enemy.speed *= (1 + (self.wave - 3) * 0.1)
            
        enemies.add(enemy)