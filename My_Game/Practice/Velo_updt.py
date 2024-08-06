import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Create the Game Window
win_width, win_height = 1000, 700
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Catch the Squares")

# Define Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create a Clock object to control the frame rate
clock = pygame.time.Clock()

# Game Variables
player_size = 50
player_x, player_y = win_width // 2, win_height // 2  # Centered position
max_vel = 10  # Maximum velocity
acceleration = 0.2  # Acceleration rate
current_vel_x, current_vel_y = 0, 0  # Current velocities for acceleration

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

# Function to update the player's velocity based on key presses
def update_velocity(keys, current_vel, direction_key_pos, direction_key_neg, max_vel, acceleration):
    if keys[direction_key_pos]:
        if current_vel < max_vel:
            current_vel += acceleration
        elif current_vel > max_vel:
            current_vel = max_vel
    elif keys[direction_key_neg]:
        if current_vel > -max_vel:
            current_vel -= acceleration
        elif current_vel < -max_vel:
            current_vel = -max_vel
    else:
        if current_vel > 0:
            current_vel -= acceleration
            if current_vel < 0:
                current_vel = 0
        elif current_vel < 0:
            current_vel += acceleration
            if current_vel > 0:
                current_vel = 0
    return current_vel

# Main Game Loop
running = True
while running:
    clock.tick(100)  # Limit frame rate to 60 fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle Keyboard Input
    keys = pygame.key.get_pressed()
    current_vel_x = update_velocity(keys, current_vel_x, pygame.K_d, pygame.K_a, max_vel, acceleration)
    current_vel_y = update_velocity(keys, current_vel_y, pygame.K_s, pygame.K_w, max_vel, acceleration)

    # Update the player's position
    player_x += current_vel_x
    player_y += current_vel_y

    # Keep the player within the window boundaries
    if player_x < 0:
        player_x = 0
    elif player_x + player_size > win_width:
        player_x = win_width - player_size
    if player_y < 0:
        player_y = 0
    elif player_y + player_size > win_height:
        player_y = win_height - player_size

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