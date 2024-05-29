import pygame
import sys

# General setup
pygame.init()
clock = pygame.time.Clock()

# Setting up the main window
screen = pygame.display.set_mode((1000, 800),pygame.RESIZABLE)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption('Battleship')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Font setup
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 50)

# Game state
welcome_screen = True
play_against_computer = False

# Grid settings
grid_size = 10
cell_size = min(screen_width // 20, screen_height // 12)  # Adjust cell size to fit the screen
player1_grid_origin = (screen_width // 4 - grid_size * cell_size // 2, screen_height // 2 - grid_size * cell_size // 2)
player2_grid_origin = (3 * screen_width // 4 - grid_size * cell_size // 2, screen_height // 2 - grid_size * cell_size // 2)

# Function to draw a grid at a given origin
def draw_grid(origin):
    for row in range(grid_size):
        for col in range(grid_size):
            rect = pygame.Rect(origin[0] + col * cell_size, origin[1] + row * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, BLACK, rect, 1)

# Function to display the welcome screen
def draw_welcome_screen():
    screen.fill(WHITE)
    title_text = font.render("Welcome to Battleship", True, BLACK)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 4))

    pvp_text = small_font.render("1. Play Against Player", True, BLACK)
    screen.blit(pvp_text, (screen_width // 2 - pvp_text.get_width() // 2, screen_height // 2 - 50))

    pvc_text = small_font.render("2. Play Against Computer", True, BLACK)
    screen.blit(pvc_text, (screen_width // 2 - pvc_text.get_width() // 2, screen_height // 2 + 50))

# Main game loop
while True:
    # Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if welcome_screen:
                if event.key == pygame.K_1:
                    welcome_screen = False
                    play_against_computer = False
                elif event.key == pygame.K_2:
                    welcome_screen = False
                    play_against_computer = True
            else:
                if event.key == pygame.K_ESCAPE:
                    welcome_screen = True
        
        elif event.type == pygame.MOUSEBUTTONDOWN and not welcome_screen:
            mouse_pos = event.pos
            # Check if click is within player 1's grid bounds
            if player1_grid_origin[0] <= mouse_pos[0] < player1_grid_origin[0] + grid_size * cell_size and \
               player1_grid_origin[1] <= mouse_pos[1] < player1_grid_origin[1] + grid_size * cell_size:
                # Calculate grid coordinates for player 1
                grid_x = (mouse_pos[0] - player1_grid_origin[0]) // cell_size
                grid_y = (mouse_pos[1] - player1_grid_origin[1]) // cell_size
                print(f"Player 1 Grid clicked: ({grid_x}, {grid_y})")
            # Check if click is within player 2's grid bounds
            elif player2_grid_origin[0] <= mouse_pos[0] < player2_grid_origin[0] + grid_size * cell_size and \
                 player2_grid_origin[1] <= mouse_pos[1] < player2_grid_origin[1] + grid_size * cell_size:
                # Calculate grid coordinates for player 2
                grid_x = (mouse_pos[0] - player2_grid_origin[0]) // cell_size
                grid_y = (mouse_pos[1] - player2_grid_origin[1]) // cell_size
                print(f"Player 2 Grid clicked: ({grid_x}, {grid_y})")

    if welcome_screen:
        draw_welcome_screen()
    else:
        # Filling the screen with white
        screen.fill(WHITE)
        
        # Drawing the grids for both players
        draw_grid(player1_grid_origin)
        draw_grid(player2_grid_origin)

    # Updating the window
    pygame.display.flip()
    clock.tick(60)
