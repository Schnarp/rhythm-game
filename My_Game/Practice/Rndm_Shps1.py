import pygame
import sys
import random


pygame.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Random Shapes")

def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def draw_random_shapes(win):
    for _ in range(20):
        shape_type = random.choice(['rect', 'circle', 'line'])
        color = random_color()
        if shape_type == 'rect':
            x = random.randint(0,450)
            y = random.randint(0,450)
            width = random.randint(20,50)
            height = random.randint(20,50)
            pygame.draw.rect(win, color, (x, y, width, height))
        elif shape_type == 'circle':
            x = random.randint(50, 450)
            y = random.randint(50, 450)
            radius = random.randint(10, 50)
            pygame.draw.circle(win, color, (x, y), radius)
        elif shape_type == 'line':
            x1 = random.randint(0, 500)
            y1 = random.randint(0, 500)
            x2 = random.randint(0, 500)
            y2 = random.randint(0, 500)
            width = random.randint(1, 10)
            pygame.draw.line(win, color, (x1, y1), (x2, y2), width)
        

win.fill((255, 255, 255))
draw_random_shapes(win)
pygame.display.update()

while True: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()  
            sys.exit() 
    