import pygame
import time
import random
import os
import json

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (128, 0, 128)
orange = (255, 165, 0)

dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15
level = 1
lives = 3

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

eat_sound = pygame.mixer.Sound('eat_sound.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')
power_up_sound = pygame.mixer.Sound('power_up.wav')
shield_sound = pygame.mixer.Sound('shield_sound.wav')
speed_boost_sound = pygame.mixer.Sound('speed_boost.wav')

skins = {'default': (black, green), 'rainbow': [black, green, purple, orange]}

def check_high_score(score):
    if not os.path.exists('high_score.txt'):
        with open('high_score.txt', 'w') as f:
            f.write('0')
    with open('high_score.txt', 'r') as f:
        high_score = int(f.read())
    if score > high_score:
        with open('high_score.txt', 'w') as f:
            f.write(str(score))
        return score
    return high_score

def score_display(score, high_score, level, lives, game_time):
    value = score_font.render(f"Score: {score} High Score: {high_score} Level: {level} Lives: {lives} Time: {game_time}", True, white)
    dis.blit(value, [0, 0])

def our_snake(snake_block, snake_List, colors):
    for i, x in enumerate(snake_List):
        pygame.draw.rect(dis, colors[i % len(colors)], [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3 + y_displace])

def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(dis, red, [obs[0], obs[1], obs[2], obs[3]])

def save_game(state):
    with open('save_game.json', 'w') as f:
        json.dump(state, f)

def load_game():
    if os.path.exists('save_game.json'):
        with open('save_game.json', 'r') as f:
            return json.load(f)
    return None

