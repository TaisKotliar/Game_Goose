import pygame
from pygame.locals import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT
import random
import os
import sys
"""
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
"""

def resource_path(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


pygame.mixer.init()
pygame.mixer.music.load(resource_path("AUDIO/Kosaky.mp3"))
pygame.mixer.music.play(-1,0.0)

pygame.init()

FPS = pygame.time.Clock()

HEIGHT = 800
WIDTH = 1200

FONT = pygame.font.SysFont('Verdana', 50)

COLOR_SCORE = (117, 150, 240)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load(resource_path("IMG/background.png")), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 2

IMAGE_PATH = resource_path("ANIMATION")
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player = pygame.image.load(resource_path("IMG/player.png")).convert_alpha()
player_rect = player.get_rect()
player_rect.centery = (HEIGHT / 2) - 20
player_move_down = [0, 3]
player_move_right = [3, 0]
player_move_up = [0, -3]
player_move_left = [-3, 0]

def create_bonus():
    bonus = pygame.image.load(resource_path("IMG/bonus.png")).convert_alpha()
    bonus_size = bonus.get_size()
    bonus_rect = pygame.Rect(random.randint(0, WIDTH - bonus.get_width()), -bonus.get_height(), *bonus_size)
    bonus_move = [0, random.randint(2, 6)]
    return [bonus, bonus_rect, bonus_move]

def create_enemy():
    enemy = pygame.image.load(resource_path("IMG/enemy.png")).convert_alpha()
    enemy_size = enemy.get_size()
    enemy_rect = pygame.Rect(WIDTH + enemy.get_width(), random.randint(0, HEIGHT - enemy.get_height()), *enemy_size)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy, enemy_rect, enemy_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 1500)
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []

score = 0

image_index = 0

playing = True 

while playing:
    FPS.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()     
    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))
    
    keys = pygame.key.get_pressed()
    
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)
    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)
    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)
    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)    

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False 

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_SCORE), (WIDTH - 80, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0: 
            enemies.pop(enemies.index(enemy))
            
    for bonus in bonuses:
        if bonus[1].bottom > HEIGHT:
            bonuses.pop(bonuses.index(bonus))