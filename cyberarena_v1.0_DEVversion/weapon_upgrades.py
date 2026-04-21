# weapon_upgrades.py

class WeaponUpgrade:
    def __init__(self, name, description, cost):
        self.name = name
        self.description = description
        self.cost = cost
        self.purchased = False
        
    def apply(self, player):
        """Применяет улучшение к игроку"""
        pass


class DamageUpgrade(WeaponUpgrade):
    def __init__(self):
        super().__init__(
            "УСИЛИТЕЛЬ УРОНА",
            "Увеличивает урон на 5 единиц",
            50
        )
        
    def apply(self, player):
        player.bullet_damage += 5


class SpeedUpgrade(WeaponUpgrade):
    def __init__(self):
        super().__init__(
            "УСКОРИТЕЛЬ ПУЛЬ",
            "Увеличивает скорость пуль",
            40
        )
        
    def apply(self, player):
        player.bullet_speed += 2


class SpreadUpgrade(WeaponUpgrade):
    def __init__(self):
        super().__init__(
            "ВЕЕРНЫЙ ОГОНЬ",
            "Стреляет тремя пулями одновременно",
            100
        )
        
    def apply(self, player):
        player.weapon_type = "spread"
        player.bullet_damage = 10  # Немного снижаем урон для баланса


class WeaponUpgradeSystem:
    def __init__(self, player):
        self.player = player
        self.upgrades = [
            DamageUpgrade(),
            SpeedUpgrade(),
            SpreadUpgrade()
        ]
        self.points = 0  # Очки для покупки улучшений
        
    def add_points(self, amount):
        self.points += amount
        
    def purchase_upgrade(self, index):
        if index < len(self.upgrades):
            upgrade = self.upgrades[index]
            if not upgrade.purchased and self.points >= upgrade.cost:
                upgrade.apply(self.player)
                upgrade.purchased = True
                self.points -= upgrade.cost
                return True
        return False