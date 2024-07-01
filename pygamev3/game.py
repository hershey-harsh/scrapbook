import pygame
import time
import random
import os

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15
level = 1

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

eat_sound = pygame.mixer.Sound('eat_sound.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')

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

def score_display(score, high_score):
    value = score_font.render("Score: " + str(score) + " High Score: " + str(high_score), True, white)
    dis.blit(value, [0, 0])

def our_snake(snake_block, snake_List):
    for x in snake_List:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3 + y_displace])

def gameLoop():
    global snake_speed, level
    game_over = False
    game_close = False

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

    pygame.mixer.music.load('background.mp3')
    pygame.mixer.music.play(-1)

    while not game_over:
        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
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
            pygame.mixer.Sound.play(game_over_sound)
            game_close = True
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
                pygame.mixer.Sound.play(game_over_sound)
                game_close = True

        our_snake(snake_block, snake_List)
        score_display(score, high_score)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            pygame.mixer.Sound.play(eat_sound)
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score += 1
            high_score = check_high_score(score)
            if score % 5 == 0:
                level += 1
                snake_speed += 1
                message(f"Level Up! Welcome to Level {level}", green, 50)
                pygame.display.update()
                time.sleep(2)

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()