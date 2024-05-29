import pygame
import sys
import random
import os

# Initialize pygame
pygame.init()

# Constants for the game
SCREEN_WIDTH, SCREEN_HEIGHT = 665, 525
GRIDSIZE = 35
GRID_WIDTH = SCREEN_WIDTH // GRIDSIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRIDSIZE

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DARK_GREEN = (162, 208, 74)
LIGHT_GREEN = (169, 215, 81)
# Font setup
font = pygame.font.Font(None, 36)

def draw_grid():
    for x in range(0, SCREEN_WIDTH, GRIDSIZE):
        for y in range(0, SCREEN_HEIGHT, GRIDSIZE):
            rect = pygame.Rect(x, y, GRIDSIZE, GRIDSIZE)
            if (x // GRIDSIZE + y // GRIDSIZE) % 2 == 0:
                pygame.draw.rect(screen, DARK_GREEN, rect)
            else:
                pygame.draw.rect(screen, LIGHT_GREEN, rect)


def move(snake):
    head_x, head_y = snake[0]
    if direction == 'UP':
        head_y -= 1
    elif direction == 'DOWN':
        head_y += 1
    elif direction == 'LEFT':
        head_x -= 1
    elif direction == 'RIGHT':
        head_x += 1
    head = head_x, head_y
    snake.insert(0, head)
    if head != food:
        snake.pop()
    return snake

def check_collision(snake):
    head = snake[0]
    if head[0] < 0 or head[0] >= GRID_WIDTH or head[1] < 0 or head[1] >= GRID_HEIGHT or head in snake[1:]:
        return True
    return False

def get_random_food(snake):
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    while food in snake:
        food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    return food

def show_start_screen():
    screen.fill(BLACK)
    title = font.render('Welcome to Snake Game', True, WHITE)
    prompt = font.render('Enter Username and press Enter', True, WHITE)
    screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, 150))
    screen.blit(prompt, (SCREEN_WIDTH / 2 - prompt.get_width() / 2, 200))
    pygame.display.update()
    username = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username:
                    return username
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode
        screen.fill(BLACK)
        screen.blit(title, (SCREEN_WIDTH / 2 - title.get_width() / 2, 150))
        screen.blit(prompt, (SCREEN_WIDTH / 2 - prompt.get_width() / 2, 200))
        block = font.render(username, True, WHITE)
        screen.blit(block, (SCREEN_WIDTH / 2 - block.get_width() / 2, 250))
        pygame.display.update()

def show_game_over_screen(score):
    screen.fill(BLACK)
    message = font.render('Game Over!', True, WHITE)
    score_text = font.render(f'Score: {score}', True, WHITE)
    retry = font.render('Press R to play again or Q to quit', True, WHITE)
    screen.blit(message, (SCREEN_WIDTH / 2 - message.get_width() / 2, 150))
    screen.blit(score_text, (SCREEN_WIDTH / 2 - score_text.get_width() / 2, 200))
    screen.blit(retry, (SCREEN_WIDTH / 2 - retry.get_width() / 2, 250))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'QUIT'
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'RETRY'
                elif event.key == pygame.K_q:
                    return 'QUIT'

def write_score(username, score):
    with open('scores.txt', 'a') as file:
        file.write(f'{username}: {score}\n')

# Game initialization
username = show_start_screen()
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
direction = 'UP'
food = get_random_food(snake)
score = 0

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'

    snake = move(snake)
    if check_collision(snake):
        choice = show_game_over_screen(score)
        if choice == 'QUIT':
            write_score(username, score)
            pygame.quit()
            sys.exit()
        elif choice == 'RETRY':
            write_score(username, score)
            snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
            direction = 'UP'
            food = get_random_food(snake)
            score = 0
            continue
    if snake[0] == food:
        food = get_random_food(snake)  # New food
        score += 1

    screen.fill(BLACK)
    for x, y in snake:
        snake_rect = pygame.Rect(x * GRIDSIZE, y * GRIDSIZE, GRIDSIZE, GRIDSIZE)
        pygame.draw.rect(screen, GREEN, snake_rect)
    food_rect = pygame.Rect(food[0] * GRIDSIZE, food[1] * GRIDSIZE, GRIDSIZE, GRIDSIZE)
    pygame.draw.rect(screen, RED, food_rect)

    pygame.display.update()
    clock.tick(10)  # Controls the speed of the game
