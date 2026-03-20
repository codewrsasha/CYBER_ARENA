# test_fonts.py
import pygame
from fonts import FontManager
from ui import CyberText, Button

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
settings = type('Settings', (), {'CYBER_BLUE': (0,255,255), 
                                  'CYBER_PINK': (255,0,140)})()

# Тест разных текстов
test_texts = [
    ("CYBER ARENA", 48, settings.CYBER_BLUE, False),
    ("КИБЕР АРЕНА", 48, settings.CYBER_PINK, True),
    ("Player Health", 36, (0,255,0), False),
    ("Здоровье игрока", 36, (255,0,0), True),
]

running = True
y_pos = 50

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    screen.fill((0,0,0))
    
    y_pos = 50
    for text, size, color, use_cyrillic in test_texts:
        cyber_text = CyberText(text, size, color, use_cyrillic=use_cyrillic)
        cyber_text.draw(screen, (50, y_pos))
        y_pos += size + 20
        
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()