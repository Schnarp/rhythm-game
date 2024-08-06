import pygame
import sys

x = 50
y = 50
width = 40
height = 40
vel = .1

pygame.init()

win = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("First Game")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and x - vel >= 0:
        x -= vel
    if keys[pygame.K_d] and x + vel + width <= 1000:
        x += vel
    if keys[pygame.K_w] and y - vel >= 0:
        y -= vel
    if keys[pygame.K_s] and y + vel + height <= 700:
        y += vel
    
    
    win.fill((0, 0, 0)) 
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height))
    pygame.display.update()