def gameLoop():
    global snake_speed, level, lives
    game_over = False
    game_close = False
    multiplier = 1
    bonus_round = False
    bonus_start_time = 0
    shield_active = False
    shield_time = 0
    speed_boost_active = False
    speed_boost_time = 0
    selected_skin = skins['rainbow']

    state = load_game()
    if state:
        x1, y1, x1_change, y1_change, snake_List, Length_of_snake, foodx, foody, score, high_score, obstacles, power_up_active, power_up_time, power_up_x, power_up_y, special_food_active, special_food_time, special_food_x, special_food_y, special_food_bonus, colors, level, snake_speed, lives, game_start_time = state.values()
    else:
        x1 = dis_width / 2
        y1 = dis_height / 2
        x1_change = 0
        y1_change = 0
        snake_List = []
        Length_of_snake = 1
        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        score = 0
        high_score = check_high_score(score)
        obstacles = []
        power_up_active = False
        power_up_time = 0
        colors = selected_skin
        special_food_active = False
        special_food_time = 0
        special_food_bonus = 5
        game_start_time = time.time()

    pygame.mixer.music.load('background.mp3')
    pygame.mixer.music.play(-1)

    while not game_over:
        game_time = int(time.time() - game_start_time)
        if game_time % 60 == 0 and game_time != 0 and not bonus_round:
            bonus_round = True
            bonus_start_time = time.time()

        if bonus_round and time.time() - bonus_start_time > 10:
            bonus_round = False

        while game_close:
            dis.fill(blue)
            message("You Lost! Press Q-Quit, C-Play Again, or S-Save Game", red)
            message(f"Score: {score} High Score: {high_score}", white, 50)
            pygame.display.update()
            pygame.mixer.music.stop()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
                    if event.key == pygame.K_s:
                        state = {
                            "x1": x1, "y1": y1, "x1_change": x1_change, "y1_change": y1_change,
                            "snake_List": snake_List, "Length_of_snake": Length_of_snake,
                            "foodx": foodx, "foody": foody, "score": score, "high_score": high_score,
                            "obstacles": obstacles, "power_up_active": power_up_active, "power_up_time": power_up_time,
                            "power_up_x": power_up_x, "power_up_y": power_up_y, "special_food_active": special_food_active,
                            "special_food_time": special_food_time, "special_food_x": special_food_x, "special_food_y": special_food_y,
                            "special_food_bonus": special_food_bonus, "colors": colors, "level": level, "snake_speed": snake_speed,
                            "lives": lives, "game_start_time": game_start_time
                        }
                        save_game(state)
                        game_over = True
                        game_close = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    pause = True
                    while pause:
                        message("Paused. Press P to continue or Q to quit.", red)
                        pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                    pause = False
                                elif event.key == pygame.K_q:
                                    pygame.quit()
                                    quit()

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            if shield_active:
                shield_active = False
            else:
                lives -= 1
                if lives == 0:
                    pygame.mixer.Sound.play(game_over_sound)
                    game_close = True
                else:
                    x1 = dis_width / 2
                    y1 = dis_height / 2
                    x1_change = 0
                    y1_change = 0
                    snake_List = []
                    Length_of_snake = 1
                    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                    power_up_active = False
                    power_up_time = 0
                    special_food_active = False
                    special_food_time = 0

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                if shield_active:
                    shield_active = False
                else:
                    lives -= 1
                    if lives == 0:
                        pygame.mixer.Sound.play(game_over_sound)
                        game_close = True
                    else:
                        x1 = dis_width / 2
                        y1 = dis_height / 2
                        x1_change = 0
                        y1_change = 0
                        snake_List = []
                        Length_of_snake = 1
                        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                        power_up_active = False
                        power_up_time = 0
                        special_food_active = False
                        special_food_time = 0

        our_snake(snake_block, snake_List, colors)
        score_display(score, high_score, level, lives, game_time)
        draw_obstacles(obstacles)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            pygame.mixer.Sound.play(eat_sound)
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score += 1 * multiplier
            high_score = check_high_score(score)
            if score % 5 == 0:
                level += 1
                snake_speed += 1
                message(f"Level Up! Welcome to Level {level}", green, 50)
                pygame.display.update()
                time.sleep(2)
                if level % 2 == 0:
                    obs_x = round(random.randrange(0, dis_width - 20) / 10.0) * 10.0
                    obs_y = round(random.randrange(0, dis_height - 20) / 10.0) * 10.0
                    obstacles.append([obs_x, obs_y, 20, 20])
                if level % 3 == 0:
                    power_up_active = True
                    power_up_time = time.time()
                    power_up_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                    power_up_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                if level % 4 == 0:
                    special_food_active = True
                    special_food_time = time.time()
                    special_food_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                    special_food_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

        if power_up_active:
            pygame.draw.rect(dis, yellow, [power_up_x, power_up_y, snake_block, snake_block])
            if x1 == power_up_x and y1 == power_up_y:
                pygame.mixer.Sound.play(power_up_sound)
                multiplier = 2
                power_up_active = False
                power_up_time = time.time()
            if time.time() - power_up_time > 10:
                multiplier = 1
                power_up_active = False

        if special_food_active:
            pygame.draw.rect(dis, orange, [special_food_x, special_food_y, snake_block, snake_block])
            if x1 == special_food_x and y1 == special_food_y:
                pygame.mixer.Sound.play(eat_sound)
                special_food_active = False
                score += special_food_bonus
                high_score = check_high_score(score)
            if time.time() - special_food_time > 10:
                special_food_active = False

        if bonus_round:
            pygame.draw.rect(dis, purple, [foodx, foody, snake_block, snake_block])
            if x1 == foodx and y1 == foody:
                pygame.mixer.Sound.play(eat_sound)
                foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                score += 2
                high_score = check_high_score(score)

        if random.random() < 0.01:
            shield_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            shield_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            pygame.draw.rect(dis, blue, [shield_x, shield_y, snake_block, snake_block])
            if x1 == shield_x and y1 == shield_y:
                pygame.mixer.Sound.play(shield_sound)
                shield_active = True
                shield_time = time.time()

        if time.time() - shield_time > 10:
            shield_active = False

        if random.random() < 0.01:
            speed_boost_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            speed_boost_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            pygame.draw.rect(dis, purple, [speed_boost_x, speed_boost_y, snake_block, snake_block])
            if x1 == speed_boost_x and y1 == speed_boost_y:
                pygame.mixer.Sound.play(speed_boost_sound)
                speed_boost_active = True
                snake_speed += 5
                speed_boost_time = time.time()

        if time.time() - speed_boost_time > 5:
            if speed_boost_active:
                snake_speed -= 5
                speed_boost_active = False

        for obs in obstacles:
            obs[0] += random.choice([-1, 1]) * snake_block
            obs[1] += random.choice([-1, 1]) * snake_block
            if x1 == obs[0] and y1 == obs[1]:
                if shield_active:
                    shield_active = False
                else:
                    lives -= 1
                    if lives == 0:
                        pygame.mixer.Sound.play(game_over_sound)
                        game_close = True
                    else:
                        x1 = dis_width / 2
                        y1 = dis_height / 2
                        x1_change = 0
                        y1_change = 0
                        snake_List = []
                        Length_of_snake = 1
                        foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                        foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                        power_up_active = False
                        power_up_time = 0
                        special_food_active = False
                        special_food_time = 0

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
