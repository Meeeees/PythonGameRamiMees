import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 800
screen_height = 600
cell_size = 20
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Snake settings
snake_pos = [100, 50]
snake_body = [[100, 50], [80, 50], [60, 50]]
snake_direction = 'RIGHT'
change_to = snake_direction

# Food settings
def random_food_position():
    return [random.randrange(0, screen_width // cell_size) * cell_size,
            random.randrange(0, screen_height // cell_size) * cell_size]

food_pos = random_food_position()
food_spawn = True

# Game settings
clock = pygame.time.Clock()
speed = 15

# Font settings
font = pygame.font.SysFont('times new roman', 35)

def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your Score: ' + str(len(snake_body) - 3), True, RED)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (screen_width / 2, screen_height / 4)
    screen.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    pygame.time.sleep(3)
    pygame.quit()
    sys.exit()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and change_to != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and change_to != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and change_to != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and change_to != 'LEFT':
                change_to = 'RIGHT'

    # If snake is moving in the current direction, do not change direction
    if change_to == 'UP' and snake_direction != 'DOWN':
        snake_direction = 'UP'
    if change_to == 'DOWN' and snake_direction != 'UP':
        snake_direction = 'DOWN'
    if change_to == 'LEFT' and snake_direction != 'RIGHT':
        snake_direction = 'LEFT'
    if change_to == 'RIGHT' and snake_direction != 'LEFT':
        snake_direction = 'RIGHT'

    # Move snake
    if snake_direction == 'UP':
        snake_pos[1] -= cell_size
    if snake_direction == 'DOWN':
        snake_pos[1] += cell_size
    if snake_direction == 'LEFT':
        snake_pos[0] -= cell_size
    if snake_direction == 'RIGHT':
        snake_pos[0] += cell_size

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = random_food_position()
    food_spawn = True

    # Fill screen and draw snake and food
    screen.fill(BLACK)
    for pos in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], cell_size, cell_size))

    pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], cell_size, cell_size))

    # Game over conditions
    if snake_pos[0] < 0 or snake_pos[0] >= screen_width:
        game_over()
    if snake_pos[1] < 0 or snake_pos[1] >= screen_height:
        game_over()

    for block in snake_body[1:]:
        if snake_pos == block:
            game_over()

    # Display score
    score = font.render("Score: " + str(len(snake_body) - 3), True, WHITE)
    screen.blit(score, [0, 0])

    # Update display and set frame rate
    pygame.display.flip()
    clock.tick(speed)
