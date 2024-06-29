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
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)

background_images = [
    pygame.image.load('background1.jpg'),
    pygame.image.load('background2.jpg'),
    pygame.image.load('background3.jpg')
]

player_size = 50
player_pos = [width // 2, height - 2 * player_size]
companion_size = 30
companion_pos = [width // 2, height - 3 * player_size]
enemy_size = 50
boss_size = 100
powerup_size = 30
health_potion_size = 30
trap_size = 40
treasure_size = 40
obstacle_size = 60
bullet_size = 10
shield_size = 30

speed = 10
initial_enemy_speed = 5
enemy_speed = initial_enemy_speed
initial_boss_speed = 2
boss_speed = initial_boss_speed
initial_powerup_speed = 5
powerup_speed = initial_powerup_speed
initial_health_potion_speed = 5
health_potion_speed = initial_health_potion_speed
trap_speed = 3
treasure_speed = 3
bullet_speed = 15
enemy_bullet_speed = 7
companion_bullet_speed = 12
player_health = 100
shield_duration = 300
score = 0
level = 1
lives = 3
score_multiplier = 1
shield_active = False
shield_timer = 0
enemies = []
bosses = []
powerups = []
health_potions = []
traps = []
treasures = []
bullets = []
enemy_bullets = []
companion_bullets = []
obstacles = [[100, 200], [300, 400], [500, 100]]
companion_follow = True

collision_sound = pygame.mixer.Sound('collision.wav')
powerup_sound = pygame.mixer.Sound('powerup.wav')
health_potion_sound = pygame.mixer.Sound('health_potion.wav')
boss_sound = pygame.mixer.Sound('boss.wav')
trap_sound = pygame.mixer.Sound('trap.wav')
treasure_sound = pygame.mixer.Sound('treasure.wav')
shoot_sound = pygame.mixer.Sound('shoot.wav')
background_music = pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)

font = pygame.font.SysFont("monospace", 35)
small_font = pygame.font.SysFont("monospace", 25)

clock = pygame.time.Clock()

def detect_collision(player_pos, obj_pos, obj_size):
    p_x, p_y = player_pos
    o_x, o_y = obj_pos

    if (o_x >= p_x and o_x < (p_x + player_size)) or (p_x >= o_x and p_x < (o_x + obj_size)):
        if (o_y >= p_y and o_y < (p_y + player_size)) or (p_y >= o_y and p_y < (o_y + obj_size)):
            return True
    return False

def update_health_and_score(player_health, score, collision_type):
    global shield_active, score_multiplier
    if collision_type == "enemy":
        if not shield_active:
            player_health -= 10
            score_multiplier = 1
            collision_sound.play()
    elif collision_type == "boss":
        if not shield_active:
            player_health -= 30
            score_multiplier = 1
            boss_sound.play()
    elif collision_type == "powerup":
        score += 10 * score_multiplier
        powerup_sound.play()
    elif collision_type == "health_potion":
        player_health += 20
        if player_health > 100:
            player_health = 100
        health_potion_sound.play()
    elif collision_type == "trap":
        if not shield_active:
            player_health -= 20
            score_multiplier = 1
            trap_sound.play()
    elif collision_type == "treasure":
        score += 50 * score_multiplier
        treasure_sound.play()
    elif collision_type == "shield":
        shield_active = True
        shield_timer = shield_duration
        powerup_sound.play()
    return player_health, score

def create_enemy():
    enemy_pos = [random.randint(0, width - enemy_size), 0]
    enemies.append(enemy_pos)

def create_boss():
    boss_pos = [random.randint(0, width - boss_size), 0]
    bosses.append(boss_pos)

def create_powerup():
    powerup_pos = [random.randint(0, width - powerup_size), 0]
    powerups.append(powerup_pos)

def create_health_potion():
    health_potion_pos = [random.randint(0, width - health_potion_size), 0]
    health_potions.append(health_potion_pos)

def create_trap():
    trap_pos = [random.randint(0, width - trap_size), 0]
    traps.append(trap_pos)

def create_treasure():
    treasure_pos = [random.randint(0, width - treasure_size), 0]
    treasures.append(treasure_pos)

def create_shield():
    shield_pos = [random.randint(0, width - shield_size), 0]
    powerups.append(shield_pos)

def create_bullet():
    bullet_pos = [player_pos[0] + player_size // 2 - bullet_size // 2, player_pos[1]]
    bullets.append(bullet_pos)
    shoot_sound.play()

def create_enemy_bullet(enemy_pos):
    enemy_bullet_pos = [enemy_pos[0] + enemy_size // 2 - bullet_size // 2, enemy_pos[1] + enemy_size]
    enemy_bullets.append(enemy_bullet_pos)

def create_companion_bullet():
    companion_bullet_pos = [companion_pos[0] + companion_size // 2 - bullet_size // 2, companion_pos[1]]
    companion_bullets.append(companion_bullet_pos)
    shoot_sound.play()

def random_event():
    event_type = random.choice(['meteor_shower', 'powerup_rain'])
    if event_type == 'meteor_shower':
        for _ in range(5):
            create_enemy()
    elif event_type == 'powerup_rain':
        for _ in range(5):
            create_powerup()

def game_over_screen():
    window.fill(BLACK)
    game_over_text = font.render("Game Over!", True, RED)
    score_text = font.render("Your Score: {}".format(score), True, WHITE)
    window.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - game_over_text.get_height() // 2 - 30))
    window.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2 - score_text.get_height() // 2 + 30))
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.quit()
    exit()

for _ in range(5):
    create_enemy()
create_powerup()
create_health_potion()
create_trap()
create_treasure()
create_shield()

game_over = False
paused = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
            if event.key == pygame.K_SPACE:
                create_bullet()

    if not paused:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= speed
        if keys[pygame.K_RIGHT] and player_pos[0] < width - player_size:
            player_pos[0] += speed
        if keys[pygame.K_UP] and player_pos[1] > 0:
            player_pos[1] -= speed
        if keys[pygame.K_DOWN] and player_pos[1] < height - player_size:
            player_pos[1] += speed

        if companion_follow:
            companion_pos[0] = player_pos[0]

        for enemy_pos in enemies:
            enemy_pos[1] += enemy_speed
            if enemy_pos[1] >= height:
                enemy_pos[1] = 0
                enemy_pos[0] = random.randint(0, width - enemy_size)
                create_enemy_bullet(enemy_pos)

        for boss_pos in bosses:
            boss_pos[1] += boss_speed
            if boss_pos[1] >= height:
                boss_pos[1] = 0
                boss_pos[0] = random.randint(0, width - boss_size)
                create_enemy_bullet(boss_pos)

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

        for trap_pos in traps:
            trap_pos[1] += trap_speed
            if trap_pos[1] >= height:
                trap_pos[1] = 0
                trap_pos[0] = random.randint(0, width - trap_size)

        for treasure_pos in treasures:
            treasure_pos[1] += treasure_speed
            if treasure_pos[1] >= height:
                treasure_pos[1] = 0
                treasure_pos[0] = random.randint(0, width - treasure_size)

        for bullet_pos in bullets:
            bullet_pos[1] -= bullet_speed
            if bullet_pos[1] < 0:
                bullets.remove(bullet_pos)

        for enemy_bullet_pos in enemy_bullets:
            enemy_bullet_pos[1] += enemy_bullet_speed
            if enemy_bullet_pos[1] > height:
                enemy_bullets.remove(enemy_bullet_pos)

        for companion_bullet_pos in companion_bullets:
            companion_bullet_pos[1] -= companion_bullet_speed
            if companion_bullet_pos[1] < 0:
                companion_bullets.remove(companion_bullet_pos)

        if shield_active:
            shield_timer -= 1
            if shield_timer <= 0:
                shield_active = False

        window.blit(background_images[level - 1], (0, 0))

        if any(detect_collision(player_pos, enemy_pos, enemy_size) for enemy_pos in enemies):
            player_health, score = update_health_and_score(player_health, score, "enemy")
            create_enemy()

        if any(detect_collision(player_pos, boss_pos, boss_size) for boss_pos in bosses):
            player_health, score = update_health_and_score(player_health, score, "boss")
            create_boss()

        if any(detect_collision(player_pos, powerup_pos, powerup_size) for powerup_pos in powerups):
            player_health, score = update_health_and_score(player_health, score, "powerup")
            create_powerup()

        if any(detect_collision(player_pos, health_potion_pos, health_potion_size) for health_potion_pos in health_potions):
            player_health, score = update_health_and_score(player_health, score, "health_potion")
            create_health_potion()

        if any(detect_collision(player_pos, trap_pos, trap_size) for trap_pos in traps):
            player_health, score = update_health_and_score(player_health, score, "trap")
            create_trap()

        if any(detect_collision(player_pos, treasure_pos, treasure_size) for treasure_pos in treasures):
            player_health, score = update_health_and_score(player_health, score, "treasure")
            create_treasure()

        if any(detect_collision(player_pos, powerup_pos, shield_size) for powerup_pos in powerups):
            player_health, score = update_health_and_score(player_health, score, "shield")
            create_shield()

        for bullet_pos in bullets:
            for enemy_pos in enemies:
                if detect_collision(bullet_pos, enemy_pos, bullet_size):
                    enemies.remove(enemy_pos)
                    bullets.remove(bullet_pos)
                    create_enemy()
                    score += 5 * score_multiplier
                    score_multiplier += 1
                    break

            for boss_pos in bosses:
                if detect_collision(bullet_pos, boss_pos, bullet_size):
                    bosses.remove(boss_pos)
                    bullets.remove(bullet_pos)
                    create_boss()
                    score += 20 * score_multiplier
                    score_multiplier += 1
                    break

        for enemy_bullet_pos in enemy_bullets:
            if detect_collision(player_pos, enemy_bullet_pos, bullet_size):
                enemy_bullets.remove(enemy_bullet_pos)
                player_health, score = update_health_and_score(player_health, score, "enemy")

        for companion_bullet_pos in companion_bullets:
            for enemy_pos in enemies:
                if detect_collision(companion_bullet_pos, enemy_pos, bullet_size):
                    enemies.remove(enemy_pos)
                    companion_bullets.remove(companion_bullet_pos)
                    create_enemy()
                    score += 5 * score_multiplier
                    score_multiplier += 1
                    break

            for boss_pos in bosses:
                if detect_collision(companion_bullet_pos, boss_pos, bullet_size):
                    bosses.remove(boss_pos)
                    companion_bullets.remove(companion_bullet_pos)
                    create_boss()
                    score += 20 * score_multiplier
                    score_multiplier += 1
                    break

        player = pygame.draw.rect(window, BLUE, (player_pos[0], player_pos[1], player_size, player_size))
        companion = pygame.draw.rect(window, YELLOW, (companion_pos[0], companion_pos[1], companion_size, companion_size))

        for enemy_pos in enemies:
            pygame.draw.rect(window, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

        for boss_pos in bosses:
            pygame.draw.rect(window, PURPLE, (boss_pos[0], boss_pos[1], boss_size, boss_size))

        for powerup_pos in powerups:
            pygame.draw.rect(window, GREEN, (powerup_pos[0], powerup_pos[1], powerup_size, powerup_size))

        for health_potion_pos in health_potions:
            pygame.draw.rect(window, WHITE, (health_potion_pos[0], health_potion_pos[1], health_potion_size, health_potion_size))

        for trap_pos in traps:
            pygame.draw.rect(window, BROWN, (trap_pos[0], trap_pos[1], trap_size, trap_size))

        for treasure_pos in treasures:
            pygame.draw.rect(window, YELLOW, (treasure_pos[0], treasure_pos[1], treasure_size, treasure_size))

        for obstacle_pos in obstacles:
            pygame.draw.rect(window, WHITE, (obstacle_pos[0], obstacle_pos[1], obstacle_size, obstacle_size))

        for bullet_pos in bullets:
            pygame.draw.rect(window, ORANGE, (bullet_pos[0], bullet_pos[1], bullet_size, bullet_size))

        for enemy_bullet_pos in enemy_bullets:
            pygame.draw.rect(window, CYAN, (enemy_bullet_pos[0], enemy_bullet_pos[1], bullet_size, bullet_size))

        for companion_bullet_pos in companion_bullets:
            pygame.draw.rect(window, BLUE, (companion_bullet_pos[0], companion_bullet_pos[1], bullet_size, bullet_size))

        health_text = font.render("Health: {}".format(player_health), True, WHITE)
        window.blit(health_text, (10, 10))

        score_text = font.render("Score: {}".format(score), True, WHITE)
        window.blit(score_text, (10, 50))

        level_text = font.render("Level: {}".format(level), True, WHITE)
        window.blit(level_text, (10, 90))

        lives_text = font.render("Lives: {}".format(lives), True, WHITE)
        window.blit(lives_text, (10, 130))

        if player_health <= 0:
            lives -= 1
            if lives > 0:
                player_health = 100
                score_multiplier = 1
                enemies.clear()
                bosses.clear()
                powerups.clear()
                health_potions.clear()
                traps.clear()
                treasures.clear()
                bullets.clear()
                enemy_bullets.clear()
                companion_bullets.clear()
                obstacles.clear()
                for _ in range(5):
                    create_enemy()
                create_powerup()
                create_health_potion()
                create_trap()
                create_treasure()
                create_shield()
            else:
                game_over_screen()

        if score > level * 100:
            level += 1
            enemy_speed += 2
            boss_speed += 1
            powerup_speed += 1
            health_potion_speed += 1
            create_boss()
            random_event()

        pygame.display.update()
        clock.tick(30)

pygame.quit()
