import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Create the Game Window
win_width, win_height = 1000, 700
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Square Catch")

# Define Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create a Clock object
clock = pygame.time.Clock()

# Game Variables
player_size = 50
player_x, player_y = win_width // 2, win_height // 2  # Centered position
player_vel = 5  # Player velocity

small_square_size = 20

# Function to create a new small square at a random position
def create_small_square():
    x = random.randint(0, win_width - small_square_size)
    y = random.randint(0, win_height - small_square_size)
    return pygame.Rect(x, y, small_square_size, small_square_size)

small_square = create_small_square()

# Initialize score
score = 0

# Font for displaying the score
font = pygame.font.SysFont(None, 36)

# Create a Clock object
clock = pygame.time.Clock()

# Main Game Loop
running = True
while running:
    clock.tick(100)  # Limit frame rate to 60 fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle Keyboard Input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_x - player_vel >= 0:  # Move left
        player_x -= player_vel
    if keys[pygame.K_d] and player_x + player_vel + player_size <= win_width:  # Move right
        player_x += player_vel
    if keys[pygame.K_w] and player_y - player_vel >= 0:  # Move up
        player_y -= player_vel
    if keys[pygame.K_s] and player_y + player_vel + player_size <= win_height:  # Move down
        player_y += player_vel

    # Player rectangle
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

    # Check for collision
    if player_rect.colliderect(small_square):
        score += 1
        small_square = create_small_square()

    # Draw
    win.fill(WHITE)  # Clear the screen with white
    pygame.draw.rect(win, RED, player_rect)  # Draw the player
    pygame.draw.rect(win, BLUE, small_square)  # Draw the small square

    # Render the score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    win.blit(score_text, (10, 10))

    pygame.display.update()  # Update the display

# Clean Up
pygame.quit()
sys.exit()