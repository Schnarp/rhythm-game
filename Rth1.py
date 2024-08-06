import pygame
import sys
import time

pygame.init()

# Window setup
window_width, window_height = 1140, 1275
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Rhythm Game")

# Colors
BLACK = (0, 0, 0)

# Load images
outline_image = pygame.image.load('photos/outline.png')
start_screen_images = [
    pygame.image.load('photos/start_screen1.png'),
    pygame.image.load('photos/start_screen2.png')
]
hovered_play_button1 = pygame.image.load('photos/hovered_play_button.png')
hovered_play_button2 = pygame.image.load('photos/hovered_play_button2.png')
select_screen_images = [
    pygame.image.load('photos/select_screen.png'),
    pygame.image.load('photos/select_screen2.png')
]

# Load note images
note_images = {
    'd': pygame.image.load('notes/d_note.png'),
    'f': pygame.image.load('notes/f_note.png'),
    'j': pygame.image.load('notes/j_note.png'),
    'k': pygame.image.load('notes/k_note.png')
}

# Load images for pressed keys
pressed_images = {
    pygame.K_d: pygame.image.load('pressed/d_pressed.png'),
    pygame.K_f: pygame.image.load('pressed/f_pressed.png'),
    pygame.K_j: pygame.image.load('pressed/j_pressed.png'),
    pygame.K_k: pygame.image.load('pressed/k_pressed.png')
}

# Load number images for scoring
number_images = {str(i): pygame.image.load(f'photos/{i}.png') for i in range(10)}

# Define positions for each key (x, y)
key_positions = {
    pygame.K_d: (376, 1196),
    pygame.K_f: (474, 1196),
    pygame.K_j: (573, 1196),
    pygame.K_k: (670, 1196)
}

# Note drop positions
note_positions = {
    'd': (376, -50),
    'f': (474, -50),
    'j': (573, -50),
    'k': (670, -50)
}

# Adjusted note sequence for "Mary Had a Little Lamb"
note_sequence = [
    ('f', 0), ('j', 1.15), ('k', 1.4), ('j', 2.05), 
    ('f', 2.7), ('f', 3.35), ('f', 4.0), 
    ('j', 5.3), ('j', 5.95), ('j', 6.6), 
    ('f', 7.9), ('d', 8.55), ('d', 9.2), 
    ('f', 10.35), ('j', 11.5), ('k', 11.75), ('j', 12.4), 
    ('f', 13.05), ('f', 13.7), ('f', 14.35), ('k', 15.0),
    ('j', 15.65), ('j', 16.3), ('f', 16.95), ('j', 17.6), ('k', 18.25)
]

# Invisible line position for collision detection
line_y = 1193

# Red line position for key press detection
red_line_y = 1012

# Customizable thickness for the hit detection area around the red line
hit_thickness = 100

# Customizable note falling speed
note_speed = 5  # Adjust this value to change the speed of the notes

# Set up key press tracking
pressed_keys = set()

# Flag to track if the song has started
song_started = False

# Note class
class Note:
    def __init__(self, note_type, x, y, invisible=False):
        self.image = note_images[note_type] if not invisible else None
        self.rect = pygame.Rect(x, y, 95, 20) if invisible else self.image.get_rect()
        self.rect.topleft = (x, y)
        self.note_type = note_type
        self.invisible = invisible

    def move(self, speed):
        self.rect.y += speed

    def draw(self, window):
        if not self.invisible:
            window.blit(self.image, self.rect.topleft)

# Draw the score
def draw_score(window, score, start_x, start_y):
    score_str = str(score)
    x_offset = start_x
    for digit in score_str:
        window.blit(number_images[digit], (x_offset, start_y))
        x_offset += number_images[digit].get_width()

