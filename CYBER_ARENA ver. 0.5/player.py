# player.py
import pygame
import math
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
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
        
        # Устанавливаем начальный спрайт (вид спереди)
        self.current_direction = "front"
        self.image = self.sprites["front"]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Параметры робота
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.energy = 100
        self.max_energy = 100
        self.damage = 10
        self.shoot_cooldown = 0
        self.shoot_delay = 200  # миллисекунды
        
        # Параметры стрельбы
        self.bullet_speed = 12
        self.bullet_damage = 15
        self.weapon_type = "bullet"
        self.last_shot_time = 0
        self.spread_angle = 15
        
        # Для анимации
        self.last_shot = 0
        self.direction = "down"
        
        # Флаг движения
        self.is_moving = False
        
    def load_sprite(self, filename):
        """Загружает спрайт игрока"""
        image_path = os.path.join("assets", "images", filename)
        
        try:
            original_image = pygame.image.load(image_path).convert_alpha()
            # Масштабируем до нужного размера (128x128)
            sprite = pygame.transform.scale(original_image, (self.size, self.size))
            return sprite
        except FileNotFoundError:
            print(f"Внимание: файл {image_path} не найден. Используется заглушка.")
            # Создаем заглушку с указанием направления
            sprite = pygame.Surface((self.size, self.size))
            
            # Цвета для разных направлений
            colors = {
                "front": (0, 255, 255),   # Голубой - вид спереди
                "back": (255, 0, 255),    # Пурпурный - вид сзади
                "left": (255, 255, 0),    # Желтый - вид слева
                "right": (0, 255, 0)      # Зеленый - вид справа
            }
            
            color = colors.get(filename.replace(".png", ""), (0, 255, 255))
            sprite.fill(color)
            
            # Рисуем стрелку для указания направления
            center = self.size // 2
            if "front" in filename:
                pygame.draw.polygon(sprite, (255, 255, 255), 
                                  [(center, self.size-20), (center-10, self.size-40), 
                                   (center+10, self.size-40)])
            elif "back" in filename:
                pygame.draw.polygon(sprite, (255, 255, 255), 
                                  [(center, 20), (center-10, 40), (center+10, 40)])
            elif "left" in filename:
                pygame.draw.polygon(sprite, (255, 255, 255), 
                                  [(20, center), (40, center-10), (40, center+10)])
            elif "right" in filename:
                pygame.draw.polygon(sprite, (255, 255, 255), 
                                  [(self.size-20, center), (self.size-40, center-10), 
                                   (self.size-40, center+10)])
            
            return sprite
            
    def update_sprite(self):
        """Обновляет спрайт в зависимости от направления движения"""
        if self.is_moving:
            # Меняем спрайт в зависимости от направления
            if self.direction == "up":
                self.image = self.sprites["back"]
            elif self.direction == "down":
                self.image = self.sprites["front"]
            elif self.direction == "left":
                self.image = self.sprites["left"]
            elif self.direction == "right":
                self.image = self.sprites["right"]
        else:
            # При остановке используем вид спереди
            self.image = self.sprites["front"]
            
    def update(self):
        # Управление
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
            dx *= 0.7071  # нормализация диагональной скорости
            dy *= 0.7071
            
        self.rect.x += dx
        self.rect.y += dy
        
        # Обновляем спрайт в зависимости от движения
        self.update_sprite()
        
        # Обновление кулдауна стрельбы
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            
    def shoot(self, target_pos, bullet_group):
        """Создает выстрел в направлении мыши"""
        from bullet import Bullet, LaserBeam
        
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = current_time
            
            if self.weapon_type == "bullet":
                self.shoot_bullet(target_pos, bullet_group)
            elif self.weapon_type == "spread":
                self.shoot_spread(target_pos, bullet_group)
            elif self.weapon_type == "laser":
                self.shoot_laser(target_pos, bullet_group)
                
            return True
        return False
    
    def shoot_bullet(self, target_pos, bullet_group):
        """Одиночный выстрел"""
        from bullet import Bullet
        
        bullet = Bullet(
            self.rect.centerx, 
            self.rect.centery,
            target_pos[0], 
            target_pos[1],
            self.bullet_damage,
            self.bullet_speed
        )
        bullet_group.add(bullet)
        
    def shoot_spread(self, target_pos, bullet_group):
        """Веерный выстрел (3 пули)"""
        from bullet import Bullet
        
        angles = [-self.spread_angle, 0, self.spread_angle]
        
        for angle in angles:
            dx = target_pos[0] - self.rect.centerx
            dy = target_pos[1] - self.rect.centery
            distance = math.sqrt(dx ** 2 + dy ** 2)
            
            if distance > 0:
                dx = dx / distance
                dy = dy / distance
                
                rad_angle = math.radians(angle)
                rotated_dx = dx * math.cos(rad_angle) - dy * math.sin(rad_angle)
                rotated_dy = dx * math.sin(rad_angle) + dy * math.cos(rad_angle)
                
                new_target_x = self.rect.centerx + rotated_dx * 100
                new_target_y = self.rect.centery + rotated_dy * 100
                
                bullet = Bullet(
                    self.rect.centerx, 
                    self.rect.centery,
                    new_target_x, 
                    new_target_y,
                    self.bullet_damage // 2,
                    self.bullet_speed
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
            self.bullet_damage * 2
        )
        bullet_group.add(laser)
    
    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0
    
    def draw_ui(self, screen, camera):
        # Отрисовка полоски здоровья
        health_bar_width = 80
        health_bar_height = 8
        health_percent = self.health / self.max_health
        
        # Позиция над игроком
        bar_x = self.rect.x + (self.rect.width - health_bar_width) // 2
        bar_y = self.rect.y - 15
        
        # Применяем камеру
        bar_rect = pygame.Rect(bar_x, bar_y, health_bar_width, health_bar_height)
        bar_rect = camera.apply(bar_rect)
        
        # Рисуем фон
        pygame.draw.rect(screen, (60, 60, 60), bar_rect)
        # Рисуем здоровье
        health_rect = pygame.Rect(bar_x, bar_y, 
                                 health_bar_width * health_percent, health_bar_height)
        health_rect = camera.apply(health_rect)
        pygame.draw.rect(screen, (0, 255, 100), health_rect)