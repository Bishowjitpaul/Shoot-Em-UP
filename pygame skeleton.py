# pygame template - skeleton for a new pygame project

import pygame
import random

WIDTH = 360
HEIGHT = 480

# define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

FPS = 30  # how fast your game run that stand for frames per second

pygame.init()  # initialize the pygame
pygame.mixer.init()  # sound effect

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PYGAME SKELETON")

clock = pygame.time.Clock()  # handle the speed and  keep track of how fast we going

all_sprites= pygame.sprite.Group()
# game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)  # for more and more updates , without right game loop FPS , it will lagging

    # process input(event)
    for event in pygame.event.get():
        # close window
        if event.type == pygame.QUIT:
            running = False

    # update game
    all_sprites.update()

    # draw/ render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # *after* drawing everything, flip the dispaly
    pygame.display.flip()

pygame.quit()