def display_start_screen(current_image_index, show_hovered_button=False, button_x=0, button_y=0, hovered_button_image=None):
    window.blit(start_screen_images[current_image_index], (0, 0))
    if show_hovered_button:
        window.blit(hovered_button_image, (button_x, button_y))
    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    notes = []
    note_index = 0
    last_time = time.time()
    score = 0
    game_started = False
    select_screen_active = False
    global song_started
    paused = False  # Flag to track if the game is paused
    pause_start_time = 0  # Track when the game was paused

    # Score position
    score_position_x = 95  # x-coordinate
    score_position_y = 1230  # y-coordinate

    # Start button coordinates
    start_button_rect = pygame.Rect(290, 627, 510, 150)

    # Hovered play button positions
    hovered_button_x, hovered_button_y = 280, 615
    hovered_button_images = [hovered_play_button1, hovered_play_button2]
    hovered_button_index = 0

    # Select screen state and coordinates
    select_screen_image_index = 0
    left_arrow_area = pygame.Rect(20, 607, 65, 65)  # Customize as needed
    right_arrow_area = pygame.Rect(1055, 607, 65, 65)  # Customize as needed
    play_button_rect = pygame.Rect(342, 657, 460, 96)  # Customize as needed

    # Load and prepare the music
    pygame.mixer.music.load('mary_had_a_little_lamb.mp3')

    # Animation variables for the start screen
    current_image_index = 0
    last_switch_time = time.time()
    last_hover_switch_time = time.time()  # Track time for button image switching

    while not game_started:
        show_hovered_button = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    select_screen_active = True

        # Animate the start screen
        current_time = time.time()
        if current_time - last_switch_time >= 0.5:
            current_image_index = (current_image_index + 1) % 2
            last_switch_time = current_time

        # Check for mouse hover
        mouse_pos = pygame.mouse.get_pos()
        if start_button_rect.collidepoint(mouse_pos):
            show_hovered_button = True

            # Switch hovered button image
            if current_time - last_hover_switch_time >= 0.5:
                hovered_button_index = (hovered_button_index + 1) % len(hovered_button_images)
                last_hover_switch_time = current_time

        display_start_screen(current_image_index, show_hovered_button, hovered_button_x, hovered_button_y, hovered_button_images[hovered_button_index])

        if select_screen_active:
            break

    while select_screen_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if left_arrow_area.collidepoint(event.pos):
                    select_screen_image_index = (select_screen_image_index - 1) % len(select_screen_images)
                elif right_arrow_area.collidepoint(event.pos):
                    select_screen_image_index = (select_screen_image_index + 1) % len(select_screen_images)
                elif play_button_rect.collidepoint(event.pos):
                    if select_screen_image_index == 0:
                        game_started = True
                        select_screen_active = False
                        break
                    else:
                        # Add other songs handling here
                        pass

        window.blit(select_screen_images[select_screen_image_index], (0, 0))
        pygame.display.flip()

    window.fill(BLACK)
    pygame.display.flip()
    time.sleep(0.5)  # Brief pause to transition

    last_time = time.time()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if paused:
                        paused = False
                        pygame.mixer.music.unpause()
                        last_time = time.time() - (pause_start_time - last_time)
                    else:
                        paused = True
                        pygame.mixer.music.pause()
                        pause_start_time = time.time()

                pressed_keys.add(event.key)
            elif event.type == pygame.KEYUP:
                pressed_keys.discard(event.key)

        if paused:
            continue

        window.fill(BLACK)
        window.blit(outline_image, (0, 0))

        current_time = time.time()
        elapsed_time = current_time - last_time

        notes_to_remove = []
        for note in notes:
            note.move(note_speed)
            note.draw(window)
            if note.rect.colliderect(pygame.Rect(0, red_line_y, window_width, hit_thickness)):
                if not note.invisible and note.note_type in [pygame.key.name(k) for k in pressed_keys]:
                    notes_to_remove.append(note)
                    score += 1

        for note in notes_to_remove:
            notes.remove(note)

        # Draw the score
        draw_score(window, score, score_position_x, score_position_y)

        # Display pressed key images
        for key in pressed_keys:
            if key in key_positions and key in pressed_images:
                window.blit(pressed_images[key], key_positions[key])

        pygame.display.flip()
        clock.tick(60)

        while note_index < len(note_sequence) and elapsed_time >= note_sequence[note_index][1]:
            note_type = note_sequence[note_index][0]
            note_x, note_y = note_positions[note_type]
            new_note = Note(note_type, note_x, note_y)
            notes.append(new_note)
            note_index += 1

        if not song_started and notes and notes[0].rect.y >= red_line_y:
            pygame.mixer.music.play()
            song_started = True

if __name__ == "__main__":
    main()
