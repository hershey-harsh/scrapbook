import pygame
import random

pygame.init()

width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Adventure Quest")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

player_size = 50
player_pos = [width // 2, height - 2 * player_size]
enemy_size = 50
powerup_size = 30
health_potion_size = 30

speed = 10
initial_enemy_speed = 5
enemy_speed = initial_enemy_speed
initial_powerup_speed = 5
powerup_speed = initial_powerup_speed
initial_health_potion_speed = 5
health_potion_speed = initial_health_potion_speed
player_health = 100
score = 0
level = 1
enemies = []
powerups = []
health_potions = []

collision_sound = pygame.mixer.Sound('collision.wav')
powerup_sound = pygame.mixer.Sound('powerup.wav')
health_potion_sound = pygame.mixer.Sound('health_potion.wav')

font = pygame.font.SysFont("monospace", 35)

clock = pygame.time.Clock()

def detect_collision(player_pos, obj_pos, obj_size):
    p_x, p_y = player_pos
    o_x, o_y = obj_pos

    if (o_x >= p_x and o_x < (p_x + player_size)) or (p_x >= o_x and p_x < (o_x + obj_size)):
        if (o_y >= p_y and o_y < (p_y + player_size)) or (p_y >= o_y and p_y < (o_y + obj_size)):
            return True
    return False

def update_health_and_score(player_health, score, collision_type):
    if collision_type == "enemy":
        player_health -= 10
        collision_sound.play()
    elif collision_type == "powerup":
        score += 10
        powerup_sound.play()
    elif collision_type == "health_potion":
        player_health += 20
        if player_health > 100:
            player_health = 100
        health_potion_sound.play()
    return player_health, score

def create_enemy():
    enemy_pos = [random.randint(0, width - enemy_size), 0]
    enemies.append(enemy_pos)

def create_powerup():
    powerup_pos = [random.randint(0, width - powerup_size), 0]
    powerups.append(powerup_pos)

def create_health_potion():
    health_potion_pos = [random.randint(0, width - health_potion_size), 0]
    health_potions.append(health_potion_pos)

for _ in range(5):
    create_enemy()
create_powerup()
create_health_potion()

game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= speed
    if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
        player_pos[0] += speed

    for enemy_pos in enemies:
        enemy_pos[1] += enemy_speed
        if enemy_pos[1] >= height:
            enemy_pos[1] = 0
            enemy_pos[0] = random.randint(0, width - enemy_size)

    for powerup_pos in powerups:
        powerup_pos[1] += powerup_speed
        if powerup_pos[1] >= height:
            powerup_pos[1] = 0
            powerup_pos[0] = random.randint(0, width - powerup_size)

    for health_potion_pos in health_potions:
        health_potion_pos[1] += health_potion_speed
        if health_potion_pos[1] >= height:
            health_potion_pos[1] = 0
            health_potion_pos[0] = random.randint(0, width - health_potion_size)

    window.fill(BLACK)

    if any(detect_collision(player_pos, enemy_pos, enemy_size) for enemy_pos in enemies):
        player_health, score = update_health_and_score(player_health, score, "enemy")
        create_enemy()

    if any(detect_collision(player_pos, powerup_pos, powerup_size) for powerup_pos in powerups):
        player_health, score = update_health_and_score(player_health, score, "powerup")
        create_powerup()

    if any(detect_collision(player_pos, health_potion_pos, health_potion_size) for health_potion_pos in health_potions):
        player_health, score = update_health_and_score(player_health, score, "health_potion")
        create_health_potion()

    player = pygame.draw.rect(window, BLUE, (player_pos[0], player_pos[1], player_size, player_size))

    for enemy_pos in enemies:
        pygame.draw.rect(window, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
    
    for powerup_pos in powerups:
        pygame.draw.rect(window, GREEN, (powerup_pos[0], powerup_pos[1], powerup_size, powerup_size))
    
    for health_potion_pos in health_potions:
        pygame.draw.rect(window, WHITE, (health_potion_pos[0], health_potion_pos[1], health_potion_size, health_potion_size))

    health_text = font.render("Health: {}".format(player_health), True, WHITE)
    window.blit(health_text, (10, 10))

    score_text = font.render("Score: {}".format(score), True, WHITE)
    window.blit(score_text, (10, 50))

    level_text = font.render("Level: {}".format(level), True, WHITE)
    window.blit(level_text, (10, 90))

    if player_health <= 0:
        game_over = True

    if score > level * 50:
        level += 1
        enemy_speed += 2
        powerup_speed += 1
        health_potion_speed += 1

    pygame.display.update()
    clock.tick(30)

pygame.quit()
