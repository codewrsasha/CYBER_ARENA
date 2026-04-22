# player.py
import pygame
import math
import os

class Player(pygame.sprite.Sprite):

    @property
    def position(self):
        return (self.rect.x, self.rect.y)

    @position.setter
    def position(self, value):
        self.rect.x, self.rect.y = value

    def __init__(self, x, y, game_speed=True):
        super().__init__()
        
        # Размеры игрока 128x128
        self.size = 128
        
        # Загрузка спрайтов для разных направлений
        self.sprites = {
            "front": self.load_sprite("player_front.png"),
            "back": self.load_sprite("player_back.png"),
            "left": self.load_sprite("player_left.png"),
            "right": self.load_sprite("player_right.png")
        }
        
        # Устанавливаем начальный спрайт
        self.current_direction = "front"
        self.image = self.sprites["front"]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Параметры игрока
        self.speed = 5    
        self.original_speed = self.speed
        self.health = 100
        self.max_health = 100
        
        # Система оружия
        self.weapons = {
            "standard": {
                "name": "СТАНДАРТНЫЙ БЛАСТЕР",
                "damage": 15,
                "bullet_speed": 12,
                "fire_delay": 200,  # мс между выстрелами
                "ammo": 12,
                "max_ammo": 12,
                "reload_time": 60,  # 1 секунда (60 FPS)
                "bullet_count": 1,  # количество пуль за выстрел
                "spread": 0,  # разброс в градусах
                "color": (0, 255, 255)  # голубой
            },
            "rapid": {
                "name": "СКОРОСТНОЙ БЛАСТЕР",
                "damage": 8,
                "bullet_speed": 15,
                "fire_delay": 100,  # быстрее стрельба
                "ammo": 30,
                "max_ammo": 30,
                "reload_time": 90,  # 1.5 секунды
                "bullet_count": 3,  # 3 пули за выстрел
                "spread": 3,  # маленький разброс
                "color": (0, 255, 0)  # зеленый
            },
            "shotgun": {
                "name": "ВЕЕРНЫЙ РАЗРЯД",
                "damage": 12,
                "bullet_speed": 10,
                "fire_delay": 400,  # медленная стрельба
                "ammo": 5,
                "max_ammo": 5,
                "reload_time": 120,  # 2 секунды
                "bullet_count": 5,  # 5 пуль за выстрел
                "spread": 20,  # большой разброс
                "color": (255, 0, 255)  # пурпурный
            },
            "laser": {
                "name": "ЛАЗЕР",
                "damage": 40,
                "bullet_speed": 20,
                "fire_delay": 500,  # очень медленная стрельба
                "ammo": 1,
                "max_ammo": 1,
                "reload_time": 180,  # 3 секунды
                "bullet_count": 1,
                "spread": 0,
                "color": (255, 100, 100)  # красный
            }
        }
        
        # Текущее оружие
        self.current_weapon = "standard"
        self.weapon_data = self.weapons[self.current_weapon].copy()
        
        # Состояние стрельбы
        self.last_shot_time = 0
        self.is_reloading = False
        self.reload_progress = 0
        self.reload_start_time = 0
        
        # Для анимации
        self.direction = "down"
        self.is_moving = False
        
        # Для эффекта мерцания
        self.invincible_frames = 0
        self.invincible_duration = 30
        self.visible = True

        # Эффекты усилений
        self.damage_boost_active = False
        self.damage_boost_timer = 0
        self.damage_multiplier = 1
        self.original_damage = self.weapon_data["damage"]
        
        self.infinite_ammo_active = False
        self.infinite_ammo_timer = 0
        
        self.speed_boost_active = False
        self.speed_boost_timer = 0
        self.speed_multiplier = 1
        self.original_speed = self.speed
        
        # Получаем размеры арены
        from settings import Settings
        self.settings = Settings()

    def set_speed(self, speed):
        """Устанавливает скорость игрока (для обучения)"""
        self.speed = speed
        self.original_speed = speed

    def activate_damage_boost(self, duration, multiplier):
        """Активирует усиление урона"""
        self.damage_boost_active = True
        self.damage_boost_timer = duration
        self.damage_multiplier = multiplier
        # Обновляем урон для всех видов оружия
        for weapon in self.weapons.values():
            weapon["damage"] = weapon["damage"] * multiplier
        self.weapon_data["damage"] = self.weapon_data["damage"] * multiplier
        
    def activate_infinite_ammo(self, duration):
        """Активирует бесконечные патроны"""
        self.infinite_ammo_active = True
        self.infinite_ammo_timer = duration
        
    def activate_speed_boost(self, duration, multiplier):
        """Активирует усиление скорости"""
        self.speed_boost_active = True
        self.speed_boost_timer = duration
        self.speed_multiplier = multiplier
        self.speed = self.original_speed * multiplier
        
    def update_effects(self):
        """Обновляет таймеры эффектов"""
        if self.damage_boost_active:
            self.damage_boost_timer -= 1
            if self.damage_boost_timer <= 0:
                # Деактивируем усиление урона
                self.damage_boost_active = False
                self.damage_multiplier = 1
                # Восстанавливаем оригинальный урон
                for weapon in self.weapons.values():
                    weapon["damage"] = weapon["damage"] // 2
                self.weapon_data["damage"] = self.original_damage
                
        if self.infinite_ammo_active:
            self.infinite_ammo_timer -= 1
            if self.infinite_ammo_timer <= 0:
                self.infinite_ammo_active = False
                
        if self.speed_boost_active:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.speed_boost_active = False
                self.speed = self.original_speed
        
    def load_sprite(self, filename):
        """Загружает спрайт игрока"""
        image_path = os.path.join("assets", "images", filename)
        
        try:
            original_image = pygame.image.load(image_path).convert_alpha()
            sprite = pygame.transform.scale(original_image, (self.size, self.size))
            return sprite
        except FileNotFoundError:
            print(f"Внимание: файл {image_path} не найден. Используется заглушка.")
            sprite = pygame.Surface((self.size, self.size))
            sprite.fill((0, 255, 255))
            return sprite
            
    def switch_weapon(self, weapon_name):
        """Смена оружия"""
        if weapon_name in self.weapons and weapon_name != self.current_weapon:
            # Сохраняем текущие патроны если были
            if hasattr(self, 'weapon_data'):
                self.weapons[self.current_weapon]["ammo"] = self.weapon_data["ammo"]
            
            self.current_weapon = weapon_name
            self.weapon_data = self.weapons[self.current_weapon].copy()
            self.is_reloading = False
            print(f"Оружие сменено на: {weapon_name}")  # Отладка
            
    def update_sprite(self):
        """Обновляет спрайт в зависимости от направления движения"""
        if self.is_moving:
            if self.direction == "up":
                self.image = self.sprites["back"]
            elif self.direction == "down":
                self.image = self.sprites["front"]
            elif self.direction == "left":
                self.image = self.sprites["left"]
            elif self.direction == "right":
                self.image = self.sprites["right"]
        else:
            self.image = self.sprites["front"]
            
    def update(self):
        # Управление движением
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        self.is_moving = False
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed
            self.direction = "up"
            self.is_moving = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed
            self.direction = "down"
            self.is_moving = True
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
            self.direction = "left"
            self.is_moving = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed
            self.direction = "right"
            self.is_moving = True
            
        # Диагональное движение
        if dx != 0 and dy != 0:
            dx *= 0.7071
            
        # Проверка границ
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy
        
        if 0 <= new_x <= self.settings.ARENA_WIDTH - self.rect.width:
            self.rect.x = new_x
        if 0 <= new_y <= self.settings.ARENA_HEIGHT - self.rect.height:
            self.rect.y = new_y
            
        # Обновляем спрайт
        self.update_sprite()

        # Обновляем эффекты
        self.update_effects()
        
        # Обновление перезарядки
        if self.is_reloading:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.reload_start_time
            reload_duration = self.weapon_data["reload_time"] * (1000 / 60)  # конвертируем в мс
            
            if elapsed >= reload_duration:
                # Перезарядка завершена
                self.weapon_data["ammo"] = self.weapon_data["max_ammo"]
                self.is_reloading = False
                self.reload_progress = 0
            else:
                self.reload_progress = min(1.0, elapsed / reload_duration)
        
        # Обновление мерцания
        if self.invincible_frames > 0:
            self.invincible_frames -= 1
            self.visible = (self.invincible_frames // 3) % 2 == 0
        else:
            self.visible = True
            
    def shoot(self, target_pos, bullet_group):
        """Стрельба из текущего оружия"""
        from bullet import Bullet, LaserBeam
        
        current_time = pygame.time.get_ticks()
        
        # Проверяем перезарядку
        if self.is_reloading:
            return False
            
        # Проверяем кулдаун
        if current_time - self.last_shot_time < self.weapon_data["fire_delay"]:
            return False
            
        # Проверяем патроны
        if not self.infinite_ammo_active and self.weapon_data["ammo"] <= 0:
            self.start_reload()
            return False
            
        # Стреляем
        if self.current_weapon == "laser":
            self.shoot_laser(target_pos, bullet_group)
        else:
            self.shoot_bullets(target_pos, bullet_group)
            
        # Уменьшаем патроны
        if not self.infinite_ammo_active:
            self.weapon_data["ammo"] -= 1
            
        self.last_shot_time = current_time
        
        # Автоматическая перезарядка
        if not self.infinite_ammo_active and self.weapon_data["ammo"] <= 0:
            self.start_reload()
            
        return True
        
    def shoot_bullets(self, target_pos, bullet_group):
        """Стрельба несколькими пулями с разбросом"""
        from bullet import Bullet
        
        bullet_count = self.weapon_data["bullet_count"]
        spread = self.weapon_data["spread"]
        
        for i in range(bullet_count):
            # Рассчитываем направление с разбросом
            if bullet_count > 1 and spread > 0:
                # Для веерного огня распределяем пули веером
                if bullet_count == 3:  # скоростной бластер
                    angle_offset = -spread + (i * spread * 2 / (bullet_count - 1))
                else:  # дробовик
                    angle_offset = -spread + (i * spread * 2 / (bullet_count - 1))
                    
                dx = target_pos[0] - self.rect.centerx
                dy = target_pos[1] - self.rect.centery
                distance = math.sqrt(dx ** 2 + dy ** 2)
                
                if distance > 0:
                    dx = dx / distance
                    dy = dy / distance
                    
                    rad_angle = math.radians(angle_offset)
                    rotated_dx = dx * math.cos(rad_angle) - dy * math.sin(rad_angle)
                    rotated_dy = dx * math.sin(rad_angle) + dy * math.cos(rad_angle)
                    
                    new_target_x = self.rect.centerx + rotated_dx * 100
                    new_target_y = self.rect.centery + rotated_dy * 100
                    
                    bullet = Bullet(
                        self.rect.centerx, 
                        self.rect.centery,
                        new_target_x, 
                        new_target_y,
                        self.weapon_data["damage"],
                        self.weapon_data["bullet_speed"]
                    )
                    bullet_group.add(bullet)
            else:
                # Одиночный выстрел
                bullet = Bullet(
                    self.rect.centerx, 
                    self.rect.centery,
                    target_pos[0], 
                    target_pos[1],
                    self.weapon_data["damage"],
                    self.weapon_data["bullet_speed"]
                )
                bullet_group.add(bullet)
                
    def shoot_laser(self, target_pos, bullet_group):
        """Лазерный выстрел"""
        from bullet import LaserBeam
        
        laser = LaserBeam(
            self.rect.centerx,
            self.rect.centery,
            target_pos[0],
            target_pos[1],
            self.weapon_data["damage"]
        )
        bullet_group.add(laser)
        
    def start_reload(self):
        """Начинает перезарядку"""
        if not self.is_reloading and self.weapon_data["ammo"] < self.weapon_data["max_ammo"]:
            self.is_reloading = True
            self.reload_start_time = pygame.time.get_ticks()
            self.reload_progress = 0
            
    def take_damage(self, amount):
        """Получение урона с неуязвимостью"""
        if self.invincible_frames <= 0:
            self.health -= amount
            self.invincible_frames = self.invincible_duration
            return self.health <= 0
        return False
        
    def draw_reload_bar(self, screen, camera):
        """Рисует полоску перезарядки над игроком"""
        if self.is_reloading:
            bar_width = 80
            bar_height = 6
            bar_x = self.rect.x + (self.rect.width - bar_width) // 2
            bar_y = self.rect.y - 25
            
            # Применяем камеру
            bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
            bar_rect = camera.apply(bar_rect)
            
            # Фон полоски
            pygame.draw.rect(screen, (60, 60, 60), bar_rect)
            
            # Полоска перезарядки (цвет оружия)
            reload_rect = pygame.Rect(bar_x, bar_y, 
                                     bar_width * self.reload_progress, bar_height)
            reload_rect = camera.apply(reload_rect)
            pygame.draw.rect(screen, self.weapon_data["color"], reload_rect)
            
    def draw_ammo_bar(self, screen, camera):
        """Рисует полоску боезапаса над игроком"""
        bar_width = 80
        bar_height = 4
        bar_x = self.rect.x + (self.rect.width - bar_width) // 2
        bar_y = self.rect.y - 20
        
        # Применяем камеру
        bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        bar_rect = camera.apply(bar_rect)
        
        # Фон
        pygame.draw.rect(screen, (60, 60, 60), bar_rect)
        
        # Полоска патронов
        ammo_percent = self.weapon_data["ammo"] / self.weapon_data["max_ammo"]
        ammo_rect = pygame.Rect(bar_x, bar_y, 
                               bar_width * ammo_percent, bar_height)
        ammo_rect = camera.apply(ammo_rect)
        pygame.draw.rect(screen, self.weapon_data["color"], ammo_rect)
        
    def draw_ui(self, screen, camera):
        # Полоска здоровья
        health_bar_width = 80
        health_bar_height = 8
        health_percent = self.health / self.max_health
        
        bar_x = self.rect.x + (self.rect.width - health_bar_width) // 2
        bar_y = self.rect.y - 15
        
        bar_rect = pygame.Rect(bar_x, bar_y, health_bar_width, health_bar_height)
        bar_rect = camera.apply(bar_rect)
        
        pygame.draw.rect(screen, (60, 60, 60), bar_rect)
        health_rect = pygame.Rect(bar_x, bar_y, 
                                 health_bar_width * health_percent, health_bar_height)
        health_rect = camera.apply(health_rect)
        pygame.draw.rect(screen, (0, 255, 100), health_rect)
        
        # Полоска патронов и перезарядки
        self.draw_ammo_bar(screen, camera)
        self.draw_reload_bar(screen, camera)