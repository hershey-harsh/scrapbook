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

player_size = 50
player_pos = [width // 2, height - 2 * player_size]
enemy_size = 50
enemy_pos = [random.randint(0, width - enemy_size), 0]
powerup_size = 30
powerup_pos = [random.randint(0, width - powerup_size), 0]
health_potion_size = 30
health_potion_pos = [random.randint(0, width - health_potion_size), 0]

speed = 10
enemy_speed = 10
powerup_speed = 5
health_potion_speed = 5
player_health = 100
score = 0

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
    elif collision_type == "powerup":
        score += 10
    elif collision_type == "health_potion":
        player_health += 20
        if player_health > 100:
            player_health = 100
    return player_health, score

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

    enemy_pos[1] += enemy_speed
    if enemy_pos[1] >= height:
        enemy_pos = [random.randint(0, width - enemy_size), 0]

    powerup_pos[1] += powerup_speed
    if powerup_pos[1] >= height:
        powerup_pos = [random.randint(0, width - powerup_size), 0]

    health_potion_pos[1] += health_potion_speed
    if health_potion_pos[1] >= height:
        health_potion_pos = [random.randint(0, width - health_potion_size), 0]

    window.fill(BLACK)

    if detect_collision(player_pos, enemy_pos, enemy_size):
        player_health, score = update_health_and_score(player_health, score, "enemy")
        enemy_pos = [random.randint(0, width - enemy_size), 0]
    
    if detect_collision(player_pos, powerup_pos, powerup_size):
        player_health, score = update_health_and_score(player_health, score, "powerup")
        powerup_pos = [random.randint(0, width - powerup_size), 0]
    
    if detect_collision(player_pos, health_potion_pos, health_potion_size):
        player_health, score = update_health_and_score(player_health, score, "health_potion")
        health_potion_pos = [random.randint(0, width - health_potion_size), 0]

    player = pygame.draw.rect(window, BLUE, (player_pos[0], player_pos[1], player_size, player_size))
    enemy = pygame.draw.rect(window, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))
    powerup = pygame.draw.rect(window, GREEN, (powerup_pos[0], powerup_pos[1], powerup_size, powerup_size))
    health_potion = pygame.draw.rect(window, WHITE, (health_potion_pos[0], health_potion_pos[1], health_potion_size, health_potion_size))

    health_text = font.render("Health: {}".format(player_health), True, WHITE)
    window.blit(health_text, (10, 10))

    score_text = font.render("Score: {}".format(score), True, WHITE)
    window.blit(score_text, (10, 50))

    if player_health <= 0:
        game_over = True

    pygame.display.update()
    clock.tick(30)

pygame.quit()
