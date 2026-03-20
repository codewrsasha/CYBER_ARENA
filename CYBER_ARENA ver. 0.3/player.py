# player.py
import pygame
import math
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Загрузка изображения игрока
        image_path = os.path.join("assets", "images", "player.png")
        try:
            # Загружаем изображение и конвертируем для лучшей производительности
            original_image = pygame.image.load(image_path).convert_alpha()
            # Масштабируем до нужного размера (например, 48x48)
            self.image = pygame.transform.scale(original_image, (48, 48))
        except FileNotFoundError:
            # Если файл не найден, создаем заглушку
            print(f"Внимание: файл {image_path} не найден. Используется заглушка.")
            self.image = pygame.Surface((48, 48))
            self.image.fill((0, 255, 255))  # Голубой цвет робота


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
        
        # Для анимации
        self.last_shot = 0
        self.direction = "down"

        # Параметры стрельбы
        self.shoot_cooldown = 0
        self.shoot_delay = 200  # миллисекунды
        self.bullet_speed = 12
        self.bullet_damage = 15
        self.weapon_type = "bullet"  # bullet, laser, spread
        self.last_shot_time = 0
        
        # Для оружия с разбросом
        self.spread_angle = 15  # градусов
        
    def update(self):
        # Управление
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= self.speed
            self.direction = "up"
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += self.speed
            self.direction = "down"
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= self.speed
            self.direction = "left"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += self.speed
            self.direction = "right"
            
        # Диагональное движение
        if dx != 0 and dy != 0:
            dx *= 0.7071  # нормализация диагональной скорости
            dy *= 0.7071
            
        self.rect.x += dx
        self.rect.y += dy
        
        # Обновление кулдауна стрельбы
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # Обновление кулдауна
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.shoot_delay:
            self.shoot_cooldown = 0
            
    def shoot(self, target_pos, bullet_group):
        """Создает выстрел в зависимости от типа оружия"""
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
            # Поворачиваем направление на угол
            dx = target_pos[0] - self.rect.centerx
            dy = target_pos[1] - self.rect.centery
            distance = math.sqrt(dx ** 2 + dy ** 2)
            
            if distance > 0:
                # Нормализуем вектор
                dx = dx / distance
                dy = dy / distance
                
                # Поворачиваем
                rad_angle = math.radians(angle)
                rotated_dx = dx * math.cos(rad_angle) - dy * math.sin(rad_angle)
                rotated_dy = dx * math.sin(rad_angle) + dy * math.cos(rad_angle)
                
                # Создаем пулю в повернутом направлении
                new_target_x = self.rect.centerx + rotated_dx * 100
                new_target_y = self.rect.centery + rotated_dy * 100
                
                bullet = Bullet(
                    self.rect.centerx, 
                    self.rect.centery,
                    new_target_x, 
                    new_target_y,
                    self.bullet_damage // 2,  # Меньше урона за пулю
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
        health_bar_width = 50
        health_bar_height = 6
        health_percent = self.health / self.max_health
        
        # Позиция над игроком
        bar_x = self.rect.x + (self.rect.width - health_bar_width) // 2
        bar_y = self.rect.y - 10
        
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